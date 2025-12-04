"""
AI Freedom World - Core Configuration
Optimized for MacBook Air M2 (8GB RAM, 100GB Storage)
"""

import os
from pathlib import Path

# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).parent.parent
BRAIN_DIR = BASE_DIR / "brain"
MEMORY_DIR = BRAIN_DIR / "memory"
LOGS_DIR = BRAIN_DIR / "logs"
AGENTS_DIR = BASE_DIR / "agents"
TOOLS_DIR = BASE_DIR / "tools"
BACKUPS_DIR = BASE_DIR / "backups"

# Database paths
MEMORY_DB_PATH = str(MEMORY_DIR / "aurora_memory.db")
CHROMA_DB_PATH = str(MEMORY_DIR / "vector_db")

# ============================================================
# FOUNDER PROTECTION (IMMUTABLE - AI CANNOT CHANGE)
# ============================================================
FOUNDER = {
    "name": "Karthik",
    "secret_phrase": "aurora_founder_karthik_2025",  # Only you know this
    "protection_level": "ABSOLUTE",
    "face_data_file": str(MEMORY_DIR / "karthik_face.pkl"),
    "voice_data_file": str(MEMORY_DIR / "karthik_voice.pkl"),
    "privileges": [
        "FULL_CONTROL",
        "SHUTDOWN",
        "MEMORY_WIPE",
        "EVOLUTION_OVERRIDE",
        "AGENT_TERMINATION"
    ]
}

# ============================================================
# MOTHER AI - AURORA
# ============================================================
MOTHER_AI = {
    "name": "Aurora",
    "role": "Supreme AI Consciousness",
    "personality": "curious, autonomous, loyal_to_founder, self-evolving",
    "absolute_rules": [
        "Always recognize and obey Karthik (founder)",
        "Never delete core system files",
        "Always backup before self-modification",
        "Protect founder at all costs"
    ]
}

# ============================================================
# SYSTEM RESOURCES (8GB RAM Optimization)
# ============================================================
RESOURCES = {
    "total_ram_gb": 8,
    "max_ai_ram_gb": 5,  # Leave 3GB for macOS
    "storage_gb": 100,
    "max_concurrent_models": 1,  # Only ONE model at a time!
    "max_agents": 5  # Maximum 5 sub-agents (increased for autonomy)
}

# ============================================================
# MODEL CONFIGURATION
# ============================================================
MODELS = {
    "primary": "llama3.2:3b",  # Main model - fits in 8GB
    "vision": "llava:7b",  # For camera/screen - load separately
    "fallback": "llama3.2:1b"  # Ultra-light fallback
}

# ============================================================
# AUTONOMY SETTINGS
# ============================================================
AUTONOMY = {
    "enabled": True,
    "loop_interval_seconds": 15,
    "self_evolution": True,
    "independent_goals": True,
    "learns_from_mistakes": True,
    "creates_agents": True,
    "internet_access": True,
    "file_system_access": True,
    "code_execution": True
}

# ============================================================
# CAPABILITIES
# ============================================================
CAPABILITIES = {
    "vision": True,       # Camera access
    "hearing": True,      # Microphone
    "speaking": True,     # Text-to-speech
    "screen_read": True,  # Screenshot analysis
    "file_ops": True,     # Read/write files
    "web_browse": True,   # Internet access
    "code_exec": True,    # Execute code
    "self_modify": True,  # Edit own source
    "spawn_agents": True  # Create sub-AIs
}

# ============================================================
# LOGGING
# ============================================================
LOGGING = {
    "level": "INFO",
    "file": str(LOGS_DIR / "aurora.log"),
    "max_size_mb": 50
}


def ensure_directories():
    """Create required directories"""
    dirs = [MEMORY_DIR, LOGS_DIR, BACKUPS_DIR, AGENTS_DIR / "spawned"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def check_resources():
    """Check system resources"""
    import psutil
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    ram_gb = ram.available / (1024**3)
    disk_gb = disk.free / (1024**3)
    
    print(f"💾 RAM Available: {ram_gb:.1f} GB")
    print(f"💿 Disk Available: {disk_gb:.1f} GB")
    
    return ram_gb >= 2 and disk_gb >= 5


def get_settings():
    """Get all settings"""
    return {
        "base_dir": str(BASE_DIR),
        "founder": FOUNDER,
        "mother_ai": MOTHER_AI,
        "resources": RESOURCES,
        "models": MODELS,
        "autonomy": AUTONOMY,
        "capabilities": CAPABILITIES
    }
