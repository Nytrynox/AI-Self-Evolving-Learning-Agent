"""
RESOURCE TRACKER - System Resource Monitoring
==============================================
Tracks and manages system resources for Aurora.
No fake "energy" or "soul" - just real resource monitoring.
"""

import logging
import psutil
from datetime import datetime

logger = logging.getLogger(__name__)


class ResourceTracker:
    """
    Tracks real system resources that affect Aurora's behavior:
    - CPU availability
    - Memory availability  
    - Disk space
    - Network status
    """
    
    def __init__(self):
        self.last_check = None
        self._cache = {}
        self._cache_duration = 5  # seconds
        logger.info("📊 Resource Tracker initialized")
    
    def get_resources(self) -> dict:
        """Get current system resources"""
        now = datetime.now()
        
        # Use cache if recent
        if self.last_check:
            elapsed = (now - self.last_check).total_seconds()
            if elapsed < self._cache_duration and self._cache:
                return self._cache
        
        try:
            resources = {
                "cpu_available": 100 - psutil.cpu_percent(interval=0.1),
                "memory_available": psutil.virtual_memory().available / (1024**3),  # GB
                "memory_percent_free": 100 - psutil.virtual_memory().percent,
                "disk_free_gb": psutil.disk_usage('/').free / (1024**3),
                "battery": self._get_battery(),
                "timestamp": now.isoformat()
            }
            
            self._cache = resources
            self.last_check = now
            return resources
            
        except Exception as e:
            logger.error(f"Resource check failed: {e}")
            return {
                "cpu_available": 50,
                "memory_available": 4,
                "memory_percent_free": 50,
                "disk_free_gb": 50,
                "battery": {"percent": 100, "plugged": True},
                "timestamp": now.isoformat()
            }
    
    def _get_battery(self) -> dict:
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged
                }
        except:
            pass
        return {"percent": 100, "plugged": True}
    
    def can_run_heavy_task(self) -> bool:
        """Check if we have resources for heavy tasks"""
        resources = self.get_resources()
        return (
            resources["cpu_available"] > 30 and
            resources["memory_percent_free"] > 25
        )
    
    def should_rest(self) -> bool:
        """Check if we should pause due to low resources"""
        resources = self.get_resources()
        return (
            resources["cpu_available"] < 10 or
            resources["memory_percent_free"] < 15
        )
    
    def get_status_summary(self) -> str:
        """Human readable resource status"""
        r = self.get_resources()
        return f"CPU: {r['cpu_available']:.0f}% free | RAM: {r['memory_available']:.1f}GB free | Disk: {r['disk_free_gb']:.0f}GB free"


# Global instance
_tracker = None

def get_resource_tracker():
    """Get resource tracker instance"""
    global _tracker
    if _tracker is None:
        _tracker = ResourceTracker()
    return _tracker
