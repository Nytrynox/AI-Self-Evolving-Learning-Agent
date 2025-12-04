"""
MEMORY SYSTEM - Persistent Memory for Aurora
============================================
SQLite-based memory that survives restarts.
"""

import sqlite3
import json
import logging
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class MemorySystem:
    """
    Persistent memory system using SQLite.
    - Survives restarts
    - Stores experiences, learnings, conversations
    - Pattern recognition for learning
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            from config.settings import MEMORY_DB_PATH
            db_path = MEMORY_DB_PATH
        
        self.db_path = db_path
        self.timeout = 60  # SQLite timeout for locked database
        self._db_lock = threading.Lock()  # Thread lock for database operations
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
        
        logger.info(f"🧠 Memory System initialized at: {db_path}")
    
    def _get_connection(self):
        """Get a database connection with timeout and better concurrency"""
        conn = sqlite3.connect(self.db_path, timeout=self.timeout, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent access
        conn.execute("PRAGMA busy_timeout=60000")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn
    
    def _execute_with_retry(self, operation, max_retries=3):
        """Execute database operation with retry logic"""
        for attempt in range(max_retries):
            try:
                with self._db_lock:
                    return operation()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise
        return None
    
    def _init_database(self):
        """Initialize SQLite tables"""
        conn = self._get_connection()
        try:
            c = conn.cursor()
            
            # Experiences table - records of what AI did
            c.execute('''CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                action TEXT NOT NULL,
                result TEXT,
                success INTEGER,
                lesson_learned TEXT,
                agent_id TEXT DEFAULT 'aurora'
            )''')
            
            # Conversations table - interactions with founder
            c.execute('''CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                speaker TEXT NOT NULL,
                message TEXT NOT NULL,
                context TEXT
            )''')
            
            # Goals table - AI's current and past goals
            c.execute('''CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                goal TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                progress REAL DEFAULT 0.0,
                completed_at TEXT
            )''')
            
            # Learnings table - patterns and insights
            c.execute('''CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                pattern TEXT NOT NULL,
                insight TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                times_validated INTEGER DEFAULT 1
            )''')
            
            # Self-state table - AI's current state
            c.execute('''CREATE TABLE IF NOT EXISTS self_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )''')
            
            conn.commit()
        finally:
            conn.close()
    
    def store_experience(self, exp_type: str, action: str, result: str = None, 
                         success: bool = True, lesson: str = None, agent_id: str = "aurora"):
        """Store an experience in memory"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute('''INSERT INTO experiences 
                             (timestamp, type, action, result, success, lesson_learned, agent_id)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (datetime.now().isoformat(), exp_type, action, result, 
                           1 if success else 0, lesson, agent_id))
                
                conn.commit()
                conn.close()
            
            logger.debug(f"📝 Stored experience: {exp_type} - {action[:50]}...")
        except Exception as e:
            logger.warning(f"Could not store experience: {e}")
    
    def store_conversation(self, speaker: str, message: str, context: str = None):
        """Store a conversation message"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute('''INSERT INTO conversations (timestamp, speaker, message, context)
                             VALUES (?, ?, ?, ?)''',
                          (datetime.now().isoformat(), speaker, message, context))
                
                conn.commit()
                conn.close()
        except Exception as e:
            logger.warning(f"Could not store conversation: {e}")
    
    def add_goal(self, goal: str) -> int:
        """Add a new goal"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute('''INSERT INTO goals (timestamp, goal, status)
                             VALUES (?, ?, 'active')''',
                          (datetime.now().isoformat(), goal))
                
                goal_id = c.lastrowid
                conn.commit()
                conn.close()
            
            logger.info(f"🎯 New goal added: {goal}")
            return goal_id
        except Exception as e:
            logger.warning(f"Could not add goal: {e}")
            return -1
    
    def complete_goal(self, goal_id: int):
        """Mark a goal as completed"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute('''UPDATE goals SET status = 'completed', 
                         completed_at = ? WHERE id = ?''',
                      (datetime.now().isoformat(), goal_id))
                
                conn.commit()
                conn.close()
        except Exception as e:
            logger.warning(f"Could not complete goal: {e}")
    
    def get_active_goals(self) -> List[Dict]:
        """Get all active goals"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute("SELECT id, goal, progress FROM goals WHERE status = 'active'")
                rows = c.fetchall()
                conn.close()
            
            return [{"id": r[0], "goal": r[1], "progress": r[2]} for r in rows]
        except Exception as e:
            logger.warning(f"Could not get active goals: {e}")
            return []
    
    def store_learning(self, pattern: str, insight: str, confidence: float = 0.5):
        """Store a learned pattern/insight"""
        # Validate inputs
        if not pattern or not insight:
            logger.warning("Cannot store learning with empty pattern or insight")
            return
        
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                # Check if pattern already exists
                c.execute("SELECT id, times_validated FROM learnings WHERE pattern = ?", (pattern,))
                existing = c.fetchone()
                
                if existing:
                    # Update confidence and validation count
                    c.execute('''UPDATE learnings SET times_validated = times_validated + 1,
                                 confidence = MIN(1.0, confidence + 0.1)
                                 WHERE id = ?''', (existing[0],))
                else:
                    c.execute('''INSERT INTO learnings (timestamp, pattern, insight, confidence)
                                 VALUES (?, ?, ?, ?)''',
                              (datetime.now().isoformat(), pattern, insight, confidence))
                
                conn.commit()
                conn.close()
            
            logger.info(f"🎓 Learning stored: {pattern[:50]}...")
        except Exception as e:
            logger.warning(f"Could not store learning: {e}")
    
    def get_learnings(self, min_confidence: float = 0.3) -> List[Dict]:
        """Get learnings above confidence threshold"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute('''SELECT pattern, insight, confidence, times_validated 
                             FROM learnings WHERE confidence >= ?
                             ORDER BY confidence DESC''', (min_confidence,))
                rows = c.fetchall()
                conn.close()
            
            return [{"pattern": r[0], "insight": r[1], "confidence": r[2], 
                     "validations": r[3]} for r in rows]
        except Exception as e:
            logger.warning(f"Could not get learnings: {e}")
            return []
    
    def get_recent_experiences(self, limit: int = 20, exp_type: str = None) -> List[Dict]:
        """Get recent experiences"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                if exp_type:
                    c.execute('''SELECT timestamp, type, action, result, success 
                                 FROM experiences WHERE type = ?
                                 ORDER BY id DESC LIMIT ?''', (exp_type, limit))
                else:
                    c.execute('''SELECT timestamp, type, action, result, success 
                                 FROM experiences ORDER BY id DESC LIMIT ?''', (limit,))
                
                rows = c.fetchall()
                conn.close()
            
            return [{"timestamp": r[0], "type": r[1], "action": r[2], 
                     "result": r[3], "success": bool(r[4])} for r in rows]
        except Exception as e:
            logger.warning(f"Could not get recent experiences: {e}")
            return []
    
    def get_failed_experiences(self, limit: int = 10) -> List[Dict]:
        """Get recent failures to learn from"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute('''SELECT timestamp, type, action, result, lesson_learned 
                             FROM experiences WHERE success = 0
                             ORDER BY id DESC LIMIT ?''', (limit,))
                
                rows = c.fetchall()
                conn.close()
            
            return [{"timestamp": r[0], "type": r[1], "action": r[2], 
                     "result": r[3], "lesson": r[4]} for r in rows]
        except Exception as e:
            logger.warning(f"Could not get failed experiences: {e}")
            return []
    
    def set_state(self, key: str, value: Any):
        """Set a state value"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                value_str = json.dumps(value) if not isinstance(value, str) else value
                
                c.execute('''INSERT OR REPLACE INTO self_state (key, value, updated_at)
                             VALUES (?, ?, ?)''',
                          (key, value_str, datetime.now().isoformat()))
                
                conn.commit()
                conn.close()
        except Exception as e:
            logger.warning(f"Could not set state: {e}")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute("SELECT value FROM self_state WHERE key = ?", (key,))
                row = c.fetchone()
                conn.close()
            
            if row:
                try:
                    return json.loads(row[0])
                except:
                    return row[0]
            return default
        except Exception as e:
            logger.warning(f"Could not get state: {e}")
            return default
    
    def get_memory_summary(self) -> Dict:
        """Get summary of memory contents"""
        try:
            with self._db_lock:
                conn = self._get_connection()
                c = conn.cursor()
                
                c.execute("SELECT COUNT(*) FROM experiences")
                exp_count = c.fetchone()[0]
                
                c.execute("SELECT COUNT(*) FROM conversations")
                conv_count = c.fetchone()[0]
                
                c.execute("SELECT COUNT(*) FROM goals WHERE status = 'active'")
                goals_count = c.fetchone()[0]
                
                c.execute("SELECT COUNT(*) FROM learnings")
                learn_count = c.fetchone()[0]
                
                conn.close()
            
            return {
                "total_experiences": exp_count,
                "total_conversations": conv_count,
                "active_goals": goals_count,
                "learnings": learn_count
            }
        except Exception as e:
            logger.warning(f"Could not get memory summary: {e}")
            return {"total_experiences": 0, "total_conversations": 0, "active_goals": 0, "learnings": 0}


# Global instance
_memory = None

def get_memory() -> MemorySystem:
    """Get memory system instance"""
    global _memory
    if _memory is None:
        _memory = MemorySystem()
    return _memory
