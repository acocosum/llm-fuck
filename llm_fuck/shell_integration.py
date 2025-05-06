#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict

def get_shell_config_path() -> str:
    """获取当前shell的配置文件路径"""
    shell = os.environ.get('SHELL', '')
    home = os.path.expanduser("~")
    
    if 'zsh' in shell:
        return os.path.join(home, '.zshrc')
    elif 'bash' in shell:
        # 优先检查.bashrc，如果没有则使用.bash_profile
        bashrc = os.path.join(home, '.bashrc')
        if os.path.exists(bashrc):
            return bashrc
        return os.path.join(home, '.bash_profile')
    elif 'fish' in shell:
        return os.path.join(home, '.config', 'fish', 'config.fish')
    else:
        # 默认返回bashrc
        return os.path.join(home, '.bashrc')

def generate_shell_script(shell_type: str) -> str:
    """生成特定shell的配置脚本"""
    scripts = {
        'bash': '''
# LLM-Fuck shell integration
function llmf {
    python -m llm_fuck.main "$@"
}
alias fuck='llmf'
''',
        'zsh': '''
# LLM-Fuck shell integration
function llmf {
    python -m llm_fuck.main "$@"
}
alias fuck='llmf'
''',
        'fish': '''
# LLM-Fuck shell integration
function llmf
    python -m llm_fuck.main $argv
end
alias fuck='llmf'
'''
    }
    
    return scripts.get(shell_type, scripts['bash'])

def install_shell_integration() -> bool:
    """安装shell集成"""
    try:
        shell_config_path = get_shell_config_path()
        shell_type = 'bash'
        
        if 'zsh' in shell_config_path:
            shell_type = 'zsh'
        elif 'fish' in shell_config_path:
            shell_type = 'fish'
        
        script = generate_shell_script(shell_type)
        
        # 检查是否已经集成
        with open(shell_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'LLM-Fuck shell integration' in content:
                print(f"Shell集成已存在于 {shell_config_path}")
                return True
        
        # 添加集成脚本
        with open(shell_config_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{script}\n")
        
        print(f"Shell集成已安装到 {shell_config_path}")
        print(f"请运行 'source {shell_config_path}' 或重启终端以使更改生效")
        return True
    except Exception as e:
        print(f"安装shell集成失败: {str(e)}")
        return False