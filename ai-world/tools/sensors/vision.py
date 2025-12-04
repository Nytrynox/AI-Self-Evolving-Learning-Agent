"""
VISION SYSTEM - Camera and Screen Capture
=========================================
Allows Aurora to see through camera and read screen.
Uses llava:7b for image analysis (auto-swaps models).
"""

import os
import io
import logging
import tempfile
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class VisionSystem:
    """
    Aurora's vision capabilities:
    - Camera capture
    - Screen capture
    - Image analysis via LLM (llava:7b)
    
    NOTE: Vision uses a different model than text.
    With 8GB RAM, model swapping will occur (takes ~10-20 sec).
    """
    
    def __init__(self):
        self.camera_available = False
        self.screen_available = False
        self.last_capture = None
        self.cv2 = None
        self.pyautogui = None
        
        # Try to import cv2
        try:
            import cv2
            self.cv2 = cv2
            self.camera_available = True
            logger.info("📷 Camera available")
        except ImportError:
            logger.warning("⚠️ OpenCV not installed - camera disabled")
        
        # Try to import screen capture
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.screen_available = True
            logger.info("🖥️ Screen capture available")
        except ImportError:
            logger.warning("⚠️ PyAutoGUI not installed - screen capture disabled")
        
        logger.info("👁️ Vision System initialized")
    
    def capture_camera(self, save_path: str = None) -> Optional[str]:
        """Capture image from camera"""
        if not self.camera_available or self.cv2 is None:
            logger.warning("Camera not available")
            return None
        
        try:
            # Open camera
            cap = self.cv2.VideoCapture(0)
            if not cap.isOpened():
                logger.error("❌ Cannot open camera")
                return None
            
            # Read frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                logger.error("❌ Cannot read from camera")
                return None
            
            # Save image
            if save_path is None:
                save_path = tempfile.mktemp(suffix='.jpg')
            
            self.cv2.imwrite(save_path, frame)
            self.last_capture = save_path
            
            logger.info(f"📷 Camera capture saved: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"❌ Camera capture failed: {e}")
            return None
    
    def capture_camera_bytes(self) -> Optional[bytes]:
        """Capture camera image as bytes (for direct LLM analysis)"""
        if not self.camera_available or self.cv2 is None:
            return None
        
        try:
            cap = self.cv2.VideoCapture(0)
            if not cap.isOpened():
                return None
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None
            
            # Encode as JPEG bytes
            _, buffer = self.cv2.imencode('.jpg', frame)
            return buffer.tobytes()
            
        except Exception as e:
            logger.error(f"❌ Camera capture failed: {e}")
            return None
    
    def capture_screen(self, save_path: str = None) -> Optional[str]:
        """Capture screenshot"""
        if not self.screen_available or self.pyautogui is None:
            logger.warning("Screen capture not available")
            return None
        
        try:
            screenshot = self.pyautogui.screenshot()
            
            if save_path is None:
                save_path = tempfile.mktemp(suffix='.png')
            
            screenshot.save(save_path)
            self.last_capture = save_path
            
            logger.info(f"🖥️ Screen capture saved: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"❌ Screen capture failed: {e}")
            return None
    
    def capture_screen_bytes(self) -> Optional[bytes]:
        """Capture screen as bytes (for direct LLM analysis)"""
        if not self.screen_available or self.pyautogui is None:
            return None
        
        try:
            screenshot = self.pyautogui.screenshot()
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Screen capture failed: {e}")
            return None
    
    def analyze_image(self, image_path: str, question: str = "Describe what you see") -> Optional[str]:
        """
        Analyze an image using llava:7b vision model.
        
        NOTE: This will swap models (slow on 8GB RAM, ~10-20 sec).
        """
        from agents.llm_interface import get_llm
        llm = get_llm()
        
        if not llm.has_vision():
            logger.error("Vision model (llava:7b) not available")
            return None
        
        logger.info(f"👁️ Analyzing image: {image_path}")
        logger.info("⏳ Switching to vision model (may take 10-20 seconds)...")
        
        result = llm.analyze_image(image_path, question)
        
        if result:
            logger.info(f"👁️ Vision result: {result[:100]}...")
        
        return result
    
    def see_camera(self, question: str = "Describe what you see") -> Optional[str]:
        """
        Capture from camera and analyze.
        Model swap will occur (~10-20 sec on 8GB RAM).
        """
        image_path = self.capture_camera()
        if image_path:
            return self.analyze_image(image_path, question)
        return None
    
    def see_screen(self, question: str = "Describe what you see on screen") -> Optional[str]:
        """
        Capture screen and analyze.
        Model swap will occur (~10-20 sec on 8GB RAM).
        """
        image_path = self.capture_screen()
        if image_path:
            return self.analyze_image(image_path, question)
        return None
    
    def look_for(self, target: str, source: str = "screen") -> Optional[Dict]:
        """
        Look for something specific in camera or screen.
        Returns dict with found status and description.
        """
        if source == "camera":
            image_path = self.capture_camera()
        else:
            image_path = self.capture_screen()
        
        if not image_path:
            return None
        
        question = f"Look at this image. Do you see '{target}'? If yes, describe where it is and what it looks like. If no, say 'not found'."
        description = self.analyze_image(image_path, question)
        
        if description:
            found = "not found" not in description.lower() and target.lower() in description.lower()
            return {
                "target": target,
                "found": found,
                "description": description,
                "image_path": image_path,
                "source": source
            }
        
        return None
    
    def get_status(self) -> Dict:
        """Get vision system status"""
        from agents.llm_interface import get_llm
        llm = get_llm()
        
        return {
            "camera_available": self.camera_available,
            "screen_available": self.screen_available,
            "vision_model_available": llm.has_vision(),
            "last_capture": self.last_capture
        }


# Global instance
_vision = None

def get_vision() -> VisionSystem:
    """Get vision system instance"""
    global _vision
    if _vision is None:
        _vision = VisionSystem()
    return _vision
