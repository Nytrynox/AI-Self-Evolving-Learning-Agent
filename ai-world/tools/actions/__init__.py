# Actions Module
"""
Aurora's Action Capabilities:
- file_ops: File system operations (read, write, list, search)
- web_tools: Web operations (search, fetch)
- code_executor: Execute Python code safely
- gui_control: Full GUI automation (mouse, keyboard, apps)
- browser_automation: Advanced Selenium browser control
"""

from .file_ops import get_file_ops
from .web_tools import get_web_tools
from .code_executor import get_code_executor
from .gui_control import get_gui_control
from .browser_automation import get_browser_automation

__all__ = [
    'get_file_ops',
    'get_web_tools', 
    'get_code_executor',
    'get_gui_control',
    'get_browser_automation'
]
