#!/bin/bash

# 设置UTF-8编码
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo "自动化环境设置脚本"
echo

# 获取CUDA版本参数，默认为129（CUDA 12.9）
CUDA_VERSION=${1:-129}

echo "使用CUDA版本: $CUDA_VERSION"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未找到Python，请先安装Python 3.8或更高版本"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "使用Python命令: $PYTHON_CMD"

# 检查Python版本
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "Python版本: $PYTHON_VERSION"

# 运行Python设置脚本
$PYTHON_CMD setup.py $CUDA_VERSION

if [ $? -ne 0 ]; then
    echo
    echo "安装过程中出现错误"
    exit 1
fi

echo
echo "安装完成！"
echo
echo "使用方法:"
echo "1. 激活虚拟环境: ./activate.sh 或 source venv/bin/activate"
echo "2. 启动应用: python app.py"
echo
