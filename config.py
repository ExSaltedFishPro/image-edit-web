"""
配置文件
"""

import os

# 应用配置
class Config:
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwen-image-edit-secret-key-2023'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # 服务器配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # 文件路径配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'outputs')
    API_KEYS_FILE = os.environ.get('API_KEYS_FILE', 'api_keys.json')
    
    # 文件限制
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # 模型配置
    MODEL_NAME = os.environ.get('MODEL_NAME', 'Qwen/Qwen-Image-Edit')
    DEVICE = os.environ.get('DEVICE', 'cuda')  # 'cuda' or 'cpu'
    TORCH_DTYPE = os.environ.get('TORCH_DTYPE', 'bfloat16')  # 'bfloat16' or 'float16' or 'float32'
    
    # 默认参数
    DEFAULT_CFG_SCALE = float(os.environ.get('DEFAULT_CFG_SCALE', 4.0))
    DEFAULT_INFERENCE_STEPS = int(os.environ.get('DEFAULT_INFERENCE_STEPS', 50))
    DEFAULT_SEED = int(os.environ.get('DEFAULT_SEED', 0))
    
    # 参数限制
    MIN_CFG_SCALE = 1.0
    MAX_CFG_SCALE = 20.0
    MIN_INFERENCE_STEPS = 10
    MAX_INFERENCE_STEPS = 100
    
    # 安全配置
    REQUIRE_API_KEY = os.environ.get('REQUIRE_API_KEY', 'True').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    WTF_CSRF_ENABLED = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
