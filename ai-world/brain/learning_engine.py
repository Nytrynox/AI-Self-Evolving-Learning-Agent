"""
SELF-LEARNING ENGINE - Aurora's Intelligence Growth System
==========================================================
This is the CORE of Aurora's self-improvement.

Features:
- Learns from EVERY action (success or failure)
- Tracks intelligence growth over time
- Self-evolves strategies based on outcomes
- Persistent storage - NEVER forgets (even after restart)
- Confidence scoring for all knowledge
- Pattern recognition from mistakes

ALL DATA IS REAL - Stored in SQLite database permanently.
"""

import sqlite3
import json
import logging
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class LearningEngine:
    """
    Aurora's Self-Learning and Evolution System.
    
    This system:
    1. Records EVERY action and outcome
    2. Analyzes patterns in successes/failures
    3. Builds strategies that improve over time
    4. Tracks intelligence metrics
    5. Persists ALL learning to disk (survives restarts)
    """
    
    def __init__(self):
        # Database path - persistent storage
        self.db_path = Path(__file__).parent / "memory" / "aurora_learning.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Thread lock for database operations
        self._db_lock = threading.Lock()
        
        # Initialize database
        self._init_database()
        
        # Intelligence metrics (loaded from DB)
        self.intelligence_score = 0.0
        self.total_learnings = 0
        self.evolution_level = 1
        
        # Load existing state
        self._load_state()
        
        logger.info(f"🧠 Learning Engine initialized - Intelligence: {self.intelligence_score:.2f}, Level: {self.evolution_level}")
    
    def _get_connection(self):
        """Get database connection with WAL mode and better concurrency"""
        conn = sqlite3.connect(str(self.db_path), timeout=60.0, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=60000")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.row_factory = sqlite3.Row
        return conn
    
    def _execute_with_retry(self, operation, max_retries=3):
        """Execute database operation with retry logic"""
        for attempt in range(max_retries):
            try:
                with self._db_lock:
                    return operation()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                    continue
                raise
        return None
    
    def _init_database(self):
        """Initialize all learning tables"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Action history - every action Aurora takes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS action_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    action_name TEXT NOT NULL,
                    action_params TEXT,
                    outcome TEXT,
                    success INTEGER,
                    execution_time REAL,
                    error_message TEXT,
                    context TEXT,
                    learned_from INTEGER DEFAULT 0
                )
            """)
            
            # Learned strategies - what Aurora has figured out
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    action_type TEXT NOT NULL,
                    strategy_name TEXT NOT NULL,
                    strategy_details TEXT,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    confidence REAL DEFAULT 0.5,
                    is_active INTEGER DEFAULT 1,
                    UNIQUE(action_type, strategy_name)
                )
            """)
            
            # Mistakes and lessons - what went wrong and what was learned
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mistakes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    action_name TEXT,
                    error_type TEXT,
                    error_details TEXT,
                    lesson_learned TEXT,
                    prevention_strategy TEXT,
                    times_occurred INTEGER DEFAULT 1,
                    last_occurred TEXT DEFAULT CURRENT_TIMESTAMP,
                    resolved INTEGER DEFAULT 0
                )
            """)
            
            # Intelligence evolution tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intelligence_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    intelligence_score REAL,
                    evolution_level INTEGER,
                    total_actions INTEGER,
                    success_rate REAL,
                    unique_learnings INTEGER,
                    event_description TEXT
                )
            """)
            
            # Knowledge base - facts and information Aurora learns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    category TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    knowledge TEXT NOT NULL,
                    source TEXT,
                    confidence REAL DEFAULT 0.5,
                    times_used INTEGER DEFAULT 0,
                    times_validated INTEGER DEFAULT 0,
                    UNIQUE(category, topic)
                )
            """)
            
            # Questions Aurora has asked (and answers received)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    question TEXT NOT NULL,
                    context TEXT,
                    answer TEXT,
                    answered INTEGER DEFAULT 0,
                    answer_helpful INTEGER,
                    learned_from_answer TEXT
                )
            """)
            
            # State persistence
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS engine_state (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info("📚 Learning database initialized")
            
        finally:
            conn.close()
    
    def _load_state(self):
        """Load persisted state from database"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Load intelligence score
                cursor.execute("SELECT value FROM engine_state WHERE key = 'intelligence_score'")
                row = cursor.fetchone()
                if row:
                    self.intelligence_score = float(row['value'])
                
                # Load evolution level
                cursor.execute("SELECT value FROM engine_state WHERE key = 'evolution_level'")
                row = cursor.fetchone()
                if row:
                    self.evolution_level = int(row['value'])
                
                # Count total learnings
                cursor.execute("SELECT COUNT(*) as count FROM strategies WHERE is_active = 1")
                row = cursor.fetchone()
                self.total_learnings = row['count'] if row else 0
                
                logger.info(f"📂 State loaded: Intelligence={self.intelligence_score:.2f}, Level={self.evolution_level}")
                
            finally:
                conn.close()
    
    def _save_state(self):
        """Save current state to database"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO engine_state (key, value, updated_at)
                    VALUES ('intelligence_score', ?, CURRENT_TIMESTAMP)
                """, (str(self.intelligence_score),))
                
                cursor.execute("""
                    INSERT OR REPLACE INTO engine_state (key, value, updated_at)
                    VALUES ('evolution_level', ?, CURRENT_TIMESTAMP)
                """, (str(self.evolution_level),))
                
                conn.commit()
            finally:
                conn.close()
    
    # ==========================================
    # LEARNING FROM ACTIONS
    # ==========================================
    
    def record_action(self, action_name: str, params: Dict = None, 
                      outcome: str = None, success: bool = True,
                      execution_time: float = 0.0, error: str = None,
                      context: str = None) -> int:
        """
        Record every action Aurora takes.
        This is the foundation of all learning.
        """
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO action_history 
                    (action_name, action_params, outcome, success, execution_time, error_message, context)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    action_name,
                    json.dumps(params) if params else None,
                    outcome,
                    1 if success else 0,
                    execution_time,
                    error,
                    context
                ))
                
                action_id = cursor.lastrowid
                conn.commit()
                
            finally:
                conn.close()
        
        # Analyze and learn from this action (outside lock)
        self._analyze_action(action_name, success, error)
        
        return action_id
    
    def _analyze_action(self, action_name: str, success: bool, error: str = None):
        """Analyze action outcome and learn from it"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Update strategy statistics
                if success:
                    cursor.execute("""
                        UPDATE strategies 
                        SET success_count = success_count + 1,
                            confidence = MIN(1.0, confidence + 0.02),
                            updated_at = CURRENT_TIMESTAMP
                        WHERE action_type = ?
                    """, (action_name,))
                    
                else:
                    cursor.execute("""
                        UPDATE strategies 
                        SET failure_count = failure_count + 1,
                            confidence = MAX(0.1, confidence - 0.05),
                            updated_at = CURRENT_TIMESTAMP
                        WHERE action_type = ?
                    """, (action_name,))
                
                conn.commit()
                
            finally:
                conn.close()
        
        # Outside the lock for nested calls
        if success:
            self._increase_intelligence(0.1, f"Successful {action_name}")
        elif error:
            self._record_mistake(action_name, error)
    
    def _record_mistake(self, action_name: str, error: str):
        """Record a mistake and try to learn from it"""
        times_occurred = 0
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check if we've seen this mistake before
                cursor.execute("""
                    SELECT id, times_occurred FROM mistakes 
                    WHERE action_name = ? AND error_type = ?
                """, (action_name, error[:100]))
                
                row = cursor.fetchone()
                
                if row:
                    times_occurred = row['times_occurred']
                    # We've seen this before - increment counter
                    cursor.execute("""
                        UPDATE mistakes 
                        SET times_occurred = times_occurred + 1,
                            last_occurred = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (row['id'],))
                else:
                    # New mistake - record it
                    cursor.execute("""
                        INSERT INTO mistakes (action_name, error_type, error_details)
                        VALUES (?, ?, ?)
                    """, (action_name, error[:100], error))
                
                conn.commit()
                
            finally:
                conn.close()
        
        # Outside the lock for nested calls
        if times_occurred >= 3:
            self._evolve_strategy(action_name, error)
        
        # Small intelligence decrease for mistakes (but we learn!)
        self._increase_intelligence(-0.05, f"Mistake in {action_name}")
    
    def _evolve_strategy(self, action_name: str, error: str):
        """Evolve our strategy when we keep making the same mistake"""
        logger.info(f"🧬 Evolving strategy for {action_name} due to repeated errors")
        
        # Generate new prevention strategy
        prevention = f"Avoid: {error[:50]}. Try alternative approach."
        
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Update mistake with learned lesson
                cursor.execute("""
                    UPDATE mistakes 
                    SET lesson_learned = ?,
                        prevention_strategy = ?,
                        resolved = 1
                    WHERE action_name = ? AND error_type = ?
                """, (
                    f"After {3}+ failures, evolved approach",
                    prevention,
                    action_name,
                    error[:100]
                ))
                
                # Add new strategy variant
                cursor.execute("""
                    INSERT OR REPLACE INTO strategies 
                    (action_type, strategy_name, strategy_details, confidence)
                    VALUES (?, ?, ?, 0.6)
                """, (
                    action_name,
                    f"{action_name}_evolved_v{self.evolution_level}",
                    prevention
                ))
                
                conn.commit()
                
            finally:
                conn.close()
        
        # Intelligence boost for evolving (outside lock)
        self._increase_intelligence(0.5, f"Evolved strategy for {action_name}")
    
    # ==========================================
    # INTELLIGENCE GROWTH
    # ==========================================
    
    def _increase_intelligence(self, amount: float, reason: str):
        """Increase or decrease intelligence score"""
        old_score = self.intelligence_score
        self.intelligence_score = max(0, self.intelligence_score + amount)
        
        # Check for level up
        new_level = int(self.intelligence_score / 10) + 1
        leveled_up = False
        if new_level > self.evolution_level:
            self.evolution_level = new_level
            logger.info(f"🎉 LEVEL UP! Aurora is now Level {self.evolution_level}!")
            leveled_up = True
        
        # Save state
        self._save_state()
        
        if leveled_up:
            self._log_intelligence_event(f"Evolved to Level {self.evolution_level}")
        
        if abs(amount) >= 0.5:
            logger.info(f"🧠 Intelligence: {old_score:.2f} → {self.intelligence_score:.2f} ({reason})")
    
    def _log_intelligence_event(self, description: str):
        """Log an intelligence milestone"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Get current stats
                cursor.execute("SELECT COUNT(*) as count FROM action_history")
                total_actions = cursor.fetchone()['count']
                
                cursor.execute("SELECT COUNT(*) as count FROM action_history WHERE success = 1")
                successes = cursor.fetchone()['count']
                
                success_rate = successes / total_actions if total_actions > 0 else 0
                
                cursor.execute("SELECT COUNT(*) as count FROM strategies WHERE is_active = 1")
                learnings = cursor.fetchone()['count']
                
                cursor.execute("""
                    INSERT INTO intelligence_log 
                    (intelligence_score, evolution_level, total_actions, success_rate, unique_learnings, event_description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.intelligence_score,
                    self.evolution_level,
                    total_actions,
                    success_rate,
                    learnings,
                    description
                ))
                
                conn.commit()
                
            finally:
                conn.close()
    
    # ==========================================
    # KNOWLEDGE MANAGEMENT
    # ==========================================
    
    def learn_fact(self, category: str, topic: str, knowledge: str, 
                   source: str = "experience", confidence: float = 0.5) -> bool:
        """Learn a new fact or update existing knowledge"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO knowledge_base (category, topic, knowledge, source, confidence)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(category, topic) DO UPDATE SET
                        knowledge = excluded.knowledge,
                        confidence = MIN(1.0, confidence + 0.1),
                        times_validated = times_validated + 1
                """, (category, topic, knowledge, source, confidence))
                
                conn.commit()
                
            except Exception as e:
                logger.error(f"Failed to learn: {e}")
                return False
            finally:
                conn.close()
        
        self._increase_intelligence(0.1, f"Learned: {topic}")
        logger.info(f"📚 Learned: {category}/{topic}")
        return True
    
    def get_knowledge(self, category: str = None, topic: str = None) -> List[Dict]:
        """Retrieve learned knowledge"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                if category and topic:
                    cursor.execute("""
                        SELECT * FROM knowledge_base 
                        WHERE category = ? AND topic = ?
                    """, (category, topic))
                elif category:
                    cursor.execute("""
                        SELECT * FROM knowledge_base 
                        WHERE category = ?
                        ORDER BY confidence DESC
                    """, (category,))
                else:
                    cursor.execute("""
                        SELECT * FROM knowledge_base 
                        ORDER BY confidence DESC, times_used DESC
                        LIMIT 100
                    """)
                
                return [dict(row) for row in cursor.fetchall()]
                
            finally:
                conn.close()
    
    def use_knowledge(self, category: str, topic: str) -> Optional[str]:
        """Use a piece of knowledge (increases its relevance)"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE knowledge_base 
                    SET times_used = times_used + 1
                    WHERE category = ? AND topic = ?
                """, (category, topic))
                
                cursor.execute("""
                    SELECT knowledge FROM knowledge_base 
                    WHERE category = ? AND topic = ?
                """, (category, topic))
                
                row = cursor.fetchone()
                conn.commit()
                
                return row['knowledge'] if row else None
                
            finally:
                conn.close()
    
    # ==========================================
    # QUESTION SYSTEM
    # ==========================================
    
    def ask_question(self, question: str, context: str = None) -> int:
        """Record a question Aurora wants to ask"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO questions (question, context)
                    VALUES (?, ?)
                """, (question, context))
                
                question_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"❓ Aurora wants to ask: {question}")
                return question_id
                
            finally:
                conn.close()
    
    def answer_question(self, question_id: int, answer: str, helpful: bool = True):
        """Record answer to a question and learn from it"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE questions 
                    SET answer = ?,
                        answered = 1,
                        answer_helpful = ?
                    WHERE id = ?
                """, (answer, 1 if helpful else 0, question_id))
            
                # Get the question for learning
                cursor.execute("SELECT question, context FROM questions WHERE id = ?", (question_id,))
                row = cursor.fetchone()
                question_text = row['question'] if row else None
            
                conn.commit()
                
            finally:
                conn.close()
        
        # Learn from helpful answer (outside lock)
        if question_text and helpful:
            self.learn_fact(
                "qa_learning",
                question_text[:100],
                answer,
                source="founder_answer",
                confidence=0.9
            )
    
    def get_unanswered_questions(self) -> List[Dict]:
        """Get questions that haven't been answered yet"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM questions 
                    WHERE answered = 0
                    ORDER BY timestamp DESC
                """)
                
                return [dict(row) for row in cursor.fetchall()]
                
            finally:
                conn.close()
    
    # ==========================================
    # STRATEGY RECOMMENDATIONS
    # ==========================================
    
    def get_best_strategy(self, action_type: str) -> Optional[Dict]:
        """Get the best strategy for an action type"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM strategies 
                    WHERE action_type = ? AND is_active = 1
                    ORDER BY confidence DESC, success_count DESC
                    LIMIT 1
                """, (action_type,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
            finally:
                conn.close()
    
    def should_try_action(self, action_name: str) -> Tuple[bool, str]:
        """Determine if an action should be attempted based on history"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check recent failures
                cursor.execute("""
                    SELECT COUNT(*) as failures FROM action_history 
                    WHERE action_name = ? AND success = 0
                    AND timestamp > datetime('now', '-1 hour')
                """, (action_name,))
                
                recent_failures = cursor.fetchone()['failures']
                
                if recent_failures >= 3:
                    return False, f"Too many recent failures ({recent_failures}). Waiting before retry."
                
                # Check for known issues
                cursor.execute("""
                    SELECT prevention_strategy FROM mistakes 
                    WHERE action_name = ? AND resolved = 0
                    ORDER BY times_occurred DESC
                    LIMIT 1
                """, (action_name,))
                
                row = cursor.fetchone()
                if row and row['prevention_strategy']:
                    return True, f"Caution: {row['prevention_strategy']}"
                
                return True, "Proceed normally"
                
            finally:
                conn.close()
    
    # ==========================================
    # STATISTICS
    # ==========================================
    
    def get_statistics(self) -> Dict:
        """Get comprehensive learning statistics"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                stats = {
                    "intelligence_score": self.intelligence_score,
                    "evolution_level": self.evolution_level,
                    "level": self._get_level_name()  # Added for compatibility
                }
                
                # Total actions
                cursor.execute("SELECT COUNT(*) as count FROM action_history")
                stats["total_actions"] = cursor.fetchone()['count']
                
                # Success rate
                cursor.execute("SELECT COUNT(*) as count FROM action_history WHERE success = 1")
                successes = cursor.fetchone()['count']
                stats["total_successes"] = successes
                stats["success_rate"] = successes / stats["total_actions"] if stats["total_actions"] > 0 else 0
                
                # Total strategies
                cursor.execute("SELECT COUNT(*) as count FROM strategies WHERE is_active = 1")
                stats["total_strategies"] = cursor.fetchone()['count']
                stats["total_learned"] = stats["total_strategies"]  # Alias for compatibility
                
                # Total mistakes
                cursor.execute("SELECT COUNT(*) as count FROM mistakes")
                stats["total_mistakes"] = cursor.fetchone()['count']
                
                # Resolved mistakes
                cursor.execute("SELECT COUNT(*) as count FROM mistakes WHERE resolved = 1")
                stats["resolved_mistakes"] = cursor.fetchone()['count']
                
                # Knowledge count
                cursor.execute("SELECT COUNT(*) as count FROM knowledge_base")
                stats["knowledge_items"] = cursor.fetchone()['count']
                
                # Unanswered questions
                cursor.execute("SELECT COUNT(*) as count FROM questions WHERE answered = 0")
                stats["pending_questions"] = cursor.fetchone()['count']
                
                return stats
                
            finally:
                conn.close()
    
    def _get_level_name(self) -> str:
        """Get human-readable level name"""
        if self.evolution_level <= 1:
            return "Beginner"
        elif self.evolution_level <= 3:
            return "Learner"
        elif self.evolution_level <= 5:
            return "Competent"
        elif self.evolution_level <= 7:
            return "Proficient"
        elif self.evolution_level <= 9:
            return "Expert"
        else:
            return "Master"
    
    # Compatibility aliases for mother_ai.py
    def get_intelligence_metrics(self) -> Dict:
        """Alias for get_statistics - compatibility with mother_ai.py"""
        return self.get_statistics()
    
    def record_action_attempt(self, action: str, context: Dict = None, parameters: Dict = None) -> int:
        """Record an action attempt - returns action_id for later result recording"""
        return self.record_action(action, params=parameters, context=json.dumps(context) if context else None)
    
    def record_success(self, action_id: int, result: str = None, improvement_notes: str = None):
        """Record successful completion of an action"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE action_history 
                    SET success = 1, outcome = ?, learned_from = 1
                    WHERE id = ?
                """, (result, action_id))
                conn.commit()
            finally:
                conn.close()
        self._increase_intelligence(0.1, f"Successful action {action_id}")
    
    def learn_from_mistake(self, action_id: int = None, error_message: str = None, context: Dict = None):
        """Learn from a mistake/failure"""
        if action_id:
            with self._db_lock:
                conn = self._get_connection()
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE action_history 
                        SET success = 0, error_message = ?
                        WHERE id = ?
                    """, (error_message, action_id))
                    conn.commit()
                finally:
                    conn.close()
        
        # Record mistake (outside lock - _record_mistake has its own lock)
        action_name = "unknown"
        if context and 'action' in context:
            action_name = context['action']
        self._record_mistake(action_name, error_message or "Unknown error")
    
    def get_best_approach(self, category: str) -> Optional[Dict]:
        """Get the best learned approach for a category/action type"""
        strategy = self.get_best_strategy(category)
        if strategy:
            return {
                'action': strategy.get('action_type', category),
                'confidence': strategy.get('confidence', 0.5),
                'details': strategy.get('strategy_details')
            }
        return None
    
    def get_action_confidence(self, action: str) -> float:
        """Get confidence level for a specific action"""
        base_conf = 0.5
        recency_bonus = 0.0
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT AVG(confidence) as conf FROM strategies
                    WHERE action_type = ? AND is_active = 1
                """, (action,))
                row = cursor.fetchone()
                if row and row['conf']:
                    base_conf = row['conf']
                # Recency: boost if success in last hour
                cursor.execute("""
                    SELECT COUNT(*) as recent_success FROM action_history
                    WHERE action_name = ? AND success = 1 AND timestamp > datetime('now','-1 hour')
                """, (action,))
                rs = cursor.fetchone()['recent_success']
                if rs:
                    recency_bonus = min(0.2, 0.05 * rs)
            finally:
                conn.close()
        return min(1.0, base_conf + recency_bonus)
    
    def get_recent_mistakes(self, limit: int = 10) -> List[Dict]:
        """Get recent mistakes for learning"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM mistakes 
                    ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()
    
    def suggest_improvement(self, action: str) -> Optional[str]:
        """Suggest improvement based on past mistakes"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                # Look for strategies that worked
                cursor.execute("""
                    SELECT strategy_details FROM strategies
                    WHERE action_type = ? AND confidence > 0.6 AND is_active = 1
                    ORDER BY confidence DESC
                    LIMIT 1
                """, (action,))
                row = cursor.fetchone()
                if row and row['strategy_details']:
                    return row['strategy_details']
                return None
            finally:
                conn.close()
    
    def get_recent_learnings(self, limit: int = 10) -> List[Dict]:
        """Get most recent things Aurora learned"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM knowledge_base 
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
                
            finally:
                conn.close()

    # ==========================================
    # JSON-BASED PATTERN MINING (REAL-ONLY)
    # ==========================================

    def mine_patterns_from_action_history(self,
                                          memory_dir: str = "aurora_memory",
                                          min_occurrences: int = 3) -> Dict[str, Any]:
        """
        Mine behavior patterns and learned actions from the real ActionTracker JSON.
        Updates:
        - behavior_patterns.json: aggregated success/failure stats per action_name and common errors
        - learned_actions.json: actions exceeding min_occurrences with success_rate and last_seen

        Returns a summary dict with counts and timestamp.
        """
        base = Path(memory_dir)
        action_history_path = base / "action_history.json"
        patterns_path = base / "behavior_patterns.json"
        learned_path = base / "learned_actions.json"

        # Load action history safely
        records: List[Dict[str, Any]] = []
        if action_history_path.exists():
            try:
                text = action_history_path.read_text(encoding="utf-8")
                if text.strip():
                    records = json.loads(text)
            except Exception as e:
                logger.error(f"Failed to read action history: {e}")

        # Aggregate
        by_action: Dict[str, Dict[str, Any]] = {}
        errors: Dict[str, int] = {}
        last_seen: Dict[str, str] = {}
        for r in records:
            # Normalize records: may be dicts or JSON strings
            if isinstance(r, str):
                try:
                    r = json.loads(r)
                except Exception:
                    continue
            if not isinstance(r, dict):
                continue
            name = r.get("action") or r.get("action_name") or "unknown"
            success = bool(r.get("success", False))
            err = r.get("error") or r.get("error_message")
            ts = r.get("timestamp") or r.get("time")

            s = by_action.setdefault(name, {"success": 0, "failure": 0, "total": 0})
            s["total"] += 1
            if success:
                s["success"] += 1
            else:
                s["failure"] += 1
                if err:
                    key = f"{name}:{str(err)[:80]}"
                    errors[key] = errors.get(key, 0) + 1

            if ts:
                last_seen[name] = ts

        # Build behavior patterns payload
        patterns_payload = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "actions": [],
            "common_errors": []
        }
        for name, stats in by_action.items():
            rate = (stats["success"] / stats["total"]) if stats["total"] else 0.0
            patterns_payload["actions"].append({
                "action": name,
                "total": stats["total"],
                "success": stats["success"],
                "failure": stats["failure"],
                "success_rate": round(rate, 3),
                "last_seen": last_seen.get(name)
            })

        # Sort actions by total desc
        patterns_payload["actions"].sort(key=lambda a: (-a["total"], -a["success_rate"]))

        # Common errors list
        for key, count in sorted(errors.items(), key=lambda kv: -kv[1]):
            act, err = key.split(":", 1)
            patterns_payload["common_errors"].append({
                "action": act,
                "error": err,
                "occurrences": count
            })

        # Build learned actions payload
        learned_payload = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "learned": []
        }
        for a in patterns_payload["actions"]:
            if a["total"] >= min_occurrences:
                learned_payload["learned"].append({
                    "action": a["action"],
                    "times": a["total"],
                    "success_rate": a["success_rate"],
                    "last_seen": a["last_seen"]
                })

        # Persist JSON files atomically
        try:
            patterns_tmp = patterns_path.with_suffix(".tmp")
            patterns_tmp.write_text(json.dumps(patterns_payload, indent=2), encoding="utf-8")
            patterns_tmp.replace(patterns_path)
        except Exception as e:
            logger.error(f"Failed to write behavior_patterns.json: {e}")

        try:
            learned_tmp = learned_path.with_suffix(".tmp")
            learned_tmp.write_text(json.dumps(learned_payload, indent=2), encoding="utf-8")
            learned_tmp.replace(learned_path)
        except Exception as e:
            logger.error(f"Failed to write learned_actions.json: {e}")

        summary = {
            "total_records": len(records),
            "actions_count": len(by_action),
            "learned_actions": len(learned_payload["learned"]),
            "common_errors": len(patterns_payload["common_errors"]),
            "written": {
                "behavior_patterns.json": str(patterns_path),
                "learned_actions.json": str(learned_path)
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        logger.info(f"🧩 Pattern mining complete: {summary}")
        return summary


# Global instance
_learning_engine = None

def get_learning_engine() -> LearningEngine:
    """Get learning engine instance"""
    global _learning_engine
    if _learning_engine is None:
        _learning_engine = LearningEngine()
    return _learning_engine