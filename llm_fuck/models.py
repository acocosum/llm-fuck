#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Optional

from .config import Config
from .utils import log

class LLMClient(ABC):
    """LLM客户端抽象基类"""
    def __init__(self, config: Config):
        self.config = config
    
    @abstractmethod
    def get_correction(self, command: str, error: str, cwd: str, shell: str) -> Optional[str]:
        """获取命令修正"""
        pass

class OpenAIClient(LLMClient):
    """OpenAI API客户端"""
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.get_api_key("openai")
        self.model = config.settings.get("default_model", "gpt-4")
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def get_correction(self, command: str, error: str, cwd: str, shell: str) -> Optional[str]:
        """从OpenAI获取命令修正"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
你是一个专业的命令行修正助手。用户的命令出现了错误，需要你提供修正。请只返回修正后的命令，不要包含任何解释或额外信息。

当前工作目录: {cwd}
当前Shell: {shell}
执行的命令: {command}
错误信息: {error}

请提供修正后的命令:
"""
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 100
        }
        
        try:
            timeout = self.config.settings.get("timeout", 20)
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                correction = response.json()["choices"][0]["message"]["content"].strip()
                # 清除可能的引号和反斜杠
                if correction.startswith('`') and correction.endswith('`'):
                    correction = correction[1:-1]
                return correction
            else:
                log(f"API错误: {response.status_code} - {response.text}", self.config)
                return None
        except Exception as e:
            log(f"请求异常: {str(e)}", self.config)
            return None

class AnthropicClient(LLMClient):
    """Anthropic Claude API客户端"""
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.get_api_key("anthropic")
        self.api_url = "https://api.anthropic.com/v1/messages"
    
    def get_correction(self, command: str, error: str, cwd: str, shell: str) -> Optional[str]:
        """从Anthropic获取命令修正"""
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        prompt = f"""
你是一个专业的命令行修正助手。用户的命令出现了错误，需要你提供修正。请只返回修正后的命令，不要包含任何解释或额外信息。

当前工作目录: {cwd}
当前Shell: {shell}
执行的命令: {command}
错误信息: {error}

请提供修正后的命令:
"""
        
        data = {
            "model": "claude-2",
            "max_tokens": 100,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            timeout = self.config.settings.get("timeout", 20)
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                correction = response.json()["content"][0]["text"].strip()
                # 清除可能的引号和反斜杠
                if correction.startswith('`') and correction.endswith('`'):
                    correction = correction[1:-1]
                return correction
            else:
                log(f"API错误: {response.status_code} - {response.text}", self.config)
                return None
        except Exception as e:
            log(f"请求异常: {str(e)}", self.config)
            return None

class BaiduClient(LLMClient):
    """百度文心API客户端"""
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.get_api_key("baidu")
        # 百度API需要实现获取access_token等逻辑
        # 此处简化实现
    
    def get_correction(self, command: str, error: str, cwd: str, shell: str) -> Optional[str]:
        """实现百度文心的API调用"""
        # 这里需要实现百度文心的具体API调用
        # 简化实现，实际项目中需要完整实现
        return "修正后的命令示例"

class XunfeiClient(LLMClient):
    """讯飞星火API客户端"""
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.get_api_key("xunfei")
        # 讯飞API需要实现鉴权等逻辑
        # 此处简化实现
    
    def get_correction(self, command: str, error: str, cwd: str, shell: str) -> Optional[str]:
        """实现讯飞星火的API调用"""
        # 这里需要实现讯飞星火的具体API调用
        # 简化实现，实际项目中需要完整实现
        return "修正后的命令示例"

def get_llm_client(config: Config) -> LLMClient:
    """根据配置获取对应的LLM客户端"""
    provider = config.settings.get("api_provider", "openai")
    
    clients = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "baidu": BaiduClient,
        "xunfei": XunfeiClient
    }
    
    client_class = clients.get(provider, OpenAIClient)
    return client_class(config)