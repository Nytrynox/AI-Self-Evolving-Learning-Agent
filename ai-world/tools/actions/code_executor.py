"""
CODE EXECUTOR - Execute Python Code
==================================
Allows Aurora to run Python code.
"""

import sys
import logging
import subprocess
import tempfile
from typing import Dict, Optional
from io import StringIO

logger = logging.getLogger(__name__)


class CodeExecutor:
    """
    Execute Python code safely.
    """
    
    def __init__(self):
        logger.info("⚡ Code Executor initialized")
    
    def execute_python(self, code: str, timeout: int = 30) -> Dict:
        """
        Execute Python code and return result.
        """
        try:
            # Create temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            # Execute
            result = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Cleanup
            import os
            os.unlink(temp_path)
            
            success = result.returncode == 0
            
            logger.info(f"⚡ Code executed: {'✅' if success else '❌'}")
            
            return {
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            logger.error("❌ Code execution timeout")
            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out",
                "return_code": -1
            }
        except Exception as e:
            logger.error(f"❌ Execution failed: {e}")
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }
    
    def execute_shell(self, command: str, timeout: int = 30) -> Dict:
        """
        Execute shell command.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            logger.info(f"🖥️ Shell: {command[:50]}... {'✅' if success else '❌'}")
            
            return {
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }
    
    def eval_expression(self, expression: str) -> Optional[str]:
        """
        Evaluate a simple Python expression.
        """
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            logger.error(f"❌ Eval failed: {e}")
            return None


# Global instance
_executor = None

def get_code_executor() -> CodeExecutor:
    """Get code executor instance"""
    global _executor
    if _executor is None:
        _executor = CodeExecutor()
    return _executor
