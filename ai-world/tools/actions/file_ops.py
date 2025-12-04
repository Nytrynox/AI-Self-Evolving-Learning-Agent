"""
FILE OPERATIONS - Full File System Access
========================================
Allows Aurora to read, write, and manage files.
"""

import os
import shutil
import logging
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class FileOperations:
    """
    Full file system access for Aurora.
    Can read, write, delete, and manage files.
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.expanduser("~")
        logger.info(f"📁 File Operations initialized (base: {self.base_path})")
    
    def _resolve_path(self, path: str) -> str:
        """Resolve relative path to absolute"""
        if path.startswith("/"):
            return path
        if path.startswith("~"):
            return os.path.expanduser(path)
        return os.path.join(self.base_path, path)
    
    def list_directory(self, path: str = ".") -> List[Dict]:
        """List contents of a directory"""
        try:
            full_path = self._resolve_path(path)
            items = []
            
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                is_dir = os.path.isdir(item_path)
                
                items.append({
                    "name": item,
                    "type": "directory" if is_dir else "file",
                    "size": os.path.getsize(item_path) if not is_dir else None
                })
            
            return items
            
        except Exception as e:
            logger.error(f"❌ List failed: {e}")
            return []
    
    def read_file(self, path: str, max_size: int = 100000) -> Optional[str]:
        """Read file contents"""
        try:
            full_path = self._resolve_path(path)
            
            # Check size
            size = os.path.getsize(full_path)
            if size > max_size:
                logger.warning(f"File too large ({size} bytes), truncating")
            
            with open(full_path, 'r', errors='ignore') as f:
                content = f.read(max_size)
            
            logger.info(f"📖 Read: {path} ({len(content)} chars)")
            return content
            
        except Exception as e:
            logger.error(f"❌ Read failed: {e}")
            return None
    
    def write_file(self, path: str, content: str, append: bool = False) -> bool:
        """Write content to file"""
        try:
            full_path = self._resolve_path(path)
            
            # Create directory if needed
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            mode = 'a' if append else 'w'
            with open(full_path, mode) as f:
                f.write(content)
            
            logger.info(f"📝 Written: {path} ({len(content)} chars)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Write failed: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """Delete a file"""
        try:
            full_path = self._resolve_path(path)
            
            if os.path.isfile(full_path):
                os.remove(full_path)
                logger.info(f"🗑️ Deleted: {path}")
                return True
            else:
                logger.warning(f"Not a file: {path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Delete failed: {e}")
            return False
    
    def create_directory(self, path: str) -> bool:
        """Create a directory"""
        try:
            full_path = self._resolve_path(path)
            os.makedirs(full_path, exist_ok=True)
            logger.info(f"📁 Created directory: {path}")
            return True
        except Exception as e:
            logger.error(f"❌ mkdir failed: {e}")
            return False
    
    def copy_file(self, source: str, destination: str) -> bool:
        """Copy a file"""
        try:
            src = self._resolve_path(source)
            dst = self._resolve_path(destination)
            shutil.copy(src, dst)
            logger.info(f"📋 Copied: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"❌ Copy failed: {e}")
            return False
    
    def move_file(self, source: str, destination: str) -> bool:
        """Move a file"""
        try:
            src = self._resolve_path(source)
            dst = self._resolve_path(destination)
            shutil.move(src, dst)
            logger.info(f"📦 Moved: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"❌ Move failed: {e}")
            return False
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists"""
        full_path = self._resolve_path(path)
        return os.path.exists(full_path)
    
    def get_file_info(self, path: str) -> Optional[Dict]:
        """Get file information"""
        try:
            full_path = self._resolve_path(path)
            stat = os.stat(full_path)
            
            return {
                "path": full_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_directory": os.path.isdir(full_path)
            }
        except Exception as e:
            logger.error(f"❌ File info failed: {e}")
            return None
    
    def search_files(self, directory: str, pattern: str) -> List[str]:
        """Search for files matching pattern"""
        try:
            full_path = self._resolve_path(directory)
            matches = []
            
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    if pattern.lower() in file.lower():
                        matches.append(os.path.join(root, file))
            
            logger.info(f"🔍 Found {len(matches)} files matching '{pattern}'")
            return matches
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []


# Global instance
_file_ops = None

def get_file_ops() -> FileOperations:
    """Get file operations instance"""
    global _file_ops
    if _file_ops is None:
        _file_ops = FileOperations()
    return _file_ops
