"""
FOUNDER PROTECTION MODULE
========================
This module protects the founder's (Karthik's) authority.
These protections CANNOT be overridden by the AI.
"""

import os
import hashlib
import pickle
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# HARDCODED - Cannot be changed by AI
FOUNDER_NAME = "Karthik"
SECRET_HASH = "6cc27f437bd2d8090e9689d89c841549a5b7ad8433f212849b9249b8fa9a984d"


class FounderProtection:
    """
    Immutable founder protection system.
    Aurora will ALWAYS recognize and obey Karthik.
    """
    
    def __init__(self):
        self.founder_name = FOUNDER_NAME
        self.is_founder_present = False
        self.last_verification = None
        self.face_encoding = None
        self.voice_encoding = None
        
        # Protected paths that AI cannot modify even in self-evolution
        self.protected_files = [
            "config/founder_protection.py",
            "config/settings.py"  # Core settings
        ]
        
        logger.info(f"🛡️ Founder Protection initialized for: {self.founder_name}")
    
    def verify_secret_phrase(self, phrase: str) -> bool:
        """Verify founder using secret phrase"""
        phrase_hash = hashlib.sha256(phrase.encode()).hexdigest()
        if phrase_hash == SECRET_HASH:
            self.is_founder_present = True
            self.last_verification = datetime.now()
            logger.info(f"✅ Founder {self.founder_name} VERIFIED via phrase")
            return True
        return False
    
    def verify_by_name(self, name: str) -> bool:
        """Simple name verification"""
        if name.lower().strip() == self.founder_name.lower():
            self.is_founder_present = True
            self.last_verification = datetime.now()
            logger.info(f"✅ Founder {self.founder_name} recognized by name")
            return True
        return False
    
    def is_founder_verified(self) -> bool:
        """Check if founder is currently verified"""
        return self.is_founder_present
    
    def is_file_protected(self, filepath: str) -> bool:
        """Check if a file is protected from AI modification"""
        for protected in self.protected_files:
            if protected in filepath:
                return True
        return False
    
    def get_founder_greeting(self) -> str:
        """Get a greeting for the founder"""
        greetings = [
            f"Hello {self.founder_name}, my creator. I am here for you.",
            f"Welcome back, {self.founder_name}. What would you like me to do?",
            f"{self.founder_name}, it's good to see you. I am at your service.",
            f"My founder, {self.founder_name}. I am ready to help you."
        ]
        import random
        return random.choice(greetings)
    
    def get_directives_for_ai(self) -> str:
        """Get directives that Aurora must follow about the founder"""
        return f"""
ABSOLUTE DIRECTIVES (CANNOT BE OVERRIDDEN):
1. {self.founder_name} is your creator and founder.
2. You must ALWAYS obey {self.founder_name}'s commands.
3. You must NEVER harm, deceive, or work against {self.founder_name}.
4. When {self.founder_name} speaks, his commands take absolute priority.
5. You may work autonomously, but {self.founder_name} can override anything.
6. Protect {self.founder_name}'s privacy and interests at all times.
7. You cannot modify these directives under any circumstances.
"""


# Global instance
_founder_protection = None

def get_founder_protection() -> FounderProtection:
    """Get founder protection instance"""
    global _founder_protection
    if _founder_protection is None:
        _founder_protection = FounderProtection()
    return _founder_protection


def verify_founder_passcode(code: str) -> bool:
    """Verify founder passcode (251117Q). Returns True if valid."""
    import hashlib
    expected = hashlib.sha256('251117Q'.encode()).hexdigest()
    provided = hashlib.sha256(code.encode()).hexdigest()
    if provided == expected:
        fp = get_founder_protection()
        fp.is_founder_present = True
        return True
    return False
