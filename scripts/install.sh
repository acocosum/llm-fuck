#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== LLM-Fuck 安装脚本 ===${NC}"

# 检查Python版本
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$python_version >= 3.6" | bc) -eq 0 ]]; then
    echo -e "${RED}错误: 需要Python 3.6或更高版本，当前版本为${python_version}${NC}"
    exit 1
fi

echo -e "${GREEN}检测到Python版本: ${python_version} ✓${NC}"

# 安装Python包
echo -e "${BLUE}正在安装LLM-Fuck...${NC}"
pip3 install -e . || { echo -e "${RED}安装失败${NC}"; exit 1; }

# 安装shell集成
echo -e "${BLUE}正在设置shell集成...${NC}"
python3 -c "from llm_fuck.shell_integration import install_shell_integration; install_shell_integration()"

echo -e "${GREEN}安装完成!${NC}"
echo -e "${YELLOW}请运行 'llmf --config' 来设置您的API密钥${NC}"
echo -e "${YELLOW}安装后请重启终端或运行 'source ~/.bashrc' (或您的shell配置文件) 以激活集成${NC}"