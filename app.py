import os
import uuid
import hashlib
import json
from datetime import datetime
from PIL import Image
import torch
from flask import Flask, request, jsonify, render_template, send_file, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from diffusers import QwenImageEditPipeline
import io
import base64

app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
API_KEYS_FILE = 'api_keys.json'
print(torch.cuda.is_available())
# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 初始化模型管道
pipeline = None

def load_pipeline():
    global pipeline
    if pipeline is None:
        print("Loading Qwen Image Edit Pipeline...")
        pipeline = QwenImageEditPipeline.from_pretrained("Qwen/Qwen-Image-Edit")
        pipeline.to(torch.bfloat16)
        pipeline.to("cuda")
        pipeline.set_progress_bar_config(disable=None)
        print("Pipeline loaded successfully!")
        print(next(pipeline.unet.parameters()).device)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_api_keys():
    """加载API密钥"""
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_api_keys(api_keys):
    """保存API密钥"""
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f, indent=2)

def generate_api_key():
    """生成新的API密钥"""
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

def validate_api_key(api_key):
    """验证API密钥"""
    api_keys = load_api_keys()
    print(api_keys.values())
    for key in api_keys.values():
        if api_key == key['key']:
            return True
    return False

def require_api_key(f):
    """装饰器：要求API密钥"""
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/edit-image', methods=['POST'])
@require_api_key
def api_edit_image():
    """API端点：编辑图像"""
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # 获取参数
        prompt = request.form.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        negative_prompt = request.form.get('negative_prompt', ' ')
        true_cfg_scale = float(request.form.get('true_cfg_scale', 4.0))
        num_inference_steps = int(request.form.get('num_inference_steps', 50))
        seed = int(request.form.get('seed', 0))
        
        # 加载模型
        load_pipeline()
        
        # 处理图像
        image = Image.open(file.stream).convert("RGB")
        
        # 设置输入参数
        inputs = {
            "image": image,
            "prompt": prompt,
            "generator": torch.manual_seed(seed),
            "true_cfg_scale": true_cfg_scale,
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps,
        }
        
        # 生成图像
        with torch.inference_mode():
            output = pipeline(**inputs)
            output_image = output.images[0]
        
        # 保存输出图像
        output_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        output_image.save(output_path)
        
        # 将图像转换为base64返回
        img_buffer = io.BytesIO()
        output_image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'output_image': f"data:image/png;base64,{img_str}",
            'output_path': output_path,
            'parameters': {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'true_cfg_scale': true_cfg_scale,
                'num_inference_steps': num_inference_steps,
                'seed': seed
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/edit-image', methods=['POST'])
def web_edit_image():
    """Web端点：编辑图像（用于前端表单）"""
    try:
        # 检查API密钥
        api_key = request.form.get('api_key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({'error': 'Invalid or missing API key'}), 401
        
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # 获取参数
        prompt = request.form.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        negative_prompt = request.form.get('negative_prompt', ' ')
        true_cfg_scale = float(request.form.get('true_cfg_scale', 4.0))
        num_inference_steps = int(request.form.get('num_inference_steps', 50))
        seed = int(request.form.get('seed', 0))
        
        # 加载模型
        load_pipeline()
        
        # 处理图像
        image = Image.open(file.stream).convert("RGB")
        
        # 设置输入参数
        inputs = {
            "image": image,
            "prompt": prompt,
            "generator": torch.manual_seed(seed),
            "true_cfg_scale": true_cfg_scale,
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps,
        }
        
        # 生成图像
        with torch.inference_mode():
            output = pipeline(**inputs)
            output_image = output.images[0]
        
        # 保存输出图像
        output_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        output_image.save(output_path)
        
        # 将图像转换为base64返回
        img_buffer = io.BytesIO()
        output_image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'output_image': f"data:image/png;base64,{img_str}",
            'output_path': output_path,
            'parameters': {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'true_cfg_scale': true_cfg_scale,
                'num_inference_steps': num_inference_steps,
                'seed': seed
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """下载生成的图像"""
    try:
        return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
