"""
NLP CONVERSATION ENGINE - Aurora's Natural Language Understanding
================================================================
Enables Aurora to:
- Understand natural language
- Ask questions when confused
- Have real conversations
- Learn from dialogue

Uses local Ollama for NLP - no cloud dependency.
"""

import logging
import re
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class NLPEngine:
    """
    Natural Language Processing for Aurora.
    
    Capabilities:
    - Intent recognition
    - Entity extraction
    - Question generation
    - Conversation context tracking
    - Sentiment analysis
    - Command parsing
    """
    
    def __init__(self):
        # Get LLM interface
        try:
            from agents.llm_interface import get_llm
            self.llm = get_llm()
        except:
            self.llm = None
        
        # Conversation history (for context)
        self.conversation_history = []
        self.max_history = 20
        
        # Intent patterns (rule-based fallback)
        self.intent_patterns = {
            "greeting": [r"\b(hi|hello|hey|greetings)\b", r"^(hi|hello)"],
            "farewell": [r"\b(bye|goodbye|see you|later)\b"],
            "question": [r"\?$", r"^(what|who|where|when|why|how|can|could|would|is|are|do|does)\b"],
            "command": [r"^(please |)?((do|make|create|open|close|run|execute|start|stop)\b)"],
            "affirmative": [r"^(yes|yeah|yep|sure|ok|okay|correct|right)\b"],
            "negative": [r"^(no|nope|nah|wrong|incorrect)\b"],
            "help": [r"\b(help|assist|support)\b"],
            "status": [r"\b(status|how are you|what.*doing)\b"],
            "learning": [r"\b(learn|teach|remember|know)\b"],
        }
        
        # Entity patterns
        self.entity_patterns = {
            "app_name": [
                r"open\s+(\w+)",
                r"launch\s+(\w+)",
                r"start\s+(\w+)",
                r"close\s+(\w+)",
                r"quit\s+(\w+)"
            ],
            "url": [r"https?://[^\s]+", r"www\.[^\s]+"],
            "file_path": [r"[/~][^\s]+", r"\w+\.\w{2,4}"],
            "number": [r"\b\d+\b"],
            "time": [r"\b\d{1,2}:\d{2}\b", r"\b(morning|afternoon|evening|night)\b"],
        }
        
        # Doubt triggers - when Aurora should ask for clarification
        self.doubt_triggers = [
            "not sure", "unclear", "ambiguous", "multiple meanings",
            "could mean", "confused", "don't understand", "what do you mean"
        ]
        
        logger.info("💬 NLP Engine initialized")
    
    # ==========================================
    # INTENT RECOGNITION
    # ==========================================
    
    def detect_intent(self, text: str) -> Dict[str, Any]:
        """
        Detect the intent of user input.
        Returns: {intent: str, confidence: float, entities: dict}
        """
        text_lower = text.lower().strip()
        
        # Try rule-based first (fast)
        rule_intent = self._detect_intent_rules(text_lower)
        
        # If LLM available and confidence is low, use LLM
        if self.llm and self.llm.is_available() and rule_intent["confidence"] < 0.7:
            llm_intent = self._detect_intent_llm(text)
            if llm_intent["confidence"] > rule_intent["confidence"]:
                return llm_intent
        
        # Extract entities
        rule_intent["entities"] = self._extract_entities(text)
        
        return rule_intent
    
    def _detect_intent_rules(self, text: str) -> Dict:
        """Rule-based intent detection"""
        best_intent = "unknown"
        best_confidence = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    confidence = 0.8 if pattern.startswith("^") else 0.6
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent
        
        return {
            "intent": best_intent,
            "confidence": best_confidence,
            "method": "rules"
        }
    
    def _detect_intent_llm(self, text: str) -> Dict:
        """LLM-based intent detection"""
        prompt = f"""Analyze this user input and determine the intent.
Input: "{text}"

Respond with JSON only:
{{"intent": "one of: greeting, farewell, question, command, affirmative, negative, help, status, learning, conversation, unknown",
"confidence": 0.0 to 1.0,
"summary": "brief description"}}"""
        
        try:
            response = self.llm.generate(prompt, system_prompt="You are an intent classifier. Respond only with valid JSON.")
            
            # Parse JSON from response
            json_match = re.search(r'\{[^}]+\}', response)
            if json_match:
                result = json.loads(json_match.group())
                result["method"] = "llm"
                return result
        except Exception as e:
            logger.debug(f"LLM intent detection failed: {e}")
        
        return {"intent": "unknown", "confidence": 0.3, "method": "llm_failed"}
    
    # ==========================================
    # ENTITY EXTRACTION
    # ==========================================
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text"""
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, text, re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                entities[entity_type] = list(set(matches))
        
        return entities
    
    # ==========================================
    # QUESTION GENERATION
    # ==========================================
    
    def generate_clarification_question(self, context: str, confusion: str) -> str:
        """Generate a question to ask when Aurora is confused"""
        
        if self.llm and self.llm.is_available():
            prompt = f"""I'm an AI assistant and I'm confused about something.
