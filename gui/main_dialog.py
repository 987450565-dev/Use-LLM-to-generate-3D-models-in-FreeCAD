from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
import FreeCAD as App
import FreeCADGui as Gui

class LLMAutoModelerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gemini 自动建模")  # 标题改为 Gemini
        self.resize(500, 400)

        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("请描述你想要的模型（如：边长10mm的立方体）："))
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("例如：创建一个直径20mm、高度30mm的圆柱体")
        layout.addWidget(self.prompt_input)

        btn_generate = QPushButton("生成模型（Gemini-2.5-Flash）", self)  # 按钮文本标注模型
        btn_generate.clicked.connect(self.generate_model)
        layout.addWidget(btn_generate)

    def generate_model(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "提示", "请输入模型描述")
            return

        try:
            # 调用 Gemini 客户端
            from core.llm_client import LLMClient
            client = LLMClient()
            App.Console.PrintMessage("[LLMAutoModeler] 正在调用 Gemini-2.5-Flash...\n")
            
            # 获取生成的代码
            code = client.call(prompt)
            App.Console.PrintMessage(f"[LLMAutoModeler] 生成的代码:\n{code}\n")

            # 安全检查（通用逻辑，不受模型影响）
            from core.code_safety import safe_check_code, safe_exec_code
            is_safe, message = safe_check_code(code)
            if not is_safe:
                QMessageBox.critical(self, "代码不安全", f"检测到潜在危险操作：\n{message}\n\n代码未执行！")
                return

            # 执行代码生成模型
            App.newDocument("GeminiAutoModel")  # 文档名改为 Gemini
            safe_exec_code(code)
            # 安全地调整视图
            try:
                doc = Gui.activeDocument()
                if doc and doc.activeView():
                    doc.activeView().viewFit()
                else:
                    App.Console.PrintWarning("[LLMAutoModeler] 没有找到激活的视图，无法调整视图\n")
            except Exception as e:
                App.Console.PrintError(f"[LLMAutoModeler] 调整视图失败: {e}\n")
            
            QMessageBox.information(self, "成功", "模型生成成功！（由 Gemini-2.5-Flash 驱动）")

        except Exception as e:
            App.Console.PrintError(f"[LLMAutoModeler] 生成模型失败: {e}\n")
            QMessageBox.critical(self, "错误", f"生成模型失败: {str(e)}\n（请检查 Gemini API 密钥和网络）")
