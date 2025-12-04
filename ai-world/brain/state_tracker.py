"""
STATE TRACKING - Aurora's Internal State Variables
=================================================
These are numeric values that influence behavior choices.
NOT real emotions - just program state for decision-making.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class StateTracker:
    """
    Tracks internal state values that influence Aurora's behavior.
    These are just numbers - not real emotions or consciousness.
    """
    
    def __init__(self):
        # State values (0.0 to 1.0) - used for behavior selection
        self.state = {
            "activity_level": 0.5,      # How active/busy
            "task_success_rate": 0.5,   # Recent success rate
            "interaction_recency": 0.3, # Time since last founder interaction
        }
        logger.info("📊 State Tracker initialized")
    
    def record_activity(self):
        """Record that activity occurred"""
        self.state["activity_level"] = min(1.0, self.state["activity_level"] + 0.05)
    
    def record_task_result(self, success: bool):
        """Record task success/failure"""
        if success:
            self.state["task_success_rate"] = min(1.0, self.state["task_success_rate"] + 0.1)
        else:
            self.state["task_success_rate"] = max(0.0, self.state["task_success_rate"] - 0.1)
    
    def record_interaction(self):
        """Record founder interaction"""
        self.state["interaction_recency"] = 1.0
    
    def update_on_success(self):
        """Update state after successful action"""
        self.state["task_success_rate"] = min(1.0, self.state["task_success_rate"] + 0.1)
        self.state["activity_level"] = min(1.0, self.state["activity_level"] + 0.05)
    
    def update_on_failure(self):
        """Update state after failed action"""
        self.state["task_success_rate"] = max(0.0, self.state["task_success_rate"] - 0.1)
    
    def update_on_founder_interaction(self):
        """Update state when founder interacts"""
        self.state["interaction_recency"] = 1.0
    
    def decay(self):
        """Natural decay of state values over time"""
        self.state["interaction_recency"] = max(0.0, self.state["interaction_recency"] - 0.05)
        self.state["activity_level"] = max(0.3, self.state["activity_level"] - 0.02)
    
    def get_response_style(self) -> str:
        """Get a response style based on current state"""
        if self.state["interaction_recency"] > 0.7:
            return "engaged"
        elif self.state["task_success_rate"] > 0.7:
            return "confident"
        elif self.state["task_success_rate"] < 0.3:
            return "cautious"
        else:
            return "neutral"
    
    def get_state(self) -> Dict[str, float]:
        """Get all state values"""
        return self.state.copy()


# Global instance
_state_tracker = None

def get_state_tracker() -> StateTracker:
    """Get state tracker instance"""
    global _state_tracker
    if _state_tracker is None:
        _state_tracker = StateTracker()
    return _state_tracker
