#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化环境设置脚本
用法: python setup.py [cuda_version]
例如: python setup.py 129  # 对应CUDA 12.9
     python setup.py 118  # 对应CUDA 11.8
     python setup.py cpu  # CPU版本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, check=True, shell=True):
    """执行命令并处理错误"""
    try:
        print(f"执行命令: {command}")
        result = subprocess.run(command, shell=shell, check=check, 
                               capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"执行出错: {e}")
        sys.exit(1)

def get_torch_index_url(cuda_version):
    """根据CUDA版本获取PyTorch索引URL"""
    if cuda_version.lower() == 'cpu':
        return "https://download.pytorch.org/whl/cpu"
    
    # 将简化的CUDA版本转换为完整版本


    cuda_tag = cuda_version.replace('.', '')
    #return f"https://download.pytorch.org/whl/{cuda_tag}"
    return f"https://mirrors.aliyun.com/pytorch-wheels/cu{cuda_tag}/"

def main():
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # 解析命令行参数
    cuda_version = sys.argv[1] if len(sys.argv) > 1 else '129'
    
    print(f"开始设置环境，CUDA版本: {cuda_version}")
    print(f"工作目录: {script_dir}")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 设置虚拟环境目录
    venv_dir = script_dir / "venv"
    
    # 删除现有虚拟环境（如果存在）
    if venv_dir.exists():
        print("删除现有虚拟环境...")
        if platform.system() == "Windows":
            run_command(f'rmdir /s /q "{venv_dir}"')
        else:
            run_command(f'rm -rf "{venv_dir}"')
    
    # 创建虚拟环境
    print("创建虚拟环境...")
    run_command(f'python -m venv "{venv_dir}"')
    
    # 设置激活脚本路径
    if platform.system() == "Windows":
        activate_script = venv_dir / "Scripts" / "activate.bat"
        pip_executable = venv_dir / "Scripts" / "pip.exe"
        python_executable = venv_dir / "Scripts" / "python.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        pip_executable = venv_dir / "bin" / "pip"
        python_executable = venv_dir / "bin" / "python"
    
    # 升级pip
    print("升级pip...")
    run_command(f'"{python_executable}" -m pip install --upgrade pip')
    
    # 获取PyTorch索引URL
    torch_index_url = get_torch_index_url(cuda_version)
    print(f"使用PyTorch索引: {torch_index_url}")
    
    # 首先安装PyTorch相关包
    print("安装PyTorch相关包...")
    torch_packages = ["torch", "torchvision", "torchaudio"]
    for package in torch_packages:
        run_command(f'"{pip_executable}" install {package} -f {torch_index_url}')
    
    # 安装其他依赖
    print("安装其他依赖包...")
    requirements_file = script_dir / "requirements.txt"
    
    if requirements_file.exists():
        # 读取requirements.txt并过滤掉已安装的torch包
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = f.readlines()
        
        # 过滤掉torch相关包，因为我们已经安装了特定版本
        filtered_requirements = []
        torch_related = ['torch', 'torchvision', 'torchaudio']
        
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].strip()
                if package_name not in torch_related:
                    filtered_requirements.append(req)
        
        # 安装过滤后的依赖
        if filtered_requirements:
            # 创建临时requirements文件
            temp_requirements = script_dir / "temp_requirements.txt"
            with open(temp_requirements, 'w', encoding='utf-8') as f:
                f.write('\n'.join(filtered_requirements))
            
            run_command(f'"{pip_executable}" install -r "{temp_requirements}"')
            
            # 删除临时文件
            temp_requirements.unlink()
    
    # 验证安装
    print("\n验证安装...")
    run_command(f'"{pip_executable}" list')
    
    # 测试PyTorch
    print("\n测试PyTorch安装...")
    test_script = f'''
import torch
print(f"PyTorch版本: {{torch.__version__}}")
print(f"CUDA可用: {{torch.cuda.is_available()}}")
if torch.cuda.is_available():
    print(f"CUDA版本: {{torch.version.cuda}}")
    print(f"GPU数量: {{torch.cuda.device_count()}}")
    print(f"当前设备: {{torch.cuda.get_device_name(0)}}")
else:
    print("使用CPU模式")
'''
    
    run_command(f'"{python_executable}" -c "{test_script}"')
    
    # 创建激活脚本
    if platform.system() == "Windows":
        activate_bat = script_dir / "activate.bat"
        with open(activate_bat, 'w', encoding='utf-8') as f:
            f.write(f'@echo off\n')
            f.write(f'call "{activate_script}"\n')
            f.write(f'echo 虚拟环境已激活\n')
            f.write(f'echo 使用 python app.py 启动应用\n')
        
        print(f"\n设置完成!")
        print(f"激活虚拟环境: activate.bat")
        print(f"或手动激活: {activate_script}")
    else:
        activate_sh = script_dir / "activate.sh"
        with open(activate_sh, 'w', encoding='utf-8') as f:
            f.write(f'#!/bin/bash\n')
            f.write(f'source "{activate_script}"\n')
            f.write(f'echo "虚拟环境已激活"\n')
            f.write(f'echo "使用 python app.py 启动应用"\n')
        
        run_command(f'chmod +x "{activate_sh}"')
        
        print(f"\n设置完成!")
        print(f"激活虚拟环境: ./activate.sh")
        print(f"或手动激活: source {activate_script}")
    
    print(f"Python可执行文件: {python_executable}")
    print(f"pip可执行文件: {pip_executable}")

if __name__ == "__main__":
    main()
