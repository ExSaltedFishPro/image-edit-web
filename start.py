#!/usr/bin/env python3
"""
Qwen Image Edit Web应用启动脚本
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖项"""
    print("🔍 正在检查依赖项...")
    
    required_packages = [
        'torch', 'torchvision', 'diffusers', 'transformers', 
        'accelerate', 'PIL', 'flask', 'flask_cors'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  缺少以下依赖项: {', '.join(missing_packages)}")
        print("请运行以下命令安装依赖项:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖项已安装")
    return True

def check_gpu():
    """检查GPU可用性"""
    print("\n🖥️  正在检查GPU...")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"   ✅ GPU可用: {gpu_name}")
            print(f"   💾 显存: {gpu_memory:.1f} GB")
            return True
        else:
            print("   ⚠️  GPU不可用，将使用CPU (性能较慢)")
            return False
    except Exception as e:
        print(f"   ❌ 检查GPU时出错: {str(e)}")
        return False

def setup_directories():
    """设置目录结构"""
    print("\n📁 正在设置目录结构...")
    
    directories = ['uploads', 'outputs', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ 创建目录: {directory}")
        else:
            print(f"   ✅ 目录已存在: {directory}")

def check_api_keys():
    """检查API密钥配置"""
    print("\n🔑 正在检查API密钥配置...")
    
    api_keys_file = 'api_keys.json'
    
    if os.path.exists(api_keys_file):
        try:
            with open(api_keys_file, 'r') as f:
                api_keys = json.load(f)
            
            if api_keys:
                print(f"   ✅ 发现 {len(api_keys)} 个API密钥")
                return True
            else:
                print("   ⚠️  API密钥文件为空")
        except Exception as e:
            print(f"   ❌ 读取API密钥文件时出错: {str(e)}")
    else:
        print("   ⚠️  未找到API密钥文件")
    
    print("\n   请使用以下命令创建API密钥:")
    print("   python manage_api_keys.py create")
    
    return False

def start_application():
    """启动应用程序"""
    print("\n🚀 正在启动应用程序...")
    
    try:
        # 启动Flask应用
        os.system("python app.py")
    except KeyboardInterrupt:
        print("\n👋 应用程序已停止")
    except Exception as e:
        print(f"\n❌ 启动应用程序时出错: {str(e)}")

def show_usage_info():
    """显示使用说明"""
    print("\n" + "="*60)
    print("🎉 Qwen Image Edit Web应用程序")
    print("="*60)
    print()
    print("📋 使用说明:")
    print("1. 确保已安装所有依赖项 (pip install -r requirements.txt)")
    print("2. 创建API密钥 (python manage_api_keys.py create)")
    print("3. 启动应用程序 (python start.py 或 python app.py)")
    print("4. 在浏览器中访问 http://localhost:5000")
    print()
    print("🔧 管理命令:")
    print("- 管理API密钥: python manage_api_keys.py")
    print("- 测试API: python test_api.py")
    print()
    print("🌐 API端点:")
    print("- Web界面: http://localhost:5000")
    print("- API接口: http://localhost:5000/api/edit-image")
    print()
    print("📖 API使用方法:")
    print("  POST /api/edit-image")
    print("  Headers: X-API-Key: <your_api_key>")
    print("  Form Data:")
    print("    - image: 图像文件")
    print("    - prompt: 编辑提示词")
    print("    - negative_prompt: 负面提示词 (可选)")
    print("    - true_cfg_scale: CFG Scale (可选)")
    print("    - num_inference_steps: 推理步数 (可选)")
    print("    - seed: 随机种子 (可选)")
    print()

def main():
    """主函数"""
    show_usage_info()
    
    # 检查依赖项
    if not check_dependencies():
        sys.exit(1)
    
    # 检查GPU
    check_gpu()
    
    # 设置目录
    setup_directories()
    
    # 检查API密钥
    has_api_keys = check_api_keys()
    
    if not has_api_keys:
        create_key = input("\n是否现在创建API密钥? (y/N): ").strip().lower()
        if create_key in ['y', 'yes']:
            os.system("python manage_api_keys.py create")
        else:
            print("⚠️  警告: 没有API密钥，应用程序将无法正常工作")
    
    # 询问是否启动应用
    start_app = input("\n是否现在启动应用程序? (y/N): ").strip().lower()
    if start_app in ['y', 'yes']:
        start_application()
    else:
        print("\n💡 要启动应用程序，请运行: python app.py")

if __name__ == '__main__':
    main()
