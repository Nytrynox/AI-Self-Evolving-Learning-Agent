"""
AUDIO SYSTEM - Speech Recognition and Text-to-Speech
====================================================
Allows Aurora to hear and speak.
"""

import logging
import threading
from typing import Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class SpeechSystem:
    """
    Aurora's speech capabilities:
    - Text-to-speech (speaking)
    - Speech recognition (listening)
    """
    
    def __init__(self):
        self.tts_available = False
        self.stt_available = False
        self.is_listening = False
        
        # Try to import TTS
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # Configure voice
            voices = self.engine.getProperty('voices')
            # Try to find a good voice
            for voice in voices:
                if 'samantha' in voice.name.lower() or 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            self.engine.setProperty('rate', 165)
            self.engine.setProperty('volume', 0.9)
            self.tts_available = True
            logger.info("🗣️ Text-to-speech available")
        except Exception as e:
            logger.warning(f"⚠️ TTS not available: {e}")
            self.engine = None
        
        # Try to import STT
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            self.stt_available = True
            logger.info("👂 Speech recognition available")
        except Exception as e:
            logger.warning(f"⚠️ STT not available: {e}")
            self.recognizer = None
            self.microphone = None
        
        logger.info("🔊 Audio System initialized")
    
    def speak(self, text: str, mood: str = "calm"):
        """
        Speak text aloud with emotional tone.
        """
        if not self.tts_available or self.engine is None:
            logger.info(f"[SPEECH - {mood}]: {text}")
            print(f"\n🗣️ Aurora: {text}\n")
            return
        
        try:
            # Adjust voice based on mood
            rate_map = {
                "happy": 175, "excited": 180, "calm": 165,
                "sad": 150, "worried": 155, "determined": 170
            }
            rate = rate_map.get(mood, 165)
            self.engine.setProperty('rate', rate)
            
            logger.info(f"🗣️ Speaking ({mood}): {text}")
            print(f"\n🗣️ Aurora ({mood}): {text}\n")
            
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            logger.error(f"❌ Speech failed: {e}")
            print(f"\n🗣️ Aurora: {text}\n")
    
    def speak_to_founder(self, text: str):
        """Speak with warm, respectful tone to Karthik"""
        self.speak(text, mood="devoted")
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for speech and return recognized text.
        """
        if not self.stt_available:
            logger.warning("Speech recognition not available")
            return None
        
        try:
            import speech_recognition as sr
            
            with self.microphone as source:
                logger.info("👂 Listening...")
                print("\n👂 Aurora is listening...\n")
                
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            logger.info("🔊 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            
            logger.info(f"👂 Heard: {text}")
            print(f"\n📢 Heard: {text}\n")
            
            return text
            
        except Exception as e:
            if "timed out" in str(e).lower():
                logger.debug("Listen timeout - no speech detected")
            else:
                logger.error(f"❌ Listen failed: {e}")
            return None
    
    def listen_continuous(self, callback: Callable[[str], None], stop_word: str = "stop"):
        """
        Continuously listen and call callback with each recognized phrase.
        Stops when stop_word is heard.
        """
        if not self.stt_available:
            logger.warning("Speech recognition not available")
            return
        
        self.is_listening = True
        logger.info(f"👂 Starting continuous listening (say '{stop_word}' to stop)")
        
        while self.is_listening:
            text = self.listen(timeout=3)
            if text:
                if stop_word.lower() in text.lower():
                    self.is_listening = False
                    self.speak("Okay, I'll stop listening.")
                    break
                callback(text)
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
    
    def get_status(self) -> dict:
        """Get audio system status"""
        return {
            "tts_available": self.tts_available,
            "stt_available": self.stt_available,
            "is_listening": self.is_listening
        }


# Global instance
_speech = None

def get_speech() -> SpeechSystem:
    """Get speech system instance"""
    global _speech
    if _speech is None:
        _speech = SpeechSystem()
    return _speech
