"""
SMART EXECUTOR - Intelligent Natural Language Command Processor
===============================================================
Understands natural language commands and executes complex multi-step tasks.

Features:
- Natural language understanding
- Multi-step task planning
- Screen analysis for smart actions
- YouTube/Web automation
- System control (WiFi, Bluetooth, Volume, etc.)
- Self-learning from successful executions
"""

import os
import re
import time
import json
import logging
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import required modules
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("pyautogui not available")

try:
    from tools.macos_commands import MacOSCommands
    MACOS_COMMANDS_AVAILABLE = True
except ImportError:
    MACOS_COMMANDS_AVAILABLE = False
    logger.warning("MacOSCommands not available")


class SmartExecutor:
    """
    Intelligent command executor that understands natural language
    and performs complex multi-step tasks.
    """
    
    def __init__(self, llm_interface=None):
        self.llm = llm_interface
        self.macos = MacOSCommands() if MACOS_COMMANDS_AVAILABLE else None
        
        # Action history for learning
        self.action_history = []
        self.learned_patterns = {}
        
        # Load learned patterns
        self.patterns_file = Path("aurora_memory/learned_patterns.json")
        self._load_patterns()
        
        # Command patterns for quick matching
        self.command_patterns = self._build_command_patterns()
        
        logger.info("🧠 Smart Executor initialized")
    
    def _load_patterns(self):
        """Load learned command patterns"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    self.learned_patterns = json.load(f)
            except:
                self.learned_patterns = {}
    
    def _save_patterns(self):
        """Save learned patterns"""
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.patterns_file, 'w') as f:
            json.dump(self.learned_patterns, f, indent=2)
    
    def _build_command_patterns(self) -> Dict[str, Dict]:
        """Build regex patterns for common commands"""
        return {
            # WiFi Control
            r"(turn\s+)?(wifi|wi-fi)\s+(on|off|enable|disable)": {
                "action": "wifi_control",
                "extract": ["state"]
            },
            r"(connect\s+to\s+)?wifi\s+(.+)": {
                "action": "wifi_connect",
                "extract": ["network"]
            },
            
            # Bluetooth
            r"(turn\s+)?(bluetooth)\s+(on|off|enable|disable)": {
                "action": "bluetooth_control",
                "extract": ["state"]
            },
            
            # Volume
            r"(set\s+)?volume\s+(to\s+)?(\d+)(%)?": {
                "action": "set_volume",
                "extract": ["level"]
            },
            r"(turn\s+)?volume\s+(up|down|mute|unmute)": {
                "action": "volume_control",
                "extract": ["direction"]
            },
            r"(mute|unmute)(\s+volume)?": {
                "action": "volume_mute",
                "extract": ["state"]
            },
            
            # Brightness
            r"(set\s+)?brightness\s+(to\s+)?(\d+)(%)?": {
                "action": "set_brightness",
                "extract": ["level"]
            },
            r"(turn\s+)?brightness\s+(up|down)": {
                "action": "brightness_control",
                "extract": ["direction"]
            },
            
            # Dark Mode
            r"(turn\s+)?(dark\s+mode|darkmode)\s+(on|off|enable|disable)": {
                "action": "dark_mode",
                "extract": ["state"]
            },
            r"(enable|disable)\s+(dark\s+mode|darkmode)": {
                "action": "dark_mode",
                "extract": ["state"]
            },
            
            # Do Not Disturb
            r"(turn\s+)?(do\s+not\s+disturb|dnd)\s+(on|off)": {
                "action": "dnd_control",
                "extract": ["state"]
            },
            
            # YouTube
            r"(open\s+)?youtube\s+(and\s+)?(play|search)?\s*(.+)?": {
                "action": "youtube",
                "extract": ["operation", "query"]
            },
            r"play\s+(.+)\s+(on\s+)?youtube": {
                "action": "youtube_play",
                "extract": ["query"]
            },
            r"search\s+(youtube|yt)\s+(for\s+)?(.+)": {
                "action": "youtube_search",
                "extract": ["query"]
            },
            
            # Web Search
            r"(google|search\s+for|search)\s+(.+)": {
                "action": "web_search",
                "extract": ["query"]
            },
            
            # Open Apps
            r"open\s+(.+)": {
                "action": "open_app",
                "extract": ["app"]
            },
            r"close\s+(.+)": {
                "action": "close_app",
                "extract": ["app"]
            },
            r"launch\s+(.+)": {
                "action": "open_app",
                "extract": ["app"]
            },
            
            # Screenshots
            r"(take\s+)?(a\s+)?screenshot": {
                "action": "screenshot",
                "extract": []
            },
            r"(screen\s+)?capture": {
                "action": "screenshot",
                "extract": []
            },
            
            # System
            r"(put\s+)?(computer|mac|system)\s+(to\s+)?sleep": {
                "action": "sleep",
                "extract": []
            },
            r"lock\s+(screen|computer|mac)": {
                "action": "lock_screen",
                "extract": []
            },
            r"(show\s+)?battery(\s+level)?": {
                "action": "get_battery",
                "extract": []
            },
            
            # Files
            r"(open|show)\s+(finder|files)": {
                "action": "open_finder",
                "extract": []
            },
            r"empty\s+(the\s+)?trash": {
                "action": "empty_trash",
                "extract": []
            },
        }
    
    def execute(self, command: str) -> Dict[str, Any]:
        """
        Execute a natural language command.
        Returns dict with status, result, and any output.
        """
        command = command.strip().lower()
        result = {
            "success": False,
            "command": command,
            "action": None,
            "output": None,
            "error": None,
            "steps": []
        }
        
        try:
            # First, try pattern matching for fast execution
            action_result = self._match_and_execute(command)
            if action_result:
                result.update(action_result)
                self._record_success(command, action_result)
                return result
            
            # If no pattern matched, use LLM to understand and plan
            if self.llm:
                plan = self._plan_with_llm(command)
                if plan:
                    result = self._execute_plan(plan)
                    if result["success"]:
                        self._record_success(command, result)
                    return result
            
            # Fallback: try direct command execution
            result["error"] = "Could not understand command"
            result["output"] = f"I couldn't understand '{command}'. Try being more specific."
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Execution error: {e}")
        
        return result
    
    def _match_and_execute(self, command: str) -> Optional[Dict]:
        """Match command against patterns and execute"""
        
        for pattern, config in self.command_patterns.items():
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                action = config["action"]
                groups = match.groups()
                
                # Execute based on action type
                if action == "wifi_control":
                    state = self._extract_state(command, ["on", "enable"], ["off", "disable"])
                    return self._execute_wifi(state)
                
                elif action == "bluetooth_control":
                    state = self._extract_state(command, ["on", "enable"], ["off", "disable"])
                    return self._execute_bluetooth(state)
                
                elif action == "volume_control":
                    if "up" in command:
                        return self._execute_volume("up")
                    elif "down" in command:
                        return self._execute_volume("down")
                    elif "mute" in command:
                        return self._execute_volume("mute")
                    elif "unmute" in command:
                        return self._execute_volume("unmute")
                
                elif action == "set_volume":
                    level = self._extract_number(command)
                    if level is not None:
                        return self._execute_set_volume(level)
                
                elif action == "dark_mode":
                    state = self._extract_state(command, ["on", "enable"], ["off", "disable"])
                    return self._execute_dark_mode(state)
                
                elif action == "dnd_control":
                    state = self._extract_state(command, ["on"], ["off"])
                    return self._execute_dnd(state)
                
                elif action in ["youtube", "youtube_play", "youtube_search"]:
                    query = self._extract_query(command, ["play", "search", "youtube", "and", "on", "for"])
                    return self._execute_youtube(query)
                
                elif action == "web_search":
                    query = self._extract_query(command, ["google", "search", "for"])
                    return self._execute_web_search(query)
                
                elif action == "open_app":
                    app = self._extract_query(command, ["open", "launch"])
                    return self._execute_open_app(app)
                
                elif action == "close_app":
                    app = self._extract_query(command, ["close", "quit"])
                    return self._execute_close_app(app)
                
                elif action == "screenshot":
                    return self._execute_screenshot()
                
                elif action == "sleep":
                    return self._execute_system_command("sleep")
                
                elif action == "lock_screen":
                    return self._execute_system_command("lock_screen")
                
                elif action == "get_battery":
                    return self._execute_system_command("get_battery")
                
                elif action == "open_finder":
                    return self._execute_open_app("Finder")
                
                elif action == "empty_trash":
                    return self._execute_system_command("empty_trash")
        
        return None
    
    def _extract_state(self, command: str, on_words: List[str], off_words: List[str]) -> bool:
        """Extract on/off state from command"""
        for word in on_words:
            if word in command:
                return True
        for word in off_words:
            if word in command:
                return False
        return True  # Default to on
    
    def _extract_number(self, command: str) -> Optional[int]:
        """Extract number from command"""
        match = re.search(r'(\d+)', command)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_query(self, command: str, remove_words: List[str]) -> str:
        """Extract query by removing known words"""
        query = command
        for word in remove_words:
            query = re.sub(rf'\b{word}\b', '', query, flags=re.IGNORECASE)
        return query.strip()
    
    # ========================================
    # EXECUTION METHODS
    # ========================================
    
    def _execute_wifi(self, on: bool) -> Dict:
        """Turn WiFi on or off"""
        cmd = "networksetup -setairportpower en0 on" if on else "networksetup -setairportpower en0 off"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            state = "on" if on else "off"
            return {
                "success": True,
                "action": f"wifi_{state}",
                "output": f"WiFi turned {state}",
                "steps": [f"Executed: {cmd}"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_bluetooth(self, on: bool) -> Dict:
        """Turn Bluetooth on or off"""
        cmd = "blueutil -p 1" if on else "blueutil -p 0"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            state = "on" if on else "off"
            return {
                "success": True,
                "action": f"bluetooth_{state}",
                "output": f"Bluetooth turned {state}",
                "steps": [f"Executed: {cmd}"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_volume(self, direction: str) -> Dict:
        """Control volume"""
        if direction == "up":
            cmd = "osascript -e 'set volume output volume ((output volume of (get volume settings)) + 10)'"
        elif direction == "down":
            cmd = "osascript -e 'set volume output volume ((output volume of (get volume settings)) - 10)'"
        elif direction == "mute":
            cmd = "osascript -e 'set volume with output muted'"
        elif direction == "unmute":
            cmd = "osascript -e 'set volume without output muted'"
        else:
            return {"success": False, "error": f"Unknown volume direction: {direction}"}
        
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            return {
                "success": True,
                "action": f"volume_{direction}",
                "output": f"Volume {direction}",
                "steps": [cmd]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_set_volume(self, level: int) -> Dict:
        """Set volume to specific level"""
        level = max(0, min(100, level))
        cmd = f"osascript -e 'set volume output volume {level}'"
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            return {
                "success": True,
                "action": "set_volume",
                "output": f"Volume set to {level}%",
                "steps": [cmd]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_dark_mode(self, on: bool) -> Dict:
        """Toggle dark mode"""
        state = "true" if on else "false"
        cmd = f'osascript -e \'tell application "System Events" to tell appearance preferences to set dark mode to {state}\''
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            return {
                "success": True,
                "action": "dark_mode",
                "output": f"Dark mode {'enabled' if on else 'disabled'}",
                "steps": [cmd]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_dnd(self, on: bool) -> Dict:
        """Toggle Do Not Disturb"""
        state = "true" if on else "false"
        cmd = f'defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean {state} && killall NotificationCenter 2>/dev/null || true'
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            return {
                "success": True,
                "action": "dnd",
                "output": f"Do Not Disturb {'enabled' if on else 'disabled'}",
                "steps": [cmd]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_youtube(self, query: str) -> Dict:
        """Open YouTube and search/play"""
        steps = []
        
        if not query or query.strip() == "":
            # Just open YouTube
            cmd = 'open "https://www.youtube.com"'
            subprocess.run(cmd, shell=True)
            steps.append("Opened YouTube")
            return {
                "success": True,
                "action": "youtube_open",
                "output": "Opened YouTube",
                "steps": steps
            }
        
        # Clean and encode query
        query = query.strip()
        query_encoded = query.replace(" ", "+")
        
        # Open YouTube search
        url = f"https://www.youtube.com/results?search_query={query_encoded}"
        cmd = f'open "{url}"'
        subprocess.run(cmd, shell=True)
        steps.append(f"Searched YouTube for: {query}")
        
        # Wait for page to load
        time.sleep(3)
        
        # Try to click first video using keyboard (Tab + Enter)
        if PYAUTOGUI_AVAILABLE:
            try:
                # Press Tab a few times to reach first video, then Enter
                time.sleep(1)
                for _ in range(3):
                    pyautogui.press('tab')
                    time.sleep(0.2)
                pyautogui.press('enter')
                steps.append("Clicked first video result")
            except Exception as e:
                steps.append(f"Could not auto-play: {e}")
        
        return {
            "success": True,
            "action": "youtube_search_play",
            "output": f"Searching YouTube for '{query}' and attempting to play",
            "steps": steps
        }
    
    def _execute_web_search(self, query: str) -> Dict:
        """Search Google"""
        query_encoded = query.strip().replace(" ", "+")
        url = f"https://www.google.com/search?q={query_encoded}"
        cmd = f'open "{url}"'
        subprocess.run(cmd, shell=True)
        return {
            "success": True,
            "action": "web_search",
            "output": f"Searching Google for: {query}",
            "steps": [cmd]
        }
    
    def _execute_open_app(self, app: str) -> Dict:
        """Open an application"""
        app = app.strip()
        
        # Common app name mappings
        app_mappings = {
            "chrome": "Google Chrome",
            "safari": "Safari",
            "firefox": "Firefox",
            "code": "Visual Studio Code",
            "vscode": "Visual Studio Code",
            "terminal": "Terminal",
            "finder": "Finder",
            "notes": "Notes",
            "music": "Music",
            "spotify": "Spotify",
            "slack": "Slack",
            "discord": "Discord",
            "settings": "System Preferences",
            "preferences": "System Preferences",
            "calculator": "Calculator",
            "calendar": "Calendar",
            "mail": "Mail",
            "messages": "Messages",
            "photos": "Photos",
            "preview": "Preview",
        }
        
        app_name = app_mappings.get(app.lower(), app.title())
        cmd = f'open -a "{app_name}"'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return {
                    "success": True,
                    "action": "open_app",
                    "output": f"Opened {app_name}",
                    "steps": [cmd]
                }
            else:
                return {
                    "success": False,
                    "error": f"Could not open {app_name}: {result.stderr}"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_close_app(self, app: str) -> Dict:
        """Close an application"""
        app = app.strip()
        cmd = f'osascript -e \'tell application "{app}" to quit\''
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            return {
                "success": True,
                "action": "close_app",
                "output": f"Closed {app}",
                "steps": [cmd]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_screenshot(self) -> Dict:
        """Take a screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"~/Desktop/screenshot_{timestamp}.png"
        cmd = f"screencapture -x {path}"
        try:
            subprocess.run(cmd, shell=True)
            return {
                "success": True,
                "action": "screenshot",
                "output": f"Screenshot saved to {path}",
                "steps": [cmd]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_system_command(self, command: str) -> Dict:
        """Execute a system command from MacOSCommands"""
        if not self.macos:
            return {"success": False, "error": "MacOS commands not available"}
        
        try:
            result = self.macos.execute(command)
            return {
                "success": True,
                "action": command,
                "output": result,
                "steps": [command]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _plan_with_llm(self, command: str) -> Optional[List[Dict]]:
        """Use LLM to plan complex commands"""
        if not self.llm:
            return None
        
        prompt = f"""You are a macOS automation assistant. 
Given this command: "{command}"

Create a step-by-step plan to execute it. For each step, specify:
- action: the action type (open_app, click, type, wait, shell_command)
- target: what to act on
- value: any value needed (text to type, coordinates, etc.)

Return as JSON array. Example:
[
  {{"action": "open_app", "target": "Safari"}},
  {{"action": "wait", "value": 2}},
  {{"action": "type", "value": "youtube.com"}},
  {{"action": "key", "value": "enter"}}
]

Only return the JSON array, nothing else."""
        
        try:
            response = self.llm.generate(prompt)
            if response:
                # Try to parse JSON from response
                import json
                # Find JSON array in response
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]
                    return json.loads(json_str)
        except Exception as e:
            logger.error(f"LLM planning error: {e}")
        
        return None
    
    def _execute_plan(self, plan: List[Dict]) -> Dict:
        """Execute a planned sequence of actions"""
        results = {
            "success": True,
            "action": "planned_execution",
            "output": "",
            "steps": []
        }
        
        for step in plan:
            action = step.get("action", "")
            target = step.get("target", "")
            value = step.get("value", "")
            
            try:
                if action == "open_app":
                    res = self._execute_open_app(target)
                elif action == "wait":
                    time.sleep(float(value) if value else 1)
                    res = {"success": True, "output": f"Waited {value}s"}
                elif action == "type":
                    if PYAUTOGUI_AVAILABLE:
                        pyautogui.write(str(value))
                        res = {"success": True, "output": f"Typed: {value}"}
                    else:
                        res = {"success": False, "error": "pyautogui not available"}
                elif action == "key":
                    if PYAUTOGUI_AVAILABLE:
                        pyautogui.press(str(value))
                        res = {"success": True, "output": f"Pressed: {value}"}
                    else:
                        res = {"success": False, "error": "pyautogui not available"}
                elif action == "click":
                    if PYAUTOGUI_AVAILABLE:
                        if target:
                            x, y = map(int, target.split(','))
                            pyautogui.click(x, y)
                        else:
                            pyautogui.click()
                        res = {"success": True, "output": f"Clicked at {target}"}
                    else:
                        res = {"success": False, "error": "pyautogui not available"}
                elif action == "shell_command":
                    result = subprocess.run(value, shell=True, capture_output=True, text=True)
                    res = {"success": result.returncode == 0, "output": result.stdout}
                else:
                    res = {"success": False, "error": f"Unknown action: {action}"}
                
                results["steps"].append(f"{action}: {res.get('output', res.get('error', ''))}")
                
                if not res.get("success", False):
                    results["success"] = False
                    results["error"] = res.get("error", "Step failed")
                    break
                    
            except Exception as e:
                results["success"] = False
                results["error"] = str(e)
                results["steps"].append(f"Error: {e}")
                break
        
        results["output"] = " -> ".join(results["steps"])
        return results
    
    def _record_success(self, command: str, result: Dict):
        """Record successful command for learning"""
        self.action_history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "action": result.get("action"),
            "success": result.get("success", False)
        })
        
        # Save pattern if new
        action = result.get("action", "")
        if action and action not in self.learned_patterns:
            self.learned_patterns[action] = {
                "example_command": command,
                "success_count": 1,
                "last_used": datetime.now().isoformat()
            }
        elif action:
            self.learned_patterns[action]["success_count"] += 1
            self.learned_patterns[action]["last_used"] = datetime.now().isoformat()
        
        self._save_patterns()


# Singleton instance
_executor = None

def get_smart_executor(llm_interface=None) -> SmartExecutor:
    """Get or create SmartExecutor instance"""
    global _executor
    if _executor is None:
        _executor = SmartExecutor(llm_interface)
    return _executor
