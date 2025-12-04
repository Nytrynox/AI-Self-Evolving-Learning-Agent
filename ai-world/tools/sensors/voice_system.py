"""
VOICE INTERACTION SYSTEM - Aurora Speaks and Listens
====================================================
Real voice capabilities for Aurora:
- Text-to-Speech (speaks aloud)
- Speech-to-Text (listens to user)
- Real-time conversation

Uses macOS native speech + optional Google Speech Recognition.
"""

import logging
import threading
import queue
import time
import subprocess
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class VoiceSystem:
    """
    Aurora's voice capabilities.
    REAL speech - uses actual system audio.
    """
    
    def __init__(self):
        # TTS Engine
        self.tts_engine = None
        self.tts_available = False
        
        # STT Engine
        self.stt_engine = None
        self.stt_available = False
        
        # Voice settings (set BEFORE initializing engines)
        self.voice_name = "Samantha"  # macOS voice
        self.speech_rate = 175  # Words per minute
        self.volume = 0.8
        
        # Initialize engines after settings are set
        self._init_tts()
        self._init_stt()
        
        # Listening state
        self.is_listening = False
        self.listen_thread = None
        
        # Callbacks
        self.on_speech_recognized = None  # Called when speech is heard
        self.on_doubt_question = None  # Called when Aurora asks a question
        
        # Speech queue
        self.speech_queue = queue.Queue()
        self._start_speech_worker()
        
        logger.info(f"🎤 Voice System initialized - TTS: {self.tts_available}, STT: {self.stt_available}")
    
    def _init_tts(self):
        """Initialize Text-to-Speech"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Configure voice
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'samantha' in voice.name.lower() or 'female' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_engine.setProperty('rate', self.speech_rate)
            self.tts_engine.setProperty('volume', self.volume)
            
            self.tts_available = True
            logger.info("🔊 TTS initialized with pyttsx3")
            
        except Exception as e:
            logger.warning(f"⚠️ pyttsx3 not available: {e}")
            # Fallback to macOS say command
            self.tts_available = True  # macOS 'say' is always available
            logger.info("🔊 TTS will use macOS 'say' command")
    
    def _init_stt(self):
        """Initialize Speech-to-Text"""
        try:
            import speech_recognition as sr
            self.stt_engine = sr.Recognizer()
            
            # Test microphone
            try:
                with sr.Microphone() as source:
                    self.stt_engine.adjust_for_ambient_noise(source, duration=0.5)
                self.stt_available = True
                logger.info("🎤 STT initialized with speech_recognition")
            except Exception as e:
                logger.warning(f"⚠️ Microphone not available: {e}")
                self.stt_available = False
                
        except ImportError:
            logger.warning("⚠️ speech_recognition not available")
            self.stt_available = False
    
    def _start_speech_worker(self):
        """Start background speech worker"""
        def worker():
            while True:
                try:
                    text, callback = self.speech_queue.get(timeout=1)
                    self._speak_now(text)
                    if callback:
                        callback()
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Speech worker error: {e}")
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    # ==========================================
    # TEXT-TO-SPEECH (SPEAKING)
    # ==========================================
    
    def speak(self, text: str, callback: Callable = None, blocking: bool = False):
        """
        Speak text aloud.
        
        Args:
            text: What to say
            callback: Called when done speaking
            blocking: Wait until done if True
        """
        if not text:
            return
        
        if blocking:
            self._speak_now(text)
            if callback:
                callback()
        else:
            self.speech_queue.put((text, callback))
    
    def _speak_now(self, text: str):
        """Actually speak the text"""
        logger.info(f"🗣️ Speaking: {text[:50]}...")
        
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return
            except Exception as e:
                logger.debug(f"pyttsx3 failed: {e}, falling back to 'say'")
        
        # Fallback to macOS say command
        try:
            # Escape quotes for shell
            safe_text = text.replace('"', '\\"').replace("'", "\\'")
            subprocess.run(
                ["say", "-v", self.voice_name, safe_text],
                timeout=60
            )
        except Exception as e:
            logger.error(f"Speech failed: {e}")
    
    def speak_with_emotion(self, text: str, emotion: str = "calm"):
        """Speak with emotional context"""
        # Adjust speech based on emotion
        emotion_settings = {
            "calm": {"rate": 175, "pitch": "normal"},
            "excited": {"rate": 200, "pitch": "high"},
            "concerned": {"rate": 150, "pitch": "low"},
            "happy": {"rate": 190, "pitch": "high"},
            "confused": {"rate": 160, "pitch": "normal"},
        }
        
        settings = emotion_settings.get(emotion, emotion_settings["calm"])
        
        logger.info(f"🗣️ Aurora ({emotion}): {text[:50]}...")
        print(f"\n🗣️ Aurora ({emotion}): {text}\n")
        
        self.speak(text)
    
    def announce(self, message: str):
        """Make an important announcement"""
        print(f"\n📢 Aurora: {message}\n")
        self.speak(message)
    
    # ==========================================
    # SPEECH-TO-TEXT (LISTENING)
    # ==========================================
    
    def listen(self, timeout: float = 5.0, phrase_limit: float = 10.0) -> Optional[str]:
        """
        Listen for speech and return transcribed text.
        
        Args:
            timeout: How long to wait for speech to start
            phrase_limit: Max length of phrase to capture
            
        Returns:
            Transcribed text or None
        """
        if not self.stt_available:
            logger.warning("Speech recognition not available")
            return None
        
        import speech_recognition as sr
        
        try:
            with sr.Microphone() as source:
                logger.info("🎤 Listening...")
                print("\n🎤 Listening... (speak now)")
                
                # Adjust for ambient noise
                self.stt_engine.adjust_for_ambient_noise(source, duration=0.3)
                
                # Listen
                audio = self.stt_engine.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
                
                logger.info("🎤 Processing speech...")
                
                # Try Google Speech Recognition (free)
                try:
                    text = self.stt_engine.recognize_google(audio)
                    logger.info(f"🎤 Heard: {text}")
                    print(f"🎤 Heard: {text}\n")
                    return text
                except sr.UnknownValueError:
                    logger.info("🎤 Could not understand audio")
                    return None
                except sr.RequestError as e:
                    logger.error(f"🎤 Recognition service error: {e}")
                    return None
                    
        except Exception as e:
            logger.error(f"🎤 Listen error: {e}")
            return None
    
    def listen_continuous(self, callback: Callable[[str], None], stop_event: threading.Event = None):
        """
        Continuously listen for speech.
        
        Args:
            callback: Called with transcribed text
            stop_event: Set this to stop listening
        """
        if not self.stt_available:
            logger.warning("Speech recognition not available")
            return
        
        self.is_listening = True
        
        def listen_loop():
            while self.is_listening and (stop_event is None or not stop_event.is_set()):
                try:
                    text = self.listen(timeout=3.0)
                    if text:
                        callback(text)
                except Exception as e:
                    logger.debug(f"Listen loop error: {e}")
                time.sleep(0.1)
            
            self.is_listening = False
        
        self.listen_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
    
    # ==========================================
    # INTERACTIVE CONVERSATION
    # ==========================================
    
    def ask_question(self, question: str, wait_for_response: bool = True) -> Optional[str]:
        """
        Ask a question and wait for verbal response.
        
        Args:
            question: Question to ask
            wait_for_response: Whether to listen for answer
            
        Returns:
            User's response or None
        """
        # Speak the question
        self.speak_with_emotion(question, "confused")
        
        if not wait_for_response:
            return None
        
        # Wait a moment then listen
        time.sleep(0.5)
        
        # Listen for response
        response = self.listen(timeout=10.0, phrase_limit=30.0)
        
        return response
    
    def confirm(self, message: str) -> bool:
        """
        Ask for confirmation and listen for yes/no.
        
        Returns:
            True if user said yes, False otherwise
        """
        response = self.ask_question(f"{message} Yes or no?")
        
        if response:
            response_lower = response.lower()
            if any(word in response_lower for word in ["yes", "yeah", "yep", "sure", "ok", "okay", "correct", "right"]):
                return True
            elif any(word in response_lower for word in ["no", "nope", "nah", "wrong", "cancel", "stop"]):
                return False
        
        # Default to no if unclear
        return False
    
    def have_conversation(self, initial_message: str = None, turns: int = 5) -> list:
        """
        Have a multi-turn conversation.
        
        Returns:
            List of conversation turns
        """
        conversation = []
        
        if initial_message:
            self.speak_with_emotion(initial_message, "calm")
            conversation.append({"role": "aurora", "text": initial_message})
        
        for _ in range(turns):
            # Listen for user
            user_text = self.listen(timeout=5.0)
            
            if not user_text:
                self.speak("I didn't catch that. Could you repeat?")
                continue
            
            conversation.append({"role": "user", "text": user_text})
            
            # Check for exit keywords
            if any(word in user_text.lower() for word in ["bye", "goodbye", "exit", "stop", "quit"]):
                self.speak("Goodbye! Let me know if you need anything.")
                break
            
            # Generate response using NLP
            try:
                from brain.nlp_engine import get_nlp_engine
                nlp = get_nlp_engine()
                response = nlp.generate_response(user_text)
                
                self.speak_with_emotion(response, "calm")
                conversation.append({"role": "aurora", "text": response})
            except Exception as e:
                response = "I understand. Is there anything specific you'd like me to do?"
                self.speak(response)
                conversation.append({"role": "aurora", "text": response})
        
        return conversation
    
    # ==========================================
    # DOUBT & CLARIFICATION SYSTEM
    # ==========================================
    
    def express_doubt(self, confusion: str, context: str = None) -> Optional[str]:
        """
        Express doubt/confusion and ask for clarification.
        
        Aurora will:
        1. Speak about what's confusing
        2. Ask a clarifying question
        3. Listen for and return the answer
        """
        # Generate clarification question
        try:
            from brain.nlp_engine import get_nlp_engine
            nlp = get_nlp_engine()
            question = nlp.generate_clarification_question(context or "Current task", confusion)
        except:
            question = f"I'm not sure about something. {confusion}. Could you help me understand?"
        
        logger.info(f"❓ Aurora has doubt: {confusion}")
        
        # Ask the question
        answer = self.ask_question(question, wait_for_response=True)
        
        # Record this Q&A for learning
        try:
            from brain.learning_engine import get_learning_engine
            learning = get_learning_engine()
            q_id = learning.ask_question(question, context)
            
            if answer:
                learning.answer_question(q_id, answer, helpful=True)
        except Exception as e:
            logger.debug(f"Failed to record Q&A: {e}")
        
        return answer
    
    def request_help(self, task: str, problem: str) -> Optional[str]:
        """
        Request help from user when stuck.
        """
        message = f"I'm having trouble with {task}. {problem}. Can you help me?"
        return self.ask_question(message)
    
    # ==========================================
    # STATUS & INFO
    # ==========================================
    
    def is_available(self) -> bool:
        """Check if voice system is available (at least TTS or STT)"""
        return self.tts_available or self.stt_available
    
    def get_status(self) -> dict:
        """Get voice system status"""
        return {
            "tts_available": self.tts_available,
            "stt_available": self.stt_available,
            "is_listening": self.is_listening,
            "voice": self.voice_name,
            "speech_rate": self.speech_rate
        }
    
    def set_voice(self, voice_name: str):
        """Set the voice to use"""
        self.voice_name = voice_name
        
        if self.tts_engine:
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if voice_name.lower() in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
    
    def set_speech_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.speech_rate = rate
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)
    
    def list_voices(self) -> list:
        """List available voices"""
        try:
            result = subprocess.run(
                ["say", "-v", "?"],
                capture_output=True,
                text=True
            )
            voices = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if parts:
                        voices.append(parts[0])
            return voices
        except:
            return ["Samantha", "Alex", "Victoria"]


# Global instance
_voice_system = None

def get_voice_system() -> VoiceSystem:
    """Get voice system instance"""
    global _voice_system
    if _voice_system is None:
        _voice_system = VoiceSystem()
    return _voice_system