Context: {context}
My confusion: {confusion}

Generate a polite, clear question to ask my user for clarification.
Keep it short and specific. Just the question, nothing else."""
            
            question = self.llm.generate(prompt, system_prompt="You are helpful. Generate only the question.")
            if question:
                return question.strip()
        
        # Fallback questions
        fallbacks = [
            f"I'm not sure I understand. Could you clarify: {confusion[:50]}?",
            f"Could you explain what you mean by that?",
            f"I want to make sure I do this right. What exactly should I do?",
            f"I have a question: {confusion[:50]}?"
        ]
        
        import random
        return random.choice(fallbacks)
    
    def should_ask_question(self, situation: str) -> Tuple[bool, str]:
        """Determine if Aurora should ask a question"""
        
        # Check for doubt triggers
        situation_lower = situation.lower()
        for trigger in self.doubt_triggers:
            if trigger in situation_lower:
                return True, self.generate_clarification_question("Current situation", situation)
        
        # Use LLM to assess if clarification is needed
        if self.llm and self.llm.is_available():
            prompt = f"""Analyze this situation and determine if clarification is needed:
"{situation}"

If the situation is clear, respond: CLEAR
If clarification is needed, respond: UNCLEAR: [what needs clarification]"""
            
            response = self.llm.generate(prompt, system_prompt="Be concise.")
            if response and "UNCLEAR" in response:
                unclear_part = response.split("UNCLEAR:")[-1].strip()
                return True, self.generate_clarification_question(situation, unclear_part)
        
        return False, ""
    
    # ==========================================
    # CONVERSATION MANAGEMENT
    # ==========================================
    
    def add_to_conversation(self, role: str, message: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,  # "user" or "aurora"
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history limited
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_conversation_context(self, last_n: int = 5) -> str:
        """Get recent conversation as context"""
        recent = self.conversation_history[-last_n:] if self.conversation_history else []
        
        context_lines = []
        for entry in recent:
            role = "User" if entry["role"] == "user" else "Aurora"
            context_lines.append(f"{role}: {entry['message']}")
        
        return "\n".join(context_lines)
    
    def generate_response(self, user_input: str, context: str = None) -> str:
        """Generate a conversational response"""
        
        # Add to history
        self.add_to_conversation("user", user_input)
        
        # Detect intent
        intent_info = self.detect_intent(user_input)
        
        # Build context
        conv_context = self.get_conversation_context()
        full_context = f"{context}\n\nRecent conversation:\n{conv_context}" if context else conv_context
        
        if self.llm and self.llm.is_available():
            system_prompt = """You are Aurora, an AI assistant created by Karthik.
You are helpful, honest, and ask questions when you're unsure.
You're learning and improving constantly.
Keep responses concise but friendly."""
            
            prompt = f"""Context: {full_context}

User said: {user_input}
Intent detected: {intent_info['intent']}

