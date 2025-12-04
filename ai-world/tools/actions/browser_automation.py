"""
BROWSER AUTOMATION - Advanced Web Control
==========================================
Selenium-based browser automation for Aurora.
Can control browsers, fill forms, click buttons, navigate.
"""

import logging
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class BrowserAutomation:
    """
    Advanced browser automation using Selenium.
    """
    
    def __init__(self):
        self.selenium_available = False
        self.driver = None
        self.browser_type = None
        
        # Try to import selenium
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.action_chains import ActionChains
            
            self.webdriver = webdriver
            self.By = By
            self.Keys = Keys
            self.WebDriverWait = WebDriverWait
            self.EC = EC
            self.ActionChains = ActionChains
            
            self.selenium_available = True
            logger.info("🌐 Selenium available for browser automation")
        except ImportError:
            logger.warning("⚠️ Selenium not installed - advanced browser control disabled")
        
        logger.info("🌐 Browser Automation initialized")
    
    def start_browser(self, browser: str = "chrome", headless: bool = False) -> bool:
        """Start a browser instance"""
        if not self.selenium_available:
            logger.error("Selenium not available")
            return False
        
        try:
            if browser.lower() == "chrome":
                from selenium.webdriver.chrome.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                self.driver = self.webdriver.Chrome(options=options)
                
            elif browser.lower() == "safari":
                self.driver = self.webdriver.Safari()
                
            elif browser.lower() == "firefox":
                from selenium.webdriver.firefox.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                self.driver = self.webdriver.Firefox(options=options)
            
            else:
                logger.error(f"Unknown browser: {browser}")
                return False
            
            self.browser_type = browser
            self.driver.implicitly_wait(10)
            logger.info(f"🌐 Started {browser} browser")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start browser: {e}")
            return False
    
    def close_browser(self) -> bool:
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("🌐 Browser closed")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to close browser: {e}")
        return False
    
    def navigate(self, url: str) -> bool:
        """Navigate to a URL"""
        if not self.driver:
            logger.error("Browser not started")
            return False
        
        try:
            self.driver.get(url)
            logger.info(f"🌐 Navigated to: {url}")
            return True
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False
    
    def get_current_url(self) -> Optional[str]:
        """Get current URL"""
        if self.driver:
            return self.driver.current_url
        return None
    
    def get_page_title(self) -> Optional[str]:
        """Get page title"""
        if self.driver:
            return self.driver.title
        return None
    
    def get_page_source(self) -> Optional[str]:
        """Get page HTML source"""
        if self.driver:
            return self.driver.page_source
        return None
    
    # ==========================================
    # ELEMENT INTERACTION
    # ==========================================
    
    def find_element(self, by: str, value: str):
        """Find a single element"""
        if not self.driver:
            return None
        
        by_map = {
            "id": self.By.ID,
            "name": self.By.NAME,
            "class": self.By.CLASS_NAME,
            "tag": self.By.TAG_NAME,
            "css": self.By.CSS_SELECTOR,
            "xpath": self.By.XPATH,
            "link_text": self.By.LINK_TEXT,
            "partial_link": self.By.PARTIAL_LINK_TEXT
        }
        
        try:
            by_type = by_map.get(by.lower(), self.By.CSS_SELECTOR)
            return self.driver.find_element(by_type, value)
        except Exception as e:
            logger.debug(f"Element not found: {by}={value}")
            return None
    
    def find_elements(self, by: str, value: str) -> List:
        """Find multiple elements"""
        if not self.driver:
            return []
        
        by_map = {
            "id": self.By.ID,
            "name": self.By.NAME,
            "class": self.By.CLASS_NAME,
            "tag": self.By.TAG_NAME,
            "css": self.By.CSS_SELECTOR,
            "xpath": self.By.XPATH,
            "link_text": self.By.LINK_TEXT,
            "partial_link": self.By.PARTIAL_LINK_TEXT
        }
        
        try:
            by_type = by_map.get(by.lower(), self.By.CSS_SELECTOR)
            return self.driver.find_elements(by_type, value)
        except Exception as e:
            logger.debug(f"Elements not found: {by}={value}")
            return []
    
    def click_element(self, by: str, value: str) -> bool:
        """Click an element"""
        element = self.find_element(by, value)
        if element:
            try:
                element.click()
                logger.info(f"🖱️ Clicked element: {by}={value}")
                return True
            except Exception as e:
                logger.error(f"❌ Click failed: {e}")
        return False
    
    def type_into_element(self, by: str, value: str, text: str, clear_first: bool = True) -> bool:
        """Type text into an element"""
        element = self.find_element(by, value)
        if element:
            try:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                logger.info(f"⌨️ Typed into {by}={value}: '{text[:30]}...'")
                return True
            except Exception as e:
                logger.error(f"❌ Type failed: {e}")
        return False
    
    def get_element_text(self, by: str, value: str) -> Optional[str]:
        """Get text content of an element"""
        element = self.find_element(by, value)
        if element:
            return element.text
        return None
    
    def get_element_attribute(self, by: str, value: str, attribute: str) -> Optional[str]:
        """Get attribute of an element"""
        element = self.find_element(by, value)
        if element:
            return element.get_attribute(attribute)
        return None
    
    def element_exists(self, by: str, value: str) -> bool:
        """Check if element exists"""
        return self.find_element(by, value) is not None
    
    def wait_for_element(self, by: str, value: str, timeout: int = 10) -> bool:
        """Wait for an element to appear"""
        if not self.driver:
            return False
        
        by_map = {
            "id": self.By.ID,
            "name": self.By.NAME,
            "class": self.By.CLASS_NAME,
            "css": self.By.CSS_SELECTOR,
            "xpath": self.By.XPATH
        }
        
        try:
            by_type = by_map.get(by.lower(), self.By.CSS_SELECTOR)
            wait = self.WebDriverWait(self.driver, timeout)
            wait.until(self.EC.presence_of_element_located((by_type, value)))
            logger.info(f"✅ Element appeared: {by}={value}")
            return True
        except Exception as e:
            logger.warning(f"⏰ Timeout waiting for element: {by}={value}")
            return False
    
    def wait_for_clickable(self, by: str, value: str, timeout: int = 10) -> bool:
        """Wait for an element to be clickable"""
        if not self.driver:
            return False
        
        by_map = {
            "id": self.By.ID,
            "name": self.By.NAME,
            "class": self.By.CLASS_NAME,
            "css": self.By.CSS_SELECTOR,
            "xpath": self.By.XPATH
        }
        
        try:
            by_type = by_map.get(by.lower(), self.By.CSS_SELECTOR)
            wait = self.WebDriverWait(self.driver, timeout)
            wait.until(self.EC.element_to_be_clickable((by_type, value)))
            return True
        except Exception as e:
            logger.warning(f"⏰ Element not clickable: {by}={value}")
            return False
    
    # ==========================================
    # FORM INTERACTIONS
    # ==========================================
    
    def fill_form(self, form_data: Dict[str, str], by: str = "name") -> bool:
        """Fill a form with multiple fields"""
        success = True
        for field, value in form_data.items():
            if not self.type_into_element(by, field, value):
                success = False
        return success
    
    def submit_form(self, by: str = "css", value: str = "form") -> bool:
        """Submit a form"""
        element = self.find_element(by, value)
        if element:
            try:
                element.submit()
                logger.info("📤 Form submitted")
                return True
            except Exception as e:
                logger.error(f"❌ Submit failed: {e}")
        return False
    
    def select_dropdown(self, by: str, value: str, option_text: str) -> bool:
        """Select an option from a dropdown"""
        if not self.selenium_available:
            return False
        
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(by, value)
            if element:
                select = Select(element)
                select.select_by_visible_text(option_text)
                logger.info(f"📋 Selected: {option_text}")
                return True
        except Exception as e:
            logger.error(f"❌ Dropdown select failed: {e}")
        return False
    
    def check_checkbox(self, by: str, value: str, check: bool = True) -> bool:
        """Check or uncheck a checkbox"""
        element = self.find_element(by, value)
        if element:
            is_checked = element.is_selected()
            if check != is_checked:
                element.click()
                logger.info(f"☑️ Checkbox {'checked' if check else 'unchecked'}")
            return True
        return False
    
    # ==========================================
    # NAVIGATION
    # ==========================================
    
    def go_back(self) -> bool:
        """Go back in browser history"""
        if self.driver:
            try:
                self.driver.back()
                logger.info("⬅️ Went back")
                return True
            except:
                pass
        return False
    
    def go_forward(self) -> bool:
        """Go forward in browser history"""
        if self.driver:
            try:
                self.driver.forward()
                logger.info("➡️ Went forward")
                return True
            except:
                pass
        return False
    
    def refresh(self) -> bool:
        """Refresh current page"""
        if self.driver:
            try:
                self.driver.refresh()
                logger.info("🔄 Page refreshed")
                return True
            except:
                pass
        return False
    
    # ==========================================
    # TABS AND WINDOWS
    # ==========================================
    
    def new_tab(self, url: Optional[str] = None) -> bool:
        """Open a new tab"""
        if not self.driver:
            return False
        
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            if url:
                self.navigate(url)
            logger.info("📑 New tab opened")
            return True
        except Exception as e:
            logger.error(f"❌ New tab failed: {e}")
            return False
    
    def close_tab(self) -> bool:
        """Close current tab"""
        if self.driver:
            try:
                self.driver.close()
                if self.driver.window_handles:
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                logger.info("📑 Tab closed")
                return True
            except:
                pass
        return False
    
    def switch_to_tab(self, index: int) -> bool:
        """Switch to tab by index"""
        if self.driver:
            try:
                handles = self.driver.window_handles
                if 0 <= index < len(handles):
                    self.driver.switch_to.window(handles[index])
                    logger.info(f"📑 Switched to tab {index}")
                    return True
            except:
                pass
        return False
    
    def get_tab_count(self) -> int:
        """Get number of open tabs"""
        if self.driver:
            return len(self.driver.window_handles)
        return 0
    
    # ==========================================
    # SCREENSHOTS
    # ==========================================
    
    def screenshot(self, filepath: str) -> bool:
        """Take a screenshot"""
        if self.driver:
            try:
                self.driver.save_screenshot(filepath)
                logger.info(f"📸 Screenshot saved: {filepath}")
                return True
            except Exception as e:
                logger.error(f"❌ Screenshot failed: {e}")
        return False
    
    def screenshot_element(self, by: str, value: str, filepath: str) -> bool:
        """Screenshot a specific element"""
        element = self.find_element(by, value)
        if element:
            try:
                element.screenshot(filepath)
                logger.info(f"📸 Element screenshot saved: {filepath}")
                return True
            except:
                pass
        return False
    
    # ==========================================
    # JAVASCRIPT EXECUTION
    # ==========================================
    
    def execute_js(self, script: str) -> Any:
        """Execute JavaScript code"""
        if self.driver:
            try:
                result = self.driver.execute_script(script)
                logger.info(f"📜 JS executed")
                return result
            except Exception as e:
                logger.error(f"❌ JS execution failed: {e}")
        return None
    
    def scroll_to_element(self, by: str, value: str) -> bool:
        """Scroll to make element visible"""
        element = self.find_element(by, value)
        if element:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                logger.info("📜 Scrolled to element")
                return True
            except:
                pass
        return False
    
    def scroll_to_bottom(self) -> bool:
        """Scroll to bottom of page"""
        return self.execute_js("window.scrollTo(0, document.body.scrollHeight);") is not None
    
    def scroll_to_top(self) -> bool:
        """Scroll to top of page"""
        return self.execute_js("window.scrollTo(0, 0);") is not None
    
    # ==========================================
    # COMMON WORKFLOWS
    # ==========================================
    
    def google_search(self, query: str) -> bool:
        """Perform a Google search"""
        if self.navigate("https://www.google.com"):
            time.sleep(1)
            if self.type_into_element("name", "q", query):
                return self.click_element("name", "btnK") or self.type_into_element("name", "q", self.Keys.ENTER if self.selenium_available else "\n")
        return False
    
    def login(self, url: str, username: str, password: str,
              username_field: str = "username", password_field: str = "password",
              submit_button: str = None) -> bool:
        """Generic login workflow"""
        if not self.navigate(url):
            return False
        
        time.sleep(2)
        
        # Try common field names
        username_selectors = [username_field, "email", "user", "login", "username"]
        password_selectors = [password_field, "pass", "pwd", "password"]
        
        # Find and fill username
        for selector in username_selectors:
            if self.type_into_element("name", selector, username):
                break
            if self.type_into_element("id", selector, username):
                break
        
        # Find and fill password
        for selector in password_selectors:
            if self.type_into_element("name", selector, password):
                break
            if self.type_into_element("id", selector, password):
                break
        
        # Submit
        if submit_button:
            return self.click_element("css", submit_button)
        else:
            # Try common submit buttons
            for selector in ["[type='submit']", "button[type='submit']", ".login-button", "#login"]:
                if self.click_element("css", selector):
                    return True
        
        return False
    
    def get_all_links(self) -> List[str]:
        """Get all links on current page"""
        links = self.find_elements("tag", "a")
        return [link.get_attribute("href") for link in links if link.get_attribute("href")]
    
    def get_all_images(self) -> List[str]:
        """Get all image URLs on current page"""
        images = self.find_elements("tag", "img")
        return [img.get_attribute("src") for img in images if img.get_attribute("src")]


# Global instance
_browser_automation = None

def get_browser_automation() -> BrowserAutomation:
    """Get browser automation instance"""
    global _browser_automation
    if _browser_automation is None:
        _browser_automation = BrowserAutomation()
    return _browser_automation
