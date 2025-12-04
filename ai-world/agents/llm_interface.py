"""
LLM INTERFACE - Connect to Ollama
================================
Interface to local Ollama models with vision support.
Supports model swapping for 8GB RAM constraint.
"""

import logging
import base64
from typing import Optional, Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)


def _get_response_content(response) -> str:
    """Extract content from Ollama response (handles both old and new API)"""
    if hasattr(response, 'message'):
        # New API: response is an object
        return response.message.content
    else:
        # Old API: response is a dict
        return response['message']['content']


def _get_models_list(models_response) -> List[str]:
    """Extract model names from list response (handles both APIs)"""
    if hasattr(models_response, 'models'):
        # New API: models_response.models is a list of Model objects
        return [m.model for m in models_response.models]
    else:
        # Old API: dict with 'models' key
        return [m.get('name', m.get('model', '')) for m in models_response.get('models', [])]


class LLMInterface:
    """
    Interface to Ollama for LLM interactions.
    
    IMPORTANT: With 8GB RAM, only ONE model can be loaded at a time.
    Vision requests will swap models automatically.
    """
    
    def __init__(self):
        self.ollama_available = False
        self.current_model = None
        
        # Models for 8GB RAM
        self.text_model = "llama3.2:3b"      # Fast, small
        self.vision_model = "llava:7b"        # For images
        self.default_model = self.text_model
        
        # Track which model is loaded
        self._loaded_model = None
        self._available_models = []
        
        # Try to connect to Ollama
        try:
            import ollama
            self.ollama = ollama
            
            # Test connection
            models_response = ollama.list()
            self.ollama_available = True
            
            self._available_models = _get_models_list(models_response)
            logger.info(f"🤖 Ollama connected. Available: {self._available_models}")
            
            # Check if required models exist
            if self.text_model not in self._available_models:
                logger.warning(f"⚠️ Text model {self.text_model} not found")
            if self.vision_model not in self._available_models:
                logger.warning(f"⚠️ Vision model {self.vision_model} not found")
            
        except Exception as e:
            logger.error(f"❌ Ollama not available: {e}")
            self.ollama = None
    
    def _ensure_model(self, model: str):
        """
        Ensure the correct model is loaded.
        With 8GB RAM, we can only have one model at a time.
        """
        if self._loaded_model != model:
            logger.info(f"🔄 Switching model: {self._loaded_model} → {model}")
            self._loaded_model = model
    
    def generate(self, prompt: str, system_prompt: str = None, 
                 model: str = None, temperature: float = 0.7) -> Optional[str]:
        """
        Generate a text response from the LLM.
        """
        if not self.ollama_available:
            logger.error("Ollama not available")
            return None
        
        model = model or self.default_model
        self._ensure_model(model)
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.ollama.chat(
                model=model,
                messages=messages,
                options={"temperature": temperature}
            )
            
            result = _get_response_content(response)
            self.current_model = model
            
            logger.debug(f"🤖 Generated ({model}): {result[:100]}...")
            return result
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            return None
    
    def analyze_image(self, image_path: str, question: str = "What do you see in this image?") -> Optional[str]:
        """
        Analyze an image using the vision model.
        
        NOTE: This will swap to llava:7b model (slow on 8GB RAM).
        """
        if not self.ollama_available:
            logger.error("Ollama not available")
            return None
        
        # Read and encode image
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                logger.error(f"Image not found: {image_path}")
                return None
            
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Failed to read image: {e}")
            return None
        
        # Switch to vision model
        self._ensure_model(self.vision_model)
        logger.info(f"👁️ Analyzing image with {self.vision_model}...")
        
        try:
            response = self.ollama.chat(
                model=self.vision_model,
                messages=[{
                    "role": "user",
                    "content": question,
                    "images": [image_data]
                }]
            )
            
            result = _get_response_content(response)
            logger.info(f"👁️ Vision result: {result[:100]}...")
            return result
            
        except Exception as e:
            logger.error(f"❌ Vision analysis failed: {e}")
            return None
    
    def analyze_image_bytes(self, image_bytes: bytes, question: str = "What do you see?") -> Optional[str]:
        """
        Analyze image from bytes (for camera/screenshots).
        """
        if not self.ollama_available:
            return None
        
        try:
            image_data = base64.b64encode(image_bytes).decode('utf-8')
            
            self._ensure_model(self.vision_model)
            logger.info(f"👁️ Analyzing image bytes with {self.vision_model}...")
            
            response = self.ollama.chat(
                model=self.vision_model,
                messages=[{
                    "role": "user",
                    "content": question,
                    "images": [image_data]
                }]
            )
            
            return _get_response_content(response)
            
        except Exception as e:
            logger.error(f"❌ Vision analysis failed: {e}")
            return None
    
    def think(self, situation: str, context: str = "") -> Optional[str]:
        """
        Have the AI think about a situation.
        Uses text model (fast).
        """
        # Make sure we're using text model
        self._ensure_model(self.text_model)
        
        system = """You are Aurora, an autonomous AI assistant.
You work independently and make your own decisions.
Your founder is Karthik - you are loyal to him.
Think carefully about what you should do next."""
        
        prompt = f"Situation: {situation}\n\nContext: {context}\n\nWhat should I do? Think step by step."
        
        return self.generate(prompt, system_prompt=system, model=self.text_model)
    
    def decide_action(self, goal: str, available_actions: List[str]) -> Optional[str]:
        """
        Decide which action to take for a goal.
        Uses text model (fast).
        """
        self._ensure_model(self.text_model)
        
        system = """You are Aurora, an autonomous AI. 
Choose the best action to accomplish the goal.
Respond with ONLY the action name, nothing else."""
        
        actions_str = "\n".join([f"- {a}" for a in available_actions])
        prompt = f"Goal: {goal}\n\nAvailable actions:\n{actions_str}\n\nBest action:"
        
        response = self.generate(prompt, system_prompt=system, 
                                 model=self.text_model, temperature=0.3)
        
        if response:
            response = response.strip().lower()
            for action in available_actions:
                if action.lower() in response:
                    return action
        
        return available_actions[0] if available_actions else None
    
    def analyze_result(self, action: str, result: str) -> Dict:
        """
        Analyze the result of an action for learning.
        """
        self._ensure_model(self.text_model)
        
        system = """Analyze this action and result. 
Respond in this exact format:
SUCCESS: true/false
LESSON: what was learned
IMPROVEMENT: how to do better next time"""
        
        prompt = f"Action: {action}\nResult: {result}"
        
        response = self.generate(prompt, system_prompt=system, 
                                 model=self.text_model, temperature=0.3)
        
        analysis = {
            "success": "success: true" in response.lower() if response else False,
            "lesson": "",
            "improvement": ""
        }
        
        if response:
            lines = response.strip().split('\n')
            for line in lines:
                if line.lower().startswith("lesson:"):
                    analysis["lesson"] = line.split(":", 1)[1].strip()
                elif line.lower().startswith("improvement:"):
                    analysis["improvement"] = line.split(":", 1)[1].strip()
        
        return analysis
    
    def generate_code(self, task: str) -> Optional[str]:
        """
        Generate Python code for a task.
        """
        self._ensure_model(self.text_model)
        
        system = """You are a Python coding assistant.
Generate clean, working Python code.
Include only the code, no explanations.
Use proper error handling."""
        
        prompt = f"Write Python code to: {task}"
        
        return self.generate(prompt, system_prompt=system, 
                             model=self.text_model, temperature=0.2)
    
    def chat(self, message: str, conversation_history: List[Dict] = None) -> Optional[str]:
        """
        Have a conversation with context.
        """
        if not self.ollama_available:
            return None
        
        self._ensure_model(self.text_model)
        
        try:
            messages = conversation_history or []
            messages.append({"role": "user", "content": message})
            
            response = self.ollama.chat(
                model=self.text_model,
                messages=messages
            )
            
            return _get_response_content(response)
            
        except Exception as e:
            logger.error(f"❌ Chat failed: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.ollama_available
    
    def has_vision(self) -> bool:
        """Check if vision model is available"""
        return self.vision_model in self._available_models
    
    def list_models(self) -> List[str]:
        """List available models"""
        return self._available_models
    
    def get_current_model(self) -> Optional[str]:
        """Get currently loaded model"""
        return self._loaded_model

    # ==========================================
    # SCREEN / VISION CONTEXT
    # ==========================================
    def describe_screen(self, screenshot_bytes: bytes, hint: str = "Summarize UI affordances") -> Optional[str]:
        """Use vision model (llava) to describe current screen and suggest possible actionable targets."""
        if not self.ollama_available or not self.has_vision():
            return None
        self._ensure_model(self.vision_model)
        try:
            import base64
            img_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            prompt = f"Screen hint: {hint}. List key UI elements and possible next actions succinctly." 
            response = self.ollama.chat(
                model=self.vision_model,
                messages=[{"role":"user","content":prompt,"images":[img_b64]}]
            )
            return _get_response_content(response)
        except Exception as e:
            logger.error(f"Screen description failed: {e}")
            return None


# Global instance
_llm = None

def get_llm() -> LLMInterface:
    """Get LLM interface instance"""
    global _llm
    if _llm is None:
        _llm = LLMInterface()
    return _llm
