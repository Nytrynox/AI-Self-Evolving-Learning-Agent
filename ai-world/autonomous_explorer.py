"""
Autonomous Exploration System
Aurora's independent exploration and learning capabilities
"""

import threading
import time
import random
import pyautogui
import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from action_tracker import ActionTracker, ActionResult, SmartRetryManager

class AutonomousExplorer:
    """Autonomous screen exploration and interaction system"""
    
    def __init__(self, action_tracker: ActionTracker = None):
        self.running = False
        self.explorer_thread = None
        self.action_tracker = action_tracker
        self.retry_manager = SmartRetryManager(action_tracker) if action_tracker else None
        
        # Exploration state
        self.screen_regions = []
        self.interesting_elements = []
        self.click_history = []
        self.success_zones = []
        self.forbidden_zones = []
        
        # Safety bounds (avoid system UI)
        self.safe_bounds = {
            'left': 50,
            'right': pyautogui.size()[0] - 50,
            'top': 100,  # Avoid menu bar
            'bottom': pyautogui.size()[1] - 50
        }
        
        # Exploration parameters
        self.exploration_interval = 5.0  # seconds between actions
        self.max_click_distance = 200   # pixels
        self.curiosity_threshold = 0.3
        
    def start_exploration(self):
        """Start autonomous exploration"""
        if not self.running:
            self.running = True
            self.explorer_thread = threading.Thread(target=self._exploration_loop, daemon=True)
            self.explorer_thread.start()
            print("🤖 Aurora: Starting autonomous exploration...")
            
    def stop_exploration(self):
        """Stop autonomous exploration"""
        self.running = False
        if self.explorer_thread:
            self.explorer_thread.join(timeout=2)
        print("🤖 Aurora: Autonomous exploration stopped.")
    
    def _exploration_loop(self):
        """Main exploration loop"""
        while self.running:
            try:
                # Analyze current screen
                screen_info = self._analyze_screen()
                
                # Choose next action based on analysis
                action = self._choose_action(screen_info)
                
                if action:
                    self._execute_action(action)
                    
                # Wait before next action
                time.sleep(self.exploration_interval)
                
            except Exception as e:
                print(f"🤖 Aurora Explorer Error: {e}")
                time.sleep(2.0)
    
    def _analyze_screen(self) -> Dict:
        """Analyze current screen for interesting elements"""
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screen_array = np.array(screenshot)
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(screen_array, cv2.COLOR_RGB2GRAY)
            
            # Find edges (UI elements)
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours (potential clickable elements)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contours for clickable elements
            elements = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 5000:  # Reasonable button sizes
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if within safe bounds
                    if (self.safe_bounds['left'] < x < self.safe_bounds['right'] and
                        self.safe_bounds['top'] < y < self.safe_bounds['bottom']):
                        
                        center = (x + w//2, y + h//2)
                        elements.append({
                            'center': center,
                            'bbox': (x, y, w, h),
                            'area': area,
                            'interest_score': self._calculate_interest(center)
                        })
            
            return {
                'elements': elements,
                'timestamp': time.time(),
                'screen_size': pyautogui.size()
            }
            
        except Exception as e:
            print(f"Screen analysis error: {e}")
            return {'elements': [], 'timestamp': time.time()}
    
    def _calculate_interest(self, position: Tuple[int, int]) -> float:
        """Calculate interest score for a screen position
        
        Uses DETERMINISTIC scoring based on actual exploration history,
        not random values. Score is based on:
        - Unexplored areas (not recently clicked)
        - Past success zones
        - Forbidden zones (past failures)
        """
        x, y = position
        
        # Higher interest in unexplored areas
        unexplored_bonus = 0.0
        for prev_click in self.click_history[-20:]:  # Check recent clicks
            distance = ((x - prev_click['x'])**2 + (y - prev_click['y'])**2)**0.5
            if distance < self.max_click_distance:
                unexplored_bonus -= 0.2  # Reduce interest in explored areas
        
        # Higher interest in areas with past success
        success_bonus = 0.0
        for success_zone in self.success_zones:
            distance = ((x - success_zone['x'])**2 + (y - success_zone['y'])**2)**0.5
            if distance < 100:
                success_bonus += 0.3
                
        # Avoid forbidden zones
        forbidden_penalty = 0.0
        for forbidden in self.forbidden_zones:
            distance = ((x - forbidden['x'])**2 + (y - forbidden['y'])**2)**0.5
            if distance < 50:
                forbidden_penalty -= 1.0  # Strong penalty
        
        # Deterministic curiosity based on position hash (reproducible)
        # This creates variation without randomness
        position_hash = (x * 31 + y * 17) % 100 / 100.0
        curiosity = position_hash * self.curiosity_threshold
        
        return max(0, 0.5 + unexplored_bonus + success_bonus + forbidden_penalty + curiosity)
    
    def _choose_action(self, screen_info: Dict) -> Optional[Dict]:
        """Choose next action based on screen analysis"""
        elements = screen_info.get('elements', [])
        
        if not elements:
            return None
            
        # Sort elements by interest score
        elements.sort(key=lambda e: e['interest_score'], reverse=True)
        
        # Select most interesting element
        target = elements[0]
        
        if target['interest_score'] > 0.2:  # Minimum interest threshold
            return {
                'type': 'click',
                'position': target['center'],
                'element_info': target
            }
            
        return None
    
    def _execute_action(self, action: Dict):
        """Execute the chosen action"""
        if not action:
            return
            
        action_type = action.get('type')
        
        if action_type == 'click':
            self._execute_click(action)
        elif action_type == 'type':
            self._execute_typing(action)
        elif action_type == 'scroll':
            self._execute_scroll(action)
    
    def _execute_click(self, action: Dict):
        """Execute a click action with tracking"""
        position = action['position']
        x, y = position
        
        # Track action start
        action_data = {
            'x': x,
            'y': y,
            'element_info': action.get('element_info', {})
        }
        
        if self.action_tracker:
            action_id = f"click_{int(time.time() * 1000)}"
            self.action_tracker.start_action(action_id, 'click', action_data)
            
            try:
                # Take screenshot before click
                before_screen = pyautogui.screenshot()
                
                # Perform click
                pyautogui.click(x, y)
                print(f"🤖 Aurora: Clicked at ({x}, {y})")
                
                # Wait and analyze result
                time.sleep(1.0)
                after_screen = pyautogui.screenshot()
                
                # Determine if click was successful
                success = self._evaluate_click_success(before_screen, after_screen, position)
                
                # Record result
                result = ActionResult.SUCCESS if success else ActionResult.FAILURE
                self.action_tracker.complete_action(action_id, result)
                
                # Update exploration knowledge
                self._update_exploration_knowledge(position, success)
                
            except Exception as e:
                if self.action_tracker:
                    self.action_tracker.complete_action(action_id, ActionResult.ERROR, str(e))
                print(f"Click execution error: {e}")
        else:
            # Simple click without tracking
            try:
                pyautogui.click(x, y)
                print(f"🤖 Aurora: Clicked at ({x}, {y})")
                time.sleep(1.0)
            except Exception as e:
                print(f"Click error: {e}")
    
    def _evaluate_click_success(self, before_img, after_img, click_pos: Tuple[int, int]) -> bool:
        """Evaluate if a click was successful by comparing before/after screenshots"""
        try:
            # Convert to numpy arrays
            before_array = np.array(before_img)
            after_array = np.array(after_img)
            
            # Calculate image difference
            diff = cv2.absdiff(before_array, after_array)
            
            # Convert difference to grayscale
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            
            # Count changed pixels
            changed_pixels = np.sum(gray_diff > 30)  # Threshold for significant change
            total_pixels = gray_diff.shape[0] * gray_diff.shape[1]
            
            change_ratio = changed_pixels / total_pixels
            
            # Consider successful if significant change occurred
            # (indicates UI responded to click)
            return change_ratio > 0.05  # 5% of screen changed
            
        except Exception as e:
            print(f"Success evaluation error: {e}")
            return False
    
    def _update_exploration_knowledge(self, position: Tuple[int, int], success: bool):
        """Update exploration knowledge based on action results"""
        click_record = {
            'x': position[0],
            'y': position[1],
            'success': success,
            'timestamp': time.time()
        }
        
        # Add to click history
        self.click_history.append(click_record)
        
        # Keep only recent history
        if len(self.click_history) > 100:
            self.click_history = self.click_history[-50:]
            
        # Update success/forbidden zones
        if success:
            self.success_zones.append(click_record)
            if len(self.success_zones) > 20:
                self.success_zones = self.success_zones[-10:]
        else:
            # Don't immediately forbid, but reduce interest
            pass
    
    def get_exploration_stats(self) -> Dict:
        """Get exploration statistics"""
        if not self.click_history:
            return {}
            
        total_clicks = len(self.click_history)
        successful_clicks = sum(1 for click in self.click_history if click.get('success', False))
        
        return {
            'total_clicks': total_clicks,
            'successful_clicks': successful_clicks,
            'success_rate': successful_clicks / total_clicks if total_clicks > 0 else 0,
            'exploration_time': time.time() - self.click_history[0]['timestamp'] if self.click_history else 0,
            'success_zones': len(self.success_zones),
            'is_running': self.running
        }

class KeyboardAutomation:
    """Keyboard automation and form interaction"""
    
    def __init__(self, action_tracker: ActionTracker = None):
        self.action_tracker = action_tracker
        
    def type_text(self, text: str, delay: float = 0.05) -> bool:
        """Type text with optional delay between characters"""
        try:
            if self.action_tracker:
                action_id = f"type_{int(time.time() * 1000)}"
                self.action_tracker.start_action(action_id, 'typing', {'text': text})
                
            pyautogui.write(text, interval=delay)
            print(f"🤖 Aurora: Typed '{text[:20]}...'")
            
            if self.action_tracker:
                self.action_tracker.complete_action(action_id, ActionResult.SUCCESS)
                
            return True
            
        except Exception as e:
            if self.action_tracker:
                self.action_tracker.complete_action(action_id, ActionResult.ERROR, str(e))
            print(f"Typing error: {e}")
            return False
    
    def send_shortcut(self, *keys) -> bool:
        """Send keyboard shortcut"""
        try:
            if self.action_tracker:
                action_id = f"shortcut_{int(time.time() * 1000)}"
                self.action_tracker.start_action(action_id, 'shortcut', {'keys': list(keys)})
                
            pyautogui.hotkey(*keys)
            print(f"🤖 Aurora: Sent shortcut {'+'.join(keys)}")
            
            if self.action_tracker:
                self.action_tracker.complete_action(action_id, ActionResult.SUCCESS)
                
            return True
            
        except Exception as e:
            if self.action_tracker:
                self.action_tracker.complete_action(action_id, ActionResult.ERROR, str(e))
            print(f"Shortcut error: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """Press a single key"""
        try:
            pyautogui.press(key)
            print(f"🤖 Aurora: Pressed {key}")
            return True
        except Exception as e:
            print(f"Key press error: {e}")
            return False