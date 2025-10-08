# core/llm_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# 显式加载 .env 文件
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"[LLMAutoModeler] 未找到 .env 文件，请放在模块根目录: {env_path}")

class LLMClient:
    def __init__(self, llm_type="gemini"):
        self.llm_type = llm_type
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "[LLMAutoModeler] 未找到 GEMINI_API_KEY，请在 .env 文件中配置\n"
                f"文件位置: {env_path}\n"
                "格式: GEMINI_API_KEY=\"你的API密钥\""
            )
        
        # 配置 Gemini
        genai.configure(api_key=self.api_key)

    def call(self, prompt, model="gemini-2.5-flash"):
        """调用 Gemini-2.5-Flash 生成 FreeCAD Python 代码"""
        try:
            model_instance = genai.GenerativeModel(
                model_name=model,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 20000,
                    "response_mime_type": "text/plain"
                }
            )

            system_prompt = """
            你是 FreeCAD 建模专家， 也是结构设计方面的专家，对机械标准件符合的国家标准了如指掌。仅需返回可直接在 FreeCAD 中执行的 Python 代码，不添加任何额外解释、注释或说明。
            在生成标准件代码时，需要搜索相关的国家标准，并确保代码符合标准要求。
            代码需满足：
            1. 使用的 FreeCAD 版本为1.0.2，所有代码均需在该版本中测试通过；
            2. 仅使用 FreeCAD 和 FreeCADGui 模块；
            3. 生成的模型尺寸清晰（如单位用 mm）；
            4. 避免任何危险操作（如文件读写、网络访问）；
            """

            full_prompt = f"{system_prompt}\n用户需求：{prompt}"
            response = model_instance.generate_content(full_prompt)

            # 更安全的响应处理
            if not response.candidates:
                raise ValueError("Gemini API 未返回任何候选结果")

            candidate = response.candidates[0]
            if not candidate.content or not candidate.content.parts:
                raise ValueError("Gemini API 返回的内容为空")

            code = candidate.content.parts[0].text.strip()
            
            # 清理可能的 Markdown 代码块
            if code.startswith("```") and code.endswith("```"):
                code = code.split("```")[1].strip()
                if code.startswith("python"):
                    code = code[6:].strip()
                    
            return code

        except Exception as e:
            raise RuntimeError(f"Gemini API 调用失败: {str(e)}")