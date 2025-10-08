# core/code_generator.py
import ast
from core.llm_client import LLMClient
import FreeCAD

class CodeGenerator:
    def __init__(self, llm_type="openai"):
        self.llm_client = LLMClient(llm_type=llm_type)

    def generate_code(self, user_prompt, model=None):
        """
        生成FreeCAD Python代码并校验语法
        :param user_prompt: 用户建模提示
        :param model: LLM模型名称
        :return: (code: 生成的代码, is_valid: 语法是否有效, error_msg: 错误信息)
        """
        try:
            # 1. 调用LLM生成代码
            FreeCAD.Console.PrintMessage(f"[LLMAutoModeler] 正在调用LLM生成代码...\n")
            code = self.llm_client.call(user_prompt, model=model)

            # 2. 语法校验（使用ast模块避免执行恶意代码）
            ast.parse(code)  # 若语法错误，会抛出SyntaxError
            FreeCAD.Console.PrintMessage(f"[LLMAutoModeler] 代码语法校验通过\n")
            return code, True, ""

        except SyntaxError as e:
            error_msg = f"代码语法错误：{str(e)}"
            FreeCAD.Console.PrintError(f"[LLMAutoModeler] {error_msg}\n")
            return "", False, error_msg

        except Exception as e:
            error_msg = f"代码生成失败：{str(e)}"
            FreeCAD.Console.PrintError(f"[LLMAutoModeler] {error_msg}\n")
            return "", False, error_msg