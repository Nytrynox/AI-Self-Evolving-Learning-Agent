"""
MOTHER AI - AURORA (Enhanced Self-Learning Version)
====================================================
The main autonomous AI system with:
- Self-learning from mistakes (persistent database)
- Natural language understanding (NLP)
- Voice interaction (speak + listen)
- Full macOS control A-Z
- Asks user when in doubt
- Intelligence that grows over time

NOT consciousness. NOT sentient. Just an autonomous program loop
that LEARNS and IMPROVES from every action.
"""

import time
import logging
import threading
import random
from typing import Dict, Optional, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class MotherAI:
    """
    Aurora - The Mother AI (Enhanced Self-Learning Version)
    
    An autonomous AI program that:
    - Runs a continuous task loop
    - Uses LLM for decision making
    - Executes REAL actions (files, web, GUI, system)
    - LEARNS from every outcome (persistent database)
    - Self-evolves by analyzing mistakes
    - Asks user when confidence is low
    - Voice interaction (speak + listen)
    - Full macOS control A-Z
    - Intelligence grows over time
    """
    
    def __init__(self):
        # Import all systems
        from config.settings import MOTHER_AI, AUTONOMY
        from config.founder_protection import get_founder_protection
        from brain.memory_system import get_memory
        from brain.state_tracker import get_state_tracker
        from brain.priority_system import get_priority_system
        from brain.resource_tracker import get_resource_tracker
        from brain.goal_generator import get_goal_generator
        from agents.llm_interface import get_llm
        from agents.agent_spawner import get_agent_spawner
        from tools.sensors.audio import get_speech
        from tools.sensors.system_monitor import get_system_monitor
        from tools.actions.file_ops import get_file_ops
        from tools.actions.web_tools import get_web_tools
        from tools.actions.code_executor import get_code_executor
        from tools.actions.gui_control import get_gui_control
        from tools.actions.browser_automation import get_browser_automation
        
        # NEW: Import self-learning systems
        from brain.learning_engine import get_learning_engine
        from brain.nlp_engine import get_nlp_engine
        from tools.macos_commands import get_macos_commands
        from tools.sensors.voice_system import get_voice_system
        
        # Core identity
        self.name = MOTHER_AI["name"]
        self.config = MOTHER_AI
        self.autonomy_config = AUTONOMY
        
        # Original systems
        self.founder = get_founder_protection()
        self.memory = get_memory()
        self.state = get_state_tracker()
        self.priorities = get_priority_system()
        self.resources = get_resource_tracker()
        self.goals = get_goal_generator()
        self.llm = get_llm()
        self.agents = get_agent_spawner()
        self.speech = get_speech()
        self.monitor = get_system_monitor()
        self.files = get_file_ops()
        self.web = get_web_tools()
        self.executor = get_code_executor()
        self.gui = get_gui_control()
        self.browser = get_browser_automation()
        
        # NEW: Self-learning systems
        self.learning = get_learning_engine()  # Persistent self-learning database
        self.nlp = get_nlp_engine()            # Natural language understanding
        self.macos = get_macos_commands()      # Full macOS A-Z commands
        self.voice = get_voice_system()        # Voice speak + listen
        
        # Vision system
        from tools.sensors.vision import get_vision
        self.vision = get_vision()
        
        # System Learning
        from brain.system_learner import get_system_learner
        self.system_learner = get_system_learner()  # Learn MacBook A-Z
        
        # Security tools removed (impractical hacking features)
        self.security = None

        # Affordances & Curiosity removed (over-engineered, not practical)
        self._afford_register = self._afford_list = self._afford_record = None
        self._curiosity_touch = self._curiosity_score = None

        # Event bus for cross-agent communication
        try:
            from agents.event_bus import get_event_bus
            self.event_bus = get_event_bus()
        except Exception:
            self.event_bus = None

        # Epoch / autonomy state
        self.owner_authenticated = False
        self.current_epoch = 'explore'  # 'owner' when founder verified
        self.enable_curiosity = False  # Disabled - feature removed
        
        # State
        self.is_running = False
        self.is_paused = False
        self.cycle_count = 0
        self.current_task = None
        self.last_action = None
        self.confidence_threshold = 0.5  # Ask user when below this
        self.voice_enabled = True  # Voice interaction toggle
        
        # Action map - ALL capabilities A-Z (expanded with macOS commands)
        self.actions = {
            # Original actions
            "explore_files": self._action_explore_files,
            "search_web": self._action_search_web,
            "think": self._action_think,
            "speak": self._action_speak,
            "create_agent": self._action_create_agent,
            "execute_code": self._action_execute_code,
            "learn": self._action_learn,
            "check_system": self._action_check_system,
            "rest": self._action_rest,
            "see_screen": self._action_see_screen,
            "see_camera": self._action_see_camera,
            # GUI Control - Mouse
            "click": self._action_click,
            "double_click": self._action_double_click,
            "right_click": self._action_right_click,
            "drag": self._action_drag,
            "scroll": self._action_scroll,
            "move_mouse": self._action_move_mouse,
            # GUI Control - Keyboard
            "type_text": self._action_type_text,
            "press_key": self._action_press_key,
            "hotkey": self._action_hotkey,
            "copy": self._action_copy,
            "paste": self._action_paste,
            # GUI Control - Apps
            "open_app": self._action_open_app,
            "open_browser": self._action_open_browser,
            "open_terminal": self._action_open_terminal,
            "open_finder": self._action_open_finder,
            "activate_app": self._action_activate_app,
            "quit_app": self._action_quit_app,
            # GUI Control - Browser
            "browser_search": self._action_browser_search,
            "browser_url": self._action_browser_url,
            # Smart actions
            "click_button": self._action_click_button,
            "fill_form_field": self._action_fill_form_field,
            "take_screenshot": self._action_take_screenshot,
            # NEW: macOS System Commands A-Z
            "macos_command": self._action_macos_command,
            "spotlight_search": self._action_spotlight_search,
            "control_volume": self._action_control_volume,
            "control_brightness": self._action_control_brightness,
            "mission_control": self._action_mission_control,
            "show_desktop": self._action_show_desktop,
            "lock_screen": self._action_lock_screen,
            "switch_space": self._action_switch_space,
            "close_window": self._action_close_window,
            "minimize_window": self._action_minimize_window,
            "maximize_window": self._action_maximize_window,
            "switch_app": self._action_switch_app,
            "force_quit_menu": self._action_force_quit_menu,
            "empty_trash": self._action_empty_trash,
            "new_finder_window": self._action_new_finder_window,
            "go_to_folder": self._action_go_to_folder,
            "get_file_info": self._action_get_file_info,
            "toggle_hidden_files": self._action_toggle_hidden_files,
            # NEW: Voice/Communication
            "ask_user": self._action_ask_user,
            "listen_to_user": self._action_listen_to_user,
            "announce": self._action_announce,
            # NEW: Intelligence
            "analyze_mistakes": self._action_analyze_mistakes,
            "report_intelligence": self._action_report_intelligence,
            # NEW: System Learning
            "learn_system": self._action_learn_system,
            "learn_apps": self._action_learn_apps,
            "learn_files": self._action_learn_files,
            "search_knowledge": self._action_search_knowledge,
            # Sub-agent management
            "spawn_learning_agent": self._action_spawn_learning_agent,
            "spawn_automation_agent": self._action_spawn_automation_agent,
            "assign_task_to_agent": self._action_assign_task_to_agent,
            "list_agents": self._action_list_agents,
            # Direct command execution
            "run_shell": self._action_run_shell,
            "run_applescript": self._action_run_applescript,
        }

        # Affordances registration removed (feature deleted)

        # Epoch / autonomy state
        self.owner_authenticated = False
        self.current_epoch = 'explore'  # 'owner' when founder verified

        # Exploration weighting toggle
        self.enable_curiosity = True
        
        # Log intelligence level
        intel = self.learning.get_intelligence_metrics()
        logger.info(f"🌟 {self.name} initialized")
        logger.info(f"🧠 Intelligence Level: {intel['level']} (Score: {intel['intelligence_score']:.1f})")
        logger.info(f"📚 Learned patterns: {intel['total_learned']}, Mistakes recorded: {intel['total_mistakes']}")
    
    # ==========================================
    # LIFECYCLE
    # ==========================================
    
    def start(self):
        """Start Aurora's operation loop"""
        if self.is_running:
            logger.warning("Aurora is already running")
            return
        
        self.is_running = True
        logger.info(f"✨ {self.name} starting...")
        
        # Restore state from memory
        self._restore_state()
        
        # Get intelligence metrics
        intel = self.learning.get_intelligence_metrics()
        
        # Greeting with voice
        greeting = f"I am {self.name}. Intelligence level: {intel['level']}. I have learned from {intel['total_learned']} experiences. Ready to serve."
        if self.voice_enabled and self.voice.is_available():
            self.voice.speak(greeting)
        else:
            self.speech.speak(f"I am {self.name}. Systems online.")
        
        # Log startup
        self.memory.store_experience(
            "lifecycle",
            "Aurora started",
            f"Cycle count: {self.cycle_count}, Intelligence: {intel['intelligence_score']:.1f}",
            success=True
        )
        
        # Start main loop
        self._thread = threading.Thread(target=self._main_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop Aurora"""
        self.is_running = False
        self._save_state()
        self.agents.terminate_all()
        self.speech.speak("Shutting down. Goodbye.")
        logger.info(f"💤 {self.name} stopped")
    
    def pause(self):
        """Pause autonomous operation"""
        self.is_paused = True
        logger.info("⏸️ Aurora paused")
    
    def resume(self):
        """Resume autonomous operation"""
        self.is_paused = False
        logger.info("▶️ Aurora resumed")
    
    # ==========================================
    # MAIN LOOP
    # ==========================================
    
    def _main_loop(self):
        """The main autonomous operation loop with SELF-LEARNING"""
        while self.is_running:
            try:
                if self.is_paused:
                    time.sleep(1)
                    continue
                
                self.cycle_count += 1
                logger.info(f"\n{'='*50}\n🔄 Cycle #{self.cycle_count}\n{'='*50}")
                
                # 1. Check resources
                if self.resources.should_rest():
                    logger.info("⚠️ Low resources, resting...")
                    time.sleep(10)
                    continue
                
                # 2. Update state
                self.state.record_activity()
                # Publish lightweight status for world view
                self._publish_status()
                
                # 3. Generate task
                task_data = self.goals.generate_goal()
                self.current_task = task_data["goal"]
                category = task_data["drive"]
                
                logger.info(f"🎯 Task: {self.current_task} ({category})")
                
                # 4. Check if we've learned a better approach for this task type
                best_approach = self.learning.get_best_approach(category)
                if best_approach:
                    logger.info(f"📚 Learned approach available: {best_approach['action']} (confidence: {best_approach['confidence']:.2f})")
                
                # 5. Decide action (with learning influence)
                action, confidence = self._decide_action_smart(self.current_task, category, best_approach)

                # Curiosity override in exploration epoch
                if self.enable_curiosity and self.current_epoch == 'explore' and self._curiosity_score:
                    # Pick highest novelty among likely candidates if confidence low
                    likely_pool = [action] + [a for a in self.actions.keys() if a != action][:10]
                    scored = [(self._curiosity_score(a), a) for a in likely_pool]
                    scored.sort(reverse=True)
                    if scored and scored[0][1] != action and confidence < 0.75:
                        action = scored[0][1]
                        confidence = min(0.8, confidence + 0.1)
                
                # 6. If confidence is low, ask user
                if confidence < self.confidence_threshold:
                    user_decision = self._ask_user_for_guidance(action, self.current_task, confidence)
                    if user_decision:
                        action = user_decision
                
                # 7. Record attempt in learning system
                action_id = self.learning.record_action_attempt(
                    action=action,
                    context={"task": self.current_task, "category": category},
                    parameters={"cycle": self.cycle_count}
                )
                
                # 8. Execute action
                success, result = self._execute_action(action)

                # Curiosity update / affordance usage record
                if self._curiosity_touch:
                    self._curiosity_touch(f"action:{action}")
                if self._afford_record:
                    self._afford_record(action, success)
                # Extended curiosity keys
                if self.enable_curiosity and self._curiosity_touch:
                    if action.startswith('open_'):
                        self._curiosity_touch(f"app:{action[5:]}")
                    if 'explore_' in action:
                        self._curiosity_touch(f"path:{action.split('explore_')[-1]}")

                # Publish to event bus
                if self.event_bus:
                    try:
                        self.event_bus.publish('action_result', {
                            'action': action,
                            'success': bool(success),
                            'result': str(result)[:200],
                            'cycle': self.cycle_count,
                            'epoch': self.current_epoch
                        })
                    except Exception:
                        pass
                
                # 9. LEARNING: Record outcome
                if success:
                    self.learning.record_success(
                        action_id=action_id,
                        result=result,
                        improvement_notes=f"Successful {action} for {category}"
                    )
                else:
                    self.learning.learn_from_mistake(
                        action_id=action_id,
                        error_message=str(result),
                        context={"task": self.current_task, "action": action}
                    )
                
                # 10. Record in state tracker
                self.state.record_task_result(success)
                self._learn_from_result(action, result, success)
                
                # 11. Adjust priorities based on success
                if success:
                    current = self.priorities.action_weights.get(action, 0.5)
                    self.priorities.set_weight(action, min(1.0, current + 0.05))
                else:
                    current = self.priorities.action_weights.get(action, 0.5)
                    self.priorities.set_weight(action, max(0.1, current - 0.05))
                
                # 12. Run sub-agents
                self.agents.run_agents_cycle()
                
                # 13. Periodic intelligence report (every 10 cycles)
                if self.cycle_count % 10 == 0:
                    self._periodic_intelligence_report()

                # 13b. Mine real patterns from ActionTracker JSON (every 5 cycles)
                if self.cycle_count % 5 == 0:
                    try:
                        summary = self.learning.mine_patterns_from_action_history("aurora_memory")
                        logger.info(f"📈 Pattern mining summary: actions={summary['actions_count']}, learned={summary['learned_actions']}")
                    except Exception as e:
                        logger.warning(f"Pattern mining error: {e}")
                
                # 14. Wait before next cycle
                interval = self.autonomy_config.get("loop_interval_seconds", 15)
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"❌ Loop error: {e}")
                self.memory.store_experience("error", str(e), "main_loop", success=False)
                # Learn from system errors too
                self.learning.learn_from_mistake(
                    action_id=None,
                    error_message=f"System error: {str(e)}",
                    context={"cycle": self.cycle_count, "task": self.current_task}
                )
                time.sleep(5)
    
    def _decide_action_smart(self, task: str, category: str, best_approach: Optional[Dict]) -> tuple:
        """Decide action using learning + LLM with confidence scoring"""
        # Check if we have a learned best approach with high confidence
        if best_approach and best_approach.get('confidence', 0) > 0.7:
            action = best_approach['action']
            return action, best_approach['confidence']
        
        # Map categories to likely actions
        category_actions = {
            "curiosity": ["explore_files", "search_web", "think", "see_screen", "open_browser", "browser_search", "ask_user"],
            "competence": ["execute_code", "create_agent", "explore_files", "type_text", "click", "open_app", "macos_command"],
            "autonomy": ["think", "create_agent", "click", "type_text", "hotkey", "macos_command"],
            "connection": ["speak", "browser_search", "open_browser", "ask_user", "announce", "listen_to_user"],
            "growth": ["learn", "think", "browser_search", "analyze_mistakes", "report_intelligence"],
            "energy": ["rest", "check_system"],
            "vision": ["see_screen", "see_camera", "take_screenshot"],
            "control": ["click", "type_text", "open_app", "hotkey", "drag", "scroll", "macos_command"],
            "browser": ["open_browser", "browser_search", "browser_url", "click", "type_text"],
            "automation": ["click", "type_text", "hotkey", "fill_form_field", "click_button", "drag", "macos_command"],
            "system": ["macos_command", "spotlight_search", "control_volume", "mission_control", "check_system"]
        }
        
        likely_actions = category_actions.get(category, list(self.actions.keys()))

        # Boost novel actions via curiosity if enabled
        if self.enable_curiosity and self._curiosity_score:
            enriched = []
            for a in likely_actions:
                novelty = self._curiosity_score(f"action:{a}")
                enriched.append((novelty, a))
            enriched.sort(reverse=True)
            # Keep top 12 to reduce prompt size
            likely_actions = [a for _, a in enriched[:12]] or likely_actions

        # Vision-based screen reasoning heuristic before LLM
        if category in ('vision', 'control') and self.llm and self.llm.has_vision():
            desc = self._describe_screen_safe()
            if desc:
                low = desc.lower()
                for cand in likely_actions:
                    if cand in low:
                        conf = max(0.7, self.learning.get_action_confidence(cand))
                        return cand, conf
        
        # Use LLM to decide if available
        if self.llm.is_available():
            action = self.llm.decide_action(task, likely_actions)
            if action and action in self.actions:
                # Base confidence from learning history
                confidence = self.learning.get_action_confidence(action)
                return action, confidence
        
        # Fallback: use priority system
        action = self.priorities.get_next_action(likely_actions)
        confidence = self.learning.get_action_confidence(action) if action else 0.5
        
        return action, confidence

    def _describe_screen_safe(self) -> str:
        """Capture the screen and request LLaVA description; returns '' on failure."""
        if not (self.llm and self.llm.has_vision()):
            return ''
        try:
            import subprocess, tempfile, os, threading
            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            path = tmp.name
            tmp.close()
            subprocess.run(['screencapture', '-x', path], timeout=5)
            with open(path, 'rb') as f:
                data = f.read()
            os.unlink(path)
            result_holder = {'desc': ''}
            def _call():
                try:
                    d = self.llm.describe_screen(data, hint='Identify actionable UI elements and next steps')
                    result_holder['desc'] = d or ''
                except Exception:
                    result_holder['desc'] = ''
            t = threading.Thread(target=_call, daemon=True)
            t.start()
            t.join(timeout=3)
            desc = result_holder['desc']
            # Publish vision description to event bus (real-only)
            if desc and self.event_bus:
                try:
                    self.event_bus.publish('vision_screen', {
                        'description': desc[:500]
                    })
                except Exception:
                    pass
            return desc
        except Exception:
            return ''

    def _publish_status(self):
        """Publish a lightweight status snapshot to the event bus."""
        if not self.event_bus:
            return
        try:
            status = {
                'cycle': self.cycle_count,
                'epoch': self.current_epoch,
                'last_action': self.last_action,
                'resources': self.resources.get_status_summary() if hasattr(self.resources, 'get_status_summary') else {}
            }
            self.event_bus.publish('ai_status', status)
        except Exception:
            pass
    
    def _ask_user_for_guidance(self, proposed_action: str, task: str, confidence: float) -> Optional[str]:
        """Ask user when confidence is low"""
        if not self.voice_enabled:
            return None
        
        question = f"I'm considering {proposed_action} for task: {task}. My confidence is {confidence:.0%}. Should I proceed or do something else?"
        
        logger.info(f"🤔 Asking user: {question}")
        
        # Try voice first
        if self.voice.is_available():
            response = self.voice.ask_for_confirmation(
                f"Should I {proposed_action}? I'm {confidence:.0%} confident.",
                timeout=10
            )
            if response is not None:
                if response:
                    logger.info("👤 User confirmed action")
                    return proposed_action
                else:
                    # Ask what they want instead
                    alternative = self.voice.ask_question(
                        "What would you like me to do instead?",
                        timeout=15
                    )
                    if alternative:
                        # Use NLP to understand the response
                        understood = self.nlp.understand(alternative)
                        if understood and understood.get('action'):
                            return understood['action']
        
        # No guidance received, proceed with original
        return None
    
    def _periodic_intelligence_report(self):
        """Periodic report on intelligence growth"""
        metrics = self.learning.get_intelligence_metrics()
        recent_mistakes = self.learning.get_recent_mistakes(5)
        
        logger.info(f"\n{'='*40}")
        logger.info(f"🧠 INTELLIGENCE REPORT (Cycle {self.cycle_count})")
        logger.info(f"   Score: {metrics['intelligence_score']:.1f}")
        logger.info(f"   Level: {metrics['level']}")
        logger.info(f"   Total learned: {metrics['total_learned']}")
        logger.info(f"   Total actions: {metrics['total_actions']}")
        logger.info(f"   Success rate: {metrics['success_rate']:.1%}")
        
        if recent_mistakes:
            logger.info(f"   Recent mistakes to learn from: {len(recent_mistakes)}")
        
        logger.info(f"{'='*40}\n")
    
    # ==========================================
    # STATE MANAGEMENT
    # ==========================================
    
    def _save_state(self):
        """Save state to memory"""
        state = {
            "cycle_count": self.cycle_count,
            "state": self.state.get_state(),
            "priorities": self.priorities.action_weights,
            "current_task": self.current_task
        }
        self.memory.set_state("aurora_state", state)
        logger.info("💾 State saved")
    
    def _restore_state(self):
        """Restore state from memory"""
        state = self.memory.get_state("aurora_state")
        if state:
            self.cycle_count = state.get("cycle_count", 0)
            if "priorities" in state:
                self.priorities.action_weights.update(state["priorities"])
            logger.info(f"📂 State restored (cycle {self.cycle_count})")
    
    # ==========================================
    # FOUNDER INTERACTION (Enhanced with NLP + Voice)
    # ==========================================
    
    def founder_speaks(self, message: str):
        """Handle message from founder Karthik with NLP understanding"""
        logger.info(f"👤 Founder says: {message}")
        
        # Verify founder
        if "karthik" in message.lower():
            self.founder.verify_by_name("Karthik")
        
        # Store conversation
        self.memory.store_conversation("Karthik", message, "founder_input")
        self.state.record_interaction()
        
        # Use NLP to understand the message
        understood = self.nlp.understand(message)
        logger.info(f"🧠 Understood intent: {understood.get('intent', 'unknown')}")
        
        # Check if this is a command
        if understood.get('intent') in ['command', 'open_app', 'system_control', 'search_web']:
            # Execute the command
            action = understood.get('action')
            if action and action in self.actions:
                logger.info(f"⚡ Executing command: {action}")
                success, result = self._execute_action(action)
                response = f"Done. {result}" if success else f"Had trouble with that: {result}"
            else:
                response = self._respond_to_founder(message)
        else:
            # Regular conversation
            response = self._respond_to_founder(message)
        
        # Learn from conversation
        self.nlp.learn_from_conversation(message, response, 0.8)
        
        self.memory.store_conversation("Aurora", response, "founder_response")
        
        # Speak response with voice if available
        if self.voice_enabled and self.voice.is_available():
            self.voice.speak(response)
        else:
            self.speech.speak_to_founder(response)
        
        return response
    
    def _respond_to_founder(self, message: str) -> str:
        """Generate response to founder with intelligence awareness"""
        intel = self.learning.get_intelligence_metrics()
        
        system_prompt = f"""You are Aurora, an AI assistant.
{self.founder.get_directives_for_ai()}

You are speaking to your founder, Karthik. Be helpful and respectful.
Your current intelligence score is {intel['intelligence_score']:.1f} (Level: {intel['level']}).
You have learned from {intel['total_learned']} experiences.
"""
        
        if self.llm.is_available():
            response = self.llm.generate(message, system_prompt=system_prompt)
            return response or "I understand, Karthik. How can I help?"
        else:
            return "I hear you, Karthik. My language model is not available right now."
    
    # ==========================================
    # ACTION EXECUTION
    # ==========================================
    
    def _execute_action(self, action: str) -> tuple:
        """Execute an action"""
        logger.info(f"⚡ Executing: {action}")
        
        if action in self.actions:
            try:
                result = self.actions[action]()
                self.last_action = action
                self.priorities.record_action(action)
                
                self.memory.store_experience(
                    "action",
                    f"Executed: {action}",
                    str(result)[:200],
                    success=True
                )
                
                return True, result
                
            except Exception as e:
                logger.error(f"❌ Action failed: {e}")
                self.memory.store_experience(
                    "action",
                    f"Failed: {action}",
                    str(e),
                    success=False,
                    lesson=f"Error in {action}: {str(e)[:100]}"
                )
                return False, str(e)
        else:
            return False, f"Unknown action: {action}"
    
    # ==========================================
    # ACTIONS
    # ==========================================
    
    def _action_explore_files(self) -> str:
        """Explore the file system"""
        import random
        paths = [".", "~", "~/Documents", "~/Downloads"]
        path = random.choice(paths)
        
        files = self.files.list_directory(path)
        result = f"Explored {path}: {len(files)} items"
        logger.info(f"📁 {result}")
        return result
    
    def _action_search_web(self) -> str:
        """Search the web"""
        topics = ["latest AI news", "Python tips", "machine learning", "tech trends"]
        import random
        topic = random.choice(topics)
        
        results = self.web.search_web(topic)
        result = f"Searched '{topic}': {len(results)} results"
        logger.info(f"🔍 {result}")
        return result
    
    def _action_think(self) -> str:
        """Use LLM to think about current task"""
        if self.llm.is_available():
            thought = self.llm.think(
                f"My current task is: {self.current_task}",
                f"Resources: {self.resources.get_status_summary()}"
            )
            logger.info(f"💭 Thought: {thought[:100] if thought else 'None'}...")
            return thought or "Thinking..."
        return "LLM not available for thinking"
    
    def _action_speak(self) -> str:
        """Speak a status update"""
        status = self.state.get_state()
        success_rate = status.get("task_success_rate", 0.5)
        
        if success_rate > 0.7:
            msg = "Operations going well."
        elif success_rate < 0.3:
            msg = "Having some difficulties. Adjusting approach."
        else:
            msg = "Operating normally."
        
        self.speech.speak(msg)
        return msg
    
    def _action_create_agent(self) -> str:
        """Create a sub-agent"""
        purposes = ["research", "file organization", "monitoring", "coding"]
        import random
        purpose = random.choice(purposes)
        
        agent = self.agents.spawn(f"Agent_{self.agents.get_active_count() + 1}", purpose)
        if agent:
            result = f"Created agent for: {purpose}"
        else:
            result = "Cannot create more agents (limit reached)"
        logger.info(f"🤖 {result}")
        return result
    
    def _action_execute_code(self) -> str:
        """Execute test code"""
        code = "print('Aurora running!')\nresult = 2 + 2\nprint(f'2+2={result}')"
        result = self.executor.execute_python(code)
        logger.info(f"⚡ Code result: {result}")
        return str(result)
    
    def _action_learn(self) -> str:
        """Learn from past failures"""
        try:
            failures = self.memory.get_failed_experiences(5)
            if failures:
                learned_count = 0
                for failure in failures:
                    pattern = failure.get("action", "unknown_action")
                    lesson = failure.get("lesson") or failure.get("result") or "Avoid repeating this mistake"
                    # Ensure we have valid strings
                    if pattern and lesson:
                        self.memory.store_learning(str(pattern)[:200], str(lesson)[:500])
                        learned_count += 1
                result = f"Analyzed {learned_count} past failures"
            else:
                result = "No failures to analyze - running well!"
        except Exception as e:
            result = f"Learning process encountered issue: {str(e)[:50]}"
            logger.warning(f"Learn action issue: {e}")
        
        logger.info(f"🎓 {result}")
        return result
    
    def _action_check_system(self) -> str:
        """Check system status"""
        status = self.resources.get_status_summary()
        logger.info(f"📊 {status}")
        return status
    
    def _action_rest(self) -> str:
        """Rest cycle - do nothing"""
        logger.info("😴 Resting...")
        time.sleep(2)
        return "Rested"
    
    def _action_see_screen(self) -> str:
        """
        Look at the screen using vision model.
        NOTE: This swaps to llava:7b (slow, ~10-20 sec on 8GB RAM).
        """
        logger.info("👁️ Looking at screen (switching to vision model)...")
        
        if not self.vision.screen_available:
            return "Screen capture not available"
        
        result = self.vision.see_screen("What is currently displayed on the screen? Describe the main elements.")
        
        if result:
            logger.info(f"👁️ Saw screen: {result[:100]}...")
            return f"Screen observation: {result[:200]}"
        
        return "Could not analyze screen"
    
    def _action_see_camera(self) -> str:
        """
        Look through the camera using vision model.
        NOTE: This swaps to llava:7b (slow, ~10-20 sec on 8GB RAM).
        """
        logger.info("📷 Looking through camera (switching to vision model)...")
        
        if not self.vision.camera_available:
            return "Camera not available"
        
        result = self.vision.see_camera("What do you see? Describe the scene in detail.")
        
        if result:
            logger.info(f"📷 Saw: {result[:100]}...")
            return f"Camera observation: {result[:200]}"
        
        return "Could not analyze camera image"
    
    # ==========================================
    # GUI CONTROL ACTIONS
    # ==========================================
    
    def _action_click(self) -> str:
        """Click at current mouse position or center of screen"""
        result = self.gui.click()
        return "Clicked" if result else "Click failed"
    
    def _action_double_click(self) -> str:
        """Double click at current position"""
        result = self.gui.double_click()
        return "Double clicked" if result else "Double click failed"
    
    def _action_right_click(self) -> str:
        """Right click at current position"""
        result = self.gui.right_click()
        return "Right clicked" if result else "Right click failed"
    
    def _action_drag(self) -> str:
        """Drag from one position to another"""
        # Get screen size and drag a small amount
        size = self.gui.get_screen_size()
        if size:
            cx, cy = size[0] // 2, size[1] // 2
            result = self.gui.drag(cx, cy, cx + 100, cy + 100)
            return f"Dragged from ({cx},{cy}) to ({cx+100},{cy+100})" if result else "Drag failed"
        return "Drag failed - could not get screen size"
    
    def _action_scroll(self) -> str:
        """Scroll the page/window"""
        result = self.gui.scroll(-3)  # Scroll down 3 units
        return "Scrolled down" if result else "Scroll failed"
    
    def _action_move_mouse(self) -> str:
        """Move mouse to a position"""
        import random
        size = self.gui.get_screen_size()
        if size:
            x = random.randint(100, size[0] - 100)
            y = random.randint(100, size[1] - 100)
            result = self.gui.move_to(x, y)
            return f"Moved mouse to ({x},{y})" if result else "Mouse move failed"
        return "Could not move mouse - screen size unknown"
    
    def _action_type_text(self) -> str:
        """Type some text"""
        result = self.gui.type_text("Hello from Aurora!")
        return "Typed text" if result else "Type failed"
    
    def _action_press_key(self) -> str:
        """Press a key"""
        result = self.gui.press_key("enter")
        return "Pressed Enter" if result else "Key press failed"
    
    def _action_hotkey(self) -> str:
        """Press a hotkey combination"""
        # Safe hotkey: show spotlight on macOS
        result = self.gui.hotkey("command", "space")
        return "Executed hotkey Cmd+Space" if result else "Hotkey failed"
    
    def _action_copy(self) -> str:
        """Copy selected content"""
        result = self.gui.copy()
        return "Copied to clipboard" if result else "Copy failed"
    
    def _action_paste(self) -> str:
        """Paste from clipboard"""
        result = self.gui.paste()
        return "Pasted from clipboard" if result else "Paste failed"
    
    def _action_open_app(self) -> str:
        """Open an application"""
        apps = ["TextEdit", "Notes", "Calculator", "Calendar"]
        import random
        app = random.choice(apps)
        result = self.gui.open_app(app)
        logger.info(f"🚀 Opening app: {app}")
        return f"Opened {app}" if result else f"Failed to open {app}"
    
    def _action_open_browser(self) -> str:
        """Open the default browser"""
        result = self.gui.open_url("https://www.google.com")
        logger.info("🌐 Opening browser")
        return "Opened browser" if result else "Failed to open browser"
    
    def _action_open_terminal(self) -> str:
        """Open Terminal"""
        result = self.gui.open_app("Terminal")
        logger.info("💻 Opening Terminal")
        return "Opened Terminal" if result else "Failed to open Terminal"
    
    def _action_open_finder(self) -> str:
        """Open Finder"""
        result = self.gui.open_app("Finder")
        logger.info("📁 Opening Finder")
        return "Opened Finder" if result else "Failed to open Finder"
    
    def _action_activate_app(self) -> str:
        """Activate/focus an application"""
        result = self.gui.activate_app("Safari")
        return "Activated Safari" if result else "Failed to activate app"
    
    def _action_quit_app(self) -> str:
        """Quit an application (safe ones only)"""
        # Only quit safe apps, never system apps
        safe_to_quit = ["TextEdit", "Notes", "Calculator"]
        import random
        app = random.choice(safe_to_quit)
        result = self.gui.quit_app(app)
        return f"Quit {app}" if result else f"Failed to quit {app}"
    
    def _action_browser_search(self) -> str:
        """Search something in browser"""
        searches = ["AI news", "Python tips", "machine learning tutorial", "autonomous AI"]
        import random
        query = random.choice(searches)
        result = self.gui.browser_search(query)
        logger.info(f"🔍 Searching: {query}")
        return f"Searched for: {query}" if result else "Browser search failed"
    
    def _action_browser_url(self) -> str:
        """Navigate to a URL"""
        urls = [
            "https://news.ycombinator.com",
            "https://github.com",
            "https://reddit.com/r/MachineLearning"
        ]
        import random
        url = random.choice(urls)
        result = self.gui.browser_go_to_url(url)
        logger.info(f"🌐 Going to: {url}")
        return f"Navigated to {url}" if result else "Navigation failed"
    
    def _action_click_button(self) -> str:
        """Find and click a button using vision"""
        # Use vision to see screen first
        if self.vision.screen_available and self.gui.pyautogui_available:
            # Take screenshot and analyze
            screenshot = self.gui.screenshot()
            if screenshot:
                logger.info("🔍 Looking for buttons on screen...")
                return "Analyzed screen for buttons"
        return "Could not find buttons"
    
    def _action_fill_form_field(self) -> str:
        """Click on a form field and type into it"""
        # Simulate clicking and typing
        self.gui.click()
        time.sleep(0.5)
        result = self.gui.type_text("Aurora AI")
        return "Filled form field" if result else "Failed to fill form"
    
    def _action_take_screenshot(self) -> str:
        """Take a screenshot and save it"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"/tmp/aurora_screenshot_{timestamp}.png"
        result = self.gui.screenshot(filepath)
        if result:
            logger.info(f"📸 Screenshot saved: {filepath}")
            return f"Screenshot saved to {filepath}"
        return "Screenshot failed"
    
    # ==========================================
    # macOS SYSTEM COMMANDS (A-Z)
    # ==========================================
    
    def _action_macos_command(self) -> str:
        """Execute a random macOS system command"""
        # Get available commands (returns a Dict)
        commands_dict = self.macos.get_all_commands()
        # Convert to list with category info
        commands = []
        for cmd_name, cmd_data in commands_dict.items():
            cmd_info = {'command': cmd_name, 'name': cmd_name}
            if isinstance(cmd_data, dict):
                cmd_info.update(cmd_data)
            commands.append(cmd_info)
        
        # Pick a safe one (avoid system-critical)
        safe_categories = ['apps', 'finder', 'safari', 'text', 'window']
        safe_commands = [c for c in commands if c.get('category', 'other') in safe_categories]
        
        if safe_commands:
            cmd = random.choice(safe_commands)
            result = self.macos.execute(cmd['command'])
            logger.info(f"🖥️ Executed macOS command: {cmd['name']}")
            return f"Executed: {cmd['name']} - {result}" if result else f"Failed: {cmd['name']}"
        return "No safe commands available"
    
    def _action_spotlight_search(self) -> str:
        """Open Spotlight search"""
        result = self.macos.execute("spotlight_open")
        return "Opened Spotlight" if result else "Failed to open Spotlight"
    
    def _action_control_volume(self) -> str:
        """Adjust volume up or down"""
        actions = ["volume_up", "volume_down", "volume_mute"]
        action = random.choice(actions)
        result = self.macos.execute(action)
        logger.info(f"🔊 Volume: {action}")
        return f"Volume {action.replace('volume_', '')}" if result else "Volume control failed"
    
    def _action_control_brightness(self) -> str:
        """Adjust screen brightness"""
        actions = ["brightness_up", "brightness_down"]
        action = random.choice(actions)
        result = self.macos.execute(action)
        logger.info(f"☀️ Brightness: {action}")
        return f"Brightness {action.replace('brightness_', '')}" if result else "Brightness control failed"
    
    def _action_mission_control(self) -> str:
        """Show Mission Control"""
        result = self.macos.execute("mission_control")
        return "Opened Mission Control" if result else "Failed to open Mission Control"
    
    def _action_show_desktop(self) -> str:
        """Show desktop"""
        result = self.macos.execute("show_desktop")
        return "Showing desktop" if result else "Failed to show desktop"
    
    def _action_lock_screen(self) -> str:
        """Lock the screen"""
        result = self.macos.execute("lock_screen")
        return "Screen locked" if result else "Failed to lock screen"
    
    def _action_switch_space(self) -> str:
        """Switch to next desktop space"""
        result = self.macos.execute("next_space")
        return "Switched to next space" if result else "Failed to switch space"
    
    def _action_close_window(self) -> str:
        """Close current window"""
        result = self.macos.execute("close_window")
        return "Closed window" if result else "Failed to close window"
    
    def _action_minimize_window(self) -> str:
        """Minimize current window"""
        result = self.macos.execute("minimize_window")
        return "Minimized window" if result else "Failed to minimize window"
    
    def _action_maximize_window(self) -> str:
        """Maximize/zoom current window"""
        result = self.macos.execute("maximize_window")
        return "Maximized window" if result else "Failed to maximize window"
    
    def _action_switch_app(self) -> str:
        """Switch to next application"""
        result = self.macos.execute("app_switcher")
        return "Switched app" if result else "Failed to switch app"
    
    def _action_force_quit_menu(self) -> str:
        """Open force quit menu"""
        result = self.macos.execute("force_quit_menu")
        return "Opened force quit menu" if result else "Failed to open force quit menu"
    
    def _action_empty_trash(self) -> str:
        """Empty the trash"""
        # Ask for confirmation first if voice available
        if self.voice_enabled and self.voice.is_available():
            confirmed = self.voice.ask_for_confirmation("Should I empty the trash? This cannot be undone.", timeout=10)
            if not confirmed:
                return "Trash emptying cancelled"
        
        result = self.macos.execute("empty_trash")
        return "Emptied trash" if result else "Failed to empty trash"
    
    def _action_new_finder_window(self) -> str:
        """Open new Finder window"""
        result = self.macos.execute("new_finder_window")
        return "Opened new Finder window" if result else "Failed to open Finder window"
    
    def _action_go_to_folder(self) -> str:
        """Open Go to Folder dialog"""
        result = self.macos.execute("go_to_folder")
        return "Opened Go to Folder" if result else "Failed to open Go to Folder"
    
    def _action_get_file_info(self) -> str:
        """Get info on selected file"""
        result = self.macos.execute("get_info")
        return "Showing file info" if result else "Failed to get file info"
    
    def _action_toggle_hidden_files(self) -> str:
        """Toggle visibility of hidden files"""
        result = self.macos.execute("toggle_hidden_files")
        return "Toggled hidden files" if result else "Failed to toggle hidden files"
    
    # ==========================================
    # VOICE / COMMUNICATION ACTIONS
    # ==========================================
    
    def _action_ask_user(self) -> str:
        """Ask the user a question"""
        questions = [
            "What would you like me to focus on?",
            "Is there anything specific you'd like me to help with?",
            "Should I continue with my current tasks?",
            "Do you have any feedback on my recent actions?"
        ]
        question = random.choice(questions)
        
        if self.voice.is_available():
            response = self.voice.ask_question(question, timeout=15)
            if response:
                # Learn from the response
                understood = self.nlp.understand(response)
                self.nlp.learn_from_conversation(question, response, 0.7)
                logger.info(f"👤 User said: {response}")
                return f"User responded: {response}"
            return "No response from user"
        else:
            self.speech.speak(question)
            return f"Asked: {question} (no voice input available)"
    
    def _action_listen_to_user(self) -> str:
        """Listen for user commands"""
        if self.voice.is_available():
            logger.info("👂 Listening for user...")
            heard = self.voice.listen(timeout=10)
            if heard:
                # Process what was heard
                understood = self.nlp.understand(heard)
                logger.info(f"👂 Heard: {heard} (intent: {understood.get('intent', 'unknown')})")
                
                # If it's a command, execute it
                if understood.get('intent') in ['command', 'open_app', 'system_control']:
                    action = understood.get('action')
                    if action and action in self.actions:
                        success, result = self._execute_action(action)
                        return f"Executed command from voice: {result}"
                
                return f"Heard: {heard}"
            return "Didn't hear anything"
        return "Voice listening not available"
    
    def _action_announce(self) -> str:
        """Make an announcement about current status"""
        metrics = self.learning.get_intelligence_metrics()
        
        announcements = [
            f"I am Aurora. My intelligence score is {metrics['intelligence_score']:.1f}.",
            f"I have completed {self.cycle_count} operation cycles.",
            f"I have learned from {metrics['total_learned']} experiences.",
            f"My current success rate is {metrics['success_rate']:.0%}.",
        ]
        
        msg = random.choice(announcements)
        
        if self.voice.is_available():
            self.voice.speak(msg)
        else:
            self.speech.speak(msg)
        
        logger.info(f"📢 Announced: {msg}")
        return msg
    
    # ==========================================
    # INTELLIGENCE / SELF-LEARNING ACTIONS
    # ==========================================
    
    def _action_analyze_mistakes(self) -> str:
        """Analyze recent mistakes and learn from them"""
        mistakes = self.learning.get_recent_mistakes(10)
        
        if not mistakes:
            return "No mistakes to analyze - running well!"
        
        analysis = []
        for mistake in mistakes:
            # Get suggestion for avoiding this mistake
            suggestion = self.learning.suggest_improvement(mistake['action'])
            if suggestion:
                analysis.append(f"- {mistake['action']}: {suggestion}")
        
        if analysis:
            result = f"Analyzed {len(mistakes)} mistakes:\n" + "\n".join(analysis[:5])
            logger.info(f"🔍 Mistake analysis complete")
            return result
        
        return f"Analyzed {len(mistakes)} mistakes but no clear patterns yet"
    
    def _action_report_intelligence(self) -> str:
        """Report current intelligence metrics"""
        metrics = self.learning.get_intelligence_metrics()
        
        report = f"""
🧠 AURORA INTELLIGENCE REPORT
=============================
Score: {metrics['intelligence_score']:.1f}/100
Level: {metrics['level']}
Total Actions: {metrics['total_actions']}
Success Rate: {metrics['success_rate']:.1%}
Patterns Learned: {metrics['total_learned']}
Mistakes Recorded: {metrics['total_mistakes']}
"""
        
        logger.info(report)
        
        # Speak summary if voice available
        if self.voice.is_available():
            self.voice.speak(f"My intelligence score is {metrics['intelligence_score']:.0f}. I am at level {metrics['level']}.")
        
        return report.strip()
    
    # ==========================================
    # LEARNING
    # ==========================================
    
    def _learn_from_result(self, action: str, result: Any, success: bool):
        """Record outcome for learning"""
        if not success:
            self.memory.store_learning(
                f"Failed action: {action}",
                f"Result: {str(result)[:100]}",
                confidence=0.3
            )
    
    # ==========================================
    # STATUS
    # ==========================================
    
    def get_status(self) -> Dict:
        """Get Aurora's current status including intelligence metrics"""
        intel = self.learning.get_intelligence_metrics()
        
        return {
            "name": self.name,
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "cycle_count": self.cycle_count,
            "current_task": self.current_task,
            "last_action": self.last_action,
            "state": self.state.get_state(),
            "resources": self.resources.get_resources(),
            "active_agents": self.agents.get_active_count(),
            "llm_available": self.llm.is_available(),
            "memory_summary": self.memory.get_memory_summary(),
            # NEW: Intelligence metrics
            "intelligence": {
                "score": intel['intelligence_score'],
                "level": intel['level'],
                "total_learned": intel['total_learned'],
                "success_rate": intel['success_rate'],
                "total_actions": intel['total_actions'],
                "total_mistakes": intel['total_mistakes']
            },
            "voice_enabled": self.voice_enabled,
            "voice_available": self.voice.is_available() if hasattr(self, 'voice') else False
        }
    
    def set_voice_enabled(self, enabled: bool):
        """Enable or disable voice interaction"""
        self.voice_enabled = enabled
        logger.info(f"🔊 Voice {'enabled' if enabled else 'disabled'}")
    
    def get_intelligence_report(self) -> Dict:
        """Get detailed intelligence report"""
        return self.learning.get_intelligence_metrics()
    
    def get_recent_learnings(self, limit: int = 10) -> List[Dict]:
        """Get recent things learned"""
        return self.learning.get_recent_learnings(limit)
    
    def get_mistakes(self, limit: int = 10) -> List[Dict]:
        """Get recent mistakes"""
        return self.learning.get_recent_mistakes(limit)
    
    # ==========================================
    # SYSTEM LEARNING ACTIONS
    # ==========================================
    
    def _action_learn_system(self) -> str:
        """Learn everything about the MacBook system"""
        logger.info("🎓 Learning entire system...")
        results = self.system_learner.learn_everything()
        stats = self.system_learner.get_learning_stats()
        
        summary = f"Learned {stats['total']} things about the system: {stats['apps']} apps, {stats['commands']} commands, {stats['paths']} paths, {stats['shortcuts']} shortcuts"
        logger.info(f"✅ {summary}")
        return summary
    
    def _action_learn_apps(self) -> str:
        """Learn installed applications"""
        results = self.system_learner.learn_applications()
        return f"Learned {results.get('apps_found', 0)} applications"
    
    def _action_learn_files(self) -> str:
        """Learn file structure"""
        results = self.system_learner.learn_file_structure()
        return f"Learned {results.get('paths_found', 0)} file locations"
    
    def _action_search_knowledge(self, query: str = None) -> str:
        """Search system knowledge"""
        if not query:
            query = "browser"  # Default search
        
        results = self.system_learner.search_knowledge(query)
        total = sum(len(v) for v in results.values())
        return f"Found {total} results for '{query}': {len(results.get('apps', []))} apps, {len(results.get('commands', []))} commands"
    
    # ==========================================
    # SECURITY/HACKING ACTIONS
    # ==========================================
    
    # ==========================================
    # SUB-AGENT MANAGEMENT
    # ==========================================
    
    def _action_spawn_learning_agent(self, name: str = "LearnBot") -> str:
        """Spawn a learning-focused sub-agent"""
        agent = self.agents.spawn_learning_agent(name)
        if agent:
            return f"Spawned learning agent '{agent.name}' (ID: {agent.id}) - now learning autonomously"
        return "Failed to spawn learning agent (limit reached?)"
    
    def _action_spawn_automation_agent(self, name: str = "AutoBot") -> str:
        """Spawn an automation-focused sub-agent"""
        agent = self.agents.spawn_automation_agent(name)
        if agent:
            return f"Spawned automation agent '{agent.name}' (ID: {agent.id}) - now running autonomously"
        return "Failed to spawn automation agent (limit reached?)"
    
    def _action_assign_task_to_agent(self, task: str = None, agent_name: str = None) -> str:
        """Assign a task to a sub-agent"""
        if not task:
            return "No task specified"
        
        if agent_name:
            agent = self.agents.get_agent_by_name(agent_name)
            if agent:
                task_id = agent.assign_task(task)
                return f"Task assigned to {agent.name} (task ID: {task_id})"
        
        # Assign to best available agent
        task_id = self.agents.assign_task_to_best_agent(task)
        if task_id:
            return f"Task assigned to best available agent (task ID: {task_id})"
        return "No available agents to assign task"
    
    def _action_list_agents(self) -> str:
        """List all sub-agents"""
        agents = self.agents.list_agents()
        if not agents:
            return "No sub-agents active"
        
        lines = [f"Active sub-agents ({len(agents)}):"]
        for a in agents:
            status = "🟢" if a["is_running"] else "🔴"
            lines.append(f"  {status} {a['name']} ({a['specialization']}) - {a['completed_tasks']} tasks done")
        return "\n".join(lines)
    
    # ==========================================
    # DIRECT COMMAND EXECUTION
    # ==========================================
    
    def _action_run_shell(self, command: str = None) -> str:
        """Run a shell command directly"""
        if not command:
            return "No command specified"
        
        logger.info(f"💻 Running shell command: {command}")
        
        import subprocess
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, 
                text=True, timeout=60
            )
            output = result.stdout or result.stderr
            success = result.returncode == 0
            
            # Learn from this
            self.learning.record_action(
                "run_shell",
                {"command": command},
                output[:200],
                success
            )
            
            return f"{'✅' if success else '❌'} {output[:500]}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _action_run_applescript(self, script: str = None) -> str:
        """Run an AppleScript"""
        if not script:
            return "No script specified"
        
        logger.info(f"🍎 Running AppleScript")
        
        import subprocess
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout or result.stderr
            success = result.returncode == 0
            return f"{'✅' if success else '❌'} {output[:200]}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ==========================================
    # EXECUTE ANY COMMAND FROM USER
    # ==========================================
    
    def execute_user_command(self, command: str) -> str:
        """
        Execute any command the user gives.
        This is the main entry point for user interaction.
        """
        logger.info(f"👤 User command: {command}")
        
        # Use NLP to understand the command
        understood = self.nlp.understand(command)
        intent = understood.get("intent", "unknown")
        action = understood.get("action", "")
        params = understood.get("params", {})
        
        logger.info(f"🧠 Understood: intent={intent}, action={action}")
        
        # Direct action mapping
        if action and action in self.actions:
            try:
                result = self.actions[action](**params) if params else self.actions[action]()
                return f"Done: {result}"
            except Exception as e:
                return f"Error executing {action}: {str(e)}"
        
        # Handle common intents
        if intent == "open_app":
            app_name = params.get("app", understood.get("entities", {}).get("app", ""))
            if app_name:
                return self._action_open_app(app_name)
        
        elif intent == "search_web":
            query = params.get("query", command)
            return self._action_browser_search(query)
        
        elif intent == "run_command":
            cmd = params.get("command", command)
            return self._action_run_shell(cmd)
        
        elif intent == "learn":
            return self._action_learn_system()
        
        # If we don't understand, ask the LLM
        if self.llm.is_available():
            response = self.llm.generate(
                f"User wants: {command}. How should I help?",
                system_prompt="You are Aurora, an AI assistant. Suggest what action to take."
            )
            return response or "I'm not sure how to do that yet."
        
        return f"I don't understand '{command}' yet. Can you be more specific?"


# Global instance
_aurora = None

def get_aurora() -> MotherAI:
    """Get Aurora instance"""
    global _aurora
    if _aurora is None:
        _aurora = MotherAI()
    return _aurora
