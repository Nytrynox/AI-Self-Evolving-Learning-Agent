"""
SYSTEM LEARNER - Learn EVERYTHING About MacBook A-Z
===================================================
This module actively discovers, catalogs, and learns
everything about the user's MacBook system.

Learns:
- All installed applications
- System capabilities and specs
- File structure and locations
- User preferences and shortcuts
- Available commands and tools
- Network configuration
- Security settings
- Running services
- Keyboard shortcuts
- And much more...

ALL KNOWLEDGE IS PERSISTENT - survives restarts.
"""

import subprocess
import os
import json
import logging
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class SystemLearner:
    """
    Learns EVERYTHING about the MacBook system.
    All knowledge is stored permanently in a database.
    """
    
    def __init__(self):
        # Database path
        self.db_path = Path(__file__).parent / "memory" / "system_knowledge.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Thread lock
        self._db_lock = threading.Lock()
        
        # Initialize database
        self._init_database()
        
        # Cache frequently accessed data
        self._cache = {}
        self._cache_time = {}
        self._cache_ttl = 300  # 5 minutes
        
        # Learning progress
        self.categories_learned = []
        
        logger.info("📚 System Learner initialized")
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """Initialize knowledge database"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Applications table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        path TEXT,
                        bundle_id TEXT,
                        version TEXT,
                        category TEXT,
                        how_to_open TEXT,
                        last_used TEXT,
                        usage_count INTEGER DEFAULT 0,
                        discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # System info
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_info (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        category TEXT,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # File locations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS file_locations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT,
                        path TEXT UNIQUE,
                        type TEXT,
                        purpose TEXT,
                        discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Commands and tools
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS commands (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        path TEXT,
                        description TEXT,
                        category TEXT,
                        example_usage TEXT,
                        discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Keyboard shortcuts
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS shortcuts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        app TEXT,
                        keys TEXT,
                        action TEXT,
                        context TEXT,
                        UNIQUE(app, keys)
                    )
                """)
                
                # Network info
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS network_info (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # User preferences
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        source TEXT,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Services
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        label TEXT,
                        status TEXT,
                        path TEXT,
                        type TEXT,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("📚 System knowledge database initialized")
                
            finally:
                conn.close()
    
    # ==========================================
    # LEARN APPLICATIONS
    # ==========================================
    
    def learn_applications(self) -> Dict:
        """Learn all installed applications"""
        logger.info("📱 Learning installed applications...")
        
        apps_found = []
        
        # Scan /Applications
        apps_dirs = ["/Applications", os.path.expanduser("~/Applications")]
        
        for apps_dir in apps_dirs:
            if not os.path.exists(apps_dir):
                continue
                
            for item in os.listdir(apps_dir):
                if item.endswith('.app'):
                    app_path = os.path.join(apps_dir, item)
                    app_name = item.replace('.app', '')
                    
                    # Try to get bundle info
                    bundle_id = ""
                    version = ""
                    try:
                        plist_path = os.path.join(app_path, "Contents", "Info.plist")
                        if os.path.exists(plist_path):
                            result = subprocess.run(
                                ["defaults", "read", plist_path, "CFBundleIdentifier"],
                                capture_output=True, text=True
                            )
                            bundle_id = result.stdout.strip()
                            
                            result = subprocess.run(
                                ["defaults", "read", plist_path, "CFBundleShortVersionString"],
                                capture_output=True, text=True
                            )
                            version = result.stdout.strip()
                    except:
                        pass
                    
                    app_info = {
                        "name": app_name,
                        "path": app_path,
                        "bundle_id": bundle_id,
                        "version": version,
                        "how_to_open": f"open -a '{app_name}'"
                    }
                    apps_found.append(app_info)
                    
                    # Store in database
                    self._store_app(app_info)
        
        # Also learn command-line tools
        self._learn_cli_tools()
        
        self.categories_learned.append("applications")
        logger.info(f"✅ Learned {len(apps_found)} applications")
        
        return {"apps_found": len(apps_found), "apps": apps_found[:20]}
    
    def _store_app(self, app_info: Dict):
        """Store application in database"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO applications 
                    (name, path, bundle_id, version, how_to_open)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    app_info["name"],
                    app_info["path"],
                    app_info.get("bundle_id", ""),
                    app_info.get("version", ""),
                    app_info.get("how_to_open", "")
                ))
                conn.commit()
            finally:
                conn.close()
    
    def _learn_cli_tools(self):
        """Learn available command-line tools"""
        common_tools = [
            ("python3", "Python interpreter"),
            ("pip3", "Python package manager"),
            ("git", "Version control"),
            ("brew", "Homebrew package manager"),
            ("node", "Node.js runtime"),
            ("npm", "Node package manager"),
            ("docker", "Container platform"),
            ("code", "VS Code editor"),
            ("vim", "Text editor"),
            ("nano", "Text editor"),
            ("curl", "HTTP client"),
            ("wget", "File downloader"),
            ("ssh", "Secure shell"),
            ("scp", "Secure copy"),
            ("rsync", "File sync"),
            ("tmux", "Terminal multiplexer"),
            ("htop", "Process viewer"),
            ("nmap", "Network scanner"),
            ("ffmpeg", "Media processor"),
            ("imagemagick", "Image processor"),
        ]
        
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                for tool, desc in common_tools:
                    # Check if tool exists
                    result = subprocess.run(
                        ["which", tool],
                        capture_output=True, text=True
                    )
                    
                    if result.returncode == 0:
                        path = result.stdout.strip()
                        cursor.execute("""
                            INSERT OR REPLACE INTO commands 
                            (name, path, description, category)
                            VALUES (?, ?, ?, 'cli_tool')
                        """, (tool, path, desc))
                
                conn.commit()
            finally:
                conn.close()
    
    # ==========================================
    # LEARN SYSTEM INFO
    # ==========================================
    
    def learn_system_info(self) -> Dict:
        """Learn comprehensive system information"""
        logger.info("💻 Learning system information...")
        
        system_info = {}
        
        # macOS version
        result = subprocess.run(["sw_vers"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    system_info[key.strip()] = value.strip()
        
        # Hardware info
        result = subprocess.run(
            ["system_profiler", "SPHardwareDataType", "-json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                hw = data.get("SPHardwareDataType", [{}])[0]
                system_info["model_name"] = hw.get("machine_model", "")
                system_info["chip"] = hw.get("chip_type", hw.get("cpu_type", ""))
                system_info["memory"] = hw.get("physical_memory", "")
                system_info["serial"] = hw.get("serial_number", "")
            except:
                pass
        
        # Disk space
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                system_info["disk_total"] = parts[1] if len(parts) > 1 else ""
                system_info["disk_used"] = parts[2] if len(parts) > 2 else ""
                system_info["disk_free"] = parts[3] if len(parts) > 3 else ""
        
        # User info
        system_info["username"] = os.environ.get("USER", "")
        system_info["home_dir"] = os.path.expanduser("~")
        system_info["shell"] = os.environ.get("SHELL", "")
        
        # Screen resolution
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType", "-json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                displays = data.get("SPDisplaysDataType", [{}])[0].get("spdisplays_ndrvs", [])
                if displays:
                    system_info["display_resolution"] = displays[0].get("_spdisplays_resolution", "")
            except:
                pass
        
        # Store all info
        self._store_system_info(system_info)
        
        self.categories_learned.append("system_info")
        logger.info(f"✅ Learned {len(system_info)} system details")
        
        return system_info
    
    def _store_system_info(self, info: Dict):
        """Store system info in database"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                for key, value in info.items():
                    cursor.execute("""
                        INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
                        VALUES (?, ?, 'system', CURRENT_TIMESTAMP)
                    """, (key, str(value)))
                conn.commit()
            finally:
                conn.close()
    
    # ==========================================
    # LEARN FILE STRUCTURE
    # ==========================================
    
    def learn_file_structure(self) -> Dict:
        """Learn important file locations"""
        logger.info("📁 Learning file structure...")
        
        important_paths = [
            ("Home Directory", "~", "directory", "User's home folder"),
            ("Desktop", "~/Desktop", "directory", "Desktop files"),
            ("Documents", "~/Documents", "directory", "Document storage"),
            ("Downloads", "~/Downloads", "directory", "Downloaded files"),
            ("Pictures", "~/Pictures", "directory", "Image files"),
            ("Music", "~/Music", "directory", "Music files"),
            ("Movies", "~/Movies", "directory", "Video files"),
            ("Applications", "/Applications", "directory", "Installed apps"),
            ("Library", "~/Library", "directory", "User library"),
            ("Preferences", "~/Library/Preferences", "directory", "App preferences"),
            ("Caches", "~/Library/Caches", "directory", "App caches"),
            ("Logs", "~/Library/Logs", "directory", "App logs"),
            ("SSH Keys", "~/.ssh", "directory", "SSH configuration"),
            ("Git Config", "~/.gitconfig", "file", "Git configuration"),
            ("Bash Profile", "~/.bash_profile", "file", "Bash settings"),
            ("Zsh Config", "~/.zshrc", "file", "Zsh settings"),
            ("Trash", "~/.Trash", "directory", "Deleted files"),
        ]
        
        found_paths = []
        
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                for desc, path, ptype, purpose in important_paths:
                    expanded = os.path.expanduser(path)
                    if os.path.exists(expanded):
                        cursor.execute("""
                            INSERT OR REPLACE INTO file_locations 
                            (description, path, type, purpose)
                            VALUES (?, ?, ?, ?)
                        """, (desc, expanded, ptype, purpose))
                        found_paths.append({"desc": desc, "path": expanded})
                
                conn.commit()
            finally:
                conn.close()
        
        self.categories_learned.append("file_structure")
        logger.info(f"✅ Learned {len(found_paths)} file locations")
        
        return {"paths_found": len(found_paths), "paths": found_paths}
    
    # ==========================================
    # LEARN NETWORK
    # ==========================================
    
    def learn_network(self) -> Dict:
        """Learn network configuration"""
        logger.info("🌐 Learning network configuration...")
        
        network_info = {}
        
        # Current WiFi
        result = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    network_info[f"wifi_{key.strip()}"] = value.strip()
        
        # IP addresses
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        if result.returncode == 0:
            import re
            ips = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
            network_info["ip_addresses"] = json.dumps(ips)
        
        # DNS servers
        result = subprocess.run(["cat", "/etc/resolv.conf"], capture_output=True, text=True)
        if result.returncode == 0:
            import re
            dns = re.findall(r'nameserver (\S+)', result.stdout)
            network_info["dns_servers"] = json.dumps(dns)
        
        # Hostname
        result = subprocess.run(["hostname"], capture_output=True, text=True)
        network_info["hostname"] = result.stdout.strip()
        
        # External IP
        try:
            result = subprocess.run(
                ["curl", "-s", "ifconfig.me"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                network_info["external_ip"] = result.stdout.strip()
        except:
            pass
        
        # Store network info
        self._store_network_info(network_info)
        
        self.categories_learned.append("network")
        logger.info(f"✅ Learned {len(network_info)} network details")
        
        return network_info
    
    def _store_network_info(self, info: Dict):
        """Store network info"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                for key, value in info.items():
                    cursor.execute("""
                        INSERT OR REPLACE INTO network_info (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    """, (key, str(value)))
                conn.commit()
            finally:
                conn.close()
    
    # ==========================================
    # LEARN SHORTCUTS
    # ==========================================
    
    def learn_shortcuts(self) -> Dict:
        """Learn system and app keyboard shortcuts"""
        logger.info("⌨️ Learning keyboard shortcuts...")
        
        # Common macOS shortcuts
        shortcuts = [
            ("System", "Cmd+Space", "Spotlight Search", "global"),
            ("System", "Cmd+Tab", "Switch Applications", "global"),
            ("System", "Cmd+Q", "Quit Application", "global"),
            ("System", "Cmd+W", "Close Window", "global"),
            ("System", "Cmd+N", "New Window/Document", "global"),
            ("System", "Cmd+O", "Open File", "global"),
            ("System", "Cmd+S", "Save", "global"),
            ("System", "Cmd+Z", "Undo", "global"),
            ("System", "Cmd+Shift+Z", "Redo", "global"),
            ("System", "Cmd+C", "Copy", "global"),
            ("System", "Cmd+V", "Paste", "global"),
            ("System", "Cmd+X", "Cut", "global"),
            ("System", "Cmd+A", "Select All", "global"),
            ("System", "Cmd+F", "Find", "global"),
            ("System", "Cmd+,", "Open Preferences", "global"),
            ("System", "Cmd+H", "Hide Application", "global"),
            ("System", "Cmd+M", "Minimize Window", "global"),
            ("System", "Cmd+Shift+3", "Screenshot Full Screen", "global"),
            ("System", "Cmd+Shift+4", "Screenshot Selection", "global"),
            ("System", "Cmd+Shift+5", "Screenshot Options", "global"),
            ("System", "Ctrl+Cmd+Q", "Lock Screen", "global"),
            ("System", "Cmd+Option+Esc", "Force Quit Menu", "global"),
            ("System", "F11", "Show Desktop", "global"),
            ("System", "Ctrl+Up", "Mission Control", "global"),
            ("System", "Ctrl+Down", "App Windows", "global"),
            ("Finder", "Cmd+Shift+G", "Go to Folder", "finder"),
            ("Finder", "Cmd+Shift+.", "Toggle Hidden Files", "finder"),
            ("Finder", "Cmd+Delete", "Move to Trash", "finder"),
            ("Finder", "Cmd+Shift+Delete", "Empty Trash", "finder"),
            ("Terminal", "Cmd+T", "New Tab", "terminal"),
            ("Terminal", "Cmd+K", "Clear Screen", "terminal"),
            ("Terminal", "Ctrl+C", "Cancel Command", "terminal"),
            ("Terminal", "Ctrl+D", "Exit/EOF", "terminal"),
            ("Safari", "Cmd+T", "New Tab", "browser"),
            ("Safari", "Cmd+L", "Focus URL Bar", "browser"),
            ("Safari", "Cmd+R", "Reload Page", "browser"),
            ("Chrome", "Cmd+T", "New Tab", "browser"),
            ("Chrome", "Cmd+L", "Focus URL Bar", "browser"),
            ("Chrome", "Cmd+Shift+T", "Reopen Closed Tab", "browser"),
        ]
        
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                for app, keys, action, context in shortcuts:
                    cursor.execute("""
                        INSERT OR REPLACE INTO shortcuts (app, keys, action, context)
                        VALUES (?, ?, ?, ?)
                    """, (app, keys, action, context))
                conn.commit()
            finally:
                conn.close()
        
        self.categories_learned.append("shortcuts")
        logger.info(f"✅ Learned {len(shortcuts)} keyboard shortcuts")
        
        return {"shortcuts_count": len(shortcuts)}
    
    # ==========================================
    # LEARN SERVICES
    # ==========================================
    
    def learn_services(self) -> Dict:
        """Learn running services and daemons"""
        logger.info("⚙️ Learning system services...")
        
        services = []
        
        # LaunchAgents (user)
        launch_agents = os.path.expanduser("~/Library/LaunchAgents")
        if os.path.exists(launch_agents):
            for item in os.listdir(launch_agents):
                if item.endswith('.plist'):
                    services.append({
                        "name": item.replace('.plist', ''),
                        "type": "user_agent",
                        "path": os.path.join(launch_agents, item)
                    })
        
        # System LaunchDaemons
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n')[1:]:
                parts = line.split('\t')
                if len(parts) >= 3:
                    services.append({
                        "name": parts[2],
                        "type": "daemon",
                        "status": "running" if parts[0] != "-" else "stopped"
                    })
        
        # Store services (first 100)
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                for svc in services[:100]:
                    cursor.execute("""
                        INSERT OR REPLACE INTO services 
                        (name, type, status, path, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (
                        svc["name"],
                        svc.get("type", ""),
                        svc.get("status", "unknown"),
                        svc.get("path", "")
                    ))
                conn.commit()
            finally:
                conn.close()
        
        self.categories_learned.append("services")
        logger.info(f"✅ Learned {len(services)} services")
        
        return {"services_count": len(services), "services": services[:20]}
    
    # ==========================================
    # LEARN EVERYTHING
    # ==========================================
    
    def learn_everything(self) -> Dict:
        """Run complete system learning"""
        logger.info("🎓 Starting comprehensive system learning...")
        
        results = {}
        
        results["applications"] = self.learn_applications()
        results["system_info"] = self.learn_system_info()
        results["file_structure"] = self.learn_file_structure()
        results["network"] = self.learn_network()
        results["shortcuts"] = self.learn_shortcuts()
        results["services"] = self.learn_services()
        
        logger.info("✅ Complete system learning finished!")
        
        return results
    
    # ==========================================
    # QUERY KNOWLEDGE
    # ==========================================
    
    def get_app(self, name: str) -> Optional[Dict]:
        """Get info about an application"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM applications WHERE name LIKE ?",
                    (f"%{name}%",)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
            finally:
                conn.close()
        return None
    
    def get_all_apps(self) -> List[str]:
        """Get list of all known apps"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM applications ORDER BY name")
                return [row["name"] for row in cursor.fetchall()]
            finally:
                conn.close()
    
    def get_system_value(self, key: str) -> Optional[str]:
        """Get a system info value"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM system_info WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return row["value"]
            finally:
                conn.close()
        return None
    
    def get_path(self, description: str) -> Optional[str]:
        """Get a file path by description"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT path FROM file_locations WHERE description LIKE ?",
                    (f"%{description}%",)
                )
                row = cursor.fetchone()
                if row:
                    return row["path"]
            finally:
                conn.close()
        return None
    
    def get_shortcut(self, action: str) -> Optional[str]:
        """Get keyboard shortcut for an action"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT keys FROM shortcuts WHERE action LIKE ?",
                    (f"%{action}%",)
                )
                row = cursor.fetchone()
                if row:
                    return row["keys"]
            finally:
                conn.close()
        return None
    
    def get_command(self, name: str) -> Optional[Dict]:
        """Get info about a command"""
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM commands WHERE name LIKE ?",
                    (f"%{name}%",)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
            finally:
                conn.close()
        return None
    
    def search_knowledge(self, query: str) -> Dict:
        """Search across all knowledge"""
        results = {
            "apps": [],
            "commands": [],
            "paths": [],
            "shortcuts": []
        }
        
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Search apps
                cursor.execute(
                    "SELECT name, path FROM applications WHERE name LIKE ?",
                    (f"%{query}%",)
                )
                results["apps"] = [dict(r) for r in cursor.fetchall()]
                
                # Search commands
                cursor.execute(
                    "SELECT name, description FROM commands WHERE name LIKE ? OR description LIKE ?",
                    (f"%{query}%", f"%{query}%")
                )
                results["commands"] = [dict(r) for r in cursor.fetchall()]
                
                # Search paths
                cursor.execute(
                    "SELECT description, path FROM file_locations WHERE description LIKE ?",
                    (f"%{query}%",)
                )
                results["paths"] = [dict(r) for r in cursor.fetchall()]
                
                # Search shortcuts
                cursor.execute(
                    "SELECT app, keys, action FROM shortcuts WHERE action LIKE ?",
                    (f"%{query}%",)
                )
                results["shortcuts"] = [dict(r) for r in cursor.fetchall()]
                
            finally:
                conn.close()
        
        return results
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learned knowledge"""
        stats = {}
        
        with self._db_lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM applications")
                stats["apps"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM commands")
                stats["commands"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM file_locations")
                stats["paths"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM shortcuts")
                stats["shortcuts"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM services")
                stats["services"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM system_info")
                stats["system_info"] = cursor.fetchone()[0]
                
            finally:
                conn.close()
        
        stats["total"] = sum(stats.values())
        stats["categories_learned"] = self.categories_learned
        
        return stats


# Global instance
_learner = None

def get_system_learner() -> SystemLearner:
    """Get system learner instance"""
    global _learner
    if _learner is None:
        _learner = SystemLearner()
    return _learner
