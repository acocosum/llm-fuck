#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import readline
import json
import time
from typing import Tuple, Optional

from .config import Config
from .models import get_llm_client
from .utils import log, colored_text

def get_last_command_and_error() -> Tuple[str, str, bool]:
    """获取最近的命令和错误信息"""
    try:
        # 获取历史命令
        history_length = readline.get_current_history_length()
        if history_length == 0:
            return "", "没有历史命令", False
            
        last_command = readline.get_history_item(history_length)
        
        # 忽略 llm-fuck 自身的调用
        if "llm-fuck" in last_command or "llmf" in last_command:
            if history_length > 1:
                last_command = readline.get_history_item(history_length - 1)
            else:
                return "", "没有有效的历史命令", False
        
        # 模拟执行以获取错误信息
        result = subprocess.run(last_command, shell=True, capture_output=True, text=True)
        error_message = result.stderr if result.returncode != 0 else ""
        return last_command, error_message, result.returncode != 0
    except Exception as e:
        return "", str(e), False

def get_correction(command: str, error: str, config: Config) -> Optional[str]:
    """从LLM获取命令修正建议"""
    llm_client = get_llm_client(config)
    
    # 获取当前工作目录和环境信息
    cwd = os.getcwd()
    shell = os.environ.get('SHELL', '')
    
    start_time = time.time()
    log(f"正在请求LLM修正建议...", config)
    
    correction = llm_client.get_correction(command, error, cwd, shell)
    
    elapsed = time.time() - start_time
    log(f"LLM响应时间: {elapsed:.2f}秒", config)
    
    return correction

def execute_command(command: str) -> int:
    """执行修正后的命令"""
    print(colored_text(f"\n执行命令: {command}", "green"))
    return os.system(command)

def main():
    """主函数入口"""
    # 加载配置
    config = Config()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("""LLM-Fuck: 使用大语言模型修正命令行错误

用法: llmf [选项]

选项:
  -h, --help     显示帮助信息
  -v, --verbose  显示详细日志
  --config       配置API密钥和其他设置
  --version      显示版本信息
""")
        return 0
        
    if len(sys.argv) > 1 and sys.argv[1] == '--config':
        config.setup_interactive()
        return 0
        
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        print("LLM-Fuck v0.1.0")
        return 0
        
    if len(sys.argv) > 1 and sys.argv[1] in ['-v', '--verbose']:
        config.verbose = True
    
    # 检查配置
    if not config.is_configured():
        print(colored_text("LLM-Fuck尚未配置。请运行 'llmf --config' 进行配置。", "yellow"))
        return 1
    
    # 获取上一条命令和错误信息
    command, error, has_error = get_last_command_and_error()
    
    if not has_error or not command:
        print(colored_text("上一条命令执行成功或无历史命令，无需修正。", "green"))
        return 0
    
    print(colored_text(f"检测到命令错误: {command}", "red"))
    print(colored_text(f"错误信息: {error[:200]}{'...' if len(error) > 200 else ''}", "red"))
    
    # 获取修正建议
    correction = get_correction(command, error, config)
    
    if not correction:
        print(colored_text("无法提供修正建议。", "yellow"))
        return 1
    
    print(colored_text(f"建议修正为: {correction}", "green"))
    
    # 确认执行
    try:
        confirm = input(colored_text("是否执行修正后的命令？[y/N]: ", "cyan"))
        if confirm.lower() in ['y', 'yes']:
            return execute_command(correction)
    except KeyboardInterrupt:
        print("\n操作已取消")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())