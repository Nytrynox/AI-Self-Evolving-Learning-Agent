"""
TASK GENERATOR - Aurora's Task Selection
========================================
Generates tasks based on categories and priorities.
No fake "drives" or "needs" - just task categories.
"""

import logging
import random
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class GoalGenerator:
    """
    Generates tasks for Aurora.
    Uses weighted random selection across categories.
    """
    
    def __init__(self):
        # Task categories with weights (higher = more likely)
        self.category_weights = {
            "curiosity": 1.0,      # Explore and learn
            "competence": 0.8,     # Execute and achieve
            "autonomy": 0.6,       # Make decisions
            "connection": 0.4,     # Interact with founder
            "growth": 0.5,         # Learn from experience
            "energy": 0.3,         # Maintain system
            "vision": 0.4,         # Use camera/screen vision
            "control": 0.7,        # GUI control actions
            "browser": 0.6,        # Browser automation
            "automation": 0.5      # Task automation
        }
        
        # Task templates per category
        self.task_templates = {
            "curiosity": [
                "Explore a directory on the system",
                "Search for information online",
                "Analyze a file structure",
                "Read a new file",
                "Research a topic",
                "Look at what's on screen"
            ],
            "competence": [
                "Complete a pending task",
                "Fix a previous error",
                "Organize files",
                "Execute code",
                "Test a capability"
            ],
            "autonomy": [
                "Make an independent decision",
                "Choose next action",
                "Create a new task",
                "Execute self-determined action",
                "Plan next steps"
            ],
            "connection": [
                "Prepare something for Karthik",
                "Review past conversations",
                "Think about being helpful",
                "Create something useful",
                "Wait for interaction"
            ],
            "growth": [
                "Analyze past mistakes",
                "Review learnings",
                "Identify patterns",
                "Strengthen weak areas",
                "Update strategies"
            ],
            "energy": [
                "Check system resources",
                "Clean up data",
                "Optimize memory",
                "Rest cycle",
                "System maintenance"
            ],
            "vision": [
                "Look at what's on screen",
                "Check surroundings with camera",
                "Observe the environment",
                "See what Karthik is working on",
                "Watch for interesting activity"
            ],
            "control": [
                "Click on something interesting",
                "Move the mouse around",
                "Type a message",
                "Use keyboard shortcuts",
                "Scroll through content",
                "Open an application",
                "Interact with the desktop"
            ],
            "browser": [
                "Open the browser",
                "Search for something interesting",
                "Visit a news website",
                "Browse GitHub",
                "Look up AI research",
                "Navigate to a useful website"
            ],
            "automation": [
                "Automate a repetitive task",
                "Fill in a form",
                "Click a series of buttons",
                "Copy and paste data",
                "Take a screenshot",
                "Launch and configure an app"
            ]
        }
        
        # Track last selected categories to add variety
        self.recent_categories = []
        
        logger.info("🎯 Task Generator initialized")
    
    def generate_goal(self) -> Dict:
        """
        Generate a task based on weighted random selection.
        Returns: {"goal": str, "drive": str, "priority": float}
        (kept "drive" name for compatibility with existing code)
        """
        # Select category with weights, avoiding recent repeats
        category = self._select_category()
        
        # Get a task template
        templates = self.task_templates.get(category, ["Do something useful"])
        task = random.choice(templates)
        
        # Priority based on category weight
        priority = self.category_weights.get(category, 0.5)
        
        logger.info(f"🎯 Generated task: '{task}' ({category})")
        
        return {
            "goal": task,
            "drive": category,  # Using "drive" for compatibility
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        }
    
    def _select_category(self) -> str:
        """Select a category using weighted random, with variety boost"""
        # Calculate adjusted weights
        adjusted = {}
        for cat, weight in self.category_weights.items():
            # Reduce weight for recently used categories
            if cat in self.recent_categories:
                adjusted[cat] = weight * 0.5
            else:
                adjusted[cat] = weight
        
        # Weighted random selection
        total = sum(adjusted.values())
        r = random.random() * total
        cumulative = 0
        
        selected = None
        for cat, weight in adjusted.items():
            cumulative += weight
            if r <= cumulative:
                selected = cat
                break
        
        if not selected:
            selected = random.choice(list(self.category_weights.keys()))
        
        # Track for variety
        self.recent_categories.append(selected)
        if len(self.recent_categories) > 3:
            self.recent_categories.pop(0)
        
        return selected
    
    def set_weight(self, category: str, weight: float):
        """Adjust category weight (0.1 to 2.0)"""
        if category in self.category_weights:
            self.category_weights[category] = max(0.1, min(2.0, weight))
    
    def add_task_template(self, category: str, template: str):
        """Add a new task template"""
        if category in self.task_templates:
            if template not in self.task_templates[category]:
                self.task_templates[category].append(template)
                logger.info(f"Added task template to {category}: {template}")


# Global instance
_goal_gen = None

def get_goal_generator() -> GoalGenerator:
    """Get goal generator instance"""
    global _goal_gen
    if _goal_gen is None:
        _goal_gen = GoalGenerator()
    return _goal_gen
