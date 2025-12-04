#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║            VISION AI BRAIN - TRUE NLP SCREEN UNDERSTANDING                       ║
║    Takes screenshots, analyzes with LLaVA, executes actions intelligently        ║
║                    NO PREDEFINED PATTERNS - PURE AI UNDERSTANDING                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

This is the core AI brain that:
1. Takes screenshots of the screen
2. Sends to LLaVA vision model for REAL understanding
3. Uses LLM to decide what actions to take
4. Executes keyboard/mouse actions based on intelligent understanding
"""

import subprocess
import tempfile
import os
import json
import base64
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import requests


@dataclass
class ScreenElement:
    """Detected UI element on screen"""
    element_type: str  # button, text_field, link, menu, icon, etc.
    description: str
    x: int
    y: int
    width: int = 0
    height: int = 0
    text: str = ""
    clickable: bool = True
    confidence: float = 0.8


@dataclass
class ActionPlan:
    """AI-generated action plan"""
    goal: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.8
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class VisionAIBrain:
    """
    TRUE NLP Vision-Based AI Brain
    
    Uses LLaVA vision model to understand what's on screen
    and intelligently decide what actions to take.
    """
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.vision_model = "llava:7b"  # Vision model for screen analysis
        self.text_model = "llama3.2:3b"  # Text model for reasoning
        
        # Screen state
        self.last_screenshot_path: Optional[str] = None
        self.last_analysis: Dict = {}
        self.screen_elements: List[ScreenElement] = []
        
        # Learning memory
        self.memory_path = Path("aurora_memory")
        self.memory_path.mkdir(exist_ok=True)
        self.action_memory_file = self.memory_path / "vision_action_memory.json"
        self.action_memory = self._load_action_memory()
        
        # Action history for learning
        self.action_history: List[Dict] = []
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
        print("VisionAIBrain initialized - TRUE NLP Understanding Active")
    
    def _load_action_memory(self) -> Dict:
        """Load previous action memory"""
        try:
            if self.action_memory_file.exists():
                with open(self.action_memory_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading action memory: {e}")
        return {
            "successful_actions": [],
            "failed_actions": [],
            "learned_patterns": {},
            "element_locations": {}
        }
    
    def _save_action_memory(self):
        """Save action memory"""
        try:
            with open(self.action_memory_file, 'w') as f:
                json.dump(self.action_memory, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving action memory: {e}")
    
    def take_screenshot(self) -> Optional[str]:
        """Take a screenshot and return the path"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                path = tmp.name
            
            # Use screencapture on macOS
            result = subprocess.run(
                ['screencapture', '-x', path],
                timeout=5,
                capture_output=True
            )
            
            if result.returncode == 0 and os.path.exists(path):
                self.last_screenshot_path = path
                return path
            return None
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def _encode_image_base64(self, image_path: str) -> Optional[str]:
        """Encode image to base64 for LLaVA"""
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"Image encoding error: {e}")
            return None
    
    def analyze_screen(self, task: str = None) -> Dict:
        """
        Analyze current screen using LLaVA vision model.
        This is TRUE AI understanding - no predefined patterns!
        
        Args:
            task: Optional task context to help AI understand what to look for
        
        Returns:
            Dictionary with screen analysis
        """
        # Take screenshot
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return {"error": "Failed to take screenshot"}
        
        # Encode image
        image_base64 = self._encode_image_base64(screenshot_path)
        if not image_base64:
            return {"error": "Failed to encode screenshot"}
        
        # Build analysis prompt
        if task:
            prompt = f"""Analyze this screenshot. I need to: {task}

Describe:
1. What application/window is currently active?
2. What UI elements do you see (buttons, text fields, links, menus)?
3. Where should I click or type to accomplish the task?
4. Provide approximate coordinates (as percentage of screen) for key elements.

Be specific and actionable. Format response as:
ACTIVE_APP: <app name>
VISIBLE_ELEMENTS:
- <element>: <description> (location: <x%>, <y%>)
RECOMMENDED_ACTION: <what to do>
TARGET_LOCATION: <x%>, <y%>"""
        else:
            prompt = """Analyze this screenshot comprehensively.

Describe:
1. What application/window is currently active?
2. What are the main UI elements visible?
3. What actions appear possible?
4. Current state of the interface.

Format response as:
ACTIVE_APP: <app name>
INTERFACE_STATE: <description>
VISIBLE_ELEMENTS:
- <element>: <description> (location: <x%>, <y%>)
POSSIBLE_ACTIONS:
- <action 1>
- <action 2>"""
        
        try:
            # Call LLaVA for vision analysis
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.vision_model,
                    "prompt": prompt,
                    "images": [image_base64],
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 1024
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get("response", "")
                
                self.last_analysis = {
                    "raw_response": analysis,
                    "task": task,
                    "timestamp": datetime.now().isoformat(),
                    "screenshot_path": screenshot_path
                }
                
                # Parse the analysis
                parsed = self._parse_analysis(analysis)
                self.last_analysis.update(parsed)
                
                return self.last_analysis
            else:
                return {"error": f"LLaVA request failed: {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"error": "LLaVA request timed out"}
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}
        finally:
            # Clean up screenshot
            try:
                if screenshot_path and os.path.exists(screenshot_path):
                    os.unlink(screenshot_path)
            except:
                pass
    
    def _parse_analysis(self, analysis: str) -> Dict:
        """Parse LLaVA analysis response into structured data"""
        result = {
            "active_app": "",
            "interface_state": "",
            "elements": [],
            "recommended_action": "",
            "target_location": None,
            "possible_actions": []
        }
        
        lines = analysis.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("ACTIVE_APP:"):
                result["active_app"] = line.replace("ACTIVE_APP:", "").strip()
            elif line.startswith("INTERFACE_STATE:"):
                result["interface_state"] = line.replace("INTERFACE_STATE:", "").strip()
            elif line.startswith("VISIBLE_ELEMENTS:"):
                current_section = "elements"
            elif line.startswith("RECOMMENDED_ACTION:"):
                result["recommended_action"] = line.replace("RECOMMENDED_ACTION:", "").strip()
            elif line.startswith("TARGET_LOCATION:"):
                loc = line.replace("TARGET_LOCATION:", "").strip()
                try:
                    # Parse "x%, y%" format
                    parts = loc.replace("%", "").split(",")
                    if len(parts) >= 2:
                        x_pct = float(parts[0].strip())
                        y_pct = float(parts[1].strip())
                        result["target_location"] = {"x_percent": x_pct, "y_percent": y_pct}
                except:
                    pass
            elif line.startswith("POSSIBLE_ACTIONS:"):
                current_section = "actions"
            elif line.startswith("-") and current_section == "elements":
                result["elements"].append(line[1:].strip())
            elif line.startswith("-") and current_section == "actions":
                result["possible_actions"].append(line[1:].strip())
        
        return result
    
    def generate_action_plan(self, user_request: str) -> ActionPlan:
        """
        Generate an intelligent action plan based on user request.
        Uses LLM to reason about what actions to take.
        
        Args:
            user_request: Natural language description of what user wants
        
        Returns:
            ActionPlan with steps to execute
        """
        # First, analyze the current screen with task context
        screen_analysis = self.analyze_screen(task=user_request)
        
        if "error" in screen_analysis:
            return ActionPlan(
                goal=user_request,
                steps=[],
                reasoning=f"Error analyzing screen: {screen_analysis['error']}",
                confidence=0.0
            )
        
        # Build planning prompt
        prompt = f"""You are an AI assistant that controls a computer. Based on the screen analysis and user request, create an action plan.

USER REQUEST: {user_request}

CURRENT SCREEN STATE:
- Active App: {screen_analysis.get('active_app', 'Unknown')}
- Interface: {screen_analysis.get('interface_state', 'Unknown')}
- Visible Elements: {screen_analysis.get('elements', [])}
- Recommended Action: {screen_analysis.get('recommended_action', 'None')}
- Target Location: {screen_analysis.get('target_location', 'None')}

Generate a step-by-step action plan. Each step should be one of:
1. CLICK x y - Click at coordinates (use percentages, e.g., CLICK 50 50 for center)
2. TYPE text - Type the specified text
3. KEY key_name - Press a key (e.g., KEY enter, KEY tab, KEY escape)
4. HOTKEY key1+key2 - Press key combination (e.g., HOTKEY cmd+t, HOTKEY cmd+l)
5. SCROLL direction - Scroll up or down
6. WAIT seconds - Wait for specified time
7. SCREENSHOT - Take screenshot to check progress

Response format (JSON):
{{
    "reasoning": "explanation of the plan",
    "steps": [
        {{"action": "CLICK", "x": 50, "y": 10, "description": "Click address bar"}},
        {{"action": "TYPE", "text": "youtube.com", "description": "Type URL"}},
        {{"action": "KEY", "key": "enter", "description": "Navigate to site"}}
    ],
    "confidence": 0.8
}}

IMPORTANT: Use ACTUAL coordinates based on where you saw elements in the screenshot.
If you need to open an app, use HOTKEY cmd+space then TYPE app name then KEY enter.
For browser address bar, use HOTKEY cmd+l to focus it."""

        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.text_model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 1024
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "{}")
                
                # Parse JSON response
                try:
                    plan_data = json.loads(response_text)
                except json.JSONDecodeError:
                    # Try to extract JSON from response
                    import re
                    json_match = re.search(r'\{[\s\S]*\}', response_text)
                    if json_match:
                        plan_data = json.loads(json_match.group())
                    else:
                        plan_data = {"steps": [], "reasoning": response_text, "confidence": 0.5}
                
                return ActionPlan(
                    goal=user_request,
                    steps=plan_data.get("steps", []),
                    reasoning=plan_data.get("reasoning", ""),
                    confidence=plan_data.get("confidence", 0.7)
                )
            
        except Exception as e:
            print(f"Error generating plan: {e}")
        
        return ActionPlan(goal=user_request, steps=[], reasoning="Failed to generate plan", confidence=0.0)
    
    def execute_action(self, action: Dict) -> Dict:
        """
        Execute a single action from the plan.
        
        Args:
            action: Action dictionary with type and parameters
        
        Returns:
            Result dictionary with success status
        """
        action_type = action.get("action", "").upper()
        result = {"success": False, "action": action}
        
        try:
            if action_type == "CLICK":
                x_pct = action.get("x", 50)
                y_pct = action.get("y", 50)
                result = self._execute_click(x_pct, y_pct)
                
            elif action_type == "TYPE":
                text = action.get("text", "")
                result = self._execute_type(text)
                
            elif action_type == "KEY":
                key = action.get("key", "")
                result = self._execute_key(key)
                
            elif action_type == "HOTKEY":
                keys = action.get("keys", "")
                if not keys:
                    # Parse from key field if present
                    keys = action.get("key", "")
                result = self._execute_hotkey(keys)
                
            elif action_type == "SCROLL":
                direction = action.get("direction", "down")
                result = self._execute_scroll(direction)
                
            elif action_type == "WAIT":
                seconds = action.get("seconds", 1)
                time.sleep(seconds)
                result = {"success": True, "action": action}
                
            elif action_type == "SCREENSHOT":
                path = self.take_screenshot()
                result = {"success": path is not None, "action": action, "path": path}
            
            # Record action for learning
            self._record_action(action, result)
            
        except Exception as e:
            result = {"success": False, "action": action, "error": str(e)}
            self._record_action(action, result)
        
        return result
    
    def _execute_click(self, x_percent: float, y_percent: float) -> Dict:
        """Execute click at percentage coordinates"""
        try:
            # Get screen dimensions
            script = '''
            tell application "Finder"
                set _bounds to bounds of window of desktop
                set screenWidth to item 3 of _bounds
                set screenHeight to item 4 of _bounds
            end tell
            return (screenWidth as string) & "," & (screenHeight as string)
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                dims = result.stdout.strip().split(',')
                screen_w = int(dims[0])
                screen_h = int(dims[1])
            else:
                # Default screen size
                screen_w, screen_h = 1920, 1080
            
            # Calculate actual coordinates
            x = int(screen_w * x_percent / 100)
            y = int(screen_h * y_percent / 100)
            
            # Execute click using AppleScript
            click_script = f'''
            tell application "System Events"
                click at {{{x}, {y}}}
            end tell
            '''
            result = subprocess.run(['osascript', '-e', click_script], capture_output=True, text=True, timeout=5)
            
            return {"success": result.returncode == 0, "x": x, "y": y}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_type(self, text: str) -> Dict:
        """Execute typing"""
        try:
            # Escape special characters for AppleScript
            escaped = text.replace('\\', '\\\\').replace('"', '\\"')
            
            script = f'''
            tell application "System Events"
                keystroke "{escaped}"
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
            
            return {"success": result.returncode == 0, "text": text}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_key(self, key: str) -> Dict:
        """Execute key press"""
        # Map common key names to key codes
        key_codes = {
            'enter': 36, 'return': 36,
            'tab': 48,
            'escape': 53, 'esc': 53,
            'space': 49,
            'delete': 51, 'backspace': 51,
            'up': 126, 'down': 125, 'left': 123, 'right': 124,
            'home': 115, 'end': 119,
            'pageup': 116, 'pagedown': 121,
            'f1': 122, 'f2': 120, 'f3': 99, 'f4': 118,
            'f5': 96, 'f6': 97, 'f7': 98, 'f8': 100,
        }
        
        try:
            key_lower = key.lower()
            
            if key_lower in key_codes:
                code = key_codes[key_lower]
                script = f'''
                tell application "System Events"
                    key code {code}
                end tell
                '''
            else:
                # Single character key
                script = f'''
                tell application "System Events"
                    keystroke "{key}"
                end tell
                '''
            
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
            return {"success": result.returncode == 0, "key": key}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_hotkey(self, keys: str) -> Dict:
        """Execute key combination like cmd+t, cmd+l"""
        try:
            # Parse key combination
            parts = keys.lower().replace('+', ' ').split()
            
            modifiers = []
            main_key = None
            
            for part in parts:
                if part in ['cmd', 'command']:
                    modifiers.append('command down')
                elif part in ['ctrl', 'control']:
                    modifiers.append('control down')
                elif part in ['alt', 'option']:
                    modifiers.append('option down')
                elif part in ['shift']:
                    modifiers.append('shift down')
                else:
                    main_key = part
            
            if not main_key:
                return {"success": False, "error": "No main key specified"}
            
            modifier_str = ', '.join(modifiers) if modifiers else ''
            
            if modifier_str:
                script = f'''
                tell application "System Events"
                    keystroke "{main_key}" using {{{modifier_str}}}
                end tell
                '''
            else:
                script = f'''
                tell application "System Events"
                    keystroke "{main_key}"
                end tell
                '''
            
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
            return {"success": result.returncode == 0, "keys": keys}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_scroll(self, direction: str) -> Dict:
        """Execute scroll"""
        try:
            delta = 5 if direction.lower() == "up" else -5
            
            script = f'''
            tell application "System Events"
                scroll ({{0, {delta}}})
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
            
            return {"success": result.returncode == 0, "direction": direction}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _record_action(self, action: Dict, result: Dict):
        """Record action for learning"""
        record = {
            "action": action,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "screen_context": self.last_analysis.get("active_app", "Unknown")
        }
        
        self.action_history.append(record)
        
        # Update memory
        if result.get("success"):
            self.action_memory["successful_actions"].append(record)
            # Keep last 500
            self.action_memory["successful_actions"] = self.action_memory["successful_actions"][-500:]
        else:
            self.action_memory["failed_actions"].append(record)
            self.action_memory["failed_actions"] = self.action_memory["failed_actions"][-200:]
        
        # Save periodically
        if len(self.action_history) % 10 == 0:
            self._save_action_memory()
    
    def execute_user_request(self, request: str, verbose: bool = True) -> Dict:
        """
        Main entry point: Execute a natural language user request.
        
        This is the TRUE NLP interface - no predefined patterns!
        
        Args:
            request: Natural language description of what user wants
            verbose: Whether to print progress
        
        Returns:
            Result dictionary with success status and details
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Executing: {request}")
            print(f"{'='*60}")
        
        # Generate action plan
        if verbose:
            print("Analyzing screen and generating plan...")
        
        plan = self.generate_action_plan(request)
        
        if verbose:
            print(f"Plan confidence: {plan.confidence:.1%}")
            print(f"Reasoning: {plan.reasoning}")
            print(f"Steps: {len(plan.steps)}")
        
        if not plan.steps:
            return {
                "success": False,
                "request": request,
                "error": "Could not generate action plan",
                "plan": plan
            }
        
        # Execute steps
        results = []
        overall_success = True
        
        for i, step in enumerate(plan.steps):
            if verbose:
                desc = step.get("description", str(step))
                print(f"  Step {i+1}: {desc}")
            
            result = self.execute_action(step)
            results.append(result)
            
            if not result.get("success"):
                overall_success = False
                if verbose:
                    print(f"    FAILED: {result.get('error', 'Unknown error')}")
                # Continue anyway - some steps might fail but overall goal achieved
            else:
                if verbose:
                    print(f"    OK")
            
            # Small delay between actions
            time.sleep(0.3)
        
        # Final result
        final_result = {
            "success": overall_success,
            "request": request,
            "plan": plan,
            "results": results,
            "steps_completed": sum(1 for r in results if r.get("success")),
            "total_steps": len(plan.steps)
        }
        
        if verbose:
            print(f"\nCompleted: {final_result['steps_completed']}/{final_result['total_steps']} steps")
        
        return final_result
    
    def quick_analyze(self) -> str:
        """Quick screen analysis for status display"""
        analysis = self.analyze_screen()
        
        if "error" in analysis:
            return f"Analysis error: {analysis['error']}"
        
        return f"""Active: {analysis.get('active_app', 'Unknown')}
State: {analysis.get('interface_state', 'Unknown')}
Elements: {len(analysis.get('elements', []))}
Actions: {', '.join(analysis.get('possible_actions', [])[:3])}"""


# Global instance for easy access
_brain_instance: Optional[VisionAIBrain] = None


def get_vision_brain() -> VisionAIBrain:
    """Get or create global VisionAIBrain instance"""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = VisionAIBrain()
    return _brain_instance


def execute_nlp_task(task: str) -> Dict:
    """
    Convenience function to execute a natural language task.
    
    Usage:
        from vision_ai_brain import execute_nlp_task
        result = execute_nlp_task("open youtube and search for cats")
    """
    brain = get_vision_brain()
    return brain.execute_user_request(task)


if __name__ == "__main__":
    # Demo
    print("VisionAIBrain - TRUE NLP Screen Understanding")
    print("=" * 50)
    
    brain = VisionAIBrain()
    
    # Test analysis
    print("\n[TEST] Analyzing current screen...")
    analysis = brain.analyze_screen()
    print(f"Active App: {analysis.get('active_app', 'Unknown')}")
    print(f"Elements: {analysis.get('elements', [])}")
    
    # Test with a task
    print("\n[TEST] Would execute: 'open youtube'")
    print("(Not executing in demo mode)")
