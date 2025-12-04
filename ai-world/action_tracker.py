"""
Action Tracking and Success Analysis System
Monitors Aurora's actions and learns from success/failure patterns
"""

import json
import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ActionResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure" 
    PARTIAL = "partial"
    TIMEOUT = "timeout"
    ERROR = "error"

@dataclass
class ActionRecord:
    """Record of an attempted action"""
    timestamp: float
    action_type: str
    action_data: Dict[str, Any]
    result: ActionResult
    execution_time: float
    error_message: Optional[str] = None
    retry_count: int = 0
    success_probability: float = 0.0
    context: Dict[str, Any] = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['result'] = self.result.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary"""
        data['result'] = ActionResult(data['result'])
        return cls(**data)

class ActionTracker:
    """Tracks and analyzes Aurora's actions for learning"""
    
    def __init__(self, memory_path: str = "aurora_memory/action_history.json"):
        self.memory_path = memory_path
        self.action_history: List[ActionRecord] = []
        self.success_patterns: Dict[str, Dict] = {}
        self.failure_patterns: Dict[str, Dict] = {}
        self.active_actions: Dict[str, Dict] = {}
        # Simple event listeners for real-time integrations (UI, logs, etc.)
        self._listeners: List = []
        self.load_memory()

    def register_listener(self, callback):
        """Register a callback to be invoked when an action completes.
        Callback signature: fn(ActionRecord)
        """
        if callback and callback not in self._listeners:
            self._listeners.append(callback)

    def _notify_listeners(self, record: ActionRecord):
        """Notify all registered listeners of a new action record."""
        for cb in list(self._listeners):
            try:
                cb(record)
            except Exception as e:
                # Listener errors should not break tracking
                pass
        
    def start_action(self, action_id: str, action_type: str, action_data: Dict, context: Dict = None) -> str:
        """Start tracking an action"""
        start_time = time.time()
        
        self.active_actions[action_id] = {
            'start_time': start_time,
            'action_type': action_type,
            'action_data': action_data,
            'context': context or {}
        }
        
        return action_id
    
    def complete_action(self, action_id: str, result: ActionResult, 
                       error_message: str = None, retry_count: int = 0) -> ActionRecord:
        """Complete an action and record results"""
        if action_id not in self.active_actions:
            return None
            
        action_info = self.active_actions.pop(action_id)
        end_time = time.time()
        execution_time = end_time - action_info['start_time']
        
        # Calculate success probability based on history
        success_prob = self._calculate_success_probability(
            action_info['action_type'], 
            action_info['action_data']
        )
        
        record = ActionRecord(
            timestamp=action_info['start_time'],
            action_type=action_info['action_type'],
            action_data=action_info['action_data'],
            result=result,
            execution_time=execution_time,
            error_message=error_message,
            retry_count=retry_count,
            success_probability=success_prob,
            context=action_info['context']
        )
        
        self.action_history.append(record)
        self._update_patterns(record)
        # Fire event for real-time consumers
        self._notify_listeners(record)
        
        # Save periodically
        if len(self.action_history) % 10 == 0:
            self.save_memory()
            
        return record
    
    def _calculate_success_probability(self, action_type: str, action_data: Dict) -> float:
        """Calculate probability of success based on historical data"""
        similar_actions = [
            record for record in self.action_history[-100:]  # Last 100 actions
            if record.action_type == action_type
        ]
        
        if not similar_actions:
            return 0.5  # No data, assume 50%
            
        successes = sum(1 for action in similar_actions 
                       if action.result == ActionResult.SUCCESS)
        
        return successes / len(similar_actions)
    
    def _update_patterns(self, record: ActionRecord):
        """Update success/failure patterns"""
        action_type = record.action_type
        
        if record.result == ActionResult.SUCCESS:
            if action_type not in self.success_patterns:
                self.success_patterns[action_type] = {
                    'count': 0,
                    'avg_time': 0.0,
                    'common_contexts': {},
                    'best_times': []
                }
            
            pattern = self.success_patterns[action_type]
            pattern['count'] += 1
            pattern['avg_time'] = (pattern['avg_time'] * (pattern['count'] - 1) + 
                                 record.execution_time) / pattern['count']
            
            # Track best execution times
            pattern['best_times'].append(record.execution_time)
            pattern['best_times'] = sorted(pattern['best_times'])[:10]  # Keep top 10
            
            # Track successful contexts
            if record.context:
                for key, value in record.context.items():
                    if key not in pattern['common_contexts']:
                        pattern['common_contexts'][key] = {}
                    if str(value) not in pattern['common_contexts'][key]:
                        pattern['common_contexts'][key][str(value)] = 0
                    pattern['common_contexts'][key][str(value)] += 1
                    
        elif record.result in [ActionResult.FAILURE, ActionResult.ERROR]:
            if action_type not in self.failure_patterns:
                self.failure_patterns[action_type] = {
                    'count': 0,
                    'common_errors': {},
                    'contexts': {},
                    'retry_success_rate': 0.0
                }
            
            pattern = self.failure_patterns[action_type]
            pattern['count'] += 1
            
            # Track error messages
            if record.error_message:
                if record.error_message not in pattern['common_errors']:
                    pattern['common_errors'][record.error_message] = 0
                pattern['common_errors'][record.error_message] += 1
                
    def should_retry(self, action_type: str, error_message: str = None) -> bool:
        """Determine if an action should be retried"""
        if action_type not in self.failure_patterns:
            return True  # No failure history, try once
            
        pattern = self.failure_patterns[action_type]
        
        # Don't retry if error is very common
        if error_message and error_message in pattern['common_errors']:
            error_frequency = pattern['common_errors'][error_message]
            if error_frequency > 5:  # Very common error
                return False
                
        # Retry if success rate is decent
        success_prob = self._calculate_success_probability(action_type, {})
        return success_prob > 0.2  # 20% success rate threshold
    
    def get_best_context(self, action_type: str) -> Dict:
        """Get the best context for an action type"""
        if action_type not in self.success_patterns:
            return {}
            
        pattern = self.success_patterns[action_type]
        best_context = {}
        
        for key, values in pattern['common_contexts'].items():
            # Get most successful value for each context key
            best_value = max(values.keys(), key=lambda k: values[k])
            best_context[key] = best_value
            
        return best_context
    
    def get_action_stats(self, action_type: str = None) -> Dict:
        """Get statistics for actions"""
        if action_type:
            actions = [r for r in self.action_history if r.action_type == action_type]
        else:
            actions = self.action_history
            
        if not actions:
            return {}
            
        total = len(actions)
        successes = sum(1 for a in actions if a.result == ActionResult.SUCCESS)
        failures = sum(1 for a in actions if a.result == ActionResult.FAILURE)
        errors = sum(1 for a in actions if a.result == ActionResult.ERROR)
        
        return {
            'total_actions': total,
            'success_rate': successes / total if total > 0 else 0,
            'failure_rate': failures / total if total > 0 else 0,
            'error_rate': errors / total if total > 0 else 0,
            'avg_execution_time': sum(a.execution_time for a in actions) / total if total > 0 else 0,
            'recent_success_rate': self._calculate_success_probability(action_type, {}) if action_type else 0
        }
    
    def load_memory(self):
        """Load action history from memory"""
        try:
            with open(self.memory_path, 'r') as f:
                data = json.load(f)
                self.action_history = [ActionRecord.from_dict(record) for record in data.get('history', [])]
                self.success_patterns = data.get('success_patterns', {})
                self.failure_patterns = data.get('failure_patterns', {})
        except FileNotFoundError:
            print(f"No action history found at {self.memory_path}, starting fresh")
        except Exception as e:
            print(f"Error loading action history: {e}")
    
    def save_memory(self):
        """Save action history to memory"""
        try:
            data = {
                'history': [record.to_dict() for record in self.action_history[-1000:]],  # Keep last 1000
                'success_patterns': self.success_patterns,
                'failure_patterns': self.failure_patterns,
                'last_updated': time.time()
            }
            
            import os
            os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
            
            with open(self.memory_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving action history: {e}")

class SmartRetryManager:
    """Manages smart retry logic based on action tracking"""
    
    def __init__(self, action_tracker: ActionTracker):
        self.tracker = action_tracker
        
    def execute_with_retry(self, action_func, action_type: str, 
                          action_data: Dict, max_retries: int = 3,
                          context: Dict = None) -> ActionRecord:
        """Execute an action with intelligent retry logic"""
        action_id = f"{action_type}_{int(time.time() * 1000)}"
        
        self.tracker.start_action(action_id, action_type, action_data, context)
        
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # Execute the action
                result = action_func(**action_data)
                
                # Determine if successful
                if result and result.get('success', False):
                    return self.tracker.complete_action(
                        action_id, ActionResult.SUCCESS, retry_count=retry_count
                    )
                else:
                    last_error = result.get('error', 'Unknown failure')
                    
            except Exception as e:
                last_error = str(e)
                
            # Check if we should retry
            if retry_count < max_retries:
                should_retry = self.tracker.should_retry(action_type, last_error)
                if should_retry:
                    retry_count += 1
                    time.sleep(min(2 ** retry_count, 10))  # Exponential backoff
                    continue
                    
            break
            
        # All retries failed
        return self.tracker.complete_action(
            action_id, ActionResult.FAILURE, 
            error_message=last_error, retry_count=retry_count
        )