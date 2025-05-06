#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional

def log(message: str, config) -> None:
    """日志输出工具"""
    if config.settings.get("verbose", False) or config.verbose:
        print(f"[LLM-Fuck] {message}", file=sys.stderr)

def colored_text(text: str, color: str) -> str:
    """给文本添加颜色"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'end': '\033[0m'
    }
    
    # 如果终端不支持颜色，直接返回原文本
    if not sys.stdout.isatty():
        return text
        
    return f"{colors.get(color, '')}{text}{colors['end']}"