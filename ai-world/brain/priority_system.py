"""
PRIORITY SYSTEM - What Aurora Should Do Next
============================================
Simple priority queue for task selection.
"""

import logging
import random
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class PrioritySystem:
    """
    Determines what Aurora should do next based on:
    - Time since last action type
    - System resources
    - Pending tasks
    """
    
    def __init__(self):
        self.last_actions = {}  # action_type -> timestamp
        self.action_weights = {
            "explore_files": 1.0,
            "search_web": 0.8,
            "think": 1.2,
            "execute_code": 0.6,
            "check_system": 0.5,
            "rest": 0.3
        }
        logger.info("🎯 Priority System initialized")
    
    def get_next_action(self, available_actions: List[str]) -> str:
        """
        Select next action based on weights and recency.
        Actions not done recently get higher priority.
        """
        if not available_actions:
            return "rest"
        
        # Calculate scores
        scores = {}
        now = datetime.now()
        
        for action in available_actions:
            base_weight = self.action_weights.get(action, 0.5)
            
            # Boost if not done recently
            if action in self.last_actions:
                seconds_ago = (now - self.last_actions[action]).total_seconds()
                recency_boost = min(1.0, seconds_ago / 300)  # Max boost after 5 min
            else:
                recency_boost = 1.0  # Never done = high priority
            
            scores[action] = base_weight + recency_boost
        
        # Weighted random selection
        total = sum(scores.values())
        r = random.random() * total
        cumulative = 0
        
        for action, score in scores.items():
            cumulative += score
            if r <= cumulative:
                self.last_actions[action] = now
                return action
        
        return available_actions[0]
    
    def record_action(self, action: str):
        """Record that an action was performed"""
        self.last_actions[action] = datetime.now()
    
    def set_weight(self, action: str, weight: float):
        """Adjust action weight based on success/failure"""
        if action in self.action_weights:
            # Clamp between 0.1 and 2.0
            self.action_weights[action] = max(0.1, min(2.0, weight))


# Global instance
_priority = None

def get_priority_system():
    """Get priority system instance"""
    global _priority
    if _priority is None:
        _priority = PrioritySystem()
    return _priority
