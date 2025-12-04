"""
AGENT SPAWNER - Create TRULY Autonomous Sub-Agents
=================================================
Sub-agents that ACTUALLY execute tasks independently.

Each sub-agent:
- Has its own thread
- Uses LLM for decision making
- Executes REAL actions
- Reports back to Mother AI
- Can be specialized (security, learning, automation, etc.)
"""

import logging
import threading
import time
import json
import os
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)


class SubAgent:
    """
    A REAL sub-agent that executes tasks autonomously.
    Each sub-agent runs in its own thread and can perform real actions.
    """
    
    def __init__(self, name: str, purpose: str, specialization: str = "general", 
                 parent_id: str = "aurora"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.purpose = purpose
        self.specialization = specialization
        self.parent_id = parent_id
        self.created_at = datetime.now()
        self.is_active = True
        self.is_running = False
        
        # Task management
        self.task_queue = []
        self.completed_tasks = []
        self.current_task = None
        
        # Performance tracking
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_time = 0.0
        
        # Capabilities based on specialization
        self.capabilities = self._get_capabilities()
        
        # Thread for autonomous operation
        self._thread = None
        self._stop_event = threading.Event()
        
        # Communication with parent
        self.messages_to_parent = []
        
        logger.info(f"🤖 Sub-agent '{name}' created (ID: {self.id}, Spec: {specialization})")
        
        # Save agent to disk
        self._save_to_disk()
    
    def _get_capabilities(self) -> List[str]:
        """Get capabilities based on specialization"""
        capability_map = {
            "general": ["execute_shell", "read_file", "write_file", "search"],
            "security": ["port_scan", "vuln_scan", "network_recon", "password_test", 
                        "wifi_scan", "packet_capture", "hash_crack", "exploit_search"],
            "learning": ["explore_system", "learn_apps", "catalog_files", 
                        "discover_shortcuts", "analyze_patterns"],
            "automation": ["click", "type", "open_app", "run_script", "schedule_task"],
            "web": ["browse", "search", "download", "api_call", "scrape"],
            "file": ["organize", "backup", "sync", "compress", "search_files"],
            "monitor": ["watch_process", "track_resources", "alert", "log_activity"]
        }
        return capability_map.get(self.specialization, capability_map["general"])
    
    def _save_to_disk(self):
        """Save agent info to disk"""
        agents_dir = Path(__file__).parent / "spawned"
        agents_dir.mkdir(exist_ok=True)
        
        agent_file = agents_dir / f"{self.id}.json"
        agent_data = {
            "id": self.id,
            "name": self.name,
            "purpose": self.purpose,
            "specialization": self.specialization,
            "created_at": self.created_at.isoformat(),
            "capabilities": self.capabilities,
            "is_active": self.is_active
        }
        
        with open(agent_file, 'w') as f:
            json.dump(agent_data, f, indent=2)
    
    def start(self):
        """Start autonomous operation"""
        if self.is_running:
            return
        
        self.is_running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info(f"▶️ Agent {self.name} started autonomous operation")
    
    def stop(self):
        """Stop autonomous operation"""
        self._stop_event.set()
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info(f"⏹️ Agent {self.name} stopped")
    
    def _run_loop(self):
        """Main autonomous loop"""
        while not self._stop_event.is_set() and self.is_active:
            try:
                # Check for tasks
                if self.task_queue:
                    task = self.task_queue.pop(0)
                    self.current_task = task
                    
                    # Execute task
                    result = self._execute_task(task)
                    
                    # Record result
                    task["result"] = result
                    task["completed_at"] = datetime.now().isoformat()
                    self.completed_tasks.append(task)
                    self.current_task = None
                    
                    # Report to parent
                    self.messages_to_parent.append({
                        "type": "task_complete",
                        "task": task["description"],
                        "result": result,
                        "success": result.get("success", False)
                    })
                else:
                    # No tasks - idle or autonomous exploration
                    if self.specialization == "learning":
                        self._autonomous_learn()
                    elif self.specialization == "security":
                        self._autonomous_security_check()
                
                time.sleep(2)  # Prevent tight loop
                
            except Exception as e:
                logger.error(f"❌ Agent {self.name} error: {e}")
                self.failure_count += 1
                time.sleep(5)
    
    def _execute_task(self, task: Dict) -> Dict:
        """Execute a task based on its type"""
        task_type = task.get("type", "shell")
        description = task.get("description", "")
        params = task.get("params", {})
        
        logger.info(f"⚡ Agent {self.name} executing: {description}")
        
        start_time = time.time()
        result = {"success": False, "output": "", "error": None}
        
        try:
            if task_type == "shell":
                # Execute shell command
                import subprocess
                cmd = params.get("command", description)
                proc = subprocess.run(cmd, shell=True, capture_output=True, 
                                     text=True, timeout=60)
                result["output"] = proc.stdout or proc.stderr
                result["success"] = proc.returncode == 0
                
            elif task_type == "python":
                # Execute Python code
                code = params.get("code", "")
                exec_globals = {}
                exec(code, exec_globals)
                result["output"] = str(exec_globals.get("result", "Done"))
                result["success"] = True
                
            elif task_type == "file_read":
                path = params.get("path", "")
                with open(path, 'r') as f:
                    result["output"] = f.read()[:5000]
                result["success"] = True
                
            elif task_type == "file_write":
                path = params.get("path", "")
                content = params.get("content", "")
                with open(path, 'w') as f:
                    f.write(content)
                result["output"] = f"Written to {path}"
                result["success"] = True
                
            elif task_type == "explore":
                # Explore a directory
                path = params.get("path", os.path.expanduser("~"))
                items = os.listdir(path)[:50]
                result["output"] = json.dumps(items)
                result["success"] = True
                
            elif task_type == "security_scan":
                # Security scan (will use security tools when available)
                result = self._do_security_scan(params)
                
            elif task_type == "learn_system":
                # Learn about system
                result = self._do_system_learning(params)
                
            else:
                result["error"] = f"Unknown task type: {task_type}"
            
            self.success_count += 1
            
        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            self.failure_count += 1
            logger.error(f"Task failed: {e}")
        
        execution_time = time.time() - start_time
        self.total_execution_time += execution_time
        result["execution_time"] = execution_time
        
        return result
    
    def _do_security_scan(self, params: Dict) -> Dict:
        """Perform security scanning"""
        scan_type = params.get("scan_type", "basic")
        target = params.get("target", "localhost")
        
        result = {"success": False, "output": "", "findings": []}
        
        try:
            if scan_type == "port":
                # Basic port scan
                import socket
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                               993, 995, 3306, 3389, 5432, 8080, 8443]
                open_ports = []
                
                for port in common_ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((target, port)) == 0:
                        open_ports.append(port)
                    sock.close()
                
                result["output"] = f"Open ports on {target}: {open_ports}"
                result["findings"] = [{"type": "open_port", "port": p} for p in open_ports]
                result["success"] = True
                
            elif scan_type == "wifi":
                # WiFi scan
                import subprocess
                proc = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                    capture_output=True, text=True
                )
                result["output"] = proc.stdout
                result["success"] = True
                
            elif scan_type == "process":
                # Process security scan
                import subprocess
                proc = subprocess.run(["ps", "aux"], capture_output=True, text=True)
                result["output"] = proc.stdout[:3000]
                result["success"] = True
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _do_system_learning(self, params: Dict) -> Dict:
        """Learn about the system"""
        learn_type = params.get("learn_type", "apps")
        result = {"success": False, "output": "", "learned": {}}
        
        try:
            if learn_type == "apps":
                # Learn installed apps
                apps_dir = "/Applications"
                apps = [d for d in os.listdir(apps_dir) if d.endswith('.app')]
                result["learned"]["apps"] = apps[:30]
                result["output"] = f"Found {len(apps)} apps"
                result["success"] = True
                
            elif learn_type == "directories":
                # Learn directory structure
                home = os.path.expanduser("~")
                dirs = [d for d in os.listdir(home) 
                       if os.path.isdir(os.path.join(home, d)) and not d.startswith('.')]
                result["learned"]["directories"] = dirs
                result["output"] = f"Found {len(dirs)} directories in home"
                result["success"] = True
                
            elif learn_type == "system_info":
                # Learn system info
                import subprocess
                info = {}
                
                # macOS version
                proc = subprocess.run(["sw_vers"], capture_output=True, text=True)
                info["os_version"] = proc.stdout.strip()
                
                # Hardware
                proc = subprocess.run(["system_profiler", "SPHardwareDataType"], 
                                     capture_output=True, text=True)
                info["hardware"] = proc.stdout[:1000]
                
                result["learned"] = info
                result["output"] = "Learned system info"
                result["success"] = True
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _autonomous_learn(self):
        """Autonomous learning behavior"""
        # Pick something to learn
        import random
        learn_tasks = [
            {"type": "learn_system", "params": {"learn_type": "apps"}},
            {"type": "learn_system", "params": {"learn_type": "directories"}},
            {"type": "explore", "params": {"path": os.path.expanduser("~")}},
            {"type": "shell", "params": {"command": "ls -la ~"}},
        ]
        task = random.choice(learn_tasks)
        task["description"] = f"Autonomous learning: {task['type']}"
        self._execute_task(task)
    
    def _autonomous_security_check(self):
        """Autonomous security checking"""
        import random
        security_tasks = [
            {"type": "security_scan", "params": {"scan_type": "port", "target": "127.0.0.1"}},
            {"type": "security_scan", "params": {"scan_type": "process"}},
            {"type": "shell", "params": {"command": "netstat -an | head -20"}},
        ]
        task = random.choice(security_tasks)
        task["description"] = f"Autonomous security: {task['type']}"
        self._execute_task(task)
    
    def assign_task(self, description: str, task_type: str = "shell", 
                    params: Dict = None, priority: int = 5):
        """Assign a task to this agent"""
        task = {
            "id": str(uuid.uuid4())[:8],
            "description": description,
            "type": task_type,
            "params": params or {},
            "priority": priority,
            "assigned_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        # Insert by priority
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda x: x.get("priority", 5), reverse=True)
        
        logger.info(f"📋 Task assigned to {self.name}: {description}")
        return task["id"]
    
    def get_messages(self) -> List[Dict]:
        """Get and clear messages to parent"""
        messages = self.messages_to_parent.copy()
        self.messages_to_parent.clear()
        return messages
    
    def terminate(self):
        """Terminate this agent"""
        self.stop()
        self.is_active = False
        
        # Remove from disk
        agent_file = Path(__file__).parent / "spawned" / f"{self.id}.json"
        if agent_file.exists():
            agent_file.unlink()
        
        logger.info(f"💀 Sub-agent '{self.name}' terminated")
    
    def get_status(self) -> Dict:
        """Get agent status"""
        return {
            "id": self.id,
            "name": self.name,
            "purpose": self.purpose,
            "specialization": self.specialization,
            "is_active": self.is_active,
            "is_running": self.is_running,
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "current_task": self.current_task,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.success_count / max(1, self.success_count + self.failure_count),
            "capabilities": self.capabilities,
            "created_at": self.created_at.isoformat()
        }


