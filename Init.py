# Init.py
import FreeCAD
import os
from pathlib import Path

# 1. 定义模块元信息（名称、版本、作者）
__name__ = "LLMAutoModeler"
__version__ = "1.0.0"
__author__ = "JJJ"

# 2. 添加模块路径到Python环境（确保能导入core/gui下的文件）
module_path = Path(__file__).parent
import sys
if str(module_path) not in sys.path:
    sys.path.append(str(module_path))

# 3. 初始化LLM配置（加载.env文件）
from dotenv import load_dotenv
load_dotenv(module_path / ".env")  # 加载API密钥

# 4. 注册模块到FreeCAD（可选，用于后续版本管理）
def initialize():
    FreeCAD.Console.PrintMessage(f"[{__name__}] 模块加载成功（版本：{__version__}）\n")

# FreeCAD启动时自动执行
initialize()
