"""
GUI CONTROL - Full Computer Control
====================================
Gives Aurora the ability to control mouse, keyboard, 
and interact with the computer like a human.

CAPABILITIES:
- Mouse: move, click, drag, scroll
- Keyboard: type, hotkeys, press keys
- Screen: find images, locate elements
- Apps: open, switch, close applications
- Browser: open URLs, fill forms, click buttons
"""

import logging
import time
import subprocess
from typing import Tuple, Optional, List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class GUIControl:
    """
    Full GUI automation for Aurora.
    Controls mouse, keyboard, and applications.
    """
    
    def __init__(self):
        self.pyautogui_available = False
        self.screen_size = (0, 0)
        
        # Try to import pyautogui
        try:
            import pyautogui
            self.pyautogui = pyautogui
            
            # Safety settings
            pyautogui.FAILSAFE = True  # Move mouse to corner to abort
            pyautogui.PAUSE = 0.1  # Small pause between actions
            
            self.screen_size = pyautogui.size()
            self.pyautogui_available = True
            logger.info(f"🖱️ GUI Control available (screen: {self.screen_size})")
        except ImportError:
            logger.warning("⚠️ pyautogui not installed - GUI control disabled")
            self.pyautogui = None
        
        logger.info("🎮 GUI Control initialized")
    
    # ==========================================
    # MOUSE CONTROL
    # ==========================================
    
    def mouse_move(self, x: int, y: int, duration: float = 0.5) -> bool:
        """Move mouse to absolute position"""
        if not self.pyautogui_available:
            logger.error("GUI control not available")
            return False
        
        try:
            self.pyautogui.moveTo(x, y, duration=duration)
            logger.info(f"🖱️ Mouse moved to ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"❌ Mouse move failed: {e}")
            return False
    
    def mouse_move_relative(self, dx: int, dy: int, duration: float = 0.3) -> bool:
        """Move mouse relative to current position"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.move(dx, dy, duration=duration)
            logger.info(f"🖱️ Mouse moved by ({dx}, {dy})")
            return True
        except Exception as e:
            logger.error(f"❌ Mouse move failed: {e}")
            return False
    
    def mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        if not self.pyautogui_available:
            return (0, 0)
        return self.pyautogui.position()
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1) -> bool:
        """Click at position (or current position if not specified)"""
        if not self.pyautogui_available:
            return False
        
        try:
            if x is not None and y is not None:
                self.pyautogui.click(x, y, clicks=clicks, button=button)
                logger.info(f"🖱️ {button.title()} clicked at ({x}, {y})")
            else:
                self.pyautogui.click(clicks=clicks, button=button)
                pos = self.pyautogui.position()
                logger.info(f"🖱️ {button.title()} clicked at current position {pos}")
            return True
        except Exception as e:
            logger.error(f"❌ Click failed: {e}")
            return False
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Double click"""
        return self.click(x, y, clicks=2)
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Right click"""
        return self.click(x, y, button="right")
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 0.5) -> bool:
        """Drag from one position to another"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.moveTo(start_x, start_y)
            self.pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
            logger.info(f"🖱️ Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
        except Exception as e:
            logger.error(f"❌ Drag failed: {e}")
            return False
    
    def scroll(self, amount: int, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Scroll up (positive) or down (negative)"""
        if not self.pyautogui_available:
            return False
        
        try:
            if x is not None and y is not None:
                self.pyautogui.scroll(amount, x, y)
            else:
                self.pyautogui.scroll(amount)
            direction = "up" if amount > 0 else "down"
            logger.info(f"🖱️ Scrolled {direction} by {abs(amount)}")
            return True
        except Exception as e:
            logger.error(f"❌ Scroll failed: {e}")
            return False
    
    # ==========================================
    # KEYBOARD CONTROL
    # ==========================================
    
    def type_text(self, text: str, interval: float = 0.02) -> bool:
        """Type text like a human"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.write(text, interval=interval)
            logger.info(f"⌨️ Typed: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            return True
        except Exception as e:
            logger.error(f"❌ Type failed: {e}")
            return False
    
    def type_text_slow(self, text: str) -> bool:
        """Type text slowly (for problematic fields)"""
        return self.type_text(text, interval=0.1)
    
    def press_key(self, key: str) -> bool:
        """Press a single key (enter, tab, escape, etc.)"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.press(key)
            logger.info(f"⌨️ Pressed: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ Key press failed: {e}")
            return False
    
    def hotkey(self, *keys) -> bool:
        """Press a hotkey combination (e.g., 'command', 'c' for copy)"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.hotkey(*keys)
            logger.info(f"⌨️ Hotkey: {'+'.join(keys)}")
            return True
        except Exception as e:
            logger.error(f"❌ Hotkey failed: {e}")
            return False
    
    def copy(self) -> bool:
        """Copy (Cmd+C on Mac)"""
        return self.hotkey('command', 'c')
    
    def paste(self) -> bool:
        """Paste (Cmd+V on Mac)"""
        return self.hotkey('command', 'v')
    
    def cut(self) -> bool:
        """Cut (Cmd+X on Mac)"""
        return self.hotkey('command', 'x')
    
    def select_all(self) -> bool:
        """Select all (Cmd+A on Mac)"""
        return self.hotkey('command', 'a')
    
    def undo(self) -> bool:
        """Undo (Cmd+Z on Mac)"""
        return self.hotkey('command', 'z')
    
    def save(self) -> bool:
        """Save (Cmd+S on Mac)"""
        return self.hotkey('command', 's')
    
    def new_tab(self) -> bool:
        """New tab (Cmd+T on Mac)"""
        return self.hotkey('command', 't')
    
    def close_tab(self) -> bool:
        """Close tab (Cmd+W on Mac)"""
        return self.hotkey('command', 'w')
    
    def switch_app(self) -> bool:
        """Switch app (Cmd+Tab on Mac)"""
        return self.hotkey('command', 'tab')
    
    def spotlight(self) -> bool:
        """Open Spotlight (Cmd+Space on Mac)"""
        return self.hotkey('command', 'space')
    
    # ==========================================
    # SCREEN INTERACTION
    # ==========================================
    
    def find_on_screen(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """Find an image on screen and return its center position"""
        if not self.pyautogui_available:
            return None
        
        try:
            location = self.pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = self.pyautogui.center(location)
                logger.info(f"🔍 Found image at ({center.x}, {center.y})")
                return (center.x, center.y)
            else:
                logger.info(f"🔍 Image not found on screen")
                return None
        except Exception as e:
            logger.error(f"❌ Screen search failed: {e}")
            return None
    
    def click_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """Find an image on screen and click it"""
        pos = self.find_on_screen(image_path, confidence)
        if pos:
            return self.click(pos[0], pos[1])
        return False
    
    def wait_for_image(self, image_path: str, timeout: float = 10, 
                       confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """Wait for an image to appear on screen"""
        start = time.time()
        while time.time() - start < timeout:
            pos = self.find_on_screen(image_path, confidence)
            if pos:
                return pos
            time.sleep(0.5)
        logger.warning(f"⏰ Timeout waiting for image")
        return None
    
    def get_pixel_color(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get the RGB color of a pixel"""
        if not self.pyautogui_available:
            return None
        
        try:
            return self.pyautogui.pixel(x, y)
        except Exception as e:
            logger.error(f"❌ Pixel color failed: {e}")
            return None
    
    # ==========================================
    # APPLICATION CONTROL (macOS)
    # ==========================================
    
    def open_app(self, app_name: str) -> bool:
        """Open an application by name"""
        try:
            subprocess.run(['open', '-a', app_name], check=True)
            logger.info(f"🚀 Opened app: {app_name}")
            time.sleep(1)  # Wait for app to launch
            return True
        except Exception as e:
            logger.error(f"❌ Failed to open {app_name}: {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """Open a URL in default browser"""
        try:
            subprocess.run(['open', url], check=True)
            logger.info(f"🌐 Opened URL: {url}")
            time.sleep(2)  # Wait for browser
            return True
        except Exception as e:
            logger.error(f"❌ Failed to open URL: {e}")
            return False
    
    def open_file(self, file_path: str) -> bool:
        """Open a file with default application"""
        try:
            subprocess.run(['open', file_path], check=True)
            logger.info(f"📂 Opened file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to open file: {e}")
            return False
    
    def open_finder(self, path: str = "~") -> bool:
        """Open Finder at a location"""
        try:
            expanded_path = str(Path(path).expanduser())
            subprocess.run(['open', expanded_path], check=True)
            logger.info(f"📁 Opened Finder: {path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to open Finder: {e}")
            return False
    
    def run_applescript(self, script: str) -> Optional[str]:
        """Run an AppleScript command"""
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info(f"🍎 AppleScript executed")
                return result.stdout.strip()
            else:
                logger.error(f"❌ AppleScript error: {result.stderr}")
                return None
        except Exception as e:
            logger.error(f"❌ AppleScript failed: {e}")
            return None
    
    def get_frontmost_app(self) -> Optional[str]:
        """Get the name of the frontmost application"""
        script = 'tell application "System Events" to get name of first application process whose frontmost is true'
        return self.run_applescript(script)
    
    def activate_app(self, app_name: str) -> bool:
        """Bring an app to the front"""
        script = f'tell application "{app_name}" to activate'
        result = self.run_applescript(script)
        return result is not None
    
    def quit_app(self, app_name: str) -> bool:
        """Quit an application"""
        script = f'tell application "{app_name}" to quit'
        result = self.run_applescript(script)
        if result is not None:
            logger.info(f"🛑 Quit app: {app_name}")
            return True
        return False
    
    def minimize_window(self) -> bool:
        """Minimize current window"""
        return self.hotkey('command', 'm')
    
    def maximize_window(self) -> bool:
        """Maximize/fullscreen current window"""
        return self.hotkey('command', 'control', 'f')
    
    def close_window(self) -> bool:
        """Close current window"""
        return self.hotkey('command', 'w')
    
    # ==========================================
    # BROWSER CONTROL
    # ==========================================
    
    def browser_open(self, url: str) -> bool:
        """Open URL in Safari"""
        return self.open_url(url)
    
    def browser_new_tab(self) -> bool:
        """Open new browser tab"""
        return self.new_tab()
    
    def browser_close_tab(self) -> bool:
        """Close current browser tab"""
        return self.close_tab()
    
    def browser_refresh(self) -> bool:
        """Refresh current page"""
        return self.hotkey('command', 'r')
    
    def browser_back(self) -> bool:
        """Go back in browser"""
        return self.hotkey('command', '[')
    
    def browser_forward(self) -> bool:
        """Go forward in browser"""
        return self.hotkey('command', ']')
    
    def browser_address_bar(self) -> bool:
        """Focus address bar"""
        return self.hotkey('command', 'l')
    
    def browser_go_to_url(self, url: str) -> bool:
        """Navigate to URL in current tab"""
        if self.browser_address_bar():
            time.sleep(0.2)
            if self.type_text(url):
                time.sleep(0.1)
                return self.press_key('enter')
        return False
    
    def browser_search(self, query: str) -> bool:
        """Search in browser"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.browser_go_to_url(search_url)
    
    # ==========================================
    # COMPLEX ACTIONS
    # ==========================================
    
    def click_and_type(self, x: int, y: int, text: str) -> bool:
        """Click at position and type text"""
        if self.click(x, y):
            time.sleep(0.2)
            return self.type_text(text)
        return False
    
    def triple_click_and_type(self, x: int, y: int, text: str) -> bool:
        """Triple click to select line, then type replacement"""
        if self.click(x, y, clicks=3):
            time.sleep(0.2)
            return self.type_text(text)
        return False
    
    def click_button_by_text(self, button_text: str) -> bool:
        """
        Try to click a button using AppleScript accessibility.
        Works for native macOS buttons.
        """
        script = f'''
        tell application "System Events"
            tell (first process whose frontmost is true)
                click button "{button_text}" of window 1
            end tell
        end tell
        '''
        result = self.run_applescript(script)
        return result is not None
    
    def fill_form_field(self, field_name: str, value: str) -> bool:
        """
        Fill a form field by name using AppleScript.
        """
        script = f'''
        tell application "System Events"
            tell (first process whose frontmost is true)
                set value of text field "{field_name}" of window 1 to "{value}"
            end tell
        end tell
        '''
        result = self.run_applescript(script)
        return result is not None
    
    def take_action(self, action_type: str, **params) -> Dict[str, Any]:
        """
        Universal action interface for Aurora.
        Returns dict with success status and result.
        """
        result = {"success": False, "action": action_type, "result": None}
        
        try:
            if action_type == "click":
                result["success"] = self.click(params.get("x"), params.get("y"))
            elif action_type == "type":
                result["success"] = self.type_text(params.get("text", ""))
            elif action_type == "hotkey":
                result["success"] = self.hotkey(*params.get("keys", []))
            elif action_type == "open_app":
                result["success"] = self.open_app(params.get("app", ""))
            elif action_type == "open_url":
                result["success"] = self.open_url(params.get("url", ""))
            elif action_type == "scroll":
                result["success"] = self.scroll(params.get("amount", 0))
            elif action_type == "move_mouse":
                result["success"] = self.mouse_move(params.get("x", 0), params.get("y", 0))
            else:
                result["result"] = f"Unknown action: {action_type}"
            
            result["result"] = "completed" if result["success"] else "failed"
            
        except Exception as e:
            result["result"] = str(e)
        
        return result
    
    def get_capabilities(self) -> List[str]:
        """Return list of available capabilities"""
        if not self.pyautogui_available:
            return ["open_app", "open_url", "open_file", "applescript"]
        
        return [
            "mouse_move", "click", "double_click", "right_click", "drag", "scroll",
            "type_text", "press_key", "hotkey", "copy", "paste", "cut", "select_all",
            "open_app", "open_url", "open_file", "activate_app", "quit_app",
            "browser_open", "browser_search", "browser_go_to_url",
            "find_on_screen", "click_image", "click_button_by_text"
        ]


# Global instance
_gui_control = None

def get_gui_control() -> GUIControl:
    """Get GUI control instance"""
    global _gui_control
    if _gui_control is None:
        _gui_control = GUIControl()
    return _gui_control
