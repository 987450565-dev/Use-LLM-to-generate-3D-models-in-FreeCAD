
# -*- coding: utf-8 -*-
import FreeCAD as App
import FreeCADGui as Gui
import sys
import subprocess  # ✅ 新增导入

App.Console.PrintMessage("[LLMAutoModeler] 正在加载 InitGui.py\n")

# ====================
# 依赖检查与安装（Gemini 版本）
# ====================
def check_dependencies():
    try:
        import google.generativeai as genai
        import dotenv
        App.Console.PrintMessage("[LLMAutoModeler] 依赖已安装 ✅\n")
        return True
    except ImportError as e:
        missing_lib = e.name
        App.Console.PrintWarning(f"[LLMAutoModeler] 缺少依赖: {missing_lib}\n")
        App.Console.PrintMessage("[LLMAutoModeler] 正在自动安装依赖...\n")

        try:
            # 使用 FreeCAD 内置 Python 安装依赖
            python_exe = sys.executable.replace("freecad.exe", "python.exe")
            subprocess.check_call(
                [python_exe, "-m", "pip", "install", "google-generativeai", "python-dotenv", "--user"]
            )
            App.Console.PrintMessage("[LLMAutoModeler] 依赖安装完成，请重启 FreeCAD\n")
            return False
        except Exception as install_err:
            App.Console.PrintError(f"[LLMAutoModeler] 依赖安装失败: {install_err}\n")
            return False

# ====================
# 检查依赖
# ====================
if not check_dependencies():
    App.Console.PrintMessage("[LLMAutoModeler] 等待依赖安装并重启 FreeCAD...\n")
else:
    # ====================
    # 命令类
    # ====================
    class LLMAutoModelerCommand:
        def GetResources(self):
            return {
                "MenuText": "LLM自动建模",
                "ToolTip": "使用 Gemini-2.5-Flash 自动生成FreeCAD模型",
                "Pixmap": ""
            }

        def Activated(self):
            try:
                from gui.main_dialog import LLMAutoModelerDialog
                dialog = LLMAutoModelerDialog(Gui.getMainWindow())
                dialog.exec_()
            except Exception as e:
                App.Console.PrintError(f"[LLMAutoModeler] 打开对话框失败: {e}\n")

    # 注册命令
    Gui.addCommand("LLMAutoModeler_Command", LLMAutoModelerCommand())

    # ====================
    # 工作台类
    # ====================
    class LLMAutoModelerWorkbench(Gui.Workbench):
        MenuText = "LLM建模"
        ToolTip = "基于 Gemini-2.5-Flash 的自动建模工作台"
        Icon = ""

        def Initialize(self):
            App.Console.PrintMessage("[LLMAutoModeler] 初始化工作台\n")
            self.appendMenu("LLM建模", ["LLMAutoModeler_Command"])

        def Activated(self):
            App.Console.PrintMessage("[LLMAutoModeler] 已切换到 LLM建模 工作台\n")

        def Deactivated(self):
            pass

    # 注册工作台
    Gui.addWorkbench(LLMAutoModelerWorkbench())

    App.Console.PrintMessage("[LLMAutoModeler] GUI初始化完成 ✅\n")
