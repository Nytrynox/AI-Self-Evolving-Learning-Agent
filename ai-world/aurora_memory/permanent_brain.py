"""
PermanentBrain - Aurora AI's Persistent Memory System

This module provides persistent storage and retrieval of experiences, 
failures, plans, and learned knowledge that survives across sessions.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


class PermanentBrain:
    """
    Manages Aurora's persistent memory across sessions.
    
    Features:
    - Experience logging (observations, actions, outcomes)
    - Failure tracking for avoiding repeated mistakes  
    - Plan history for learning from past strategies
    - Screen insights storage
    - Intelligent summary generation
    """
    
    def __init__(self, memory_dir: str):
        """
        Initialize the permanent brain with a memory directory.
        
        Args:
            memory_dir: Path to directory for storing memory files
        """
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)
        
        # File paths
        self.experiences_file = os.path.join(memory_dir, 'experiences_log.json')
        self.failures_file = os.path.join(memory_dir, 'failure_log.json')
        self.plans_file = os.path.join(memory_dir, 'plans_history.json')
        self.screen_file = os.path.join(memory_dir, 'screen_analysis.json')
        self.skills_file = os.path.join(memory_dir, 'acquired_skills.json')
        self.knowledge_file = os.path.join(memory_dir, 'system_knowledge.json')
        
        # Load existing data
        self.experiences = self._load_json(self.experiences_file, [])
        self.failures = self._load_json(self.failures_file, [])
        self.plans = self._load_json(self.plans_file, [])
        self.screen_insights = self._load_json(self.screen_file, [])
        self.skills = self._load_json(self.skills_file, {})
        self.knowledge = self._load_json(self.knowledge_file, {})
        
        # Statistics
        self.session_start = datetime.now().isoformat()
        self.success_count = 0
        self.failure_count = 0
    
    def _load_json(self, filepath: str, default: Any) -> Any:
        """Load JSON file, return default if not exists or error."""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return default
    
    def _save_json(self, filepath: str, data: Any):
        """Save data to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
    
    def record_experience(self, experience_type: str, description: str, 
                         metadata: Optional[Dict] = None) -> Dict:
        """
        Record an experience (observation, action, learning, etc.)
        
        Args:
            experience_type: Type of experience (observation, action, learning)
            description: Human-readable description
            metadata: Additional context data
            
        Returns:
            The recorded experience entry
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': experience_type,
            'description': description[:500],  # Limit size
            'metadata': metadata or {},
            'session': self.session_start
        }
        
        self.experiences.append(entry)
        
        # Keep only last 1000 experiences
        if len(self.experiences) > 1000:
            self.experiences = self.experiences[-1000:]
        
        self._save_json(self.experiences_file, self.experiences)
        return entry
    
    def record_failure(self, action: str, error: str, context: str = "") -> Dict:
        """
        Record a failed action to avoid repeating.
        
        Args:
            action: The action that failed
            error: Error message or reason
            context: Situational context when failure occurred
            
        Returns:
            The recorded failure entry
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action[:200],
            'error': str(error)[:200],
            'context': context[:200],
            'count': 1,
            'session': self.session_start
        }
        
        # Check if similar failure exists
        for existing in self.failures:
            if existing.get('action') == action:
                existing['count'] = existing.get('count', 1) + 1
                existing['last_failure'] = entry['timestamp']
                entry = existing
                break
        else:
            self.failures.append(entry)
        
        self.failure_count += 1
        
        # Keep only last 500 failures
        if len(self.failures) > 500:
            self.failures = self.failures[-500:]
        
        self._save_json(self.failures_file, self.failures)
        return entry
    
    def get_failed_actions(self, threshold: int = 2) -> List[Tuple[str, int]]:
        """
        Get actions that have failed multiple times.
        
        Args:
            threshold: Minimum failure count to include
            
        Returns:
            List of (action, count) tuples
        """
        result = []
        for failure in self.failures:
            if failure.get('count', 1) >= threshold:
                result.append((failure['action'], failure['count']))
        return result
    
    def save_plan(self, goal: str, steps: List[str]) -> Dict:
        """
        Save a plan for future reference and learning.
        
        Args:
            goal: The plan's objective
            steps: List of action steps
            
        Returns:
            The saved plan entry
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'goal': goal[:200],
            'steps': steps[:20],  # Limit steps
            'status': 'created',
            'outcome': None,
            'session': self.session_start
        }
        
        self.plans.append(entry)
        
        # Keep only last 200 plans
        if len(self.plans) > 200:
            self.plans = self.plans[-200:]
        
        self._save_json(self.plans_file, self.plans)
        return entry
    
    def save_screen_insight(self, analysis: str, screenshot_path: str = None) -> Dict:
        """
        Save insight from screen analysis.
        
        Args:
            analysis: The screen analysis text
            screenshot_path: Optional path to saved screenshot
            
        Returns:
            The saved insight entry
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis[:500],
            'screenshot': screenshot_path,
            'session': self.session_start
        }
        
        self.screen_insights.append(entry)
        
        # Keep only last 100 screen insights
        if len(self.screen_insights) > 100:
            self.screen_insights = self.screen_insights[-100:]
        
        self._save_json(self.screen_file, self.screen_insights)
        return entry
    
    def get_summary(self) -> Dict:
        """
        Get a summary of the brain's knowledge.
        
        Returns:
            Dictionary with memory statistics and intelligence metrics
        """
        total_memories = (
            len(self.experiences) + 
            len(self.failures) + 
            len(self.plans) + 
            len(self.screen_insights)
        )
        
        # Calculate intelligence level based on experience
        intelligence_score = min(100, (
            len(self.experiences) * 0.5 +
            len(self.plans) * 2 +
            len(self.skills) * 5 +
            len(self.screen_insights) * 1
        ))
        
        if intelligence_score < 20:
            level = "Newborn"
        elif intelligence_score < 50:
            level = "Learning"
        elif intelligence_score < 100:
            level = "Growing"
        elif intelligence_score < 200:
            level = "Capable"
        elif intelligence_score < 500:
            level = "Advanced"
        else:
            level = "Expert"
        
        return {
            'total_memories': total_memories,
            'experiences_count': len(self.experiences),
            'failures_count': len(self.failures),
            'plans_created': len(self.plans),
            'screen_insights': len(self.screen_insights),
            'skills_learned': len(self.skills),
            'intelligence_score': intelligence_score,
            'intelligence_level': level,
            'session_start': self.session_start,
            'success_rate': self.get_overall_success_rate()
        }
    
    def get_overall_success_rate(self) -> float:
        """
        Calculate overall success rate.
        
        Returns:
            Float between 0 and 1 representing success rate
        """
        total = self.success_count + self.failure_count
        if total == 0:
            # Estimate from history
            total_actions = len(self.experiences)
            failed_actions = sum(f.get('count', 1) for f in self.failures)
            if total_actions == 0:
                return 0.5  # Default
            return max(0.1, min(0.95, 1 - (failed_actions / (total_actions + 1))))
        return self.success_count / total
    
    def record_success(self, action: str, outcome: str = ""):
        """Record a successful action."""
        self.success_count += 1
        self.record_experience('success', f"Action succeeded: {action}", {
            'action': action,
            'outcome': outcome
        })
    
    def get_recent_experiences(self, count: int = 10, 
                                experience_type: str = None) -> List[Dict]:
        """
        Get most recent experiences, optionally filtered by type.
        
        Args:
            count: Number of experiences to return
            experience_type: Optional filter by type
            
        Returns:
            List of experience dictionaries
        """
        if experience_type:
            filtered = [e for e in self.experiences if e.get('type') == experience_type]
            return filtered[-count:]
        return self.experiences[-count:]
    
    def learn_skill(self, skill_name: str, skill_data: Dict):
        """
        Record a learned skill.
        
        Args:
            skill_name: Name of the skill
            skill_data: Skill details (steps, context, etc.)
        """
        self.skills[skill_name] = {
            'learned_at': datetime.now().isoformat(),
            'data': skill_data,
            'usage_count': self.skills.get(skill_name, {}).get('usage_count', 0)
        }
        self._save_json(self.skills_file, self.skills)
    
    def get_skill(self, skill_name: str) -> Optional[Dict]:
        """Get a learned skill by name."""
        return self.skills.get(skill_name)
    
    def add_knowledge(self, key: str, value: Any):
        """Add or update system knowledge."""
        self.knowledge[key] = {
            'value': value,
            'updated_at': datetime.now().isoformat()
        }
        self._save_json(self.knowledge_file, self.knowledge)
    
    def get_knowledge(self, key: str, default: Any = None) -> Any:
        """Get stored knowledge by key."""
        entry = self.knowledge.get(key)
        return entry.get('value', default) if entry else default
    
    def clear_old_data(self, days: int = 7):
        """
        Clear data older than specified days.
        
        Args:
            days: Number of days to keep
        """
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        self.experiences = [e for e in self.experiences 
                          if e.get('timestamp', '') > cutoff]
        self.screen_insights = [s for s in self.screen_insights 
                               if s.get('timestamp', '') > cutoff]
        
        self._save_json(self.experiences_file, self.experiences)
        self._save_json(self.screen_file, self.screen_insights)
