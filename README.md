# Image Edit Web应用程序

基于Qwen模型的智能图像编辑工具，提供Web界面和RESTful API。

## 功能特性

- 🎨 **智能图像编辑**: 基于Qwen Image Edit模型，支持自然语言描述的图像编辑
- 🌐 **Web界面**: 美观易用的Web前端，支持拖拽上传和参数调整
- 🔌 **RESTful API**: 完整的API接口，支持程序化调用
- 🔐 **API密钥管理**: 安全的API密钥系统，支持多用户访问控制
- ⚙️ **参数控制**: 支持调整CFG Scale、推理步数、随机种子等参数
- 📱 **响应式设计**: 支持桌面和移动设备访问

## 项目结构

```
qwen-image-edit/
├── app.py                 # 主应用程序
├── config.py              # 配置文件
├── start.py              # 启动脚本
├── manage_api_keys.py    # API密钥管理工具
├── requirements.txt      # Python依赖项
├── example.py           # 原始示例代码
├── quick_start.bat      # Windows 快速启动脚本
├── templates/
│   └── index.html       # Web前端模板
├── uploads/             # 上传的图像文件 (自动创建)
├── outputs/             # 生成的图像文件 (自动创建)
└── api_keys.json        # API密钥存储 (自动生成)
```

## 快速开始

### 方式一：使用自动化脚本（推荐）

**一键启动**：
```bash
install.bat or
install.sh
```

### 方式二：手动安装

#### 1. 创建虚拟环境
```bash
python -m venv qwen-image-edit-env

# Windows 激活
qwen-image-edit-env\Scripts\activate

# Linux/macOS 激活
source qwen-image-edit-env/bin/activate
```

#### 2. 安装依赖项
```bash
pip install -r requirements.txt
```

#### 3. 创建API密钥

```bash
python manage_api_keys.py create my_first_key
```

### 3. 启动应用程序

**方式一: 使用启动脚本**
```bash
python start.py
```

**方式二: 直接启动**
```bash
python app.py
```

### 4. 访问Web界面

在浏览器中打开: http://localhost:5000

## 使用说明

### Web界面使用

1. 在浏览器中访问 `http://localhost:5000`
2. 输入您的API密钥
3. 上传要编辑的图像文件
4. 输入编辑提示词 (例如: "Change the rabbit's color to purple")
5. 调整参数 (可选)
6. 点击"开始编辑图像"按钮
7. 等待处理完成，查看编辑结果

### API接口使用

**端点**: `POST /api/edit-image`

**请求头**:
```
X-API-Key: <your_api_key>
Content-Type: multipart/form-data
```

**请求参数**:
- `image` (文件): 要编辑的图像文件
- `prompt` (字符串): 编辑提示词
- `negative_prompt` (字符串, 可选): 负面提示词
- `true_cfg_scale` (浮点数, 可选): CFG Scale (默认: 4.0)
- `num_inference_steps` (整数, 可选): 推理步数 (默认: 50)
- `seed` (整数, 可选): 随机种子 (默认: 0)

**响应示例**:
```json
{
  "success": true,
  "output_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "output_path": "outputs/output_20231201_143022_abc12345.png",
  "parameters": {
    "prompt": "Change the rabbit's color to purple",
    "negative_prompt": "",
    "true_cfg_scale": 4.0,
    "num_inference_steps": 50,
    "seed": 0
  }
}
```

**Python API调用示例**:
```python
import requests

url = "http://localhost:5000/api/edit-image"
headers = {"X-API-Key": "your_api_key_here"}
files = {"image": open("input.png", "rb")}
data = {
    "prompt": "Change the rabbit's color to purple",
    "true_cfg_scale": 4.0,
    "num_inference_steps": 50
}

response = requests.post(url, headers=headers, files=files, data=data)
result = response.json()
```

## API密钥管理

### 创建API密钥
```bash
python manage_api_keys.py create <密钥名称>
```

### 列出所有API密钥
```bash
python manage_api_keys.py list
```

### 删除API密钥
```bash
python manage_api_keys.py delete <密钥名称>
```

### 查看帮助
```bash
python manage_api_keys.py help
```

## 测试工具

使用内置的测试脚本验证API功能:

```bash
python test_api.py
```

测试脚本支持:
- API功能测试
- 创建测试图像
- 验证API密钥有效性

## 参数说明

### 编辑参数

- **prompt**: 编辑提示词，描述您想要的图像变化
- **negative_prompt**: 负面提示词，描述不希望出现的内容
- **true_cfg_scale**: Classifier-Free Guidance Scale (1.0-20.0)
  - 较低值: 更自由的创作
  - 较高值: 更严格遵循提示词
- **num_inference_steps**: 推理步数 (10-100)
  - 更多步数通常产生更好的质量，但处理时间更长
- **seed**: 随机种子
  - 相同种子产生相同结果，用于复现编辑效果

## 故障排除

### 常见问题

1. **GPU内存不足**
   - 减少图像分辨率
   - 降低 `num_inference_steps`
   - 使用CPU模式 (修改 `app.py` 中的设备设置)

2. **模型下载失败**
   - 检查网络连接
   - 使用镜像源或手动下载模型

3. **API密钥无效**
   - 检查密钥是否正确
   - 确认密钥未被删除

4. **端口冲突**
   - 修改 `app.py` 中的端口设置
   - 检查5000端口是否被占用

### 性能优化

1. **使用GPU加速**
   - 确保安装了正确的CUDA版本
   - 检查PyTorch CUDA支持

2. **批量处理**
   - 对于大量图像，考虑实现批量处理功能

3. **模型缓存**
   - 模型在首次加载后会保持在内存中，后续请求更快

## 安全注意事项

- API密钥应当保密，不要在公共场所泄露
- 在生产环境中，建议使用HTTPS
- 定期轮换API密钥
- 监控API使用情况，防止滥用

## 许可证

本项目基于MIT许可证开源。

---

**注意**: 本项目依赖于Qwen Image Edit模型，请确保遵守相关的使用条款和许可证要求。
