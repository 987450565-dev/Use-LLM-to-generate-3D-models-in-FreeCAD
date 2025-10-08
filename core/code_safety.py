# core/code_safety.py
import re

# 危险操作黑名单（覆盖文件、系统、网络等危险行为）
DANGEROUS_PATTERNS = [
    # 文件操作
    r"open\(", r"file\(", r"os\.open\(", r"os\.remove\(", r"os\.unlink\(",
    r"os\.rmdir\(", r"os\.makedirs\(", r"shutil\.rmtree\(", r"shutil\.move\(",
    
    # 系统命令
    r"subprocess\.", r"os\.system\(", r"os\.popen\(", r"popen2\.", r"commands\.",
    
    # 网络访问
    r"requests\.get\(", r"requests\.post\(", r"urllib\.request\.", r"http\.client\.",
    r"socket\.", r"ftplib\.", r"google\.generativeai",  # 禁止代码中再次调用 LLM API
    
    # 其他危险操作
    r"exec\(", r"eval\(", r"compile\(", r"globals\(", r"locals\(", r"__import__\(",
    r"builtins\.", r"__builtins__", r"quit\(", r"exit\(", r"delattr\(", r"setattr\(",
    r"getattr\(", r"sys\.modules", r"sys\.exit\(", r"os\.fork\(", r"os\.spawn\(",
]

def safe_check_code(code):
    """检查代码是否包含危险操作"""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            return False, f"检测到危险操作: {pattern}"
    return True, "代码安全检查通过"

def safe_exec_code(code):
    """在限制环境中执行代码（仅允许 FreeCAD 相关模块）"""
    allowed_modules = {
        "FreeCAD": __import__("FreeCAD"),
        "FreeCADGui": __import__("FreeCADGui"),
    }
    exec(code, allowed_modules)