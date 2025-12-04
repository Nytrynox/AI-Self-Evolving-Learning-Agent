"""
SYSTEM MONITOR - Track System Resources
======================================
Monitors RAM, CPU, disk, and processes.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SystemMonitor:
    """
    Monitor system resources.
    """
    
    def __init__(self):
        try:
            import psutil
            self.psutil = psutil
            self.available = True
            logger.info("📊 System Monitor initialized")
        except ImportError:
            logger.warning("⚠️ psutil not available - monitoring disabled")
            self.psutil = None
            self.available = False
    
    def get_ram_usage(self) -> Dict:
        """Get RAM usage"""
        if not self.available:
            return {"error": "monitoring unavailable"}
        
        mem = self.psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent_used": mem.percent
        }
    
    def get_cpu_usage(self) -> Dict:
        """Get CPU usage"""
        if not self.available:
            return {"error": "monitoring unavailable"}
        
        return {
            "percent": self.psutil.cpu_percent(interval=1),
            "cores": self.psutil.cpu_count()
        }
    
    def get_disk_usage(self, path: str = "/") -> Dict:
        """Get disk usage"""
        if not self.available:
            return {"error": "monitoring unavailable"}
        
        disk = self.psutil.disk_usage(path)
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "percent_used": round(disk.percent, 1)
        }
    
    def get_running_processes(self, limit: int = 10) -> List[Dict]:
        """Get top processes by memory"""
        if not self.available:
            return []
        
        processes = []
        for proc in self.psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                pass
        
        # Sort by memory and return top N
        processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
        return processes[:limit]
    
    def is_ollama_running(self) -> bool:
        """Check if Ollama is running"""
        if not self.available:
            return False
        
        for proc in self.psutil.process_iter(['name']):
            try:
                if 'ollama' in proc.info['name'].lower():
                    return True
            except:
                pass
        return False
    
    def can_load_model(self, required_ram_gb: float = 4.0) -> bool:
        """Check if there's enough RAM to load a model"""
        ram = self.get_ram_usage()
        if "error" in ram:
            return False
        
        available = ram["available_gb"]
        return available >= required_ram_gb
    
    def get_full_status(self) -> Dict:
        """Get complete system status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "ram": self.get_ram_usage(),
            "cpu": self.get_cpu_usage(),
            "disk": self.get_disk_usage(),
            "ollama_running": self.is_ollama_running()
        }


# Global instance
_monitor = None

def get_system_monitor() -> SystemMonitor:
    """Get system monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = SystemMonitor()
    return _monitor
