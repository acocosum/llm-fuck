#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    def __init__(self):
        """初始化配置"""
        self.config_dir = os.path.expanduser("~/.config/llm-fuck")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.verbose = False
        self.settings = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            return {
                "api_provider": "openai",
                "api_keys": {},
                "default_model": "gpt-4",
                "timeout": 20,
                "max_retries": 3,
                "verbose": False
            }
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                "api_provider": "openai",
                "api_keys": {},
                "default_model": "gpt-4",
                "timeout": 20,
                "max_retries": 3,
                "verbose": False
            }
    
    def save_config(self) -> None:
        """保存配置到文件"""
        os.makedirs(self.config_dir, exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2)
    
    def get_api_key(self, provider: Optional[str] = None) -> str:
        """获取API密钥"""
        if provider is None:
            provider = self.settings.get("api_provider", "openai")
            
        return self.settings.get("api_keys", {}).get(provider, "")
    
    def is_configured(self) -> bool:
        """检查是否已完成配置"""
        provider = self.settings.get("api_provider", "openai")
        return bool(self.get_api_key(provider))
    
    def setup_interactive(self) -> None:
        """交互式设置配置"""
        print("欢迎配置 LLM-Fuck!")
        print("\n选择LLM提供商:")
        print("1. OpenAI (GPT-3.5, GPT-4)")
        print("2. Anthropic (Claude)")
        print("3. 百度文心")
        print("4. 讯飞星火")
        
        choice = input("\n请选择 (1-4) [默认:1]: ").strip() or "1"
        
        providers = {
            "1": "openai", 
            "2": "anthropic",
            "3": "baidu",
            "4": "xunfei"
        }
        
        provider = providers.get(choice, "openai")
        self.settings["api_provider"] = provider
        
        api_key = input(f"\n请输入 {provider} API密钥: ").strip()
        if not api_key:
            print("错误: API密钥不能为空")
            return
            
        if "api_keys" not in self.settings:
            self.settings["api_keys"] = {}
        self.settings["api_keys"][provider] = api_key
        
        # 设置模型（仅适用于OpenAI）
        if provider == "openai":
            print("\n选择默认模型:")
            print("1. GPT-3.5-turbo (更快、成本更低)")
            print("2. GPT-4 (更准确，推荐)")
            
            model_choice = input("\n请选择 (1-2) [默认:2]: ").strip() or "2"
            model = "gpt-4" if model_choice == "2" else "gpt-3.5-turbo"
            self.settings["default_model"] = model
        
        verbose = input("\n是否启用详细日志? [y/N]: ").strip().lower() in ['y', 'yes']
        self.settings["verbose"] = verbose
        
        self.save_config()
        print("\n配置已保存!")