"""
MACOS COMMAND LIBRARY - Complete A-Z Commands for Aurora
========================================================
Every command, shortcut, and AppleScript Aurora can use.

This is the KNOWLEDGE BASE of what Aurora can do on macOS.
All commands are REAL and execute actual system operations.

Categories:
- System Commands
- File Operations  
- App Control
- Keyboard Shortcuts
- AppleScripts
- Terminal Commands
- Browser Commands
- Window Management
- Media Control
- Accessibility
"""

import subprocess
import os
import logging
from typing import Dict, List, Optional, Tuple, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class MacOSCommands:
    """
    Complete library of macOS commands Aurora can execute.
    All commands are REAL - they execute actual system operations.
    """
    
    def __init__(self):
        # Initialize pyautogui if available
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.pyautogui.FAILSAFE = True
            self.pyautogui.PAUSE = 0.1
            self.gui_available = True
        except ImportError:
            self.gui_available = False
            self.pyautogui = None
        
        # Build command registry
        self.commands = self._build_command_registry()
        
        logger.info(f"🖥️ macOS Command Library loaded: {len(self.commands)} commands")
    
    def _build_command_registry(self) -> Dict[str, Dict]:
        """Build the complete command registry"""
        
        commands = {}
        
        # ==========================================
        # SYSTEM COMMANDS
        # ==========================================
        
        # Power & Session
        commands["sleep"] = {
            "description": "Put Mac to sleep",
            "category": "system",
            "method": "applescript",
            "script": 'tell application "System Events" to sleep'
        }
        commands["shutdown"] = {
            "description": "Shutdown Mac (with confirmation)",
            "category": "system", 
            "method": "shell",
            "command": "osascript -e 'tell app \"System Events\" to shut down'"
        }
        commands["restart"] = {
            "description": "Restart Mac (with confirmation)",
            "category": "system",
            "method": "shell", 
            "command": "osascript -e 'tell app \"System Events\" to restart'"
        }
        commands["logout"] = {
            "description": "Log out current user",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'tell app \"System Events\" to log out'"
        }
        commands["lock_screen"] = {
            "description": "Lock the screen",
            "category": "system",
            "method": "shell",
            "command": "/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend"
        }
        
        # Volume Control
        commands["volume_up"] = {
            "description": "Increase volume",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'set volume output volume ((output volume of (get volume settings)) + 10)'"
        }
        commands["volume_down"] = {
            "description": "Decrease volume",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'set volume output volume ((output volume of (get volume settings)) - 10)'"
        }
        commands["volume_mute"] = {
            "description": "Toggle mute",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'set volume with output muted'"
        }
        commands["volume_unmute"] = {
            "description": "Unmute",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'set volume without output muted'"
        }
        commands["volume_set"] = {
            "description": "Set volume to specific level (0-100)",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'set volume output volume {level}'"
        }
        commands["get_volume"] = {
            "description": "Get current volume level",
            "category": "system",
            "method": "shell",
            "command": "osascript -e 'output volume of (get volume settings)'"
        }
        
        # Brightness
        commands["brightness_up"] = {
            "description": "Increase screen brightness",
            "category": "system",
            "method": "key",
            "key": "brightnessup"
        }
        commands["brightness_down"] = {
            "description": "Decrease screen brightness",
            "category": "system",
            "method": "key",
            "key": "brightnessdown"
        }
        
        # WiFi Control
        commands["wifi_on"] = {
            "description": "Turn WiFi on",
            "category": "system",
            "method": "shell",
            "command": "networksetup -setairportpower en0 on"
        }
        commands["wifi_off"] = {
            "description": "Turn WiFi off",
            "category": "system",
            "method": "shell",
            "command": "networksetup -setairportpower en0 off"
        }
        commands["wifi_status"] = {
            "description": "Get WiFi status (on/off)",
            "category": "system",
            "method": "shell",
            "command": "networksetup -getairportpower en0"
        }
        commands["wifi_connect"] = {
            "description": "Connect to WiFi network",
            "category": "system",
            "method": "shell",
            "command": "networksetup -setairportnetwork en0 '{network}' '{password}'"
        }
        commands["wifi_list"] = {
            "description": "List available WiFi networks",
            "category": "system",
            "method": "shell",
            "command": "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s"
        }
        commands["wifi_disconnect"] = {
            "description": "Disconnect from WiFi",
            "category": "system",
            "method": "shell",
            "command": "networksetup -setairportpower en0 off && sleep 1 && networksetup -setairportpower en0 on"
        }
        
        # Bluetooth Control
        commands["bluetooth_on"] = {
            "description": "Turn Bluetooth on",
            "category": "system",
            "method": "shell",
            "command": "blueutil -p 1"
        }
        commands["bluetooth_off"] = {
            "description": "Turn Bluetooth off",
            "category": "system",
            "method": "shell",
            "command": "blueutil -p 0"
        }
        commands["bluetooth_status"] = {
            "description": "Get Bluetooth status",
            "category": "system",
            "method": "shell",
            "command": "blueutil -p"
        }
        
        # Do Not Disturb
        commands["dnd_on"] = {
            "description": "Turn on Do Not Disturb",
            "category": "system",
            "method": "shell",
            "command": "defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean true && killall NotificationCenter"
        }
        commands["dnd_off"] = {
            "description": "Turn off Do Not Disturb",
            "category": "system",
            "method": "shell",
            "command": "defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean false && killall NotificationCenter"
        }
        
        # Night Shift
        commands["nightshift_on"] = {
            "description": "Enable Night Shift",
            "category": "system",
            "method": "applescript",
            "script": 'do shell script "defaults write com.apple.CoreBrightness.plist CBBlueReductionStatus -dict-add BlueLightReductionSchedule -dict-add scheduleName night-shift"'
        }
        
        # AirDrop
        commands["airdrop_everyone"] = {
            "description": "Set AirDrop to everyone",
            "category": "system",
            "method": "shell",
            "command": "defaults write com.apple.sharingd DiscoverableMode -string 'Everyone'"
        }
        commands["airdrop_contacts"] = {
            "description": "Set AirDrop to contacts only",
            "category": "system",
            "method": "shell",
            "command": "defaults write com.apple.sharingd DiscoverableMode -string 'Contacts Only'"
        }
        commands["airdrop_off"] = {
            "description": "Turn AirDrop off",
            "category": "system",
            "method": "shell",
            "command": "defaults write com.apple.sharingd DiscoverableMode -string 'Off'"
        }
        
        # Dark Mode
        commands["dark_mode_on"] = {
            "description": "Enable Dark Mode",
            "category": "system",
            "method": "applescript",
            "script": 'tell application "System Events" to tell appearance preferences to set dark mode to true'
        }
        commands["dark_mode_off"] = {
            "description": "Disable Dark Mode",
            "category": "system",
            "method": "applescript",
            "script": 'tell application "System Events" to tell appearance preferences to set dark mode to false'
        }
        commands["dark_mode_toggle"] = {
            "description": "Toggle Dark Mode",
            "category": "system",
            "method": "applescript",
            "script": 'tell application "System Events" to tell appearance preferences to set dark mode to not dark mode'
        }
        
        # System Info
        commands["get_battery"] = {
            "description": "Get battery percentage",
            "category": "system",
            "method": "shell",
            "command": "pmset -g batt | grep -o '[0-9]*%'"
        }
        commands["get_wifi"] = {
            "description": "Get current WiFi network",
            "category": "system",
            "method": "shell",
            "command": "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep ' SSID' | cut -d ':' -f 2"
        }
        commands["get_ip"] = {
            "description": "Get IP address",
            "category": "system",
            "method": "shell",
            "command": "ipconfig getifaddr en0"
        }
        commands["get_hostname"] = {
            "description": "Get computer name",
            "category": "system",
            "method": "shell",
            "command": "hostname"
        }
        commands["get_user"] = {
            "description": "Get current username",
            "category": "system",
            "method": "shell",
            "command": "whoami"
        }
        commands["get_uptime"] = {
            "description": "Get system uptime",
            "category": "system",
            "method": "shell",
            "command": "uptime"
        }
        commands["get_memory"] = {
            "description": "Get memory usage",
            "category": "system",
            "method": "shell",
            "command": "vm_stat | head -5"
        }
        commands["get_disk"] = {
            "description": "Get disk usage",
            "category": "system",
            "method": "shell",
            "command": "df -h / | tail -1"
        }
        commands["get_cpu"] = {
            "description": "Get CPU info",
            "category": "system",
            "method": "shell",
            "command": "sysctl -n machdep.cpu.brand_string"
        }
        
        # ==========================================
        # FILE OPERATIONS
        # ==========================================
        
        commands["list_files"] = {
            "description": "List files in directory",
            "category": "files",
            "method": "shell",
            "command": "ls -la {path}"
        }
        commands["create_folder"] = {
            "description": "Create a new folder",
            "category": "files",
            "method": "shell",
            "command": "mkdir -p {path}"
        }
        commands["create_file"] = {
            "description": "Create an empty file",
            "category": "files",
            "method": "shell",
            "command": "touch {path}"
        }
        commands["delete_file"] = {
            "description": "Move file to trash",
            "category": "files",
            "method": "shell",
            "command": "mv {path} ~/.Trash/"
        }
        commands["copy_file"] = {
            "description": "Copy a file",
            "category": "files",
            "method": "shell",
            "command": "cp {source} {dest}"
        }
        commands["move_file"] = {
            "description": "Move a file",
            "category": "files",
            "method": "shell",
            "command": "mv {source} {dest}"
        }
        commands["read_file"] = {
            "description": "Read file contents",
            "category": "files",
            "method": "shell",
            "command": "cat {path}"
        }
        commands["write_file"] = {
            "description": "Write text to file",
            "category": "files",
            "method": "shell",
            "command": "echo '{text}' > {path}"
        }
        commands["append_file"] = {
            "description": "Append text to file",
            "category": "files",
            "method": "shell",
            "command": "echo '{text}' >> {path}"
        }
        commands["find_files"] = {
            "description": "Find files by name",
            "category": "files",
            "method": "shell",
            "command": "find {path} -name '{pattern}'"
        }
        commands["search_content"] = {
            "description": "Search for text in files",
            "category": "files",
            "method": "shell",
            "command": "grep -r '{text}' {path}"
        }
        commands["file_info"] = {
            "description": "Get file information",
            "category": "files",
            "method": "shell",
            "command": "file {path} && ls -la {path}"
        }
        commands["open_in_finder"] = {
            "description": "Open location in Finder",
            "category": "files",
            "method": "shell",
            "command": "open {path}"
        }
        commands["reveal_in_finder"] = {
            "description": "Reveal file in Finder",
            "category": "files",
            "method": "shell",
            "command": "open -R {path}"
        }
        commands["empty_trash"] = {
            "description": "Empty the trash",
            "category": "files",
            "method": "applescript",
            "script": 'tell application "Finder" to empty trash'
        }
        commands["get_downloads"] = {
            "description": "List recent downloads",
            "category": "files",
            "method": "shell",
            "command": "ls -lt ~/Downloads | head -20"
        }
        commands["get_desktop"] = {
            "description": "List desktop items",
            "category": "files",
            "method": "shell",
            "command": "ls -la ~/Desktop"
        }
        
        # ==========================================
        # APP CONTROL
        # ==========================================
        
        # Common Apps
        apps = [
            "Safari", "Google Chrome", "Firefox", "Terminal", "Finder",
            "Notes", "TextEdit", "Calculator", "Calendar", "Reminders",
            "Music", "Photos", "Preview", "Mail", "Messages", "FaceTime",
            "System Preferences", "Activity Monitor", "Disk Utility",
            "App Store", "Xcode", "Visual Studio Code", "Sublime Text",
            "Slack", "Discord", "Spotify", "VLC", "Zoom"
        ]
        
        for app in apps:
            safe_name = app.lower().replace(" ", "_")
            commands[f"open_{safe_name}"] = {
                "description": f"Open {app}",
                "category": "apps",
                "method": "shell",
                "command": f'open -a "{app}"'
            }
            commands[f"close_{safe_name}"] = {
                "description": f"Close {app}",
                "category": "apps",
                "method": "applescript",
                "script": f'tell application "{app}" to quit'
            }
        
        # Generic app commands
        commands["open_app"] = {
            "description": "Open any application",
            "category": "apps",
            "method": "shell",
            "command": 'open -a "{app}"'
        }
        commands["close_app"] = {
            "description": "Close any application",
            "category": "apps",
            "method": "applescript",
            "script": 'tell application "{app}" to quit'
        }
        commands["activate_app"] = {
            "description": "Bring app to front",
            "category": "apps",
            "method": "applescript",
            "script": 'tell application "{app}" to activate'
        }
        commands["hide_app"] = {
            "description": "Hide an application",
            "category": "apps",
            "method": "applescript",
            "script": 'tell application "System Events" to set visible of process "{app}" to false'
        }
        commands["list_running_apps"] = {
            "description": "List running applications",
            "category": "apps",
            "method": "shell",
            "command": "osascript -e 'tell application \"System Events\" to get name of every process whose background only is false'"
        }
        commands["force_quit_app"] = {
            "description": "Force quit an application",
            "category": "apps",
            "method": "shell",
            "command": "pkill -9 {app}"
        }
        
        # ==========================================
        # KEYBOARD SHORTCUTS
        # ==========================================
        
        shortcuts = {
            # System
            "spotlight": ("command", "space"),
            "force_quit_dialog": ("command", "option", "escape"),
            "screenshot_full": ("command", "shift", "3"),
            "screenshot_selection": ("command", "shift", "4"),
            "screenshot_window": ("command", "shift", "4", "space"),
            "screen_record": ("command", "shift", "5"),
            "show_desktop": ("command", "f3"),
            "mission_control": ("control", "up"),
            "app_windows": ("control", "down"),
            "notification_center": ("option", "click"),
            
            # Window Management
            "minimize": ("command", "m"),
            "minimize_all": ("command", "option", "m"),
            "close_window": ("command", "w"),
            "close_all_windows": ("command", "option", "w"),
            "new_window": ("command", "n"),
            "new_tab": ("command", "t"),
            "cycle_windows": ("command", "`"),
            "fullscreen_toggle": ("command", "control", "f"),
            
            # App Control
            "switch_app": ("command", "tab"),
            "switch_app_reverse": ("command", "shift", "tab"),
            "quit_app": ("command", "q"),
            "hide_app_shortcut": ("command", "h"),
            "hide_others": ("command", "option", "h"),
            
            # Edit
            "undo": ("command", "z"),
            "redo": ("command", "shift", "z"),
            "cut": ("command", "x"),
            "copy": ("command", "c"),
            "paste": ("command", "v"),
            "paste_match_style": ("command", "option", "shift", "v"),
            "select_all": ("command", "a"),
            "find": ("command", "f"),
            "find_replace": ("command", "option", "f"),
            "find_next": ("command", "g"),
            "find_previous": ("command", "shift", "g"),
            
            # Text
            "bold": ("command", "b"),
            "italic": ("command", "i"),
            "underline": ("command", "u"),
            
            # Navigation
            "go_to_start": ("command", "up"),
            "go_to_end": ("command", "down"),
            "go_to_line_start": ("command", "left"),
            "go_to_line_end": ("command", "right"),
            "page_up": ("fn", "up"),
            "page_down": ("fn", "down"),
            
            # Finder specific
            "new_folder": ("command", "shift", "n"),
            "go_to_folder": ("command", "shift", "g"),
            "show_info": ("command", "i"),
            "quick_look": ("space",),
            "delete_file_shortcut": ("command", "delete"),
            
            # Browser
            "reload": ("command", "r"),
            "hard_reload": ("command", "shift", "r"),
            "back": ("command", "["),
            "forward": ("command", "]"),
            "home": ("command", "shift", "h"),
            "address_bar": ("command", "l"),
            "close_tab": ("command", "w"),
            "reopen_tab": ("command", "shift", "t"),
            "next_tab": ("command", "option", "right"),
            "prev_tab": ("command", "option", "left"),
            "zoom_in": ("command", "+"),
            "zoom_out": ("command", "-"),
            "zoom_reset": ("command", "0"),
        }
        
        for name, keys in shortcuts.items():
            commands[f"shortcut_{name}"] = {
                "description": f"Press {'+'.join(keys)}",
                "category": "shortcuts",
                "method": "hotkey",
                "keys": keys
            }
        
        # ==========================================
        # BROWSER COMMANDS
        # ==========================================
        
        commands["browser_open_url"] = {
            "description": "Open URL in default browser",
            "category": "browser",
            "method": "shell",
            "command": "open {url}"
        }
        commands["safari_open_url"] = {
            "description": "Open URL in Safari",
            "category": "browser",
            "method": "applescript",
            "script": '''
                tell application "Safari"
                    activate
                    open location "{url}"
                end tell
            '''
        }
        commands["chrome_open_url"] = {
            "description": "Open URL in Chrome",
            "category": "browser",
            "method": "applescript",
            "script": '''
                tell application "Google Chrome"
                    activate
                    open location "{url}"
                end tell
            '''
        }
        commands["safari_get_url"] = {
            "description": "Get current Safari URL",
            "category": "browser",
            "method": "applescript",
            "script": 'tell application "Safari" to get URL of current tab of window 1'
        }
        commands["chrome_get_url"] = {
            "description": "Get current Chrome URL",
            "category": "browser",
            "method": "applescript",
            "script": 'tell application "Google Chrome" to get URL of active tab of window 1'
        }
        commands["safari_get_title"] = {
            "description": "Get current Safari page title",
            "category": "browser",
            "method": "applescript",
            "script": 'tell application "Safari" to get name of current tab of window 1'
        }
        commands["google_search"] = {
            "description": "Search Google",
            "category": "browser",
            "method": "shell",
            "command": 'open "https://www.google.com/search?q={query}"'
        }
        commands["youtube_search"] = {
            "description": "Search YouTube",
            "category": "browser",
            "method": "shell",
            "command": 'open "https://www.youtube.com/results?search_query={query}"'
        }
        commands["wikipedia_search"] = {
            "description": "Search Wikipedia",
            "category": "browser",
            "method": "shell",
            "command": 'open "https://en.wikipedia.org/wiki/{query}"'
        }
        
        # ==========================================
        # MEDIA CONTROL
        # ==========================================
        
        commands["play_pause"] = {
            "description": "Play/Pause media",
            "category": "media",
            "method": "key",
            "key": "playpause"
        }
        commands["next_track"] = {
            "description": "Next track",
            "category": "media",
            "method": "key",
            "key": "nexttrack"
        }
        commands["prev_track"] = {
            "description": "Previous track",
            "category": "media",
            "method": "key",
            "key": "prevtrack"
        }
        commands["music_play"] = {
            "description": "Play in Music app",
            "category": "media",
            "method": "applescript",
            "script": 'tell application "Music" to play'
        }
        commands["music_pause"] = {
            "description": "Pause Music app",
            "category": "media",
            "method": "applescript",
            "script": 'tell application "Music" to pause'
        }
        commands["music_next"] = {
            "description": "Next track in Music",
            "category": "media",
            "method": "applescript",
            "script": 'tell application "Music" to next track'
        }
        commands["music_previous"] = {
            "description": "Previous track in Music",
            "category": "media",
            "method": "applescript",
            "script": 'tell application "Music" to previous track'
        }
        commands["spotify_play"] = {
            "description": "Play Spotify",
            "category": "media",
            "method": "applescript",
            "script": 'tell application "Spotify" to play'
        }
        commands["spotify_pause"] = {
            "description": "Pause Spotify",
            "category": "media",
            "method": "applescript",
            "script": 'tell application "Spotify" to pause'
        }
        
        # ==========================================
        # NOTIFICATIONS & DIALOGS
        # ==========================================
        
        commands["notification"] = {
            "description": "Show system notification",
            "category": "ui",
            "method": "shell",
            "command": 'osascript -e \'display notification "{message}" with title "{title}"\''
        }
        commands["alert_dialog"] = {
            "description": "Show alert dialog",
            "category": "ui",
            "method": "applescript",
            "script": 'display alert "{title}" message "{message}"'
        }
        commands["input_dialog"] = {
            "description": "Show input dialog",
            "category": "ui",
            "method": "applescript",
            "script": 'display dialog "{prompt}" default answer ""'
        }
        commands["choose_file"] = {
            "description": "Show file chooser",
            "category": "ui",
            "method": "applescript",
            "script": 'choose file'
        }
        commands["choose_folder"] = {
            "description": "Show folder chooser",
            "category": "ui",
            "method": "applescript",
            "script": 'choose folder'
        }
        
        # ==========================================
        # WINDOW MANAGEMENT
        # ==========================================
        
        commands["minimize_window"] = {
            "description": "Minimize front window",
            "category": "windows",
            "method": "applescript",
            "script": 'tell application "System Events" to set miniaturized of first window of (first process whose frontmost is true) to true'
        }
        commands["maximize_window"] = {
            "description": "Maximize front window",
            "category": "windows",
            "method": "applescript",
            "script": '''
                tell application "System Events"
                    tell (first process whose frontmost is true)
                        click button 2 of window 1
                    end tell
                end tell
            '''
        }
        commands["get_window_title"] = {
            "description": "Get frontmost window title",
            "category": "windows",
            "method": "applescript",
            "script": 'tell application "System Events" to get name of first window of (first process whose frontmost is true)'
        }
        commands["get_front_app"] = {
            "description": "Get frontmost application name",
            "category": "windows",
            "method": "applescript",
            "script": 'tell application "System Events" to get name of first process whose frontmost is true'
        }
        
        # ==========================================
        # CLIPBOARD
        # ==========================================
        
        commands["get_clipboard"] = {
            "description": "Get clipboard contents",
            "category": "clipboard",
            "method": "shell",
            "command": "pbpaste"
        }
        commands["set_clipboard"] = {
            "description": "Set clipboard contents",
            "category": "clipboard",
            "method": "shell",
            "command": "echo '{text}' | pbcopy"
        }
        commands["clear_clipboard"] = {
            "description": "Clear clipboard",
            "category": "clipboard",
            "method": "shell",
            "command": "pbcopy < /dev/null"
        }
        
        # ==========================================
        # TERMINAL COMMANDS
        # ==========================================
        
        commands["run_shell"] = {
            "description": "Run shell command",
            "category": "terminal",
            "method": "shell",
            "command": "{command}"
        }
        commands["run_python"] = {
            "description": "Run Python code",
            "category": "terminal",
            "method": "shell",
            "command": "python3 -c \"{code}\""
        }
        commands["which"] = {
            "description": "Find command location",
            "category": "terminal",
            "method": "shell",
            "command": "which {command}"
        }
        commands["process_list"] = {
            "description": "List processes",
            "category": "terminal",
            "method": "shell",
            "command": "ps aux"
        }
        commands["kill_process"] = {
            "description": "Kill a process",
            "category": "terminal",
            "method": "shell",
            "command": "kill {pid}"
        }
        
        # ==========================================
        # ACCESSIBILITY
        # ==========================================
        
        commands["say_text"] = {
            "description": "Speak text aloud",
            "category": "accessibility",
            "method": "shell",
            "command": 'say "{text}"'
        }
        commands["say_text_voice"] = {
            "description": "Speak text with specific voice",
            "category": "accessibility",
            "method": "shell",
            "command": 'say -v {voice} "{text}"'
        }
        commands["list_voices"] = {
            "description": "List available voices",
            "category": "accessibility",
            "method": "shell",
            "command": "say -v '?'"
        }
        commands["zoom_in_accessibility"] = {
            "description": "Zoom in (accessibility)",
            "category": "accessibility",
            "method": "hotkey",
            "keys": ("option", "command", "=")
        }
        commands["zoom_out_accessibility"] = {
            "description": "Zoom out (accessibility)",
            "category": "accessibility",
            "method": "hotkey",
            "keys": ("option", "command", "-")
        }
        
        return commands
    
    # ==========================================
    # COMMAND EXECUTION
    # ==========================================
    
    def execute(self, command_name: str, **params) -> Tuple[bool, str]:
        """
        Execute a command by name.
        Returns (success, result/error)
        """
        if command_name not in self.commands:
            return False, f"Unknown command: {command_name}"
        
        cmd = self.commands[command_name]
        method = cmd.get("method")
        
        try:
            if method == "shell":
                return self._execute_shell(cmd["command"], params)
            elif method == "applescript":
                return self._execute_applescript(cmd["script"], params)
            elif method == "hotkey":
                return self._execute_hotkey(cmd["keys"])
            elif method == "key":
                return self._execute_key(cmd["key"])
            else:
                return False, f"Unknown method: {method}"
        except Exception as e:
            return False, str(e)
    
    def _execute_shell(self, command: str, params: Dict) -> Tuple[bool, str]:
        """Execute shell command"""
        # Substitute parameters
        try:
            cmd = command.format(**params)
        except KeyError as e:
            return False, f"Missing parameter: {e}"
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip() or f"Exit code: {result.returncode}"
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def _execute_applescript(self, script: str, params: Dict) -> Tuple[bool, str]:
        """Execute AppleScript"""
        try:
            formatted_script = script.format(**params)
        except KeyError as e:
            return False, f"Missing parameter: {e}"
        
        try:
            result = subprocess.run(
                ["osascript", "-e", formatted_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except Exception as e:
            return False, str(e)
    
    def _execute_hotkey(self, keys: tuple) -> Tuple[bool, str]:
        """Execute keyboard hotkey"""
        if not self.gui_available:
            return False, "PyAutoGUI not available"
        
        try:
            self.pyautogui.hotkey(*keys)
            return True, f"Pressed: {'+'.join(keys)}"
        except Exception as e:
            return False, str(e)
    
    def _execute_key(self, key: str) -> Tuple[bool, str]:
        """Execute single key press"""
        if not self.gui_available:
            return False, "PyAutoGUI not available"
        
        try:
            self.pyautogui.press(key)
            return True, f"Pressed: {key}"
        except Exception as e:
            return False, str(e)
    
    # ==========================================
    # COMMAND LOOKUP
    # ==========================================
    
    def get_command(self, name: str) -> Optional[Dict]:
        """Get command info by name"""
        return self.commands.get(name)
    
    def search_commands(self, query: str) -> List[str]:
        """Search commands by name or description"""
        query_lower = query.lower()
        matches = []
        
        for name, cmd in self.commands.items():
            if query_lower in name.lower() or query_lower in cmd.get("description", "").lower():
                matches.append(name)
        
        return matches
    
    def get_commands_by_category(self, category: str) -> List[str]:
        """Get all commands in a category"""
        return [name for name, cmd in self.commands.items() if cmd.get("category") == category]
    
    def list_categories(self) -> List[str]:
        """List all command categories"""
        return list(set(cmd.get("category", "other") for cmd in self.commands.values()))
    
    def get_all_commands(self) -> Dict[str, Dict]:
        """Get all commands"""
        return self.commands


# Global instance
_macos_commands = None

def get_macos_commands() -> MacOSCommands:
    """Get macOS commands instance"""
    global _macos_commands
    if _macos_commands is None:
        _macos_commands = MacOSCommands()
    return _macos_commands
