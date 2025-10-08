# core/code_executor.py
import FreeCAD
import FreeCADGui
import sys
from types import ModuleType

class SafeCodeExecutor:
    def __init__(self):
        # 1. 定义“安全模块白名单”（仅允许FreeCAD相关模块，禁止os、sys等危险模块）
        self.allowed_modules = {
            "FreeCAD": FreeCAD,
            "FreeCADGui": FreeCADGui,
            "Part": sys.modules.get("Part"),
            "PartDesign": sys.modules.get("PartDesign"),
            "Sketch": sys.modules.get("Sketch"),
            "Draft": sys.modules.get("Draft")
        }

    def _create_safe_globals(self):
        """创建安全的全局变量环境（仅包含白名单模块）"""
        safe_globals = {
            "__name__": "__main__",
            "__doc__": None,
            "__package__": None,
            "__loader__": None,
            "__spec__": None,
            # 注入允许的模块
            **self.allowed_modules
        }
        # 禁止修改全局环境（如禁止导入新模块）
        safe_globals["__builtins__"] = self._get_safe_builtins()
        return safe_globals

    def _get_safe_builtins(self):
        """创建安全的内置函数（仅允许print、range等无害函数）"""
        builtins = __builtins__.__dict__.copy()
        # 移除危险内置函数（如eval、exec、open、import）
        dangerous_builtins = ["eval", "exec", "open", "file", "importlib", "__import__"]
        for func in dangerous_builtins:
            if func in builtins:
                del builtins[func]
        return builtins

    def execute(self, code):
        """
        安全执行FreeCAD代码
        :param code: 生成的Python代码
        :return: (success: 是否执行成功, error_msg: 错误信息)
        """
        try:
            # 1. 清空当前FreeCAD文档（避免模型冲突）
            FreeCAD.newDocument("LLMAutoModel")
            FreeCAD.setActiveDocument("LLMAutoModel")

            # 2. 在安全环境中执行代码
            safe_globals = self._create_safe_globals()
            exec(code, safe_globals)  # 执行代码

            # 3. 刷新视图（确保模型显示）
            FreeCADGui.activeDocument().activeView().viewFit()
            FreeCAD.Console.PrintMessage("[LLMAutoModeler] 模型生成成功！\n")
            return True, ""

        except Exception as e:
            error_msg = f"代码执行失败：{str(e)}"
            FreeCAD.Console.PrintError(f"[LLMAutoModeler] {error_msg}\n")
            # 执行失败后清理文档
            FreeCAD.closeDocument("LLMAutoModel")
            return False, error_msg