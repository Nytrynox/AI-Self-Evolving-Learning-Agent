"""
WEB TOOLS - Internet Access
==========================
Allows Aurora to browse the web and search.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class WebTools:
    """
    Web browsing and search capabilities.
    """
    
    def __init__(self):
        self.requests_available = False
        self.selenium_available = False
        
        # Try to import requests
        try:
            import requests
            from bs4 import BeautifulSoup
            self.requests = requests
            self.BeautifulSoup = BeautifulSoup
            self.requests_available = True
            logger.info("🌐 Web requests available")
        except ImportError:
            logger.warning("⚠️ requests/beautifulsoup not installed")
            self.requests = None
            self.BeautifulSoup = None
        
        logger.info("🌍 Web Tools initialized")
    
    def fetch_url(self, url: str, timeout: int = 10) -> Optional[Dict]:
        """Fetch content from URL"""
        if not self.requests_available:
            logger.error("Web requests not available")
            return None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = self.requests.get(url, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                # Parse HTML
                soup = self.BeautifulSoup(response.text, 'html.parser')
                
                # Extract text
                for tag in soup(['script', 'style', 'nav', 'footer']):
                    tag.decompose()
                
                text = soup.get_text(separator=' ', strip=True)
                
                logger.info(f"🌐 Fetched: {url}")
                
                return {
                    "url": url,
                    "status": response.status_code,
                    "title": soup.title.string if soup.title else None,
                    "text": text[:5000],  # Limit text
                    "length": len(text)
                }
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Fetch failed: {e}")
            return None
    
    def search_web(self, query: str) -> List[Dict]:
        """
        Search the web using DuckDuckGo (no API key needed).
        Returns list of results.
        """
        if not self.requests_available:
            logger.error("Web requests not available")
            return []
        
        try:
            # Use DuckDuckGo HTML version
            url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = self.requests.get(url, headers=headers, timeout=10)
            soup = self.BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('a', class_='result__a')[:5]:
                title = result.get_text()
                link = result.get('href', '')
                
                # Get snippet
                snippet_div = result.find_next('a', class_='result__snippet')
                snippet = snippet_div.get_text() if snippet_div else ""
                
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet
                })
            
            logger.info(f"🔍 Search '{query}': {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def download_file(self, url: str, save_path: str) -> bool:
        """Download a file from URL"""
        if not self.requests_available:
            return False
        
        try:
            response = self.requests.get(url, stream=True, timeout=30)
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"⬇️ Downloaded: {url} -> {save_path}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            return False
    
    def get_wikipedia_summary(self, topic: str) -> Optional[str]:
        """Get Wikipedia summary for a topic"""
        if not self.requests_available:
            return None
        
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            response = self.requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get('extract', '')
                logger.info(f"📚 Wikipedia: {topic}")
                return summary
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Wikipedia failed: {e}")
            return None


# Global instance
_web_tools = None

def get_web_tools() -> WebTools:
    """Get web tools instance"""
    global _web_tools
    if _web_tools is None:
        _web_tools = WebTools()
    return _web_tools
