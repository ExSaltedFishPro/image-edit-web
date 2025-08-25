#!/usr/bin/env python3
"""
API密钥管理工具
用于生成、列出和删除API密钥
"""

import json
import os
import sys
import hashlib
import uuid
from datetime import datetime

API_KEYS_FILE = 'api_keys.json'

def load_api_keys():
    """加载API密钥"""
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_api_keys(api_keys):
    """保存API密钥"""
    with open(API_KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(api_keys, f, indent=2, ensure_ascii=False)

def generate_api_key():
    """生成新的API密钥"""
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

def create_api_key(name=None):
    """创建新的API密钥"""
    api_keys = load_api_keys()
    
    if name is None:
        name = input("请输入API密钥名称: ").strip()
    
    if not name:
        print("❌ 错误: API密钥名称不能为空")
        return
    
    if name in api_keys:
        print(f"❌ 错误: 名称 '{name}' 已存在")
        return
    
    api_key = generate_api_key()
    api_keys[name] = {
        'key': api_key,
        'created_at': datetime.now().isoformat(),
        'last_used': None
    }
    
    save_api_keys(api_keys)
    print(f"✅ 成功创建API密钥:")
    print(f"   名称: {name}")
    print(f"   密钥: {api_key}")
    print(f"   创建时间: {api_keys[name]['created_at']}")
    print(f"\n⚠️  请妥善保管您的API密钥，系统不会再次显示完整密钥")

def list_api_keys():
    """列出所有API密钥"""
    api_keys = load_api_keys()
    
    if not api_keys:
        print("📋 当前没有API密钥")
        return
    
    print("📋 API密钥列表:")
    print("-" * 80)
    for name, info in api_keys.items():
        masked_key = info['key'][:8] + "*" * 24 + info['key'][-8:]
        print(f"名称: {name}")
        print(f"密钥: {masked_key}")
        print(f"创建时间: {info['created_at']}")
        print(f"最后使用: {info.get('last_used', '从未使用')}")
        print("-" * 80)

def delete_api_key(name=None):
    """删除API密钥"""
    api_keys = load_api_keys()
    
    if not api_keys:
        print("📋 当前没有API密钥")
        return
    
    if name is None:
        print("现有API密钥:")
        for key_name in api_keys.keys():
            print(f"  - {key_name}")
        name = input("请输入要删除的API密钥名称: ").strip()
    
    if not name:
        print("❌ 错误: API密钥名称不能为空")
        return
    
    if name not in api_keys:
        print(f"❌ 错误: 名称 '{name}' 不存在")
        return
    
    confirm = input(f"确认要删除API密钥 '{name}' 吗? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        del api_keys[name]
        save_api_keys(api_keys)
        print(f"✅ 成功删除API密钥: {name}")
    else:
        print("❌ 取消删除操作")

def show_help():
    """显示帮助信息"""
    print("""
🔑 API密钥管理工具

用法:
    python manage_api_keys.py <命令> [参数]

命令:
    create [名称]     - 创建新的API密钥
    list              - 列出所有API密钥
    delete [名称]     - 删除指定的API密钥
    help              - 显示此帮助信息

示例:
    python manage_api_keys.py create my_key
    python manage_api_keys.py list
    python manage_api_keys.py delete my_key

注意:
    - API密钥用于访问图像编辑API
    - 请妥善保管您的API密钥
    - 删除操作不可恢复
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        name = sys.argv[2] if len(sys.argv) > 2 else None
        create_api_key(name)
    elif command == 'list':
        list_api_keys()
    elif command == 'delete':
        name = sys.argv[2] if len(sys.argv) > 2 else None
        delete_api_key(name)
    elif command == 'help':
        show_help()
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == '__main__':
    main()
