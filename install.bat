@echo off
chcp 65001 >nul
echo 自动化环境设置脚本
echo.

REM 获取CUDA版本参数，默认为129（CUDA 12.9）
set CUDA_VERSION=%1
if "%CUDA_VERSION%"=="" set CUDA_VERSION=129

echo 使用CUDA版本: %CUDA_VERSION%
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 运行Python设置脚本
python setup.py %CUDA_VERSION%

if errorlevel 1 (
    echo.
    echo 安装过程中出现错误
    pause
    exit /b 1
)

echo.
echo 安装完成！
echo.
echo 使用方法:
echo 1. 激活虚拟环境: activate.bat
echo 2. 启动应用: python app.py
echo.
pause