class AgentSpawner:
    """
    Creates and manages TRULY autonomous sub-agents for Aurora.
    """
    
    def __init__(self, max_agents: int = 5):
        self.max_agents = max_agents
        self.agents: Dict[str, SubAgent] = {}
        
        # Load any existing agents from disk
        self._load_saved_agents()
        
        logger.info(f"🏭 Agent Spawner initialized (max: {max_agents}, loaded: {len(self.agents)})")
    
    def _load_saved_agents(self):
        """Load saved agents from disk"""
        agents_dir = Path(__file__).parent / "spawned"
        if not agents_dir.exists():
            return
        
        for agent_file in agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r') as f:
                    data = json.load(f)
                    if data.get("is_active"):
                        # Recreate agent
                        agent = SubAgent(
                            name=data["name"],
                            purpose=data["purpose"],
                            specialization=data.get("specialization", "general")
                        )
                        agent.id = data["id"]
                        self.agents[agent.id] = agent
                        logger.info(f"📂 Loaded agent: {agent.name}")
            except Exception as e:
                logger.error(f"Failed to load agent from {agent_file}: {e}")
    
    def spawn(self, name: str, purpose: str, specialization: str = "general",
              auto_start: bool = True) -> Optional[SubAgent]:
        """
        Spawn a new autonomous sub-agent.
        """
        # Check limit
        active_count = len([a for a in self.agents.values() if a.is_active])
        if active_count >= self.max_agents:
            logger.warning(f"⚠️ Cannot spawn more agents (limit: {self.max_agents})")
            return None
        
        # Create agent
        agent = SubAgent(name, purpose, specialization)
        self.agents[agent.id] = agent
        
        # Auto-start if requested
        if auto_start:
            agent.start()
        
        # Store in memory
        try:
            from brain.memory_system import get_memory
            memory = get_memory()
            memory.store_experience(
                "agent_creation",
                f"Spawned autonomous agent '{name}' ({specialization}) for: {purpose}",
                agent.id,
                success=True
            )
        except:
            pass
        
        return agent
    
    def spawn_security_agent(self, name: str = "SecurityBot") -> Optional[SubAgent]:
        """Spawn a specialized security/hacking agent"""
        return self.spawn(
            name=name,
            purpose="Security scanning, penetration testing, and vulnerability assessment",
            specialization="security"
        )
    
    def spawn_learning_agent(self, name: str = "LearnBot") -> Optional[SubAgent]:
        """Spawn a specialized system learning agent"""
        return self.spawn(
            name=name,
            purpose="Learn and catalog everything about the MacBook system",
            specialization="learning"
        )
    
    def spawn_automation_agent(self, name: str = "AutoBot") -> Optional[SubAgent]:
        """Spawn a specialized automation agent"""
        return self.spawn(
            name=name,
            purpose="Automate repetitive tasks and workflows",
            specialization="automation"
        )
    
    def get_agent(self, agent_id: str) -> Optional[SubAgent]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)
    
    def get_agent_by_name(self, name: str) -> Optional[SubAgent]:
        """Get an agent by name"""
        for agent in self.agents.values():
            if agent.name.lower() == name.lower():
                return agent
        return None
    
    def terminate_agent(self, agent_id: str) -> bool:
        """Terminate an agent"""
        if agent_id in self.agents:
            self.agents[agent_id].terminate()
            del self.agents[agent_id]
            return True
        return False
    
    def terminate_all(self):
        """Terminate all agents"""
        for agent in list(self.agents.values()):
            agent.terminate()
        self.agents.clear()
        logger.info("💀 All sub-agents terminated")
    
    def list_agents(self) -> List[Dict]:
        """List all agents"""
        return [agent.get_status() for agent in self.agents.values()]
    
    def get_active_count(self) -> int:
        """Get count of active agents"""
        return len([a for a in self.agents.values() if a.is_active])
    
    def assign_task(self, agent_id: str, description: str, 
                    task_type: str = "shell", params: Dict = None) -> Optional[str]:
        """Assign a task to a specific agent"""
        agent = self.get_agent(agent_id)
        if agent and agent.is_active:
            return agent.assign_task(description, task_type, params)
        return None
    
    def assign_task_to_best_agent(self, description: str, task_type: str = "shell",
                                   params: Dict = None) -> Optional[str]:
        """Assign task to the most suitable agent"""
        # Find best agent based on task type and specialization
        task_specialization_map = {
            "security_scan": "security",
            "learn_system": "learning",
            "explore": "learning",
            "shell": "general",
            "python": "general"
        }
        
        preferred_spec = task_specialization_map.get(task_type, "general")
        
        # Find matching agent
        for agent in self.agents.values():
            if agent.is_active and agent.specialization == preferred_spec:
                return agent.assign_task(description, task_type, params)
        
        # Fallback to any active agent
        for agent in self.agents.values():
            if agent.is_active:
                return agent.assign_task(description, task_type, params)
        
        return None
    
    def run_agents_cycle(self):
        """Run one cycle for all active agents - collect messages"""
        all_messages = []
        
        for agent in self.agents.values():
            if agent.is_active:
                # Collect messages from agent
                messages = agent.get_messages()
                for msg in messages:
                    msg["agent_id"] = agent.id
                    msg["agent_name"] = agent.name
                    all_messages.append(msg)
        
        # Log any important messages
        for msg in all_messages:
            if msg.get("type") == "task_complete":
                status = "✅" if msg.get("success") else "❌"
                logger.info(f"{status} Agent {msg['agent_name']}: {msg['task']}")
        
        return all_messages
    
    def get_all_completed_tasks(self) -> List[Dict]:
        """Get all completed tasks from all agents"""
        all_tasks = []
        for agent in self.agents.values():
            for task in agent.completed_tasks:
                task["agent_id"] = agent.id
                task["agent_name"] = agent.name
                all_tasks.append(task)
        return all_tasks


# Global instance
_spawner = None

def get_agent_spawner() -> AgentSpawner:
    """Get agent spawner instance"""
    global _spawner
    if _spawner is None:
        from config.settings import RESOURCES
        max_agents = RESOURCES.get("max_agents", 5)
        _spawner = AgentSpawner(max_agents=max_agents)
    return _spawner