Respond naturally:"""
            
            response = self.llm.generate(prompt, system_prompt=system_prompt)
            if response:
                self.add_to_conversation("aurora", response)
                return response
        
        # Fallback responses based on intent
        fallbacks = {
            "greeting": "Hello! I'm Aurora. How can I help you?",
            "farewell": "Goodbye! Feel free to call me anytime.",
            "question": "That's a good question. Let me think about it...",
            "affirmative": "Great! I'll proceed.",
            "negative": "Understood. What would you like instead?",
            "help": "I'm here to help! What do you need?",
            "status": "I'm running well and ready to assist!",
            "unknown": "I heard you. Could you tell me more?"
        }
        
        response = fallbacks.get(intent_info["intent"], fallbacks["unknown"])
        self.add_to_conversation("aurora", response)
        return response
    
    # ==========================================
    # COMMAND PARSING
    # ==========================================
    
    def parse_command(self, text: str) -> Dict[str, Any]:
        """Parse a command from natural language"""
        
        text_lower = text.lower().strip()
        
        # Common command patterns
        command_patterns = [
            # App control
            (r"open\s+(\w+)", "open_app", lambda m: {"app": m.group(1)}),
            (r"close\s+(\w+)", "close_app", lambda m: {"app": m.group(1)}),
            (r"launch\s+(\w+)", "open_app", lambda m: {"app": m.group(1)}),
            (r"quit\s+(\w+)", "quit_app", lambda m: {"app": m.group(1)}),
            
            # Browser
            (r"search\s+(for\s+)?(.+)", "search_web", lambda m: {"query": m.group(2)}),
            (r"go to\s+(.+)", "open_url", lambda m: {"url": m.group(1)}),
            (r"browse\s+(.+)", "open_url", lambda m: {"url": m.group(1)}),
            
            # System
            (r"take\s+(a\s+)?screenshot", "screenshot", lambda m: {}),
            (r"check\s+(system|status)", "check_system", lambda m: {}),
            
            # GUI
            (r"click", "click", lambda m: {}),
            (r"type\s+(.+)", "type_text", lambda m: {"text": m.group(1)}),
            (r"scroll\s+(up|down)", "scroll", lambda m: {"direction": m.group(1)}),
            (r"press\s+(\w+)", "press_key", lambda m: {"key": m.group(1)}),
            
            # Learning
            (r"remember\s+that\s+(.+)", "learn", lambda m: {"fact": m.group(1)}),
            (r"learn\s+that\s+(.+)", "learn", lambda m: {"fact": m.group(1)}),
            
            # Speak
            (r"say\s+(.+)", "speak", lambda m: {"text": m.group(1)}),
            (r"tell\s+me\s+(.+)", "respond", lambda m: {"query": m.group(1)}),
        ]
        
        for pattern, action, extract in command_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return {
                    "action": action,
                    "params": extract(match),
                    "confidence": 0.8,
                    "original": text
                }
        
        # Use LLM for complex commands
        if self.llm and self.llm.is_available():
            return self._parse_command_llm(text)
        
        return {
            "action": "unknown",
            "params": {},
            "confidence": 0.2,
            "original": text
        }
    
    def _parse_command_llm(self, text: str) -> Dict:
        """Use LLM to parse complex commands"""
        prompt = f"""Parse this command into an action:
"{text}"

Available actions: open_app, close_app, search_web, open_url, screenshot, 
click, type_text, scroll, press_key, learn, speak, check_system, explore_files

Respond with JSON:
{{"action": "action_name", "params": {{"key": "value"}}, "confidence": 0.0-1.0}}"""
        
        try:
            response = self.llm.generate(prompt, system_prompt="Parse commands. JSON only.")
            json_match = re.search(r'\{[^}]+\}', response.replace('\n', ''))
            if json_match:
                result = json.loads(json_match.group())
                result["original"] = text
                return result
        except:
            pass
        
        return {"action": "unknown", "params": {}, "confidence": 0.2, "original": text}
    
    # ==========================================
    # SENTIMENT & UNDERSTANDING
    # ==========================================
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze the sentiment of text"""
        
        # Simple rule-based sentiment
        positive_words = ["good", "great", "excellent", "happy", "love", "thanks", "thank", "awesome", "perfect", "yes"]
        negative_words = ["bad", "terrible", "hate", "angry", "wrong", "no", "never", "worst", "awful", "stupid"]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return {"positive": 0.5, "negative": 0.5, "neutral": 0.0}
        
        return {
            "positive": positive_count / total,
            "negative": negative_count / total,
            "neutral": 1 - (positive_count + negative_count) / max(len(text_lower.split()), 1)
        }
    
    def extract_key_information(self, text: str) -> Dict[str, Any]:
        """Extract key information from text for learning"""
        
        info = {
            "entities": self._extract_entities(text),
            "intent": self.detect_intent(text),
            "sentiment": self.analyze_sentiment(text),
            "word_count": len(text.split()),
            "is_question": "?" in text,
            "is_command": self.detect_intent(text)["intent"] == "command"
        }
        
        return info
    
    # Compatibility method for mother_ai.py
    def understand(self, text: str) -> Dict[str, Any]:
        """
        Understand user input - compatibility wrapper for mother_ai.py
        Returns intent, entities, action, and other parsed information.
        """
        intent_result = self.detect_intent(text)
        entities = self._extract_entities(text)
        command = self.parse_command(text)
        
        return {
            "intent": intent_result.get("intent", "unknown"),
            "confidence": intent_result.get("confidence", 0.5),
            "entities": entities,
            "action": command.get("action"),
            "parameters": command.get("parameters", {}),
            "raw_command": command
        }
    
    def learn_from_conversation(self, user_input: str, response: str, satisfaction: float = 0.5):
        """
        Learn from a conversation exchange.
        satisfaction: 0.0 (bad) to 1.0 (excellent)
        """
        self.add_to_conversation("user", user_input)
        self.add_to_conversation("assistant", response)
        
        # Could store this for learning patterns in the future
        logger.debug(f"Learned from conversation (satisfaction: {satisfaction})")


# Global instance
_nlp_engine = None

def get_nlp_engine() -> NLPEngine:
    """Get NLP engine instance"""
    global _nlp_engine
    if _nlp_engine is None:
        _nlp_engine = NLPEngine()
    return _nlp_engine
