#!/usr/bin/env python3
import os
import sys
import subprocess
import readline
import requests
import json

# 配置你的大语言模型API
API_KEY = "your_api_key_here"
API_URL = "https://api.openai.com/v1/chat/completions"  # 以OpenAI为例

def get_last_command_and_error():
    # 获取历史命令
    last_command = readline.get_history_item(readline.get_current_history_length() - 1)
    
    # 模拟执行以获取错误信息
    try:
        result = subprocess.run(last_command, shell=True, capture_output=True, text=True)
        error_message = result.stderr if result.returncode != 0 else ""
        return last_command, error_message, result.returncode != 0
    except Exception as e:
        return last_command, str(e), True

def get_correction_from_llm(command, error):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    作为一个命令行修正助手，我遇到了以下命令错误：
    
    命令: {command}
    错误信息: {error}
    
    请提供正确的命令，只返回修正后的命令，不要包含任何解释。
    """
    
    data = {
        "model": "gpt-4",  # 或其他适合的模型
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        correction = response.json()["choices"][0]["message"]["content"].strip()
        return correction
    else:
        return None

def main():
    last_command, error_message, has_error = get_last_command_and_error()
    
    if not has_error:
        print("上一条命令执行成功，无需修正。")
        return
    
    print(f"检测到命令错误: {last_command}")
    print(f"错误信息: {error_message}")
    print("正在分析修正方案...")
    
    correction = get_correction_from_llm(last_command, error_message)
    
    if correction:
        print(f"建议修正为: {correction}")
        confirm = input("是否执行修正后的命令？ (y/n): ")
        if confirm.lower() == 'y':
            os.system(correction)
    else:
        print("无法提供修正建议。")

if __name__ == "__main__":
    main()