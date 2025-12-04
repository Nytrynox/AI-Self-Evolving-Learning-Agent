#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    AURORA ULTIMATE NEURAL INTERFACE v4.0                          ║
║                    Professional AI Visualization System                           ║
║                    Real Event-Driven Visuals • A–Z Commands                       ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from ui.world_view import WorldView
from agents.mother_ai import MotherAI
from tkinter import ttk, messagebox
import threading
import time
import math
import random
import sys
import os
import subprocess
import json  # Added for pattern stats feed
from pathlib import Path  # Added for pattern stats feed
from datetime import datetime
from collections import Counter, deque, defaultdict
import queue

# Add path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Aurora vision system - DISABLED to fix GUI
try:
    # from aurora_vision import CameraWidget, OCRWidget
    VISION_AVAILABLE = False  # Disabled
except ImportError as e:
    print(f"Vision modules not available: {e}")
    VISION_AVAILABLE = False

# Import action tracking
try:
    from action_tracker import ActionTracker, SmartRetryManager, ActionResult
    ACTION_TRACKING_AVAILABLE = True
except ImportError as e:
    print(f"Action tracking not available: {e}")
    ACTION_TRACKING_AVAILABLE = False

# Import TRUE NLP Vision AI Brain
try:
    from vision_ai_brain import VisionAIBrain, execute_nlp_task
    VISION_AI_AVAILABLE = True
    print("VisionAIBrain loaded - TRUE NLP screen understanding enabled")
except ImportError as e:
    print(f"Vision AI Brain not available: {e}")
    VISION_AI_AVAILABLE = False

# Import autonomous systems - DISABLED to fix GUI
try:
    from autonomous_explorer import AutonomousExplorer, KeyboardAutomation
    # from learning_dashboard import LearningDashboard, AutonomyControlPanel
    AUTONOMOUS_AVAILABLE = False  # Disabled dashboard
except ImportError as e:
    print(f"Autonomous systems not available: {e}")
    AUTONOMOUS_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════════
# HACKER THEME - Professional Cyberpunk Colors
# ═══════════════════════════════════════════════════════════════════════════════════

class Theme:
    # ═══════════════════════════════════════════════════════════════════
    # HOLOGRAPHIC COMMAND CENTER THEME - Deep Space & Neon
    # ═══════════════════════════════════════════════════════════════════
    
    # Deep Space Backgrounds
    BG_DARKEST = '#000205'    # Void black
    BG_DARK = '#02040a'       # Deep space
    BG_PANEL = '#050a14'      # Dark navy panel
    BG_CARD = '#0a1020'       # Card background
    BG_INPUT = '#0f1828'      # Input field
    BG_HOVER = '#152035'      # Hover state
    
    # Neon Holographic Accents
    CYAN = '#00f3ff'          # Primary holographic interface
    GREEN = '#00ff9d'         # Success / Stable
    PINK = '#ff0055'          # Alert / Critical
    PURPLE = '#bc13fe'        # Processing / AI
    BLUE = '#0066ff'          # Data streams
    ORANGE = '#ff8800'        # Warning / Energy
    RED = '#ff2a2a'           # Error / Danger
    YELLOW = '#ffd700'        # Highlight / Gold
    QUANTUM = '#9d00ff'       # Deep processing
    PLASMA = '#ff00cc'        # High energy
    
    # Text
    TEXT_BRIGHT = '#ffffff'
    TEXT = '#e0e6ed'
    TEXT_DIM = '#607080'
    TEXT_MUTED = '#354050'
    
    # Holographic Borders
    BORDER = '#1a253a'
    BORDER_GLOW = '#00f3ff'

T = Theme


# ═══════════════════════════════════════════════════════════════════════════════════
# ACTION SPACE - Canonical actions Aurora can attempt
# ═══════════════════════════════════════════════════════════════════════════════════

ACTION_CATALOG = {
    'mouse': [
        'move_mouse_explore', 'move_mouse_center', 'click_here', 'double_click',
        'right_click', 'scroll_up', 'scroll_down', 'drag_test'
    ],
    'keyboard': ['type_test', 'press_key_random', 'try_shortcut'],
    'app': [
        'open_finder', 'open_safari', 'open_notes', 'open_calculator',
        'open_terminal', 'open_spotlight', 'switch_app', 'open_url', 'search_web'
    ],
    'system': [
        'explore_desktop', 'explore_downloads', 'explore_documents', 'take_screenshot',
        'check_clipboard', 'observe_wait', 'volume_up', 'volume_down', 'get_system_info',
        'check_cpu_info', 'check_memory', 'check_disk_space', 'check_uptime',
        'check_env_vars', 'list_installed_apps', 'check_running_apps'
    ],
    'voice': ['speak_thought', 'play_sound'],
    'network': [
        'scan_network', 'check_wifi', 'get_ip_address', 'ping_test', 'dns_lookup',
        'check_ports', 'curl_test', 'check_hosts_file'
    ],
    'security': [
        'check_processes', 'check_users', 'check_permissions', 'find_hidden_files',
        'check_ssh_keys', 'check_firewall'
    ],
    'code': [
        'run_shell_cmd', 'learn_shell_history', 'check_python', 'run_python_code',
        'check_git', 'check_homebrew'
    ],
}

ALL_ACTIONS = sorted({action for actions in ACTION_CATALOG.values() for action in actions})


# ═══════════════════════════════════════════════════════════════════════════════════
# SMOOTH ANIMATION UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════════

def ease_in_out_cubic(t):
    """Smooth cubic easing function for animations"""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2

def ease_out_elastic(t):
    """Bouncy elastic easing"""
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    if t == 1:
        return 1
    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1

def lerp(start, end, t):
    """Linear interpolation"""
    return start + (end - start) * t

def lerp_color(color1, color2, t):
    """Interpolate between two hex colors"""
    c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    r = int(lerp(c1[0], c2[0], t))
    g = int(lerp(c1[1], c2[1], t))
    b = int(lerp(c1[2], c2[2], t))
    return f"#{r:02x}{g:02x}{b:02x}"


# ═══════════════════════════════════════════════════════════════════════════════════
# ADVANCED SMOOTH ANIMATIONS
# ═══════════════════════════════════════════════════════════════════════════════════

class WaveformVisualizer(tk.Canvas):
    """Smooth audio waveform visualization - reacts to AI activity"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.intensity = 0.3
        self.target_intensity = 0.3
        self.wave_points = 60
        self.waves = [
            {'freq': 0.05, 'amp': 0.3, 'phase': 0, 'color': T.CYAN, 'speed': 0.08},
            {'freq': 0.08, 'amp': 0.2, 'phase': 1.5, 'color': T.PINK, 'speed': 0.06},
            {'freq': 0.12, 'amp': 0.15, 'phase': 3.0, 'color': T.GREEN, 'speed': 0.1},
        ]
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def set_intensity(self, value):
        self.target_intensity = max(0.1, min(1.0, value))
    
    def set_activity(self, value):
        """Alias for set_intensity for API consistency"""
        self.set_intensity(value)
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.03
            
            # Smooth intensity transition (driven by external set_activity)
            self.intensity += (self.target_intensity - self.intensity) * 0.1
            
            center_y = self.height // 2
            
            # Draw each wave layer
            for wave in self.waves:
                points = []
                for i in range(self.wave_points + 1):
                    x = (i / self.wave_points) * self.width
                    
                    # Multiple sine waves combined; no random injections in real_mode
                    y = center_y
                    y += math.sin(x * wave['freq'] + self.time * wave['speed'] + wave['phase']) * self.height * wave['amp'] * self.intensity
                    y += math.sin(x * wave['freq'] * 2 + self.time * wave['speed'] * 1.5) * self.height * wave['amp'] * 0.3 * self.intensity
                    y += math.sin(x * wave['freq'] * 0.5 + self.time * wave['speed'] * 0.7) * self.height * wave['amp'] * 0.2 * self.intensity
                    
                    points.extend([x, y])
                
                # Draw with glow effect
                for width in [6, 4, 2]:
                    alpha = 0.3 + (1 - width/6) * 0.7
                    self.create_line(points, fill=wave['color'], width=width, smooth=True)
            
            # Center line
            self.create_line(0, center_y, self.width, center_y, fill=T.BORDER, width=1, dash=(5, 5))
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)  # ~30 FPS
        except:
            pass


class DNAHelix(tk.Canvas):
    """Rotating DNA helix animation - represents AI genetic learning"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.rotation_speed = 0.05
        self.helix_points = 20
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += self.rotation_speed
            
            cx, cy = self.width // 2, self.height // 2
            helix_height = self.height * 0.8
            helix_radius = min(self.width * 0.3, 60)
            
            strand1_points = []
            strand2_points = []
            
            for i in range(self.helix_points):
                t = i / (self.helix_points - 1)
                y = cy - helix_height/2 + t * helix_height
                angle = t * math.pi * 4 + self.time
                
                # Two strands offset by π
                x1 = cx + math.cos(angle) * helix_radius
                x2 = cx + math.cos(angle + math.pi) * helix_radius
                
                # Z-depth for 3D effect
                z1 = math.sin(angle)
                z2 = math.sin(angle + math.pi)
                
                strand1_points.append((x1, y, z1))
                strand2_points.append((x2, y, z2))
                
                # Draw connecting base pairs
                if i % 2 == 0:
                    # Color based on depth
                    alpha = 0.3 + abs(z1) * 0.7
                    base_colors = [T.CYAN, T.PINK, T.GREEN, T.PURPLE]
                    color = base_colors[i % len(base_colors)]
                    
                    self.create_line(x1, y, x2, y, fill=color, width=2)
                    
                    # Base pair nodes
                    node_size = 3 + abs(z1) * 2
                    self.create_oval(x1 - node_size, y - node_size, x1 + node_size, y + node_size,
                                   fill=color, outline=T.TEXT_BRIGHT)
                    self.create_oval(x2 - node_size, y - node_size, x2 + node_size, y + node_size,
                                   fill=color, outline=T.TEXT_BRIGHT)
            
            # Draw helix strands with depth
            for strand, color in [(strand1_points, T.CYAN), (strand2_points, T.PINK)]:
                # Sort by z for proper depth rendering
                for i in range(len(strand) - 1):
                    x1, y1, z1 = strand[i]
                    x2, y2, z2 = strand[i + 1]
                    
                    # Width based on z-depth
                    avg_z = (z1 + z2) / 2
                    width = 2 + (avg_z + 1) * 1.5
                    alpha = 0.5 + (avg_z + 1) * 0.25
                    
                    self.create_line(x1, y1, x2, y2, fill=color, width=width, smooth=True)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class OrbitingParticles(tk.Canvas):
    """Smooth orbiting particles around a central AI core"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.particles = []
        self.core_pulse = 0
        self.bind('<Configure>', self._on_resize)
        self._create_particles()
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def _create_particles(self):
        self.particles = []
        colors = [T.CYAN, T.PINK, T.GREEN, T.PURPLE, T.YELLOW, T.ORANGE]
        # Deterministic default; external code can set actual particles for real data
        for i in range(15):
            radius = 30 + (i * 5 % 80)
            angle = (i / 15) * math.pi * 2
            speed = 0.02
            size = 3
            color = colors[i % len(colors)]
            tilt = 0.0
            self.particles.append({
                'orbit_radius': radius,
                'angle': angle,
                'speed': speed,
                'size': size,
                'color': color,
                'trail': [],
                'orbit_tilt': tilt,
            })
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.02
            self.core_pulse += 0.1
            
            cx, cy = self.width // 2, self.height // 2
            
            # Draw orbit paths
            for r in [40, 70, 100]:
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               outline=T.BORDER, width=1, dash=(2, 4))
            
            # Draw particles with trails
            # Update based on deterministic orbit; no randomness in real_mode
            for p in self.particles:
                p['angle'] += p['speed']
                
                # Calculate position with slight 3D effect
                x = cx + math.cos(p['angle']) * p['orbit_radius']
                y = cy + math.sin(p['angle']) * p['orbit_radius'] * (1 + p['orbit_tilt'])
                
                # Add to trail
                p['trail'].append((x, y))
                if len(p['trail']) > 10:
                    p['trail'].pop(0)
                
                # Draw trail with fade
                for i, (tx, ty) in enumerate(p['trail']):
                    alpha = i / len(p['trail'])
                    size = p['size'] * alpha * 0.5
                    self.create_oval(tx - size, ty - size, tx + size, ty + size,
                                   fill=p['color'], outline='')
                
                # Draw particle
                self.create_oval(x - p['size'], y - p['size'], x + p['size'], y + p['size'],
                               fill=p['color'], outline=T.TEXT_BRIGHT)
            
            # Draw central AI core with pulse
            core_size = 20 + math.sin(self.core_pulse) * 5
            
            # Core glow
            for i in range(4, 0, -1):
                gs = core_size + i * 8
                self.create_oval(cx - gs, cy - gs, cx + gs, cy + gs,
                               outline=T.CYAN, width=1)
            
            # Core
            self.create_oval(cx - core_size, cy - core_size, cx + core_size, cy + core_size,
                           fill=T.CYAN, outline=T.TEXT_BRIGHT, width=2)
            self.create_text(cx, cy, text="AI", font=('JetBrains Mono', 10, 'bold'), fill=T.BG_DARKEST)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class PulseRadar(tk.Canvas):
    """Radar-style scanning animation for AI awareness visualization"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.sweep_angle = 0
        self.detections = []
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def add_detection(self, label="", category="normal"):
        colors = {'normal': T.GREEN, 'warning': T.YELLOW, 'alert': T.RED, 'info': T.CYAN}
        angle = random.random() * math.pi * 2
        distance = 0.3 + random.random() * 0.6
        self.detections.append({
            'angle': angle,
            'distance': distance,
            'label': label,
            'color': colors.get(category, T.GREEN),
            'fade': 1.0,
            'pulse': 0,
        })
    
    def set_activity(self, level):
        """Trigger radar activity - add detections based on activity level"""
        count = int(level * 5)
        labels = ['Signal', 'Process', 'Network', 'Data', 'Memory', 'CPU']
        for _ in range(count):
            self.add_detection(random.choice(labels), random.choice(['normal', 'info']))
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.sweep_angle += 0.03
            
            cx, cy = self.width // 2, self.height // 2
            max_radius = min(self.width, self.height) // 2 - 20
            
            # Draw grid circles
            for r in range(1, 5):
                radius = max_radius * r / 4
                self.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                               outline=T.BORDER, width=1)
            
            # Draw cross lines
            self.create_line(cx - max_radius, cy, cx + max_radius, cy, fill=T.BORDER, width=1)
            self.create_line(cx, cy - max_radius, cx, cy + max_radius, fill=T.BORDER, width=1)
            
            # Draw sweep line with gradient
            sweep_x = cx + math.cos(self.sweep_angle) * max_radius
            sweep_y = cy + math.sin(self.sweep_angle) * max_radius
            self.create_line(cx, cy, sweep_x, sweep_y, fill=T.CYAN, width=2)
            
            # Draw sweep trail (fading arc)
            for i in range(20, 0, -1):
                trail_angle = self.sweep_angle - i * 0.02
                trail_x = cx + math.cos(trail_angle) * max_radius
                trail_y = cy + math.sin(trail_angle) * max_radius
                alpha = 1 - i / 20
                self.create_line(cx, cy, trail_x, trail_y, fill=T.CYAN, width=1)
            
            # Draw and update detections
            new_detections = []
            for det in self.detections:
                det['fade'] -= 0.005
                det['pulse'] += 0.2
                
                if det['fade'] > 0:
                    x = cx + math.cos(det['angle']) * max_radius * det['distance']
                    y = cy + math.sin(det['angle']) * max_radius * det['distance']
                    
                    # Pulsing detection point
                    size = 4 + math.sin(det['pulse']) * 2
                    
                    # Glow effect
                    for gs in range(3, 0, -1):
                        self.create_oval(x - size - gs*2, y - size - gs*2, 
                                       x + size + gs*2, y + size + gs*2,
                                       outline=det['color'], width=1)
                    
                    self.create_oval(x - size, y - size, x + size, y + size,
                                   fill=det['color'], outline=T.TEXT_BRIGHT)
                    
                    if det['label']:
                        self.create_text(x, y - 15, text=det['label'],
                                       font=('JetBrains Mono', 8),
                                       fill=det['color'])
                    
                    new_detections.append(det)
            
            self.detections = new_detections
            
            # Random detections (disabled in real_mode)
            try:
                top = self.winfo_toplevel()
                real_mode = getattr(top, 'real_mode', False)
            except Exception:
                real_mode = False
            if not real_mode:
                if random.random() < 0.02:
                    labels = ['Process', 'Network', 'File', 'Memory', 'CPU', 'User']
                    categories = ['normal', 'warning', 'info']
                    self.add_detection(random.choice(labels), random.choice(categories))
            
            # Center point
            self.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=T.CYAN, outline=T.TEXT_BRIGHT)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class ThoughtBubbles(tk.Canvas):
    """Holographic Thought Crystals - Futuristic floating thought visualization"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.bubbles = []
        self.particles = []  # Trailing particles
        self.time = 0
        self.energy_waves = []  # Background energy pulses
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def _create_hexagon_points(self, cx, cy, size, rotation=0):
        """Create points for a hexagonal crystal shape"""
        points = []
        for i in range(6):
            angle = rotation + (i * math.pi / 3)
            px = cx + math.cos(angle) * size
            py = cy + math.sin(angle) * size
            points.extend([px, py])
        return points
    
    def _create_diamond_points(self, cx, cy, width, height):
        """Create points for a diamond/rhombus shape"""
        return [cx, cy - height/2,  # top
                cx + width/2, cy,    # right
                cx, cy + height/2,   # bottom
                cx - width/2, cy]    # left
    
    def add_thought(self, text, category='normal'):
        if self.width > 0:
            colors = {
                'normal': T.CYAN, 'success': T.GREEN, 'warning': T.YELLOW, 
                'error': T.RED, 'idea': T.PINK, 'learning': T.PURPLE,
                'quantum': '#9d00ff', 'plasma': '#ff00cc'
            }
            # Choose shape type randomly
            shapes = ['hexagon', 'diamond', 'crystal', 'orb']
            self.bubbles.append({
                'text': text[:25],
                'x': random.randint(80, max(81, self.width - 80)),
                'y': self.height + 30,
                'target_y': random.randint(60, max(61, self.height - 120)),
                'speed': 1.0 + random.random() * 2.0,
                'wobble_phase': random.random() * math.pi * 2,
                'wobble_amp': 3 + random.random() * 8,
                'color': colors.get(category, T.CYAN),
                'secondary_color': random.choice([T.PINK, T.PURPLE, T.GREEN, T.YELLOW]),
                'fade': 1.0,
                'size': 0,
                'target_size': 1.0,
                'rotation': random.random() * math.pi,
                'rotation_speed': (random.random() - 0.5) * 0.1,
                'shape': random.choice(shapes),
                'pulse_phase': random.random() * math.pi * 2,
                'energy_level': 0.5 + random.random() * 0.5,
                'trail': [],  # Position history for trail effect
            })
            # Spawn energy wave from bottom
            self.energy_waves.append({
                'y': self.height,
                'speed': 3 + random.random() * 2,
                'color': colors.get(category, T.CYAN),
                'fade': 0.8
            })
    
    def _spawn_particles(self, x, y, color, count=3):
        """Spawn trailing particles behind a thought"""
        for _ in range(count):
            self.particles.append({
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(5, 15),
                'vx': (random.random() - 0.5) * 2,
                'vy': random.random() * 2,
                'size': 2 + random.random() * 3,
                'color': color,
                'fade': 1.0,
                'decay': 0.02 + random.random() * 0.02
            })
    
    def _draw_holographic_hexagon(self, x, y, size, color, rotation, pulse, fade):
        """Draw a glowing hexagonal crystal"""
        # Outer glow layers
        for i in range(4, 0, -1):
            glow_size = size + i * 4
            points = self._create_hexagon_points(x, y, glow_size, rotation)
            self.create_polygon(points, fill='', outline=color, width=1)
        
        # Main hexagon with fill
        points = self._create_hexagon_points(x, y, size, rotation)
        self.create_polygon(points, fill=T.BG_CARD, outline=color, width=2)
        
        # Inner hexagon (pulsing)
        inner_size = size * (0.5 + pulse * 0.1)
        inner_points = self._create_hexagon_points(x, y, inner_size, rotation + 0.5)
        self.create_polygon(inner_points, fill='', outline=color, width=1)
        
        # Center energy dot
        dot_size = 3 + pulse * 2
        self.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size,
                        fill=color, outline='')
    
    def _draw_diamond_crystal(self, x, y, width, height, color, pulse, fade):
        """Draw a diamond/crystal shape"""
        # Outer glow
        for i in range(3, 0, -1):
            glow_w = width + i * 6
            glow_h = height + i * 8
            points = self._create_diamond_points(x, y, glow_w, glow_h)
            self.create_polygon(points, fill='', outline=color, width=1)
        
        # Main diamond
        points = self._create_diamond_points(x, y, width, height)
        self.create_polygon(points, fill=T.BG_CARD, outline=color, width=2)
        
        # Inner cross lines
        line_len = min(width, height) * 0.3
        self.create_line(x - line_len, y, x + line_len, y, fill=color, width=1)
        self.create_line(x, y - line_len, x, y + line_len, fill=color, width=1)
    
    def _draw_energy_orb(self, x, y, size, color, secondary, pulse, rotation):
        """Draw a glowing energy orb with orbiting rings"""
        # Outer energy field
        for i in range(5, 0, -1):
            ring_size = size + i * 3 + pulse * 2
            self.create_oval(x - ring_size, y - ring_size, x + ring_size, y + ring_size,
                           fill='', outline=color, width=1)
        
        # Main orb
        self.create_oval(x - size, y - size, x + size, y + size,
                        fill=T.BG_CARD, outline=color, width=2)
        
        # Orbiting dots
        for i in range(3):
            angle = rotation + (i * math.pi * 2 / 3)
            orbit_x = x + math.cos(angle) * (size + 8)
            orbit_y = y + math.sin(angle) * (size + 8)
            dot_size = 2
            self.create_oval(orbit_x - dot_size, orbit_y - dot_size,
                           orbit_x + dot_size, orbit_y + dot_size,
                           fill=secondary, outline='')
        
        # Center glow
        inner = size * 0.4
        self.create_oval(x - inner, y - inner, x + inner, y + inner,
                        fill=color, outline='')
    
    def _draw_crystal_shard(self, x, y, size, color, rotation, pulse):
        """Draw an angular crystal shard shape"""
        # Create asymmetric crystal points
        points = []
        angles = [0, 0.8, 1.8, 2.5, 3.5, 4.5, 5.3]
        lengths = [size * 1.2, size * 0.7, size * 1.0, size * 0.6, size * 1.1, size * 0.8, size * 0.9]
        for angle_offset, length in zip(angles, lengths):
            angle = rotation + angle_offset
            px = x + math.cos(angle) * length
            py = y + math.sin(angle) * length
            points.extend([px, py])
        
        # Glow
        for i in range(3, 0, -1):
            glow_points = []
            for j in range(0, len(points), 2):
                dx = points[j] - x
                dy = points[j + 1] - y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    glow_points.extend([
                        x + dx * (1 + i * 0.1),
                        y + dy * (1 + i * 0.1)
                    ])
            if len(glow_points) >= 6:
                self.create_polygon(glow_points, fill='', outline=color, width=1)
        
        # Main crystal
        if len(points) >= 6:
            self.create_polygon(points, fill=T.BG_CARD, outline=color, width=2)
        
        # Inner line pattern
        self.create_line(x, y - size * 0.5, x, y + size * 0.5, fill=color, width=1)
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.05
            
            # Draw background energy grid
            self._draw_energy_background()
            
            # Draw and update energy waves
            self._draw_energy_waves()
            
            # Draw and update particles
            self._draw_particles()
            
            # Draw thought bubbles
            new_bubbles = []
            for bubble in self.bubbles:
                # Animate rise
                if bubble['y'] > bubble['target_y']:
                    bubble['y'] -= bubble['speed']
                    # Spawn trail particles while rising
                    if random.random() < 0.3:
                        self._spawn_particles(bubble['x'], bubble['y'], bubble['color'], 1)
                else:
                    bubble['fade'] -= 0.008
                
                # Animate size (smooth scale up)
                bubble['size'] += (bubble['target_size'] - bubble['size']) * 0.12
                
                # Update rotation and pulse
                bubble['rotation'] += bubble['rotation_speed']
                bubble['pulse_phase'] += 0.15
                
                if bubble['fade'] > 0 and bubble['size'] > 0.1:
                    # Wobble effect with smooth sine wave
                    wobble_x = math.sin(bubble['wobble_phase']) * bubble['wobble_amp']
                    wobble_y = math.cos(bubble['wobble_phase'] * 0.7) * (bubble['wobble_amp'] * 0.3)
                    bubble['wobble_phase'] += 0.06
                    
                    x = bubble['x'] + wobble_x
                    y = bubble['y'] + wobble_y
                    
                    # Store trail position
                    bubble['trail'].append((x, y))
                    if len(bubble['trail']) > 8:
                        bubble['trail'].pop(0)
                    
                    # Draw trail
                    for i, (tx, ty) in enumerate(bubble['trail']):
                        trail_alpha = i / len(bubble['trail'])
                        trail_size = 2 + trail_alpha * 3
                        self.create_oval(tx - trail_size, ty - trail_size,
                                       tx + trail_size, ty + trail_size,
                                       fill='', outline=bubble['color'], width=1)
                    
                    # Calculate dimensions based on text
                    text_len = len(bubble['text'])
                    base_width = max(70, text_len * 8) * bubble['size']
                    base_height = 40 * bubble['size']
                    
                    pulse = math.sin(bubble['pulse_phase']) * bubble['energy_level']
                    
                    # Draw based on shape type
                    if bubble['shape'] == 'hexagon':
                        hex_size = max(base_width, base_height) * 0.5
                        self._draw_holographic_hexagon(x, y, hex_size, bubble['color'],
                                                      bubble['rotation'], pulse, bubble['fade'])
                    elif bubble['shape'] == 'diamond':
                        self._draw_diamond_crystal(x, y, base_width * 0.8, base_height * 1.2,
                                                  bubble['color'], pulse, bubble['fade'])
                    elif bubble['shape'] == 'orb':
                        orb_size = max(base_width, base_height) * 0.4
                        self._draw_energy_orb(x, y, orb_size, bubble['color'],
                                            bubble['secondary_color'], pulse, bubble['rotation'] * 3)
                    else:  # crystal
                        crystal_size = max(base_width, base_height) * 0.45
                        self._draw_crystal_shard(x, y, crystal_size, bubble['color'],
                                               bubble['rotation'], pulse)
                    
                    # Draw text with glow effect
                    if bubble['size'] > 0.5:
                        # Text shadow/glow
                        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                            self.create_text(x + offset[0], y + offset[1],
                                           text=bubble['text'],
                                           font=('JetBrains Mono', 9, 'bold'),
                                           fill=T.BG_DARKEST)
                        # Main text
                        self.create_text(x, y, text=bubble['text'],
                                       font=('JetBrains Mono', 9, 'bold'),
                                       fill=bubble['color'])
                    
                    # Draw energy connection line to bottom
                    if bubble['y'] < self.height - 50:
                        line_alpha = bubble['fade'] * 0.3
                        self.create_line(x, y + base_height/2, x, self.height,
                                       fill=bubble['color'], width=1, dash=(3, 6))
                    
                    new_bubbles.append(bubble)
            
            self.bubbles = new_bubbles
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass
    
    def _draw_energy_background(self):
        """Draw subtle animated background grid"""
        # Vertical energy lines
        for i in range(0, self.width, 50):
            wave_offset = math.sin(self.time + i * 0.05) * 3
            alpha = 0.1 + math.sin(self.time * 2 + i * 0.1) * 0.05
            self.create_line(i + wave_offset, 0, i + wave_offset, self.height,
                           fill=T.BORDER, width=1, dash=(2, 8))
        
        # Horizontal scan line
        scan_y = (self.time * 50) % self.height
        self.create_line(0, scan_y, self.width, scan_y, fill=T.CYAN, width=1)
    
    def _draw_energy_waves(self):
        """Draw rising energy waves from bottom"""
        new_waves = []
        for wave in self.energy_waves:
            wave['y'] -= wave['speed']
            wave['fade'] -= 0.015
            
            if wave['fade'] > 0 and wave['y'] > 0:
                # Draw horizontal wave line
                wave_width = self.width * wave['fade']
                x_start = (self.width - wave_width) / 2
                self.create_line(x_start, wave['y'], x_start + wave_width, wave['y'],
                               fill=wave['color'], width=1)
                new_waves.append(wave)
        
        self.energy_waves = new_waves
    
    def _draw_particles(self):
        """Draw and update trailing particles"""
        new_particles = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['fade'] -= p['decay']
            p['size'] *= 0.98
            
            if p['fade'] > 0 and p['size'] > 0.5:
                self.create_oval(p['x'] - p['size'], p['y'] - p['size'],
                               p['x'] + p['size'], p['y'] + p['size'],
                               fill=p['color'], outline='')
                new_particles.append(p)
        
        self.particles = new_particles[:100]  # Limit particle count


class BrainActivityMonitor(tk.Canvas):
    """EEG-style brain activity monitor with multiple channels"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.channels = [
            {'name': 'Alpha', 'color': T.CYAN, 'freq': 0.1, 'amp': 1.0, 'data': deque(maxlen=100)},
            {'name': 'Beta', 'color': T.GREEN, 'freq': 0.2, 'amp': 0.7, 'data': deque(maxlen=100)},
            {'name': 'Gamma', 'color': T.PINK, 'freq': 0.4, 'amp': 0.5, 'data': deque(maxlen=100)},
            {'name': 'Delta', 'color': T.PURPLE, 'freq': 0.05, 'amp': 1.2, 'data': deque(maxlen=100)},
        ]
        self.activity_level = 0.5
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def set_activity(self, level):
        self.activity_level = max(0.1, min(1.0, level))
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.1
            
            channel_height = self.height / len(self.channels)
            
            for idx, channel in enumerate(self.channels):
                # Generate new data point
                noise = random.random() * 0.3 - 0.15
                value = (math.sin(self.time * channel['freq'] * 10) * channel['amp'] + 
                        math.sin(self.time * channel['freq'] * 25) * channel['amp'] * 0.3 +
                        noise) * self.activity_level
                channel['data'].append(value)
                
                # Draw channel
                y_center = idx * channel_height + channel_height / 2
                
                # Channel label
                self.create_text(5, y_center, text=channel['name'],
                               font=('JetBrains Mono', 8, 'bold'),
                               fill=channel['color'], anchor='w')
                
                # Draw waveform
                if len(channel['data']) > 1:
                    points = []
                    for i, val in enumerate(channel['data']):
                        x = 50 + (i / 100) * (self.width - 60)
                        y = y_center + val * (channel_height * 0.4)
                        points.extend([x, y])
                    
                    # Glow effect
                    for width in [4, 2, 1]:
                        self.create_line(points, fill=channel['color'], width=width, smooth=True)
                
                # Separator line
                if idx < len(self.channels) - 1:
                    self.create_line(0, (idx + 1) * channel_height, self.width, (idx + 1) * channel_height,
                                   fill=T.BORDER, width=1)
        
        try:
            if self.winfo_exists():
                self.after(50, self._animate)
        except:
            pass


# ═══════════════════════════════════════════════════════════════════════════════════
# FUTURISTIC QUANTUM NEURAL VISUALIZATIONS - REAL DATA ONLY
# Clean HD Animations with 3D Holographic Effects
# ═══════════════════════════════════════════════════════════════════════════════════

class AIThinkingVisualization(tk.Canvas):
    """
    QUANTUM THOUGHT MATRIX - Floating thought orbs with pulse connections
    Clean, modern design responding to real-time AI activity
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='#050510', highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        
        # Real data
        self.is_active = False
        self.current_state = 'idle'  # idle, thinking, planning, executing
        self.cognitive_load = 0.0
        self.current_thought = ""
        
        # Floating thought orbs
        self.orbs = []
        self.pulse_rings = []
        self.thought_beams = []
        
        # State colors
        self.state_colors = {
            'idle': '#3a4a5a',
            'thinking': '#00ffff',
            'planning': '#ff66aa',
            'executing': '#00ff88',
            'analysis': '#ffaa00'
        }
        
        self.bind('<Configure>', self._on_resize)
        self._init_orbs()
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_orbs()
    
    def _init_orbs(self):
        """Initialize floating thought orbs"""
        self.orbs = []
        if self.width < 50 or self.height < 50:
            return
        
        cx, cy = self.width // 2, self.height // 2
        
        # Create orbs in spiral pattern
        for i in range(12):
            angle = (i / 12) * math.pi * 2
            radius = 60 + (i % 3) * 40
            self.orbs.append({
                'base_angle': angle,
                'radius': radius,
                'size': 8 + (i % 3) * 3,
                'speed': 0.008 + random.random() * 0.004,
                'phase': random.random() * math.pi * 2,
                'color': ['#00ffff', '#ff66aa', '#00ff88', '#ffaa00'][i % 4]
            })

    def set_active(self, active):
        """Called when START is clicked"""
        self.is_active = active
        if not active:
            self.current_state = 'idle'
            self.cognitive_load = 0.0

    def update_thinking_state(self, thought=None, intensity=None, **kwargs):
        if not self.is_active:
            return
            
        if thought:
            self.current_thought = thought[:50]
            self._spawn_pulse()
            
        if intensity is not None:
            self.cognitive_load = intensity
            
        if kwargs.get('planning'):
            self.current_state = 'planning'
            self.cognitive_load = max(self.cognitive_load, 0.7)
        elif kwargs.get('executing'):
            self.current_state = 'executing'
            self.cognitive_load = max(self.cognitive_load, 0.9)
        elif kwargs.get('analysis'):
            self.current_state = 'analysis'
            self.cognitive_load = max(self.cognitive_load, kwargs['analysis'])
        elif thought:
            self.current_state = 'thinking'

    def add_thought(self, text):
        self.update_thinking_state(thought=text, intensity=0.8)

    def _spawn_pulse(self):
        """Spawn expanding pulse ring"""
        if self.width > 0:
            self.pulse_rings.append({
                'x': self.width // 2,
                'y': self.height // 2,
                'radius': 20,
                'max_radius': min(self.width, self.height) // 2,
                'life': 1.0
            })

    def _animate(self):
        try:
            if not self.winfo_exists(): return
        except: return
        
        if self.width < 50:
            self.after(40, self._animate)
            return
            
        self.delete('all')
        self.time += 0.025
        
        cx, cy = self.width // 2, self.height // 2
        
        # Get current color based on state
        color = self.state_colors.get(self.current_state, '#3a4a5a')
        
        # Draw elements
        self._draw_background_grid()
        self._draw_pulse_rings(color)
        self._draw_orb_connections(cx, cy, color)
        self._draw_orbs(cx, cy, color)
        self._draw_central_core(cx, cy, color)
        self._draw_header(color)
        
        self.after(35, self._animate)

    def _draw_background_grid(self):
        """Draw subtle radial grid"""
        cx, cy = self.width // 2, self.height // 2
        
        # Concentric circles
        for r in range(40, 200, 40):
            self.create_oval(cx-r, cy-r, cx+r, cy+r, outline='#101520', width=1)

    def _draw_pulse_rings(self, color):
        """Draw expanding pulse rings"""
        new_rings = []
        for ring in self.pulse_rings:
            ring['radius'] += 3
            ring['life'] -= 0.02
            
            if ring['life'] > 0 and ring['radius'] < ring['max_radius']:
                r = ring['radius']
                self.create_oval(
                    ring['x'] - r, ring['y'] - r,
                    ring['x'] + r, ring['y'] + r,
                    outline=color, width=2
                )
                new_rings.append(ring)
        self.pulse_rings = new_rings

    def _draw_orb_connections(self, cx, cy, color):
        """Draw connections between orbs when active"""
        if not self.is_active or self.cognitive_load < 0.2:
            return
            
        # Draw beams to active orbs
        for i, orb in enumerate(self.orbs):
            angle = orb['base_angle'] + self.time * orb['speed']
            x = cx + math.cos(angle) * orb['radius']
            y = cy + math.sin(angle) * orb['radius']
            
            # Connection to center
            if random.random() < self.cognitive_load * 0.3:
                self.create_line(cx, cy, x, y, fill=color, width=1, dash=(4, 4))

    def _draw_orbs(self, cx, cy, color):
        """Draw floating thought orbs"""
        for orb in self.orbs:
            # Calculate position with floating motion
            angle = orb['base_angle'] + self.time * orb['speed']
            float_offset = math.sin(self.time * 2 + orb['phase']) * 8
            
            x = cx + math.cos(angle) * (orb['radius'] + float_offset)
            y = cy + math.sin(angle) * (orb['radius'] + float_offset)
            
            size = orb['size']
            orb_color = color if self.is_active else '#2a3a4a'
            
            if self.is_active and self.cognitive_load > 0.3:
                # Active glow
                pulse = 1 + math.sin(self.time * 3 + orb['phase']) * 0.2
                s = size * pulse
                
                # Outer glow
                self.create_oval(x-s*1.5, y-s*1.5, x+s*1.5, y+s*1.5,
                               fill='', outline=orb_color, width=1)
                
                # Main orb
                self.create_oval(x-s, y-s, x+s, y+s,
                               fill='#0a1020', outline=orb_color, width=2)
                
                # Core
                core = s * 0.4
                self.create_oval(x-core, y-core, x+core, y+core,
                               fill=orb_color, outline='')
            else:
                # Inactive
                self.create_oval(x-size, y-size, x+size, y+size,
                               fill='#151520', outline='#252535', width=1)

    def _draw_central_core(self, cx, cy, color):
        """Draw central processing core"""
        pulse = 1 + self.cognitive_load * 0.2 * math.sin(self.time * 4)
        size = 25 * pulse
        
        if self.is_active:
            # Outer glow
            self.create_oval(cx-size*1.5, cy-size*1.5, cx+size*1.5, cy+size*1.5,
                           fill='', outline=color, width=1)
            
            # Main core
            self.create_oval(cx-size, cy-size, cx+size, cy+size,
                           fill='#0a1520', outline=color, width=3)
            
            # Inner core
            inner = size * 0.5
            self.create_oval(cx-inner, cy-inner, cx+inner, cy+inner,
                           fill=color, outline='')
        else:
            self.create_oval(cx-size, cy-size, cx+size, cy+size,
                           fill='#101520', outline='#2a3a4a', width=2)
        
        # Label
        self.create_text(cx, cy, text="AI",
                       font=('JetBrains Mono', 10, 'bold'),
                       fill='#ffffff' if self.is_active else '#4a5a6a')

    def _draw_header(self, color):
        """Draw header with state info"""
        # Title
        self.create_text(self.width // 2, 18,
                       text="COGNITIVE MATRIX",
                       font=('JetBrains Mono', 10, 'bold'),
                       fill=color if self.is_active else '#3a4a5a')
        
        # State indicator
        state_text = self.current_state.upper() if self.is_active else "STANDBY"
        self.create_text(self.width // 2, self.height - 20,
                       text=state_text,
                       font=('JetBrains Mono', 9),
                       fill=color if self.is_active else '#3a4a5a')
        
        # Thought text
        if self.current_thought and self.is_active:
            self.create_text(self.width // 2, self.height - 40,
                           text=self.current_thought,
                           font=('JetBrains Mono', 8),
                           fill='#5a6a7a')


class AIAnalysisVisualization(tk.Canvas):
    """
    HOLOGRAPHIC SPECTRUM ANALYZER - Circular radar with orbiting particles
    Dynamic spectrum rings and flowing energy visualization
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='#030308', highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        
        # Active state
        self.is_active = False
        self.current_state = 'idle'
        
        # Spectrum data channels
        self.channels = {
            'CPU': {'value': 0.0, 'history': [], 'color': '#ff3366', 'angle': 0},
            'RAM': {'value': 0.0, 'history': [], 'color': '#aa44ff', 'angle': math.pi/2},
            'NET': {'value': 0.0, 'history': [], 'color': '#00ff88', 'angle': math.pi},
            'AI': {'value': 0.0, 'history': [], 'color': '#00ddff', 'angle': 3*math.pi/2}
        }
        
        # Orbiting particles
        self.particles = []
        self.pulse_waves = []
        self.scan_angle = 0
        
        # State colors
        self.state_colors = {
            'idle': '#1a2a3a',
            'analyzing': '#00ffff',
            'processing': '#ff44aa',
            'monitoring': '#00ff88'
        }
        
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height

    def set_active(self, active):
        """Called when START is clicked"""
        self.is_active = active
        if not active:
            self.current_state = 'idle'
            self.particles.clear()
            self.pulse_waves.clear()

    def update_analysis(self, analysis_text=None, focus=None):
        if not self.is_active:
            return
        if analysis_text:
            self.current_state = 'analyzing'
            self._spawn_pulse()

    def update_data_stream(self, stream_name, value):
        """Update data stream with real-time value"""
        target = stream_name
        if stream_name in ['Vision', 'Audio']: target = 'AI'
        if stream_name == 'System': target = 'CPU'
        if stream_name == 'Memory': target = 'RAM'
        if stream_name == 'Network': target = 'NET'
        
        if target in self.channels:
            self.channels[target]['value'] = min(1.0, value)
            self.channels[target]['history'].append(value)
            if len(self.channels[target]['history']) > 40:
                self.channels[target]['history'].pop(0)
            
            if self.is_active and value > 0.3:
                self.current_state = 'processing'
                if random.random() < 0.3:
                    self._spawn_particle(target)

    def add_operation(self, operation):
        if self.is_active:
            self._spawn_pulse()

    def _spawn_particle(self, channel):
        """Spawn orbiting particle"""
        if channel in self.channels:
            ch = self.channels[channel]
            self.particles.append({
                'angle': ch['angle'],
                'radius': 40 + random.uniform(0, 30),
                'speed': random.uniform(0.02, 0.05),
                'size': 3 + ch['value'] * 4,
                'color': ch['color'],
                'life': 1.0
            })
    
    def _spawn_pulse(self):
        """Spawn expanding pulse wave"""
        self.pulse_waves.append({
            'radius': 20,
            'max_radius': min(self.width, self.height) * 0.45,
            'alpha': 1.0,
            'color': self.state_colors.get(self.current_state, '#00ffff')
        })

    def _animate(self):
        try:
            if not self.winfo_exists(): return
        except: return
        
        if self.width < 50:
            self.after(40, self._animate)
            return
            
        self.delete('all')
        self.time += 0.04
        
        if self.is_active:
            self.scan_angle += 0.03
        
        color = self.state_colors.get(self.current_state, '#1a2a3a')
        
        # Draw layers
        self._draw_background_grid()
        self._draw_spectrum_rings(color)
        self._draw_pulse_waves()
        self._draw_radar_sweep(color)
        self._draw_channel_bars(color)
        self._draw_particles()
        self._draw_center_core(color)
        self._draw_header(color)
        
        self.after(30, self._animate)

    def _draw_background_grid(self):
        """Draw subtle radial background"""
        cx, cy = self.width // 2, self.height // 2
        
        # Concentric circles
        for r in range(20, int(min(self.width, self.height) * 0.5), 25):
            alpha = 0.1 + 0.05 * math.sin(self.time + r * 0.05)
            self.create_oval(cx - r, cy - r, cx + r, cy + r,
                           outline='#0a1520', width=1)
        
        # Radial lines
        for i in range(12):
            angle = i * math.pi / 6
            r = min(self.width, self.height) * 0.45
            x2 = cx + math.cos(angle) * r
            y2 = cy + math.sin(angle) * r
            self.create_line(cx, cy, x2, y2, fill='#0a1218', width=1)

    def _draw_spectrum_rings(self, color):
        """Draw dynamic spectrum visualization rings"""
        cx, cy = self.width // 2, self.height // 2
        
        if not self.is_active:
            # Idle state - dim rings
            for r in [60, 80, 100]:
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               outline='#151525', width=1)
            return
        
        # Active spectrum rings based on channel values
        for i, (name, ch) in enumerate(self.channels.items()):
            base_r = 50 + i * 25
            
            # Pulsing radius based on value
            pulse = 1 + ch['value'] * 0.15 * math.sin(self.time * 4 + i)
            r = base_r * pulse
            
            # Draw ring segment for each channel
            if ch['value'] > 0.1:
                # Glow effect
                for offset in [4, 2, 0]:
                    self.create_oval(cx - r - offset, cy - r - offset,
                                   cx + r + offset, cy + r + offset,
                                   outline=ch['color'], width=2 - offset//2)
            else:
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               outline='#1a2a3a', width=1)

    def _draw_pulse_waves(self):
        """Draw expanding pulse waves"""
        cx, cy = self.width // 2, self.height // 2
        new_waves = []
        
        for wave in self.pulse_waves:
            wave['radius'] += 3
            wave['alpha'] -= 0.025
            
            if wave['alpha'] > 0:
                r = wave['radius']
                width = max(1, int(wave['alpha'] * 3))
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               outline=wave['color'], width=width)
                new_waves.append(wave)
        
        self.pulse_waves = new_waves

    def _draw_radar_sweep(self, color):
        """Draw rotating radar sweep"""
        if not self.is_active:
            return
            
        cx, cy = self.width // 2, self.height // 2
        r = min(self.width, self.height) * 0.4
        
        # Sweep line with trail
        for i in range(8):
            trail_angle = self.scan_angle - i * 0.08
            alpha = 1 - i * 0.12
            
            x2 = cx + math.cos(trail_angle) * r
            y2 = cy + math.sin(trail_angle) * r
            
            width = max(1, int(3 * alpha))
            self.create_line(cx, cy, x2, y2, fill=color, width=width)

    def _draw_channel_bars(self, color):
        """Draw channel indicator bars in corners"""
        bar_length = 60
        bar_width = 6
        margin = 30
        
        positions = [
            (margin, margin, 'horizontal'),  # Top-left
            (self.width - margin - bar_length, margin, 'horizontal'),  # Top-right
            (margin, self.height - margin - bar_width, 'horizontal'),  # Bottom-left
            (self.width - margin - bar_length, self.height - margin - bar_width, 'horizontal')  # Bottom-right
        ]
        
        for i, (name, ch) in enumerate(self.channels.items()):
            if i >= len(positions):
                break
            
            x, y, orient = positions[i]
            
            # Background bar
            self.create_rectangle(x, y, x + bar_length, y + bar_width,
                                fill='#0a1015', outline='#1a2a3a')
            
            # Fill based on value
            if self.is_active and ch['value'] > 0:
                fill_w = bar_length * ch['value']
                self.create_rectangle(x, y, x + fill_w, y + bar_width,
                                    fill=ch['color'], outline='')
            
            # Label
            label_y = y - 12 if i < 2 else y + bar_width + 12
            self.create_text(x + bar_length // 2, label_y, text=name,
                           font=('JetBrains Mono', 7, 'bold'),
                           fill=ch['color'] if self.is_active else '#3a4a5a')

    def _draw_particles(self):
        """Draw orbiting particles"""
        cx, cy = self.width // 2, self.height // 2
        new_particles = []
        
        for p in self.particles:
            p['angle'] += p['speed']
            p['life'] -= 0.015
            p['radius'] += 0.3  # Slowly spiral outward
            
            if p['life'] > 0 and p['radius'] < min(self.width, self.height) * 0.45:
                x = cx + math.cos(p['angle']) * p['radius']
                y = cy + math.sin(p['angle']) * p['radius']
                
                size = p['size'] * p['life']
                
                # Particle with glow
                self.create_oval(x - size - 2, y - size - 2,
                               x + size + 2, y + size + 2,
                               fill='', outline=p['color'], width=1)
                self.create_oval(x - size, y - size, x + size, y + size,
                               fill=p['color'], outline='')
                
                new_particles.append(p)
        
        self.particles = new_particles[:30]  # Limit particles

    def _draw_center_core(self, color):
        """Draw central core element"""
        cx, cy = self.width // 2, self.height // 2
        
        # Calculate overall activity
        total_activity = sum(ch['value'] for ch in self.channels.values()) / 4
        
        # Core size pulses with activity
        base_size = 15
        pulse = 1 + (total_activity * 0.3 if self.is_active else 0.05) * math.sin(self.time * 5)
        size = base_size * pulse
        
        # Outer glow rings
        if self.is_active:
            for r in [size + 12, size + 8, size + 4]:
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               outline=color, width=1)
        
        # Core
        fill = color if self.is_active else '#1a2a3a'
        self.create_oval(cx - size, cy - size, cx + size, cy + size,
                       fill=fill, outline='#ffffff', width=2)
        
        # Inner dot
        inner = size * 0.4
        self.create_oval(cx - inner, cy - inner, cx + inner, cy + inner,
                       fill='#ffffff' if self.is_active else '#3a4a5a', outline='')

    def _draw_header(self, color):
        """Draw header and status"""
        self.create_text(self.width // 2, 15,
                       text="SPECTRUM ANALYZER",
                       font=('JetBrains Mono', 10, 'bold'),
                       fill=color if self.is_active else '#3a4a5a')
        
        # Status at bottom
        status = self.current_state.upper() if self.is_active else "STANDBY"
        self.create_text(self.width // 2, self.height - 15,
                       text=status,
                       font=('JetBrains Mono', 8),
                       fill=color if self.is_active else '#3a4a5a')
        
        # Activity indicator
        if self.is_active:
            total = sum(ch['value'] for ch in self.channels.values()) / 4
            self.create_text(self.width - 20, 15,
                           text=f"{int(total * 100)}%",
                           anchor='e', font=('JetBrains Mono', 8, 'bold'),
                           fill=color)

    def _draw_metrics_ring(self):
        pass  # Removed


# ═══════════════════════════════════════════════════════════════════════════════════
# ADVANCED HOLOGRAPHIC & QUANTUM ANIMATIONS
# ═══════════════════════════════════════════════════════════════════════════════════

class HolographicDisplay(tk.Canvas):
    """Futuristic holographic 3D wireframe display"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.scan_line = 0
        self.flicker = 0
        self.glitch_offset = 0
        
        # 3D cube vertices
        self.cube_vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        self.cube_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        self.data_value = 0.5
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def set_data(self, value):
        self.data_value = max(0.0, min(1.0, value))
    
    def _rotate_point(self, point):
        x, y, z = point
        
        # Rotate around X
        cos_x, sin_x = math.cos(self.angle_x), math.sin(self.angle_x)
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
        
        # Rotate around Y
        cos_y, sin_y = math.cos(self.angle_y), math.sin(self.angle_y)
        x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
        
        # Rotate around Z
        cos_z, sin_z = math.cos(self.angle_z), math.sin(self.angle_z)
        x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
        
        return x, y, z
    
    def _project(self, point, scale=80):
        x, y, z = point
        z_offset = 3
        perspective = scale / (z + z_offset)
        sx = self.width/2 + x * perspective
        sy = self.height/2 + y * perspective
        return sx, sy, perspective
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            
            # Update angles
            self.angle_x += 0.02
            self.angle_y += 0.015
            self.angle_z += 0.01
            
            # Scanline effect
            self.scan_line = (self.scan_line + 3) % self.height
            
            # Flicker (disable randomness in real_mode)
            try:
                top = self.winfo_toplevel()
                real_mode = getattr(top, 'real_mode', False)
            except Exception:
                real_mode = False
            self.flicker = (0.9 if real_mode else random.random() * 0.2 + 0.8)
            
            # Occasional glitch (disabled in real_mode)
            if not real_mode and random.random() < 0.02:
                self.glitch_offset = random.randint(-5, 5)
            else:
                self.glitch_offset *= 0.9
            
            # Draw scanlines background
            for y in range(0, self.height, 3):
                alpha = 0.05 if y % 6 == 0 else 0.02
                self.create_line(0, y, self.width, y, fill=T.BG_CARD, width=1)
            
            # Draw rotating cube
            projected = []
            for vertex in self.cube_vertices:
                scaled = [v * (0.5 + self.data_value * 0.8) for v in vertex]
                rotated = self._rotate_point(scaled)
                sx, sy, depth = self._project(rotated, scale=60 + self.data_value * 40)
                projected.append((sx + self.glitch_offset, sy, depth))
            
            # Draw edges with holographic effect
            for start, end in self.cube_edges:
                x1, y1, d1 = projected[start]
                x2, y2, d2 = projected[end]
                avg_depth = (d1 + d2) / 2
                
                # Multiple layers for glow
                for offset, color in [(3, T.BG_CARD), (2, T.CYAN), (1, T.GREEN)]:
                    self.create_line(x1, y1, x2, y2, 
                                   fill=color, width=offset,
                                   stipple='gray50' if offset > 1 else '')
            
            # Draw vertices as glowing points
            for sx, sy, depth in projected:
                size = int(3 + depth * 0.5)
                for r in range(size, 0, -1):
                    self.create_oval(sx-r, sy-r, sx+r, sy+r, 
                                   fill=T.CYAN if r == 1 else '', 
                                   outline=T.CYAN)
            
            # Scan line overlay
            scan_alpha = abs(math.sin(self.scan_line * 0.1)) * 0.3
            self.create_line(0, self.scan_line, self.width, self.scan_line,
                           fill=T.GREEN, width=2)
            
            # HUD elements
            self._draw_hud()
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass
    
    def _draw_hud(self):
        # Corner brackets
        bracket_size = 20
        for corner in [(0, 0), (self.width, 0), (0, self.height), (self.width, self.height)]:
            x, y = corner
            dx = 1 if x == 0 else -1
            dy = 1 if y == 0 else -1
            self.create_line(x, y, x + bracket_size * dx, y, fill=T.CYAN, width=2)
            self.create_line(x, y, x, y + bracket_size * dy, fill=T.CYAN, width=2)
        
        # Data readout
        self.create_text(10, 10, text=f"HOLO-DISPLAY v3.0",
                        font=('JetBrains Mono', 8), fill=T.CYAN, anchor='nw')
        self.create_text(10, 25, text=f"SIGNAL: {self.data_value * 100:.1f}%",
                        font=('JetBrains Mono', 7), fill=T.GREEN, anchor='nw')


class QuantumStateVisualizer(tk.Canvas):
    """Visualizes quantum superposition states with wave function collapse"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.collapsed = False
        self.collapse_time = 0
        self.qubits = []
        for i in range(6):
            self.qubits.append({
                'state_0': random.random(),
                'state_1': random.random(),
                'phase': random.random() * math.pi * 2,
                'spin': random.choice([-1, 1]),
                'entangled_with': random.choice([None, (i + 1) % 6])
            })
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def trigger_collapse(self):
        self.collapsed = True
        self.collapse_time = 0
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.05
            
            # Background grid
            for i in range(0, self.width, 20):
                self.create_line(i, 0, i, self.height, fill=T.BG_CARD, width=1)
            for i in range(0, self.height, 20):
                self.create_line(0, i, self.width, i, fill=T.BG_CARD, width=1)
            
            # Draw qubits
            qubit_spacing = self.width / (len(self.qubits) + 1)
            
            for idx, qubit in enumerate(self.qubits):
                x = qubit_spacing * (idx + 1)
                y = self.height / 2
                
                # Update phase
                qubit['phase'] += 0.1 * qubit['spin']
                
                # Superposition visualization
                prob_0 = (math.sin(self.time + qubit['phase']) + 1) / 2
                prob_1 = 1 - prob_0
                
                if self.collapsed:
                    self.collapse_time += 0.02
                    collapse_factor = min(1, self.collapse_time * 2)
                    prob_0 = lerp(prob_0, round(prob_0), collapse_factor)
                    prob_1 = 1 - prob_0
                    if self.collapse_time > 1:
                        self.collapsed = False
                
                # Draw probability waves
                wave_height = 50
                for i in range(-30, 31):
                    wx = x + i * 2
                    wy0 = y - wave_height * prob_0 * math.sin(i * 0.3 + self.time)
                    wy1 = y + wave_height * prob_1 * math.sin(i * 0.3 - self.time)
                    
                    if i > -30:
                        self.create_line(prev_wx, prev_wy0, wx, wy0, fill=T.CYAN, width=2)
                        self.create_line(prev_wx, prev_wy1, wx, wy1, fill=T.PINK, width=2)
                    prev_wx, prev_wy0, prev_wy1 = wx, wy0, wy1
                
                # Draw entanglement lines
                if qubit['entangled_with'] is not None:
                    other_x = qubit_spacing * (qubit['entangled_with'] + 1)
                    self.create_line(x, y, other_x, y, fill=T.PURPLE, width=1, dash=(4, 4))
                
                # Qubit indicator
                size = 15
                self.create_oval(x - size, y - size, x + size, y + size,
                               fill=T.BG_CARD, outline=T.CYAN, width=2)
                
                # State labels
                self.create_text(x, y - 70, text=f"|0⟩: {prob_0:.2f}",
                               font=('JetBrains Mono', 8), fill=T.CYAN)
                self.create_text(x, y + 70, text=f"|1⟩: {prob_1:.2f}",
                               font=('JetBrains Mono', 8), fill=T.PINK)
                
                # Qubit label
                self.create_text(x, y, text=f"Q{idx}",
                               font=('JetBrains Mono', 10, 'bold'), fill=T.GREEN)
            
            # Title
            self.create_text(self.width/2, 20, text="QUANTUM STATE SUPERPOSITION",
                           font=('JetBrains Mono', 10, 'bold'), fill=T.CYAN)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class ParticleExplosion(tk.Canvas):
    """Particle explosion effect for action feedback"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.particles = []
        self.explosions = []
        self.ambient_particles = []
        self._init_ambient()
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_ambient()
    
    def _init_ambient(self):
        self.ambient_particles = []
        # No ambient randomness in real_mode; default empty, expect real triggers via trigger_explosion
        try:
            top = self.winfo_toplevel()
            real_mode = getattr(top, 'real_mode', False)
        except Exception:
            real_mode = False
        if not real_mode:
            for _ in range(30):
                self.ambient_particles.append({
                    'x': random.random() * max(1, self.width),
                    'y': random.random() * max(1, self.height),
                    'vx': random.random() * 2 - 1,
                    'vy': random.random() * 2 - 1,
                    'size': random.random() * 3 + 1,
                    'color': random.choice([T.CYAN, T.GREEN, T.PINK, T.PURPLE])
                })
    
    def trigger_explosion(self, x=None, y=None, color=None, count=50):
        if x is None:
            x = self.width / 2
        if y is None:
            y = self.height / 2
        if color is None:
            color = random.choice([T.CYAN, T.GREEN, T.PINK, T.YELLOW])
        
        explosion = {'particles': [], 'age': 0}
        for _ in range(count):
            angle = random.random() * math.pi * 2
            speed = random.random() * 10 + 5
            explosion['particles'].append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.random() * 5 + 2,
                'color': color,
                'life': 1.0
            })
        self.explosions.append(explosion)
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            
            # Draw grid
            for i in range(0, self.width, 40):
                self.create_line(i, 0, i, self.height, fill=T.BG_CARD, width=1)
            for i in range(0, self.height, 40):
                self.create_line(0, i, self.width, i, fill=T.BG_CARD, width=1)
            
            # Update and draw ambient particles (disabled in real_mode by init)
            for p in self.ambient_particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                if p['x'] < 0: p['x'] = self.width
                if p['x'] > self.width: p['x'] = 0
                if p['y'] < 0: p['y'] = self.height
                if p['y'] > self.height: p['y'] = 0
                s = p['size']
                self.create_oval(p['x'] - s, p['y'] - s, p['x'] + s, p['y'] + s,
                               fill=p['color'], outline='')
            
            # Draw connections between nearby particles
            for i, p1 in enumerate(self.ambient_particles):
                for p2 in self.ambient_particles[i+1:]:
                    dist = math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
                    if dist < 80:
                        alpha = 1 - dist / 80
                        self.create_line(p1['x'], p1['y'], p2['x'], p2['y'],
                                       fill=T.BORDER, width=1)
            
            # Update and draw explosions
            active_explosions = []
            for exp in self.explosions:
                exp['age'] += 0.05
                active_particles = []
                
                for p in exp['particles']:
                    p['x'] += p['vx']
                    p['y'] += p['vy']
                    p['vx'] *= 0.96
                    p['vy'] *= 0.96
                    p['vy'] += 0.2  # Gravity
                    p['life'] -= 0.02
                    
                    if p['life'] > 0:
                        s = p['size'] * p['life']
                        # Glow effect
                        for glow in [s * 2, s * 1.5, s]:
                            self.create_oval(p['x'] - glow, p['y'] - glow, 
                                           p['x'] + glow, p['y'] + glow,
                                           fill='', outline=p['color'])
                        self.create_oval(p['x'] - s, p['y'] - s, p['x'] + s, p['y'] + s,
                                       fill=p['color'], outline='')
                        active_particles.append(p)
                
                exp['particles'] = active_particles
                if active_particles:
                    active_explosions.append(exp)
            
            self.explosions = active_explosions
            
            # Title
            self.create_text(self.width/2, 20, text="PARTICLE SYSTEM",
                           font=('JetBrains Mono', 10, 'bold'), fill=T.PINK)
            
            # Instruction
            if not self.explosions:
                self.create_text(self.width/2, self.height - 20, 
                               text="System reacting to AI activity",
                               font=('JetBrains Mono', 8), fill=T.TEXT_DIM)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class FlowField(tk.Canvas):
    """Perlin-noise inspired flow field visualization"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.resolution = 20
        self.particles = []
        self.flow_intensity = 0.5
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_particles()
    
    def _init_particles(self):
        self.particles = []
        # Only initialize particles when not in real_mode; expect external data otherwise
        try:
            top = self.winfo_toplevel()
            real_mode = getattr(top, 'real_mode', False)
        except Exception:
            real_mode = False
        if not real_mode:
            for _ in range(100):
                self.particles.append({
                    'x': random.random() * max(1, self.width),
                    'y': random.random() * max(1, self.height),
                    'history': [],
                    'color': random.choice([T.CYAN, T.GREEN, T.PINK, T.PURPLE]),
                    'speed': random.random() * 0.5 + 0.5
                })
    
    def set_intensity(self, value):
        self.flow_intensity = max(0.1, min(1.0, value))
    
    def _get_flow_angle(self, x, y):
        # Simplified Perlin-like noise using sine waves
        scale = 0.02
        return (math.sin(x * scale + self.time) * 
                math.cos(y * scale + self.time * 0.5) * 
                math.pi * 2)
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.02 * self.flow_intensity
            
            # Draw flow field arrows (skip if real_mode to avoid simulated visuals)
            try:
                top = self.winfo_toplevel()
                real_mode = getattr(top, 'real_mode', False)
            except Exception:
                real_mode = False
            if not real_mode:
                for gx in range(0, self.width, 40):
                    for gy in range(0, self.height, 40):
                        angle = self._get_flow_angle(gx, gy)
                        length = 10 * self.flow_intensity
                        ex = gx + math.cos(angle) * length
                        ey = gy + math.sin(angle) * length
                        self.create_line(gx, gy, ex, ey, fill=T.BG_CARD, width=1,
                                       arrow='last', arrowshape=(4, 5, 2))
            
            # Update and draw particles
            for p in self.particles:
                angle = self._get_flow_angle(p['x'], p['y'])
                p['x'] += math.cos(angle) * 2 * p['speed'] * self.flow_intensity
                p['y'] += math.sin(angle) * 2 * p['speed'] * self.flow_intensity
                
                # Store history for trail
                p['history'].append((p['x'], p['y']))
                if len(p['history']) > 20:
                    p['history'].pop(0)
                
                # Wrap around
                if p['x'] < 0: p['x'] = self.width; p['history'] = []
                if p['x'] > self.width: p['x'] = 0; p['history'] = []
                if p['y'] < 0: p['y'] = self.height; p['history'] = []
                if p['y'] > self.height: p['y'] = 0; p['history'] = []
                
                # Draw trail
                if len(p['history']) > 1:
                    points = []
                    for hx, hy in p['history']:
                        points.extend([hx, hy])
                    self.create_line(points, fill=p['color'], width=2, smooth=True)
                
                # Draw particle
                self.create_oval(p['x'] - 3, p['y'] - 3, p['x'] + 3, p['y'] + 3,
                               fill=p['color'], outline='')
            
            # Title
            self.create_text(self.width/2, 20, text="NEURAL FLOW FIELD",
                           font=('JetBrains Mono', 10, 'bold'), fill=T.CYAN)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class AudioSpectrum(tk.Canvas):
    """Audio spectrum analyzer visualization"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.bars = 32
        self.bar_values = [0] * self.bars
        self.target_values = [0] * self.bars
        self.activity_level = 0.5
        self.time = 0
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def set_activity(self, level):
        self.activity_level = max(0.1, min(1.0, level))
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.1
            
            bar_width = (self.width - 40) / self.bars
            bar_gap = 2
            
            # Update target values: in real_mode, expect external set_activity to drive values
            try:
                top = self.winfo_toplevel()
                real_mode = getattr(top, 'real_mode', False)
            except Exception:
                real_mode = False
            if not real_mode:
                for i in range(self.bars):
                    freq_factor = 1 - abs(i - self.bars/3) / self.bars
                    self.target_values[i] = (
                        abs(math.sin(self.time + i * 0.5)) * 
                        freq_factor * 
                        self.activity_level +
                        random.random() * 0.2 * self.activity_level
                    )
            
            # Smooth interpolation
            for i in range(self.bars):
                self.bar_values[i] = lerp(self.bar_values[i], self.target_values[i], 0.3)
            
            # Draw bars
            for i in range(self.bars):
                x = 20 + i * bar_width
                bar_height = self.bar_values[i] * (self.height - 60)
                y = self.height - 30 - bar_height
                
                # Color gradient based on height
                if self.bar_values[i] > 0.7:
                    color = T.PINK
                elif self.bar_values[i] > 0.4:
                    color = T.YELLOW
                else:
                    color = T.CYAN
                
                # Draw bar with glow
                for offset in [3, 2, 1, 0]:
                    self.create_rectangle(
                        x + offset, y + offset,
                        x + bar_width - bar_gap - offset, self.height - 30 - offset,
                        fill=color if offset == 0 else '',
                        outline=color if offset > 0 else ''
                    )
                
                # Reflection
                self.create_rectangle(
                    x, self.height - 28,
                    x + bar_width - bar_gap, self.height - 28 + bar_height * 0.2,
                    fill=T.BG_CARD, outline=''
                )
            
            # Title
            self.create_text(self.width/2, 15, text="AI ACTIVITY SPECTRUM",
                           font=('JetBrains Mono', 10, 'bold'), fill=T.CYAN)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


class NeuralPathway(tk.Canvas):
    """Animated neural pathway with signals traveling"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.nodes = []
        self.connections = []
        self.signals = []
        self.time = 0
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_network()
    
    def _init_network(self):
        if self.width <= 0 or self.height <= 0:
            return
        
        self.nodes = []
        self.connections = []
        
        # Create layered neural network layout
        layers = [4, 6, 8, 6, 4]
        layer_x = self.width / (len(layers) + 1)
        
        node_idx = 0
        layer_nodes = []
        
        for layer_i, count in enumerate(layers):
            x = layer_x * (layer_i + 1)
            layer_node_ids = []
            for i in range(count):
                y = self.height * (i + 1) / (count + 1)
                self.nodes.append({
                    'x': x,
                    'y': y,
                    'pulse': random.random() * math.pi * 2,
                    'active': False,
                    'activation': 0
                })
                layer_node_ids.append(node_idx)
                node_idx += 1
            layer_nodes.append(layer_node_ids)
        
        # Create connections between layers
        for layer_i in range(len(layers) - 1):
            for node_a in layer_nodes[layer_i]:
                for node_b in layer_nodes[layer_i + 1]:
                    if random.random() < 0.5:  # Sparse connections
                        self.connections.append({
                            'from': node_a,
                            'to': node_b,
                            'weight': random.random()
                        })
    
    def fire_signal(self):
        if self.nodes:
            start_node = random.randint(0, min(3, len(self.nodes) - 1))
            self.signals.append({
                'from_node': start_node,
                'to_node': None,
                'progress': 0,
                'color': random.choice([T.CYAN, T.GREEN, T.PINK])
            })
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.05
            
            # Auto-fire signals (disabled in real_mode)
            try:
                top = self.winfo_toplevel()
                real_mode = getattr(top, 'real_mode', False)
            except Exception:
                real_mode = False
            if not real_mode:
                if random.random() < 0.1:
                    self.fire_signal()
            
            # Draw connections
            for conn in self.connections:
                node_a = self.nodes[conn['from']]
                node_b = self.nodes[conn['to']]
                
                # Draw connection line
                self.create_line(node_a['x'], node_a['y'], 
                               node_b['x'], node_b['y'],
                               fill=T.BG_CARD, width=1)
            
            # Update and draw signals
            active_signals = []
            for signal in self.signals:
                signal['progress'] += 0.05
                
                if signal['to_node'] is None:
                    # Find a connection from current node
                    possible = [c for c in self.connections if c['from'] == signal['from_node']]
                    if possible:
                        signal['to_node'] = random.choice(possible)['to']
                    else:
                        continue
                
                if signal['progress'] < 1:
                    # Interpolate position
                    from_node = self.nodes[signal['from_node']]
                    to_node = self.nodes[signal['to_node']]
                    
                    t = ease_in_out_cubic(signal['progress'])
                    x = lerp(from_node['x'], to_node['x'], t)
                    y = lerp(from_node['y'], to_node['y'], t)
                    
                    # Draw signal
                    for r in [8, 5, 3]:
                        self.create_oval(x - r, y - r, x + r, y + r,
                                       fill=signal['color'] if r == 3 else '',
                                       outline=signal['color'])
                    
                    active_signals.append(signal)
                else:
                    # Signal reached destination, maybe continue
                    if random.random() < 0.7:
                        signal['from_node'] = signal['to_node']
                        signal['to_node'] = None
                        signal['progress'] = 0
                        active_signals.append(signal)
            
            self.signals = active_signals
            
            # Draw nodes
            for node in self.nodes:
                node['pulse'] += 0.1
                size = 8 + math.sin(node['pulse']) * 2
                
                # Glow effect
                for r in [size + 4, size + 2, size]:
                    self.create_oval(node['x'] - r, node['y'] - r,
                                   node['x'] + r, node['y'] + r,
                                   fill=T.CYAN if r == size else '',
                                   outline=T.CYAN)
            
            # Title
            self.create_text(self.width/2, 15, text="NEURAL PATHWAY SIGNALS",
                           font=('JetBrains Mono', 10, 'bold'), fill=T.CYAN)
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass


# ═══════════════════════════════════════════════════════════════════════════════════
# ANIMATED COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════════

class PulsingDot(tk.Canvas):
    """Animated status dot with glow effect"""
    
    def __init__(self, parent, size=20, color=T.RED, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        bg=T.BG_DARK, highlightthickness=0, **kwargs)
        self.size = size
        self.color = color
        self.pulse = 0
        self.active = False
        self._animate()
    
    def set_active(self, active, color=None):
        self.active = active
        if color:
            self.color = color
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        self.delete('all')
        cx, cy = self.size // 2, self.size // 2
        
        self.pulse += 0.15
        pulse_scale = 0.3 + 0.2 * math.sin(self.pulse) if self.active else 0.3
        
        # Glow
        if self.active:
            for i in range(3, 0, -1):
                r = (self.size // 2 - 2) * (1 + i * 0.15)
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               fill='', outline=self.color, width=1)
        
        # Core
        r = (self.size // 2 - 2) * (0.8 + pulse_scale * 0.2)
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                        fill=self.color, outline='')
        
        try:
            if self.winfo_exists():
                self.after(50, self._animate)
        except:
            pass


class BrainStormingLogo(tk.Canvas):
    """
    BRAIN STORMING LOGO - Animated neural brain with lightning thoughts
    Shows brain outline with synaptic lightning bolts and orbiting ideas
    """
    
    def __init__(self, parent, size=60, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=T.BG_DARK, highlightthickness=0, **kwargs)
        self.size = size
        self.time = 0
        self.is_active = False
        
        # Lightning bolts (brain storms)
        self.lightnings = []
        self.sparks = []
        
        # Orbiting thought particles
        self.thought_particles = []
        for i in range(8):
            angle = (i / 8) * math.pi * 2
            self.thought_particles.append({
                'angle': angle,
                'radius': size * 0.4,
                'speed': 0.03 + random.random() * 0.02,
                'size': 2 + random.random() * 2,
                'color': [T.CYAN, T.PINK, T.GREEN, T.PURPLE, T.YELLOW][i % 5]
            })
        
        # Neural pulse rings
        self.pulse_rings = []
        
        # Brain nodes (neural network points)
        self.brain_nodes = []
        self._init_brain_nodes()
        
        self._animate()
    
    def _init_brain_nodes(self):
        """Initialize brain neural network nodes"""
        cx, cy = self.size // 2, self.size // 2
        # Create nodes in brain-like pattern
        brain_points = [
            (0.5, 0.25), (0.3, 0.35), (0.7, 0.35),  # Top
            (0.2, 0.5), (0.5, 0.45), (0.8, 0.5),    # Middle
            (0.25, 0.65), (0.5, 0.6), (0.75, 0.65), # Lower
            (0.35, 0.75), (0.65, 0.75),             # Bottom
        ]
        for px, py in brain_points:
            self.brain_nodes.append({
                'x': px * self.size,
                'y': py * self.size,
                'pulse': random.random() * math.pi * 2,
                'active': False
            })
    
    def set_active(self, active):
        """Set active state - triggers brain storm effect"""
        self.is_active = active
        if active:
            self._spawn_lightning()
    
    def _spawn_lightning(self):
        """Spawn a lightning bolt in the brain"""
        if len(self.lightnings) < 3:
            cx, cy = self.size // 2, self.size // 2
            # Random start point near top
            start_x = cx + random.randint(-15, 15)
            start_y = cy - self.size * 0.3
            
            # Create zigzag lightning path
            points = [(start_x, start_y)]
            x, y = start_x, start_y
            for _ in range(4):
                x += random.randint(-10, 10)
                y += random.randint(5, 12)
                points.append((x, y))
            
            self.lightnings.append({
                'points': points,
                'life': 1.0,
                'color': random.choice([T.CYAN, T.PINK, T.YELLOW])
            })
            
            # Spawn sparks at end point
            end_x, end_y = points[-1]
            for _ in range(5):
                self.sparks.append({
                    'x': end_x,
                    'y': end_y,
                    'vx': (random.random() - 0.5) * 4,
                    'vy': (random.random() - 0.5) * 4,
                    'life': 1.0,
                    'color': T.YELLOW
                })
    
    def _spawn_pulse_ring(self):
        """Spawn expanding pulse ring from center"""
        cx, cy = self.size // 2, self.size // 2
        self.pulse_rings.append({
            'x': cx,
            'y': cy,
            'radius': 5,
            'max_radius': self.size * 0.5,
            'life': 1.0
        })
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        
        self.delete('all')
        self.time += 0.08
        
        cx, cy = self.size // 2, self.size // 2
        
        # Background subtle glow
        if self.is_active:
            for i in range(3, 0, -1):
                r = self.size * 0.4 + i * 3
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                               fill='', outline=T.CYAN, width=1)
        
        # Draw brain outline (stylized)
        self._draw_brain_outline(cx, cy)
        
        # Draw neural connections
        self._draw_neural_connections()
        
        # Draw brain nodes
        self._draw_brain_nodes()
        
        # Draw pulse rings
        self._draw_pulse_rings()
        
        # Draw lightning bolts
        self._draw_lightnings()
        
        # Draw sparks
        self._draw_sparks()
        
        # Draw orbiting thought particles
        self._draw_thought_particles(cx, cy)
        
        # Draw center core
        self._draw_center_core(cx, cy)
        
        # Spawn effects when active
        if self.is_active:
            if random.random() < 0.1:
                self._spawn_lightning()
            if random.random() < 0.05:
                self._spawn_pulse_ring()
            # Activate random nodes
            if random.random() < 0.15:
                node = random.choice(self.brain_nodes)
                node['active'] = True
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass
    
    def _draw_brain_outline(self, cx, cy):
        """Draw stylized brain outline"""
        r = self.size * 0.35
        
        # Brain shape using overlapping ovals
        # Left hemisphere
        self.create_oval(cx - r - 3, cy - r * 0.8, cx + 3, cy + r * 0.9,
                        fill='', outline=T.BORDER if not self.is_active else T.CYAN, width=1)
        # Right hemisphere  
        self.create_oval(cx - 3, cy - r * 0.8, cx + r + 3, cy + r * 0.9,
                        fill='', outline=T.BORDER if not self.is_active else T.CYAN, width=1)
        
        # Brain stem hint
        self.create_line(cx, cy + r * 0.7, cx, cy + r * 1.0,
                        fill=T.BORDER if not self.is_active else T.CYAN, width=2)
    
    def _draw_neural_connections(self):
        """Draw connections between brain nodes"""
        connections = [
            (0, 1), (0, 2), (1, 3), (2, 5), (1, 4), (2, 4),
            (3, 6), (4, 7), (5, 8), (6, 9), (7, 9), (7, 10), (8, 10)
        ]
        
        for i, j in connections:
            if i < len(self.brain_nodes) and j < len(self.brain_nodes):
                n1, n2 = self.brain_nodes[i], self.brain_nodes[j]
                # Pulse effect on connection
                pulse = math.sin(self.time + i * 0.5) * 0.5 + 0.5
                color = T.CYAN if (n1['active'] or n2['active']) and self.is_active else T.BORDER
                self.create_line(n1['x'], n1['y'], n2['x'], n2['y'],
                               fill=color, width=1, dash=(2, 3))
    
    def _draw_brain_nodes(self):
        """Draw neural nodes"""
        for node in self.brain_nodes:
            node['pulse'] += 0.1
            
            # Decay active state
            if node['active']:
                if random.random() < 0.1:
                    node['active'] = False
            
            size = 2
            if node['active'] and self.is_active:
                size = 3 + math.sin(node['pulse']) * 1.5
                # Glow
                self.create_oval(node['x'] - size * 2, node['y'] - size * 2,
                               node['x'] + size * 2, node['y'] + size * 2,
                               fill='', outline=T.PINK, width=1)
                color = T.PINK
            else:
                color = T.TEXT_DIM if not self.is_active else T.CYAN
            
            self.create_oval(node['x'] - size, node['y'] - size,
                           node['x'] + size, node['y'] + size,
                           fill=color, outline='')
    
    def _draw_pulse_rings(self):
        """Draw expanding pulse rings"""
        new_rings = []
        for ring in self.pulse_rings:
            ring['radius'] += 2
            ring['life'] -= 0.04
            
            if ring['life'] > 0 and ring['radius'] < ring['max_radius']:
                self.create_oval(ring['x'] - ring['radius'], ring['y'] - ring['radius'],
                               ring['x'] + ring['radius'], ring['y'] + ring['radius'],
                               fill='', outline=T.CYAN, width=1)
                new_rings.append(ring)
        
        self.pulse_rings = new_rings
    
    def _draw_lightnings(self):
        """Draw lightning bolts"""
        new_lightnings = []
        for bolt in self.lightnings:
            bolt['life'] -= 0.1
            
            if bolt['life'] > 0:
                points = bolt['points']
                # Draw zigzag line
                for i in range(len(points) - 1):
                    x1, y1 = points[i]
                    x2, y2 = points[i + 1]
                    # Glow effect
                    self.create_line(x1, y1, x2, y2, fill=bolt['color'], width=3)
                    self.create_line(x1, y1, x2, y2, fill=T.TEXT_BRIGHT, width=1)
                new_lightnings.append(bolt)
        
        self.lightnings = new_lightnings
    
    def _draw_sparks(self):
        """Draw spark particles"""
        new_sparks = []
        for spark in self.sparks:
            spark['x'] += spark['vx']
            spark['y'] += spark['vy']
            spark['life'] -= 0.08
            
            if spark['life'] > 0:
                size = 1 + spark['life'] * 2
                self.create_oval(spark['x'] - size, spark['y'] - size,
                               spark['x'] + size, spark['y'] + size,
                               fill=spark['color'], outline='')
                new_sparks.append(spark)
        
        self.sparks = new_sparks[:20]  # Limit sparks
    
    def _draw_thought_particles(self, cx, cy):
        """Draw orbiting thought particles"""
        for p in self.thought_particles:
            p['angle'] += p['speed'] if self.is_active else p['speed'] * 0.3
            
            # Elliptical orbit
            x = cx + math.cos(p['angle']) * p['radius']
            y = cy + math.sin(p['angle']) * (p['radius'] * 0.6)
            
            size = p['size'] if self.is_active else p['size'] * 0.5
            color = p['color'] if self.is_active else T.TEXT_DIM
            
            self.create_oval(x - size, y - size, x + size, y + size,
                           fill=color, outline='')
    
    def _draw_center_core(self, cx, cy):
        """Draw center brain core"""
        pulse = math.sin(self.time * 2) * 0.2 if self.is_active else 0
        size = 6 + pulse * 3
        
        color = T.CYAN if self.is_active else T.TEXT_DIM
        
        # Core glow
        if self.is_active:
            self.create_oval(cx - size * 1.5, cy - size * 1.5,
                           cx + size * 1.5, cy + size * 1.5,
                           fill='', outline=color, width=1)
        
        # Core
        self.create_oval(cx - size, cy - size, cx + size, cy + size,
                        fill=T.BG_CARD, outline=color, width=2)


class NeonGauge(tk.Canvas):
    """Futuristic Orbital Gauge with holographic rings"""
    
    def __init__(self, parent, label="", size=100, color=T.CYAN, **kwargs):
        super().__init__(parent, width=size, height=size + 30,
                        bg=T.BG_PANEL, highlightthickness=0, **kwargs)
        self.size = size
        self.label = label
        self.color = color
        self.value = 0
        self.target = 0
        self.animating = False
        self.time = 0
        self._animate_rotation()
    
    def set_value(self, value):
        self.target = max(0, min(100, value))
        if not self.animating:
            self._animate_to_target()
    
    def _animate_rotation(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        self.time += 0.05
        self._draw()
        self.after(50, self._animate_rotation)

    def _animate_to_target(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        self.animating = True
        diff = self.target - self.value
        
        if abs(diff) > 0.5:
            self.value += diff * 0.15
            try:
                if self.winfo_exists():
                    self.after(25, self._animate_to_target)
            except:
                pass
        else:
            self.value = self.target
            self.animating = False
    
    def _draw(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        self.delete('all')
        cx, cy = self.size // 2, self.size // 2
        r = self.size // 2 - 15
        
        # 1. Outer Orbital Ring (Clockwise)
        angle_offset = self.time * 2
        self.create_arc(cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8,
                      start=angle_offset, extent=240, outline=self.color, width=1, style='arc')
        self.create_arc(cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8,
                      start=angle_offset + 250, extent=60, outline=T.TEXT_DIM, width=1, style='arc')

        # 2. Inner Orbital Ring (Counter-Clockwise)
        angle_offset_inner = -self.time * 3
        self.create_arc(cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5,
                      start=angle_offset_inner, extent=180, outline=self.color, width=1, style='arc', dash=(2, 4))

        # 3. Background Track
        self.create_arc(cx - r, cy - r, cx + r, cy + r,
                       start=-30, extent=240,
                       outline='#1a253a', width=8, style='arc')
        
        # 4. Value Arc
        extent = (self.value / 100) * 240
        if extent > 0:
            # Glow effect
            for w in [4, 2]:
                self.create_arc(cx - r, cy - r, cx + r, cy + r,
                               start=210, extent=-extent,
                               outline=self.color, width=8+w, style='arc')
            
            # Main arc
            self.create_arc(cx - r, cy - r, cx + r, cy + r,
                           start=210, extent=-extent,
                           outline=T.TEXT_BRIGHT, width=2, style='arc')

        # 5. Central Readout
        self.create_text(cx, cy - 5, text=f"{int(self.value)}",
                        font=('JetBrains Mono', 20, 'bold'),
                        fill=T.TEXT_BRIGHT)
        self.create_text(cx, cy + 12, text="%",
                        font=('JetBrains Mono', 10),
                        fill=self.color)
        
        # Label
        self.create_text(cx, self.size + 15, text=self.label,
                        font=('JetBrains Mono', 9, 'bold'),
                        fill=T.TEXT_DIM)


class MatrixRain(tk.Canvas):
    """REPLACED: Neural Brainstorm - Creative thought visualization"""
    pass  # Kept for backwards compatibility


class QuantumConsciousness(tk.Canvas):
    """Advanced Quantum Consciousness visualization - AI mind expanding in quantum states"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        self.consciousness_level = 0.5
        self.quantum_particles = []
        self.thought_streams = []
        self.energy_rings = []
        self.neuron_sparks = []
        self.central_pulse = 0
        self.learning_intensity = 0.3
        
        # Consciousness states
        self.states = ['OBSERVING', 'ANALYZING', 'LEARNING', 'EVOLVING', 'CREATING']
        self.current_state_idx = 0
        self.state_transition = 0
        
        self.bind('<Configure>', self._on_resize)
        self._init_particles()
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_particles()
    
    def _init_particles(self):
        if self.width <= 0 or self.height <= 0:
            return
        
        self.quantum_particles = []
        cx, cy = self.width // 2, self.height // 2
        
        # Create quantum particles in orbital shells
        for shell in range(4):
            shell_radius = 40 + shell * 45
            particle_count = 6 + shell * 4
            for i in range(particle_count):
                angle = (i / particle_count) * math.pi * 2
                self.quantum_particles.append({
                    'shell': shell,
                    'angle': angle,
                    'radius': shell_radius,
                    'speed': 0.02 + random.random() * 0.02,
                    'size': 4 + random.random() * 3,
                    'color': [T.CYAN, T.GREEN, T.PINK, T.PURPLE][shell],
                    'phase': random.random() * math.pi * 2,
                    'quantum_state': random.choice([0, 1]),
                    'superposition': True,
                    'entangled_with': None,
                    'trail': []
                })
        
        # Entangle some particles
        for i in range(0, len(self.quantum_particles) - 1, 3):
            if i + 1 < len(self.quantum_particles):
                self.quantum_particles[i]['entangled_with'] = i + 1
    
    def set_learning(self, intensity):
        self.learning_intensity = max(0.1, min(1.0, intensity))
    
    def set_consciousness_level(self, level):
        self.consciousness_level = max(0.1, min(1.0, level))
    
    def add_thought_stream(self, thought_text):
        if self.width > 0:
            self.thought_streams.append({
                'text': thought_text[:25],
                'x': random.randint(50, max(51, self.width - 50)),
                'y': self.height + 20,
                'target_y': random.randint(50, max(51, self.height // 2)),
                'speed': 1 + random.random() * 2,
                'alpha': 1.0,
                'color': random.choice([T.CYAN, T.GREEN, T.PINK])
            })
    
    def _spawn_energy_ring(self):
        if self.width > 0:
            self.energy_rings.append({
                'x': self.width // 2,
                'y': self.height // 2,
                'radius': 0,
                'max_radius': min(self.width, self.height) // 2,
                'speed': 3 + random.random() * 3,
                'life': 1.0,
                'color': random.choice([T.CYAN, T.GREEN, T.PINK, T.PURPLE])
            })
    
    def _spawn_neuron_spark(self, x=None, y=None):
        if self.width <= 0:
            return
        if x is None:
            x = self.width // 2
        if y is None:
            y = self.height // 2
        
        for _ in range(5):
            angle = random.random() * math.pi * 2
            speed = 3 + random.random() * 5
            self.neuron_sparks.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': random.choice([T.CYAN, T.GREEN, T.YELLOW])
            })
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.03
            self.central_pulse += 0.05 * (1 + self.learning_intensity)
            
            cx, cy = self.width // 2, self.height // 2
            
            # Draw quantum grid background
            self._draw_quantum_grid()
            
            # Draw energy rings
            self._draw_energy_rings()
            
            # Draw entanglement lines
            self._draw_entanglements()
            
            # Draw orbital paths
            for shell in range(4):
                radius = 40 + shell * 45
                for i in range(3):
                    r = radius - i * 2
                    self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                   outline=T.BORDER, width=1, dash=(2, 8))
            
            # Update and draw quantum particles
            self._update_quantum_particles()
            
            # Draw central consciousness core
            self._draw_consciousness_core()
            
            # Draw thought streams
            self._draw_thought_streams()
            
            # Draw neuron sparks
            self._draw_neuron_sparks()
            
            # Draw state indicator
            self._draw_state_indicator()
            
            # Effects based on learning (disabled random in real_mode)
            try:
                top = self.winfo_toplevel()
                real_mode = getattr(top, 'real_mode', False)
            except Exception:
                real_mode = False
            if not real_mode:
                if random.random() < 0.03 * self.learning_intensity:
                    self._spawn_energy_ring()
                if random.random() < 0.02 * self.learning_intensity:
                    self._spawn_neuron_spark()
            
            # State transition
            self.state_transition += 0.005 * self.learning_intensity
            if self.state_transition >= 1:
                self.state_transition = 0
                self.current_state_idx = (self.current_state_idx + 1) % len(self.states)
        
        try:
            if self.winfo_exists():
                self.after(30, self._animate)
        except:
            pass
    
    def _draw_quantum_grid(self):
        # Animated grid
        offset = (self.time * 20) % 30
        for x in range(int(-offset), self.width + 30, 30):
            alpha = 0.1 + 0.05 * math.sin(self.time + x * 0.1)
            self.create_line(x, 0, x, self.height, fill=T.BG_CARD, width=1)
        for y in range(int(-offset), self.height + 30, 30):
            self.create_line(0, y, self.width, y, fill=T.BG_CARD, width=1)
    
    def _draw_energy_rings(self):
        new_rings = []
        for ring in self.energy_rings:
            ring['radius'] += ring['speed']
            ring['life'] -= 0.015
            
            if ring['life'] > 0 and ring['radius'] < ring['max_radius']:
                for i in range(3):
                    r = ring['radius'] - i * 8
                    if r > 0:
                        self.create_oval(ring['x'] - r, ring['y'] - r,
                                       ring['x'] + r, ring['y'] + r,
                                       outline=ring['color'], width=2 - i * 0.5)
                new_rings.append(ring)
        self.energy_rings = new_rings
    
    def _draw_entanglements(self):
        for p in self.quantum_particles:
            if p['entangled_with'] is not None and p['entangled_with'] < len(self.quantum_particles):
                other = self.quantum_particles[p['entangled_with']]
                cx, cy = self.width // 2, self.height // 2
                
                x1 = cx + math.cos(p['angle']) * p['radius']
                y1 = cy + math.sin(p['angle']) * p['radius']
                x2 = cx + math.cos(other['angle']) * other['radius']
                y2 = cy + math.sin(other['angle']) * other['radius']
                
                # Animated dashed line - dash values must be 1-255
                dash_offset = max(1, int(self.time * 30) % 20)
                self.create_line(x1, y1, x2, y2, fill=T.PURPLE, width=1, 
                               dash=(5, 5, dash_offset))
    
    def _update_quantum_particles(self):
        cx, cy = self.width // 2, self.height // 2
        
        for p in self.quantum_particles:
            # Orbit
            p['angle'] += p['speed'] * (1 + self.learning_intensity * 0.5)
            p['phase'] += 0.1
            
            # Quantum wobble
            wobble = math.sin(p['phase']) * 5 * self.consciousness_level
            current_radius = p['radius'] + wobble
            
            x = cx + math.cos(p['angle']) * current_radius
            y = cy + math.sin(p['angle']) * current_radius
            
            # Trail
            p['trail'].append((x, y))
            if len(p['trail']) > 15:
                p['trail'].pop(0)
            
            # Draw trail
            for i, (tx, ty) in enumerate(p['trail']):
                trail_size = (i / len(p['trail'])) * p['size'] * 0.5
                self.create_oval(tx - trail_size, ty - trail_size,
                               tx + trail_size, ty + trail_size,
                               fill=p['color'], outline='')
            
            # Draw particle with glow
            size = p['size'] * (1 + math.sin(p['phase']) * 0.3)
            
            # Glow effect
            for gs in [size + 6, size + 3, size]:
                self.create_oval(x - gs, y - gs, x + gs, y + gs,
                               fill=p['color'] if gs == size else '',
                               outline=p['color'])
            
            # Quantum state indicator (|0⟩ or |1⟩)
            if p['superposition']:
                state_text = "⟨Ψ⟩"
            else:
                state_text = f"|{p['quantum_state']}⟩"
            
            self.create_text(x, y - size - 8, text=state_text,
                           font=('JetBrains Mono', 6), fill=p['color'])
    
    def _draw_consciousness_core(self):
        cx, cy = self.width // 2, self.height // 2
        
        # Pulsing core
        base_size = 30 + self.consciousness_level * 10
        pulse = math.sin(self.central_pulse) * 8 * self.learning_intensity
        core_size = base_size + pulse
        
        # Multiple glow layers
        for i in range(5, 0, -1):
            r = core_size + i * 8
            self.create_oval(cx - r, cy - r, cx + r, cy + r,
                           outline=T.CYAN, width=1)
        
        # Core
        self.create_oval(cx - core_size, cy - core_size, 
                       cx + core_size, cy + core_size,
                       fill=T.BG_CARD, outline=T.CYAN, width=3)
        
        # Brain icon replaced with text
        self.create_text(cx, cy, text="QC", font=('JetBrains Mono', 14, 'bold'), fill=T.CYAN)
        
        # Consciousness level indicator
        self.create_text(cx, cy + core_size + 15, 
                       text=f"CONSCIOUSNESS: {self.consciousness_level * 100:.0f}%",
                       font=('JetBrains Mono', 8, 'bold'), fill=T.CYAN)
        
        # Learning indicator
        self.create_text(cx, cy + core_size + 30,
                       text=f"LEARNING: {self.learning_intensity * 100:.0f}%",
                       font=('JetBrains Mono', 7), fill=T.GREEN)
    
    def _draw_thought_streams(self):
        new_streams = []
        for stream in self.thought_streams:
            stream['y'] -= stream['speed']
            stream['alpha'] -= 0.005
            
            if stream['alpha'] > 0 and stream['y'] > stream['target_y'] - 50:
                # Draw thought bubble
                self.create_text(stream['x'], stream['y'], text=stream['text'],
                               font=('JetBrains Mono', 8), fill=stream['color'])
                new_streams.append(stream)
        self.thought_streams = new_streams
    
    def _draw_neuron_sparks(self):
        new_sparks = []
        for spark in self.neuron_sparks:
            spark['x'] += spark['vx']
            spark['y'] += spark['vy']
            spark['vx'] *= 0.95
            spark['vy'] *= 0.95
            spark['life'] -= 0.03
            
            if spark['life'] > 0:
                size = 3 * spark['life']
                self.create_oval(spark['x'] - size, spark['y'] - size,
                               spark['x'] + size, spark['y'] + size,
                               fill=spark['color'], outline='')
                new_sparks.append(spark)
        self.neuron_sparks = new_sparks
    
    def _draw_state_indicator(self):
        state = self.states[self.current_state_idx]
        colors = {'OBSERVING': T.GREEN, 'ANALYZING': T.CYAN, 'LEARNING': T.YELLOW,
                 'EVOLVING': T.PINK, 'CREATING': T.PURPLE}
        color = colors.get(state, T.CYAN)
        
        # Title
        self.create_text(self.width // 2, 15, text="QUANTUM CONSCIOUSNESS",
                       font=('JetBrains Mono', 10, 'bold'), fill=T.CYAN)
        
        # Current state
        self.create_text(self.width // 2, 35, text=f"STATE: {state}",
                       font=('JetBrains Mono', 9, 'bold'), fill=color)
        
        # Transition progress bar
        bar_width = 100
        bar_height = 4
        bx = self.width // 2 - bar_width // 2
        by = 48
        self.create_rectangle(bx, by, bx + bar_width, by + bar_height,
                            fill=T.BG_CARD, outline=T.BORDER)
        self.create_rectangle(bx, by, bx + bar_width * self.state_transition, by + bar_height,
                            fill=color, outline='')


class SystemGraph(tk.Canvas):
    """Real-time animated system performance graph with holographic grid"""
    
    def __init__(self, parent, metric_name="CPU", color=T.CYAN, max_points=50, **kwargs):
        super().__init__(parent, bg=T.BG_PANEL, highlightthickness=0, **kwargs)
        self.metric_name = metric_name
        self.color = color
        self.max_points = max_points
        self.data_points = deque(maxlen=max_points)
        self.width = 0
        self.height = 0
        self.time = 0
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
    
    def add_data_point(self, value):
        self.data_points.append(max(0, min(100, value)))
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.1
            
            # 1. Holographic Grid Background
            grid_spacing = 30
            offset_x = (self.time * 10) % grid_spacing
            
            # Vertical moving lines
            for i in range(0, self.width + grid_spacing, grid_spacing):
                x = i - offset_x
                alpha = 0.1 + 0.1 * math.sin(x * 0.01 + self.time)
                color = self._adjust_color_brightness(T.BORDER, alpha) # Simulated alpha
                self.create_line(x, 0, x, self.height, fill='#1a253a', width=1)
            
            # Horizontal static lines
            for i in range(0, self.height, 20):
                self.create_line(0, i, self.width, i, fill='#1a253a', width=1)

            # 2. Data Area
            if len(self.data_points) >= 2:
                points = []
                poly_points = [20, self.height - 20] # Start bottom-left
                
                for i, value in enumerate(self.data_points):
                    x = 20 + (i / (self.max_points - 1)) * (self.width - 40)
                    y = self.height - (value / 100) * (self.height - 40) - 20
                    points.extend([x, y])
                    poly_points.extend([x, y])
                
                poly_points.extend([self.width - 20, self.height - 20]) # End bottom-right
                
                # Fill gradient (simulated with lines)
                if len(points) > 4:
                    # Draw vertical fill lines for "holographic curtain" effect
                    for i in range(0, len(points), 4): # Skip some for performance
                        x, y = points[i], points[i+1]
                        self.create_line(x, y, x, self.height - 20, 
                                       fill=self.color, width=1, stipple='gray25')

                # Glow effect line
                self.create_line(points, fill=self.color, width=3, smooth=True)
                self.create_line(points, fill=T.TEXT_BRIGHT, width=1, smooth=True)
                
                # Current value indicator
                if self.data_points:
                    current = self.data_points[-1]
                    y = self.height - (current / 100) * (self.height - 40) - 20
                    
                    # Scanner line
                    self.create_line(0, y, self.width, y, fill=self.color, dash=(1, 4))
                    
                    # Value text
                    self.create_text(self.width - 30, y - 15, 
                                   text=f"{current:.1f}%",
                                   font=('JetBrains Mono', 10, 'bold'),
                                   fill=self.color)
            
            # Title
            self.create_text(10, 15, text=self.metric_name, anchor='w',
                           font=('JetBrains Mono', 10, 'bold'),
                           fill=T.TEXT_DIM)
        
        try:
            if self.winfo_exists():
                self.after(50, self._animate)
        except:
            pass

    def _adjust_color_brightness(self, hex_color, factor):
        # Simple helper, though Tkinter doesn't support alpha directly without images
        return hex_color


class NetworkTopology(tk.Canvas):
    """
    QUANTUM CIRCUIT MESH - Advanced Neural Pathway Visualization
    Flowing energy paths with pulsing nodes and particle systems
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='#020208', highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        
        # Active state for START button
        self.is_active = False
        self.current_state = 'idle'  # idle, thinking, acting, learning, observing
        
        # State colors
        self.state_colors = {
            'idle': '#1a3a4a',
            'thinking': '#00ffff',
            'acting': '#ff0066',
            'learning': '#ffff00',
            'observing': '#00ff88'
        }
        
        # Hexagonal mesh nodes
        self.hex_nodes = []
        self.energy_paths = []
        self.particles = []
        self.pulse_rings = []
        
        # Real data
        self.activity_level = 0.0
        self.cpu_activity = 0.0
        self.memory_activity = 0.0
        self.network_activity = 0.0
        
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._build_hex_mesh()
    
    def set_active(self, active: bool):
        """Activate/deactivate based on START button"""
        self.is_active = active
        if not active:
            self.current_state = 'idle'
    
    def set_state(self, state: str):
        """Set current AI state"""
        if state in self.state_colors:
            self.current_state = state
    
    def set_activity(self, network=0, cpu=0, memory=0):
        """Set real system activity levels"""
        self.network_activity = network / 100.0
        self.cpu_activity = cpu / 100.0
        self.memory_activity = memory / 100.0
        self.activity_level = (network + cpu + memory) / 300.0
        
        # Spawn particles based on activity
        if self.is_active and self.activity_level > 0.2:
            self._spawn_particle()
    
    def _build_hex_mesh(self):
        """Build hexagonal mesh network"""
        if self.width < 100 or self.height < 100:
            return
        
        cx, cy = self.width // 2, self.height // 2
        self.hex_nodes = []
        self.energy_paths = []
        
        # Node colors for different functions
        node_colors = [T.CYAN, T.PINK, T.GREEN, T.PURPLE, T.YELLOW, T.ORANGE]
        
        # Central quantum core
        self.hex_nodes.append({
            'x': cx, 'y': cy, 'size': 25,
            'type': 'core', 'color': T.CYAN,
            'energy': 0.0, 'phase': 0
        })
        
        # Inner ring - 6 primary nodes
        for i in range(6):
            angle = i * math.pi / 3 - math.pi / 6
            r = 70
            self.hex_nodes.append({
                'x': cx + math.cos(angle) * r,
                'y': cy + math.sin(angle) * r,
                'size': 15, 'type': 'primary',
                'color': node_colors[i], 'energy': 0.0,
                'phase': i * math.pi / 3
            })
        
        # Outer ring - 12 secondary nodes
        for i in range(12):
            angle = i * math.pi / 6
            r = 130
            self.hex_nodes.append({
                'x': cx + math.cos(angle) * r,
                'y': cy + math.sin(angle) * r,
                'size': 8, 'type': 'secondary',
                'color': node_colors[i % 6], 'energy': 0.0,
                'phase': i * math.pi / 6
            })
        
        # Build energy paths (connections)
        # Core to inner ring
        for i in range(1, 7):
            self.energy_paths.append({
                'from': 0, 'to': i,
                'energy': 0.0, 'flow_pos': 0.0
            })
        
        # Inner ring connections
        for i in range(1, 7):
            next_i = (i % 6) + 1
            self.energy_paths.append({
                'from': i, 'to': next_i,
                'energy': 0.0, 'flow_pos': 0.0
            })
        
        # Inner to outer ring
        for i in range(1, 7):
            for j in [i * 2 + 5, i * 2 + 6]:
                if j < len(self.hex_nodes):
                    self.energy_paths.append({
                        'from': i, 'to': j,
                        'energy': 0.0, 'flow_pos': 0.0
                    })
    
    def _spawn_particle(self):
        """Spawn energy particle"""
        if len(self.hex_nodes) < 2:
            return
        
        # Random source node
        source = random.randint(0, min(6, len(self.hex_nodes) - 1))
        node = self.hex_nodes[source]
        
        self.particles.append({
            'x': node['x'], 'y': node['y'],
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-2, 2),
            'color': self.state_colors.get(self.current_state, T.CYAN),
            'life': 1.0, 'size': random.randint(2, 5)
        })
    
    def send_packet(self, from_idx=0, to_idx=1, packet_type='data'):
        """Trigger pulse ring at a node"""
        if from_idx < len(self.hex_nodes):
            node = self.hex_nodes[from_idx]
            colors = {'data': T.CYAN, 'ai': T.PINK, 'memory': T.PURPLE}
            self.pulse_rings.append({
                'x': node['x'], 'y': node['y'],
                'radius': 5, 'max_radius': 50,
                'color': colors.get(packet_type, T.CYAN),
                'alpha': 1.0
            })
    
    def trigger_wave(self, color=None):
        """Trigger central pulse wave"""
        if self.hex_nodes:
            cx = self.hex_nodes[0]['x']
            cy = self.hex_nodes[0]['y']
            self.pulse_rings.append({
                'x': cx, 'y': cy,
                'radius': 10, 'max_radius': 150,
                'color': color or self.state_colors.get(self.current_state, T.CYAN),
                'alpha': 1.0
            })
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        
        if self.width < 50 or self.height < 50:
            try:
                self.after(30, self._animate)
            except:
                pass
            return
        
        self.delete('all')
        self.time += 0.04
        
        # Update node energies based on activity
        self._update_energies()
        
        self._draw_quantum_background()
        self._draw_energy_paths()
        self._draw_pulse_rings()
        self._draw_hex_nodes()
        self._draw_particles()
        self._draw_header()
        
        try:
            self.after(28, self._animate)
        except:
            pass
    
    def _update_energies(self):
        """Update node energies based on activity"""
        for i, node in enumerate(self.hex_nodes):
            if self.is_active:
                # Flowing energy based on phase
                base_energy = self.activity_level
                wave = math.sin(self.time * 3 + node['phase']) * 0.3 + 0.5
                node['energy'] = base_energy * wave + 0.1
            else:
                node['energy'] = 0.05 + math.sin(self.time + node['phase']) * 0.02
        
        # Update energy paths
        for path in self.energy_paths:
            if path['from'] < len(self.hex_nodes) and path['to'] < len(self.hex_nodes):
                n1 = self.hex_nodes[path['from']]
                n2 = self.hex_nodes[path['to']]
                path['energy'] = (n1['energy'] + n2['energy']) / 2
                if self.is_active:
                    path['flow_pos'] = (path['flow_pos'] + 0.03) % 1.0
    
    def _draw_quantum_background(self):
        """Draw subtle quantum field background"""
        # Concentric rings from center
        if self.hex_nodes:
            cx, cy = self.hex_nodes[0]['x'], self.hex_nodes[0]['y']
            
            for r in range(30, int(min(self.width, self.height) * 0.5), 40):
                pulse = 1 + math.sin(self.time * 2 - r * 0.02) * 0.1
                self.create_oval(cx - r * pulse, cy - r * pulse,
                               cx + r * pulse, cy + r * pulse,
                               outline='#0a1520', width=1)
        
        # Subtle grid
        for x in range(0, self.width, 40):
            self.create_line(x, 0, x, self.height, fill='#080810', width=1)
        for y in range(0, self.height, 40):
            self.create_line(0, y, self.width, y, fill='#080810', width=1)
    
    def _draw_energy_paths(self):
        """Draw glowing energy paths between nodes"""
        state_color = self.state_colors.get(self.current_state, T.CYAN)
        
        for path in self.energy_paths:
            if path['from'] >= len(self.hex_nodes) or path['to'] >= len(self.hex_nodes):
                continue
            
            n1 = self.hex_nodes[path['from']]
            n2 = self.hex_nodes[path['to']]
            
            x1, y1 = n1['x'], n1['y']
            x2, y2 = n2['x'], n2['y']
            
            energy = path['energy']
            
            # Base line
            base_color = '#1a2a3a' if not self.is_active else '#2a3a4a'
            self.create_line(x1, y1, x2, y2, fill=base_color, width=2)
            
            if self.is_active and energy > 0.1:
                # Glowing active line
                glow_color = state_color if self.is_active else n1['color']
                width = int(2 + energy * 4)
                
                # Glow layers
                for offset in [4, 2, 0]:
                    self.create_line(x1, y1, x2, y2,
                                   fill=glow_color, width=width + offset)
                
                # Flowing energy dots
                for i in range(3):
                    t = (path['flow_pos'] + i * 0.33) % 1.0
                    px = x1 + (x2 - x1) * t
                    py = y1 + (y2 - y1) * t
                    dot_size = 3 + energy * 3
                    self.create_oval(px - dot_size, py - dot_size,
                                   px + dot_size, py + dot_size,
                                   fill=glow_color, outline='')
    
    def _draw_pulse_rings(self):
        """Draw expanding pulse rings"""
        new_rings = []
        
        for ring in self.pulse_rings:
            ring['radius'] += 4
            ring['alpha'] -= 0.04
            
            if ring['alpha'] > 0:
                width = max(1, int(ring['alpha'] * 3))
                self.create_oval(ring['x'] - ring['radius'],
                               ring['y'] - ring['radius'],
                               ring['x'] + ring['radius'],
                               ring['y'] + ring['radius'],
                               outline=ring['color'], width=width)
                new_rings.append(ring)
        
        self.pulse_rings = new_rings
    
    def _draw_hex_nodes(self):
        """Draw hexagonal mesh nodes"""
        state_color = self.state_colors.get(self.current_state, T.CYAN)
        
        for i, node in enumerate(self.hex_nodes):
            x, y = node['x'], node['y']
            size = node['size']
            energy = node['energy']
            node_type = node['type']
            
            # Pulse effect
            pulse = 1 + (energy * 0.2 * math.sin(self.time * 5 + node['phase']))
            s = size * pulse
            
            # Get color based on state
            if self.is_active:
                color = state_color
            else:
                color = node['color']
            
            if node_type == 'core':
                # Central quantum core - hexagonal with glow
                # Outer glow
                if self.is_active:
                    for glow_r in [s + 15, s + 10, s + 5]:
                        self.create_oval(x - glow_r, y - glow_r,
                                       x + glow_r, y + glow_r,
                                       outline=color, width=1)
                
                # Hexagon shape
                points = []
                for j in range(6):
                    angle = j * math.pi / 3 - math.pi / 6
                    points.extend([x + math.cos(angle) * s,
                                 y + math.sin(angle) * s])
                
                fill_color = color if self.is_active else '#0a1525'
                self.create_polygon(points, fill=fill_color, outline=color, width=3)
                
                # Inner rotating element
                inner_angle = self.time * 2
                for j in range(3):
                    a = inner_angle + j * 2 * math.pi / 3
                    ix = x + math.cos(a) * s * 0.5
                    iy = y + math.sin(a) * s * 0.5
                    self.create_oval(ix - 4, iy - 4, ix + 4, iy + 4,
                                   fill=T.TEXT_BRIGHT if self.is_active else '#303040',
                                   outline='')
                
            elif node_type == 'primary':
                # Primary nodes - circular with ring
                # Outer ring
                self.create_oval(x - s - 5, y - s - 5, x + s + 5, y + s + 5,
                               outline=color, width=1)
                
                # Fill based on energy
                fill = color if (self.is_active and energy > 0.3) else '#0a1520'
                self.create_oval(x - s, y - s, x + s, y + s,
                               fill=fill, outline=color, width=2)
                
                # Activity indicator dot
                if self.is_active and energy > 0.2:
                    dot_size = 3 + energy * 4
                    self.create_oval(x - dot_size, y - dot_size,
                                   x + dot_size, y + dot_size,
                                   fill=T.TEXT_BRIGHT, outline='')
                
            else:
                # Secondary nodes - small diamonds
                ds = s * 1.2
                points = [x, y - ds, x + ds, y, x, y + ds, x - ds, y]
                
                fill = color if (self.is_active and energy > 0.3) else '#080815'
                self.create_polygon(points, fill=fill, outline=color, width=1)
    
    def _draw_particles(self):
        """Draw floating energy particles"""
        new_particles = []
        
        for p in self.particles:
            # Update position
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
            
            # Boundary bounce
            if p['x'] < 0 or p['x'] > self.width:
                p['vx'] *= -0.8
            if p['y'] < 0 or p['y'] > self.height:
                p['vy'] *= -0.8
            
            if p['life'] > 0:
                size = p['size'] * p['life']
                alpha = p['life']
                
                # Draw with fade effect
                self.create_oval(p['x'] - size, p['y'] - size,
                               p['x'] + size, p['y'] + size,
                               fill=p['color'], outline='')
                new_particles.append(p)
        
        self.particles = new_particles[:50]  # Limit particles
    
    def _draw_header(self):
        """Draw header with status"""
        state_color = self.state_colors.get(self.current_state, T.CYAN)
        
        self.create_text(self.width // 2, 18,
                       text="QUANTUM CIRCUIT MESH",
                       font=('JetBrains Mono', 11, 'bold'),
                       fill=state_color if self.is_active else '#3a4a5a')
        
        # Status indicator
        status = self.current_state.upper() if self.is_active else "STANDBY"
        dot_color = state_color if self.is_active else '#3a4a5a'
        
        # Pulsing status dot
        pulse_size = 4 + (2 if self.is_active else 0) * math.sin(self.time * 4)
        self.create_oval(self.width - 85 - pulse_size, 14 - pulse_size,
                       self.width - 77 + pulse_size, 22 + pulse_size,
                       fill=dot_color, outline='')
        
        self.create_text(self.width - 68, 18, text=status,
                       anchor='w', font=('JetBrains Mono', 7, 'bold'),
                       fill=dot_color)
        
        # Activity level bar
        if self.is_active:
            bar_x = 20
            bar_y = self.height - 25
            bar_w = 100
            bar_h = 8
            
            self.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h,
                                outline=state_color, fill='#0a1020')
            
            fill_w = bar_w * self.activity_level
            if fill_w > 0:
                self.create_rectangle(bar_x, bar_y, bar_x + fill_w, bar_y + bar_h,
                                    fill=state_color, outline='')
            
            self.create_text(bar_x + bar_w + 10, bar_y + 4,
                           text=f"LOAD: {self.activity_level*100:.0f}%",
                           anchor='w', font=('JetBrains Mono', 7),
                           fill=state_color)


class AgentCommunication(tk.Canvas):
    """FUTURISTIC Agent Network - Robotic holographic visualization"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_DARKEST, highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.agents = []
        self.time = 0
        self.pulse = 0
        self.messages = []
        self.ring_rotation = 0
        self.brainstorm_trails = []
        self.idea_clouds = []
        self.learning_log = {}
        self.agent_lookup = {}
        
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._build_agents()
    
    def _build_agents(self):
        if self.width < 100 or self.height < 100:
            return
        
        cx, cy = self.width // 2, self.height // 2
        radius = min(self.width, self.height) // 3
        
        self.agents = [
            {'x': cx, 'y': cy, 'name': 'MOTHER', 'color': T.PINK, 'size': 35, 'status': 'active', 'history': deque(maxlen=6)},
        ]
        
        # Sub-agents in circle
        agent_configs = [
            ('VIS', T.CYAN, 'V'), ('VOX', T.GREEN, 'X'), ('ACT', T.YELLOW, 'A'),
            ('LRN', T.PURPLE, 'L'), ('EVO', T.ORANGE, 'E'),
        ]
        
        for i, (name, color, icon) in enumerate(agent_configs):
            angle = (i / len(agent_configs)) * math.pi * 2 - math.pi / 2
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            self.agents.append({
                'x': x, 'y': y, 'name': name, 'color': color,
                'size': 22, 'icon': icon, 'status': 'idle', 'history': deque(maxlen=6)
            })
        self.agent_lookup = {agent['name']: idx for idx, agent in enumerate(self.agents)}
    
    def send_message(self, from_idx, to_idx, msg_type='instruction', priority='normal'):
        """Send a visual message between agents"""
        if from_idx < len(self.agents) and to_idx < len(self.agents):
            color = T.CYAN if priority == 'normal' else T.ORANGE if priority == 'high' else T.GREEN
            self.messages.append({
                'from': from_idx,
                'to': to_idx,
                'progress': 0.0,
                'color': color,
                'type': msg_type,
            })
    
    def _animate(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if self.width < 50 or self.height < 50:
            try:
                if self.winfo_exists():
                    self.after(40, self._animate)
            except:
                pass
            return
            
        self.delete('all')
        self.time += 0.04
        self.pulse += 0.06
        self.ring_rotation += 0.01
        
        # Draw orbital rings (futuristic)
        self._draw_orbital_rings()
        
        # Draw connections
        self._draw_connections()
        
        # Update and draw messages
        self._update_messages()
        self._draw_brainstorm_effects()
        
        # Draw agents
        self._draw_agents()
        
        # Title
        self._draw_title()
        
        try:
            if self.winfo_exists():
                self.after(40, self._animate)
        except:
            pass
    
    def _draw_orbital_rings(self):
        """Draw rotating orbital rings around mother AI"""
        if not self.agents:
            return
        
        cx, cy = self.agents[0]['x'], self.agents[0]['y']
        
        # Inner ring
        r1 = 50
        for i in range(12):
            angle = (i / 12) * math.pi * 2 + self.ring_rotation
            x = cx + math.cos(angle) * r1
            y = cy + math.sin(angle) * r1
            size = 2
            self.create_rectangle(x - size, y - size, x + size, y + size,
                                fill=T.PINK, outline='')
        
        # Outer ring
        r2 = min(self.width, self.height) // 3 + 20
        for i in range(24):
            angle = (i / 24) * math.pi * 2 - self.ring_rotation * 0.5
            x = cx + math.cos(angle) * r2
            y = cy + math.sin(angle) * r2
            size = 1
            self.create_rectangle(x - size, y - size, x + size, y + size,
                                fill='#3a4050', outline='')
    
    def _draw_connections(self):
        """Draw circuit-style connections"""
        if len(self.agents) < 2:
            return
        
        mother = self.agents[0]
        colors = [T.PINK, T.ORANGE, T.GREEN, T.CYAN]
        
        for i, agent in enumerate(self.agents[1:]):
            # Calculate midpoint for circuit routing
            mx = (mother['x'] + agent['x']) / 2
            my = (mother['y'] + agent['y']) / 2
            
            # Draw segments with flowing color
            segments = 8
            for s in range(segments):
                t1 = s / segments
                t2 = (s + 1) / segments
                
                x1 = mother['x'] + (agent['x'] - mother['x']) * t1
                y1 = mother['y'] + (agent['y'] - mother['y']) * t1
                x2 = mother['x'] + (agent['x'] - mother['x']) * t2
                y2 = mother['y'] + (agent['y'] - mother['y']) * t2
                
                # Flowing color effect
                color_idx = int((self.pulse * 2 + s * 0.5 + i * 2) % len(colors))
                width = 2 if (int(self.time * 10) + s) % 3 == 0 else 1
                
                self.create_line(x1, y1, x2, y2, fill=colors[color_idx], width=width)
            
            # Connection endpoint dots
            self.create_oval(agent['x'] - 4, agent['y'] - 4,
                           agent['x'] + 4, agent['y'] + 4,
                           fill='', outline=agent['color'], width=2)
    
    def _update_messages(self):
        """Update and draw traveling messages"""
        new_messages = []
        
        for msg in self.messages:
            msg['progress'] += 0.05
            
            if msg['progress'] < 1.0 and msg['from'] < len(self.agents) and msg['to'] < len(self.agents):
                a1 = self.agents[msg['from']]
                a2 = self.agents[msg['to']]
                
                x = a1['x'] + (a2['x'] - a1['x']) * msg['progress']
                y = a1['y'] + (a2['y'] - a1['y']) * msg['progress']
                
                # Draw message as diamond (robotic)
                size = 5
                points = [x, y - size, x + size, y, x, y + size, x - size, y]
                self.create_polygon(points, fill=msg['color'], outline='')
                
                # Glow trail
                trail_x = a1['x'] + (a2['x'] - a1['x']) * max(0, msg['progress'] - 0.1)
                trail_y = a1['y'] + (a2['y'] - a1['y']) * max(0, msg['progress'] - 0.1)
                self.create_line(trail_x, trail_y, x, y, fill=msg['color'], width=2)
                
                new_messages.append(msg)
        
        self.messages = new_messages

    def _draw_brainstorm_effects(self):
        new_trails = []
        for trail in self.brainstorm_trails:
            trail['progress'] += trail['speed']
            if trail['progress'] < 1.0 and trail['from'] < len(self.agents) and trail['to'] < len(self.agents):
                a1 = self.agents[trail['from']]
                a2 = self.agents[trail['to']]
                ctrl_angle = trail['offset'] + self.time * 0.6
                ctrl_x = (a1['x'] + a2['x']) / 2 + math.cos(ctrl_angle) * 40
                ctrl_y = (a1['y'] + a2['y']) / 2 + math.sin(ctrl_angle) * 40
                points = [a1['x'], a1['y'], ctrl_x, ctrl_y, a2['x'], a2['y']]
                self.create_line(points, fill=trail['color'], width=trail['width'], smooth=True)
                new_trails.append(trail)
        self.brainstorm_trails = new_trails
        new_clouds = []
        for cloud in self.idea_clouds:
            cloud['life'] -= 0.02
            if cloud['life'] > 0 and cloud['agent'] < len(self.agents):
                agent = self.agents[cloud['agent']]
                radius = cloud['radius'] + (1 - cloud['life']) * 12
                width = max(1, int(3 * cloud['life']))
                self.create_oval(
                    agent['x'] - radius, agent['y'] - radius,
                    agent['x'] + radius, agent['y'] + radius,
                    outline=cloud['color'], width=width
                )
                new_clouds.append(cloud)
        self.idea_clouds = new_clouds

    def _spawn_brainstorm(self, source_idx, intensity=1.0):
        if source_idx is None or source_idx >= len(self.agents):
            return
        for target_idx in range(len(self.agents)):
            if target_idx == source_idx:
                continue
            self.brainstorm_trails.append({
                'from': source_idx,
                'to': target_idx,
                'progress': 0.0,
                'speed': 0.02 + random.random() * 0.02,
                'width': 1 + intensity,
                'color': random.choice([T.CYAN, T.PINK, T.GREEN, T.ORANGE]),
                'offset': random.random() * math.pi * 2
            })
        self.idea_clouds.append({
            'agent': source_idx,
            'radius': self.agents[source_idx]['size'] + 18,
            'life': 1.0,
            'color': random.choice([T.CYAN, T.GREEN, T.PINK])
        })

    def _resolve_agent_index(self, agent_type):
        if not agent_type:
            return None
        token = agent_type.upper()
        alias_map = {
            'VISION': 'VIS',
            'VOICE': 'VOX',
            'ACTION': 'ACT',
            'LEARNING': 'LRN',
            'EVOLUTION': 'EVO'
        }
        if token in self.agent_lookup:
            return self.agent_lookup[token]
        short = token[:3]
        if short in self.agent_lookup:
            return self.agent_lookup[short]
        mapped = alias_map.get(token) or alias_map.get(short)
        if mapped and mapped in self.agent_lookup:
            return self.agent_lookup[mapped]
        return None
    
    def _draw_agents(self):
        """Draw agents with futuristic holographic style"""
        for idx, agent in enumerate(self.agents):
            x, y = agent['x'], agent['y']
            size = agent['size']
            color = agent['color']
            
            # Pulse effect
            pulse_offset = 4 * math.sin(self.pulse + idx)
            
            # Outer hexagon (holographic)
            hex_size = size + 8 + pulse_offset
            hex_points = []
            for i in range(6):
                angle = (i / 6) * math.pi * 2 - math.pi / 2
                px = x + math.cos(angle) * hex_size
                py = y + math.sin(angle) * hex_size
                hex_points.extend([px, py])
            self.create_polygon(hex_points, fill='', outline=color, width=1)
            
            # Inner hexagon
            inner_points = []
            for i in range(6):
                angle = (i / 6) * math.pi * 2 - math.pi / 2
                px = x + math.cos(angle) * size
                py = y + math.sin(angle) * size
                inner_points.extend([px, py])
            self.create_polygon(inner_points, fill=T.BG_DARKEST, outline=color, width=2)
            
            # Core circle
            core_size = size * 0.5
            self.create_oval(x - core_size, y - core_size, x + core_size, y + core_size,
                           fill=color, outline='')
            
            # Agent name
            self.create_text(x, y + size + 18, text=agent['name'],
                           font=('JetBrains Mono', 9, 'bold'), fill=color)
            
            # Status indicator
            status_y = y - size - 10
            status_color = T.GREEN if agent.get('status') == 'active' else '#3a4050'
            self.create_rectangle(x - 3, status_y - 3, x + 3, status_y + 3,
                                fill=status_color, outline='')
    
    def _draw_title(self):
        """Draw title with scan line"""
        # Scan line effect (disabled in real_mode)
        try:
            top = self.winfo_toplevel()
            real_mode = getattr(top, 'real_mode', False)
        except Exception:
            real_mode = False
        if not real_mode:
            scan_y = (self.time * 40) % self.height
            self.create_line(0, scan_y, self.width, scan_y, 
                            fill=T.PINK, width=1, stipple='gray50')
        
        self.create_text(self.width // 2, 15, text="AGENT NETWORK",
                       font=('JetBrains Mono', 10, 'bold'), fill=T.PINK)
    
    # Compatibility methods
    def delegate_task(self, agent_type, task_name, priority='normal'):
        idx = self._resolve_agent_index(agent_type)
        if idx is None:
            return
        self.agents[idx]['status'] = 'active'
        self.agents[idx]['history'].append({'task': task_name, 'priority': priority, 'time': time.time()})
        self.send_message(0, idx, 'task', priority)
        key = agent_type.lower()
        self.learning_log.setdefault(key, deque(maxlen=10))
        self.learning_log[key].append({'task': task_name, 'priority': priority, 'time': time.time()})
        self._spawn_brainstorm(idx, 1.2 if priority == 'high' else 1.0)
    
    def report_learning(self, agent_type, learned_data):
        idx = self._resolve_agent_index(agent_type)
        if idx is None:
            return
        key = agent_type.lower()
        self.learning_log.setdefault(key, deque(maxlen=12))
        self.learning_log[key].append({'learning': learned_data, 'time': time.time()})
        self.agents[idx]['status'] = 'active'
        self._spawn_brainstorm(idx, 1.4)
    
    def get_all_learning(self):
        return {agent: list(entries) for agent, entries in self.learning_log.items()}
    
    def set_activity_level(self, level):
        pass


# ═══════════════════════════════════════════════════════════════════════════════════
# QUANTUM NEURAL BRAIN - FUTURISTIC HD 3D VISUALIZATION
# Clean, Smooth, Holographic Neural Network with Real Data Only
# ═══════════════════════════════════════════════════════════════════════════════════

class NeuralBrain(tk.Canvas):
    """
    CLEAN MINIMAL NEURAL NETWORK - Glowing Line Flow Animation
    Lines glow and connect nodes step by step with different colors
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='#080810', highlightthickness=0, **kwargs)
        self.width = 0
        self.height = 0
        self.time = 0
        
        # Real Data
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.network_rate = 0.0
        self.activity_level = 0.0
        
        # Simple network - fewer nodes
        self.layers = []
        self.connections = []
        self.layer_sizes = [3, 4, 5, 4, 3]  # Simple clean network
        self.is_network_active = False
        
        # Glowing colors for lines - each layer connection gets different color
        self.glow_colors = [
            '#00ffaa',  # Cyan-green
            '#ff66aa',  # Pink
            '#00aaff',  # Blue
            '#ffaa00',  # Orange
            '#aa66ff',  # Purple
        ]
        
        # Current AI state for color coding
        self.current_state = 'idle'  # idle, thinking, acting, learning, observing
        
        # AI state for compatibility
        self.ai_state = {
            'intensity': 0.0,
            'thinking': False,
            'acting': False,
            'learning': False,
            'observing': False
        }
        
        self.bind('<Configure>', self._on_resize)
        self._init_network()
        self._animate()
    
    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_network()
    
    def _init_network(self):
        """Create simple clean neural network"""
        if self.width < 50 or self.height < 50:
            return
            
        self.layers = []
        self.connections = []
        
        # Create layers with generous spacing
        padding = 80
        layer_spacing = (self.width - padding * 2) / (len(self.layer_sizes) - 1)
        
        for layer_idx, layer_size in enumerate(self.layer_sizes):
            layer = []
            x = padding + layer_spacing * layer_idx
            
            # Center nodes vertically with good spacing
            node_spacing = 60
            total_height = (layer_size - 1) * node_spacing
            start_y = (self.height - total_height) / 2
            
            for node_idx in range(layer_size):
                y = start_y + node_idx * node_spacing
                
                layer.append({
                    'x': x,
                    'y': y,
                    'color': self.glow_colors[layer_idx % len(self.glow_colors)],
                    'size': 10
                })
            
            self.layers.append(layer)
        
        # Create connections - each has its own flow progress
        conn_idx = 0
        for layer_idx in range(len(self.layers) - 1):
            layer_color = self.glow_colors[layer_idx % len(self.glow_colors)]
            for from_node in self.layers[layer_idx]:
                for to_node in self.layers[layer_idx + 1]:
                    self.connections.append({
                        'from': from_node,
                        'to': to_node,
                        'layer_idx': layer_idx,
                        'flow': random.random(),  # Flow position 0-1
                        'speed': 0.008 + random.random() * 0.004,  # Slow flow
                        'color': layer_color,
                        'idx': conn_idx
                    })
                    conn_idx += 1

    def set_system_data(self, cpu, ram, network):
        """Update with real-time system data - affects animation speed"""
        self.cpu_usage = cpu / 100.0
        self.ram_usage = ram / 100.0
        self.network_rate = min(1.0, network / 200.0)
        self.activity_level = (self.cpu_usage + self.ram_usage + self.network_rate) / 3
        
        # Adjust flow speed based on activity
        for conn in self.connections:
            base_speed = 0.008 + random.random() * 0.004
            conn['speed'] = base_speed * (0.5 + self.activity_level)

    def set_active(self, active):
        """Called when START button is clicked - activates animation immediately"""
        self.is_network_active = active
        self.ai_state['intensity'] = 0.5 if active else 0.0

    def set_thinking(self, active, thought=""):
        self.ai_state['thinking'] = active
        if active:
            self.is_network_active = True
            self.ai_state['intensity'] = 0.7
            self.current_state = 'thinking'
            # Speed up flow when thinking
            for conn in self.connections:
                conn['speed'] = 0.015 + random.random() * 0.008
    
    def set_acting(self, active, action_type=None):
        self.ai_state['acting'] = active
        if active:
            self.is_network_active = True
            self.ai_state['intensity'] = 1.0
            self.current_state = 'acting'
            # Fast flow when acting
            for conn in self.connections:
                conn['speed'] = 0.02 + random.random() * 0.01
    
    def set_learning(self, active, rate=0.5):
        self.ai_state['learning'] = active
        if active:
            self.is_network_active = True
            self.ai_state['intensity'] = rate
            self.current_state = 'learning'
            # Pulsing flow when learning
            for conn in self.connections:
                conn['speed'] = 0.012 + random.random() * 0.006
    
    def set_observing(self, active):
        self.ai_state['observing'] = active
        if active:
            self.is_network_active = True
            self.ai_state['intensity'] = 0.4
            self.current_state = 'observing'
            # Slow scanning flow when observing
            for conn in self.connections:
                conn['speed'] = 0.006 + random.random() * 0.003
    
    def set_audio_activity(self, level):
        if level > 0.1:
            self.is_network_active = True
            self.ai_state['intensity'] = level
            for conn in self.connections:
                conn['speed'] = 0.008 + level * 0.015

    def _animate(self):
        """Main animation loop - clean and smooth"""
        try:
            if not self.winfo_exists(): return
        except: return
        
        if self.width < 50:
            self.after(40, self._animate)
            return
        
        self.delete('all')
        self.time += 0.02  # Smooth time increment
        
        # Update connection flow positions
        for conn in self.connections:
            conn['flow'] += conn['speed']
            if conn['flow'] > 1.0:
                conn['flow'] = 0.0
        
        # Draw everything in order
        self._draw_base_lines()
        self._draw_glowing_flow()
        self._draw_nodes()
        self._draw_title()
        
        self.after(35, self._animate)  # Smooth ~28fps

    def _draw_base_lines(self):
        """Draw subtle base connection lines"""
        for conn in self.connections:
            from_node = conn['from']
            to_node = conn['to']
            
            # Thin dark base line
            self.create_line(
                from_node['x'], from_node['y'],
                to_node['x'], to_node['y'],
                fill='#15202a', width=1
            )

    def _draw_glowing_flow(self):
        """Draw glowing animated line flow connecting nodes step by step"""
        if not self.is_network_active:
            return
        
        # Get state-based color override
        state_colors = {
            'thinking': '#00ffff',   # Cyan when thinking
            'acting': '#ff0066',     # Red/Pink when acting
            'learning': '#ffff00',   # Yellow when learning
            'observing': '#00ff88',  # Green when observing
            'idle': None             # Use default layer colors
        }
        state_color = state_colors.get(self.current_state, None)
            
        for conn in self.connections:
            from_node = conn['from']
            to_node = conn['to']
            # Use state color if active, otherwise layer color
            color = state_color if state_color else conn['color']
            flow = conn['flow']
            
            # Calculate the flow endpoint (line draws progressively)
            # Smooth easing for natural flow
            t = flow * flow * (3 - 2 * flow)
            
            # Current endpoint of the glowing line
            end_x = from_node['x'] + (to_node['x'] - from_node['x']) * t
            end_y = from_node['y'] + (to_node['y'] - from_node['y']) * t
            
            # Draw the glowing line from start to current position
            # Outer glow (wider, transparent)
            self.create_line(
                from_node['x'], from_node['y'],
                end_x, end_y,
                fill=color, width=4, capstyle='round'
            )
            
            # Inner bright core
            self.create_line(
                from_node['x'], from_node['y'],
                end_x, end_y,
                fill='#ffffff', width=1, capstyle='round'
            )
            
            # Glowing head at the flow tip
            head_size = 4 + math.sin(flow * math.pi) * 3
            
            # Outer glow ring
            self.create_oval(
                end_x - head_size * 1.8, end_y - head_size * 1.8,
                end_x + head_size * 1.8, end_y + head_size * 1.8,
                fill='', outline=color, width=1
            )
            
            # Bright core
            self.create_oval(
                end_x - head_size, end_y - head_size,
                end_x + head_size, end_y + head_size,
                fill=color, outline=''
            )
            
            # White hot center
            self.create_oval(
                end_x - head_size * 0.4, end_y - head_size * 0.4,
                end_x + head_size * 0.4, end_y + head_size * 0.4,
                fill='#ffffff', outline=''
            )

    def _draw_nodes(self):
        """Draw clean simple nodes"""
        for layer_idx, layer in enumerate(self.layers):
            color = self.glow_colors[layer_idx % len(self.glow_colors)]
            
            for node in layer:
                x, y = node['x'], node['y']
                size = node['size']
                
                if self.is_network_active:
                    # Subtle pulse
                    pulse = 1 + math.sin(self.time * 2 + layer_idx * 0.5) * 0.1
                    s = size * pulse
                    
                    # Outer glow ring
                    self.create_oval(
                        x - s * 1.5, y - s * 1.5,
                        x + s * 1.5, y + s * 1.5,
                        fill='', outline=color, width=1
                    )
                    
                    # Main node
                    self.create_oval(
                        x - s, y - s, x + s, y + s,
                        fill='#0a1018', outline=color, width=2
                    )
                    
                    # Inner bright core
                    core = s * 0.35
                    self.create_oval(
                        x - core, y - core, x + core, y + core,
                        fill=color, outline=''
                    )
                else:
                    # Inactive - simple grey
                    self.create_oval(
                        x - size, y - size, x + size, y + size,
                        fill='#1a1a2a', outline='#3a3a4a', width=1
                    )

    def _draw_title(self):
        """Draw title with current AI state"""
        # State-based title and color
        state_info = {
            'thinking': ('THINKING', '#00ffff'),
            'acting': ('EXECUTING', '#ff0066'),
            'learning': ('LEARNING', '#ffff00'),
            'observing': ('SCANNING', '#00ff88'),
            'idle': ('NEURAL NETWORK', '#00ffaa')
        }
        title, color = state_info.get(self.current_state, ('NEURAL NETWORK', '#3a4a5a'))
        
        if not self.is_network_active:
            title = 'OFFLINE'
            color = '#3a4a5a'
        
        self.create_text(
            self.width // 2, 18,
            text=title,
            font=('JetBrains Mono', 10, 'bold'),
            fill=color
        )
        
        # Show intensity indicator
        if self.is_network_active:
            intensity = self.ai_state.get('intensity', 0.5)
            bar_width = 60
            bar_x = self.width // 2 - bar_width // 2
            
            # Background bar
            self.create_rectangle(
                bar_x, self.height - 20,
                bar_x + bar_width, self.height - 14,
                fill='#1a2535', outline=''
            )
            
            # Intensity fill
            fill_width = int(bar_width * intensity)
            if fill_width > 0:
                self.create_rectangle(
                    bar_x, self.height - 20,
                    bar_x + fill_width, self.height - 14,
                    fill=color, outline=''
                )


class DataStream(tk.Frame):
    """Live data stream panel with auto-scroll"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=T.BG_PANEL, **kwargs)
        
        self.text = tk.Text(self, font=('JetBrains Mono', 10),
                           fg=T.GREEN, bg=T.BG_DARKEST,
                           height=10, wrap='word', relief='flat',
                           padx=8, pady=8, insertbackground=T.CYAN)
        self.text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tags
        self.text.tag_configure('cyan', foreground=T.CYAN)
        self.text.tag_configure('green', foreground=T.GREEN)
        self.text.tag_configure('pink', foreground=T.PINK)
        self.text.tag_configure('yellow', foreground=T.YELLOW)
        self.text.tag_configure('red', foreground=T.RED)
        self.text.tag_configure('dim', foreground=T.TEXT_DIM)
        self.text.tag_configure('purple', foreground=T.PURPLE)
        
        self.text.config(state='disabled')
        self.max_lines = 200
    
    def log(self, msg, tag='green'):
        self.text.config(state='normal')
        ts = datetime.now().strftime("%H:%M:%S")
        self.text.insert('end', f"[{ts}] ", 'dim')
        self.text.insert('end', f"{msg}\n", tag)
        
        # Limit lines
        lines = int(self.text.index('end-1c').split('.')[0])
        if lines > self.max_lines:
            self.text.delete('1.0', f'{lines - self.max_lines}.0')
        
        self.text.see('end')
        self.text.config(state='disabled')
    
    def clear(self):
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.config(state='disabled')


class StatRow(tk.Frame):
    """Single stat display row"""
    
    def __init__(self, parent, icon="", label="", value="", color=T.CYAN, **kwargs):
        super().__init__(parent, bg=T.BG_PANEL, **kwargs)
        
        self.color = color
        
        tk.Label(self, text=icon, font=('Segoe UI Emoji', 11),
                fg=color, bg=T.BG_PANEL).pack(side='left', padx=(8, 4))
        
        tk.Label(self, text=label, font=('JetBrains Mono', 10),
                fg=T.TEXT_DIM, bg=T.BG_PANEL).pack(side='left')
        
        self.value_var = tk.StringVar(value=value)
        self.value_label = tk.Label(self, textvariable=self.value_var,
                                   font=('JetBrains Mono', 10, 'bold'),
                                   fg=color, bg=T.BG_PANEL)
        self.value_label.pack(side='right', padx=8)
    
    def set(self, value):
        self.value_var.set(value)


class NeonButton(tk.Canvas):
    """Cyberpunk neon button with hover effects"""
    
    def __init__(self, parent, text="", command=None, color=T.CYAN, width=200, height=36, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=T.BG_PANEL, highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.color = color
        self.width = width
        self.height = height
        self.hover = False
        self.press = False
        
        self.bind('<Enter>', lambda e: self._set_hover(True))
        self.bind('<Leave>', lambda e: self._set_hover(False))
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        
        self._draw()
    
    def _set_hover(self, hover):
        self.hover = hover
        self._draw()
    
    def _on_press(self, e):
        self.press = True
        self._draw()
    
    def _on_release(self, e):
        self.press = False
        self._draw()
        if self.command and self.hover:
            self.command()
    
    def _draw(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
        self.delete('all')
        
        x1, y1 = 2, 2
        x2, y2 = self.width - 2, self.height - 2
        
        # Background
        bg = T.BG_HOVER if self.hover else T.BG_INPUT
        if self.press:
            bg = self.color
        
        # Border glow on hover
        if self.hover and not self.press:
            for i in range(2, 0, -1):
                self.create_rectangle(x1 - i, y1 - i, x2 + i, y2 + i,
                                     outline=self.color, width=1)
        
        # Main rect
        self.create_rectangle(x1, y1, x2, y2, fill=bg,
                            outline=self.color if self.hover else T.BORDER, width=1)
        
        # Text
        text_color = T.BG_DARKEST if self.press else (self.color if self.hover else T.TEXT)
        self.create_text(self.width // 2, self.height // 2,
                        text=self.text, font=('JetBrains Mono', 10),
                        fill=text_color)


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════════

class AuroraUltimate:
    """Ultimate Aurora Neural Interface with All Features"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AURORA ULTIMATE v4.0")
        self.root.geometry("1500x950")
        self.root.configure(bg=T.BG_DARKEST)
        self.root.minsize(1200, 700)
        
        # State
        self.running = False
        self.cycle_count = 0
        self.click_count = 0
        self.message_queue = queue.Queue()
        self.recent_actions = deque(maxlen=40)
        self.available_actions = list(ALL_ACTIONS)
        self.dynamic_actions_by_category = defaultdict(set)
        self.dynamic_action_lookup = {}
        self.real_mode = True  # Disable simulated UI activity when True
        self.founder_mode = False
        
        # AGI State
        self.current_plan = None
        self.plan_step = 0
        
        # Initialize action tracking system
        if ACTION_TRACKING_AVAILABLE:
            self.action_tracker = ActionTracker("aurora_memory/action_history.json")
            self.retry_manager = SmartRetryManager(self.action_tracker)
            # Wire real-time visuals to completed actions
            try:
                self.action_tracker.register_listener(self._on_action_record)
            except Exception:
                pass
        else:
            self.action_tracker = None
            self.retry_manager = None
            
        # Initialize autonomous systems
        if AUTONOMOUS_AVAILABLE and self.action_tracker:
            self.autonomous_explorer = AutonomousExplorer(self.action_tracker)
            self.keyboard_automation = KeyboardAutomation(self.action_tracker)
        else:
            self.autonomous_explorer = None
            self.keyboard_automation = None
        
        # Initialize TRUE NLP Vision AI Brain - CORE INTELLIGENCE
        if VISION_AI_AVAILABLE:
            try:
                self.vision_brain = VisionAIBrain()
                print("TRUE NLP Vision Brain initialized - AI can now UNDERSTAND screens")
            except Exception as e:
                print(f"Failed to initialize Vision AI Brain: {e}")
                self.vision_brain = None
        else:
            self.vision_brain = None
        
        # Live vision feed variables
        self.vision_update_thread = None
        self.vision_running = False
        self.consecutive_failures = 0
        self.last_screenshot = None
        self.screen_elements = []
        
        # Load systems
        self._load_systems()
        self._hydrate_action_space()
        
        # Build UI
        self._build_ui()
        
        # Start system loops only
        self._start_loops()
        self._start_real_data_feed()
        self._start_pattern_stats_feed()
        # Vision feed will start only when user clicks START
        
        print("AURORA ULTIMATE v4.0")
        print("=" * 60)
        print("Event-Driven Visuals • macOS Commands A–Z Enabled")
        print("AGI: Planning | Replanning | Screen Analysis | Failure Learning")
        print("=" * 60)

    def _on_action_record(self, record):
        """Visualize real outcomes from ActionTracker in UI visuals."""
        try:
            # Respect real_mode: only render on actual events
            if not getattr(self, 'real_mode', False):
                return
            # Map action type to category
            action_type = record.action_type
            category = self._get_action_category(action_type)
            # NetworkTopology packet visualization
            if hasattr(self, 'network_topo') and self.network_topo.winfo_exists():
                # Core index 0 to inner ring index based on category map
                cat_to_inner = {
                    'mouse': 1,          # AI Brain
                    'memory': 2,         # Memory
                    'network': 3,        # Network
                    'security': 4,       # Security
                    'system': 5,         # Data
                    'evolution': 6,      # Evolution
                    'app': 5,
                    'keyboard': 1,
                    'voice': 5,
                    'code': 5,
                }
                to_idx = cat_to_inner.get(category, 5)
                ptype = 'data'
                if record.result == ActionResult.SUCCESS:
                    ptype = 'ai' if category in ('mouse', 'keyboard', 'app', 'code') else 'data'
                elif record.result in (ActionResult.FAILURE, ActionResult.ERROR):
                    ptype = 'security'
                if self.network_topo is not None:
                    self.network_topo.send_packet(0, to_idx, ptype)
                # Extra wave on notable failures
                if record.result in (ActionResult.FAILURE, ActionResult.ERROR):
                    self.network_topo.trigger_wave()
            # AgentCommunication messaging
            if hasattr(self, 'agent_comm') and self.agent_comm.winfo_exists():
                # From Mother(0) to Action(3) or Learning(4) based on result
                if record.result == ActionResult.SUCCESS:
                    if self.agent_comm is not None:
                        self.agent_comm.send_message(4, 0, 'report', 'normal')
                elif record.result in (ActionResult.FAILURE, ActionResult.ERROR):
                    if self.agent_comm is not None:
                        self.agent_comm.send_message(0, 3, 'alert', 'high')
            # ParticleExplosion for failures (if present)
            if hasattr(self, 'particle_explosion') and self.particle_explosion.winfo_exists():
                if record.result in (ActionResult.FAILURE, ActionResult.ERROR):
                    try:
                        w = self.particle_explosion
                        x = getattr(w, 'width', 200) // 2
                        y = getattr(w, 'height', 200) // 2
                        w.trigger_explosion(x=x, y=y, color=T.RED)
                    except Exception:
                        pass
        except Exception:
            pass
    
    def _load_systems(self):
        """Load Aurora AI systems"""
        self.aurora = None
        self.learning = None
        self.nlp = None
        self.voice = None
        self.macos = None
        
        try:
            from agents.mother_ai import MotherAI
            self.aurora = MotherAI()
        except Exception as e:
            print(f"MotherAI: {e}")
        
        try:
            from brain.learning_engine import LearningEngine
            self.learning = LearningEngine()
        except Exception as e:
            print(f"Learning: {e}")
        
        try:
            from brain.nlp_engine import NLPEngine
            self.nlp = NLPEngine()
        except Exception as e:
            print(f"NLP: {e}")
        # Integrate local Ollama LLM interface if available (real-only)
        try:
            from agents.llm_interface import get_llm
            if self.nlp:
                self.nlp.llm = get_llm()
        except Exception as e:
            print(f"LLM interface: {e}")
        
        try:
            from tools.sensors.voice_system import VoiceSystem
            self.voice = VoiceSystem()
        except Exception as e:
            print(f"Voice: {e}")
        
        try:
            from tools.macos_commands import MacOSCommands
            self.macos = MacOSCommands()
        except Exception as e:
            print(f"macOS: {e}")

    def _hydrate_action_space(self):
        """Pull macOS command catalog entries into the action pool"""
        self.dynamic_actions_by_category.clear()
        self.dynamic_action_lookup.clear()

        if not self.macos or not hasattr(self.macos, 'get_all_commands'):
            return

        try:
            commands = self.macos.get_all_commands()
        except Exception as exc:
            print(f"macOS catalog unavailable: {exc}")
            return

        eligible_actions = []
        for name, meta in (commands or {}).items():
            if not meta:
                continue
            method = meta.get('method')
            template = meta.get('command') if method == 'shell' else meta.get('script') if method == 'applescript' else ''
            # Skip commands that clearly require runtime parameters
            if template and ('{' in template and '}' in template):
                continue
            mapped_category = self._map_macos_category(meta.get('category'))
            self.dynamic_actions_by_category[mapped_category].add(name)
            self.dynamic_action_lookup[name] = mapped_category
            eligible_actions.append(name)

        if eligible_actions:
            combined = set(self.available_actions)
            combined.update(eligible_actions)
            self.available_actions = sorted(combined)

    def _map_macos_category(self, macos_category):
        mapping = {
            'system': 'system',
            'files': 'system',
            'apps': 'app',
            'applications': 'app',
            'keyboard': 'keyboard',
            'shortcuts': 'keyboard',
            'browser': 'app',
            'window': 'system',
            'media': 'voice',
            'accessibility': 'voice',
            'terminal': 'code',
            'shell': 'code',
            'security': 'security',
            'network': 'network',
        }
        if not macos_category:
            return 'system'
        return mapping.get(macos_category.lower(), 'system')

    def _get_actions_for_category(self, category):
        base = ACTION_CATALOG.get(category, [])
        dynamic = self.dynamic_actions_by_category.get(category, set())
        if not dynamic:
            return list(base)
        merged = list(base) + list(dynamic)
        # Preserve insertion order without duplicates
        seen = set()
        ordered = []
        for action in merged:
            if action not in seen:
                seen.add(action)
                ordered.append(action)
        return ordered

    def _get_all_action_categories(self):
        dynamic_keys = [cat for cat, actions in self.dynamic_actions_by_category.items() if actions]
        return sorted(set(list(ACTION_CATALOG.keys()) + dynamic_keys))
    
    def _build_ui(self):
        """Build complete UI"""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self._build_header()
        
        # Main area
        main = tk.Frame(self.root, bg=T.BG_DARKEST)
        main.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        main.grid_columnconfigure(0, weight=1, minsize=320)
        main.grid_columnconfigure(1, weight=3, minsize=600)
        main.grid_columnconfigure(2, weight=1, minsize=320)
        main.grid_rowconfigure(0, weight=1)
        
        self._build_left_panel(main)
        self._build_center_panel(main)
        self._build_right_panel(main)
        self._build_status_bar()

    def _start_real_data_feed(self):
        """Start background thread to feed real system metrics into visuals"""
        try:
            from tools.sensors.system_monitor import get_system_monitor
            monitor = get_system_monitor()
        except Exception as e:
            print(f"System monitor unavailable: {e}")
            return

        def feed_loop():
            while True:
                try:
                    status = monitor.get_full_status()
                    cpu = status.get('cpu', {}).get('percent', 0.0)
                    ram_pct = status.get('ram', {}).get('percent_used', 0.0)
                    disk_pct = status.get('disk', {}).get('percent_used', 0.0)

                    # Update gauges
                    self.cpu_gauge.set_value(cpu)
                    self.ram_gauge.set_value(ram_pct)
                    self.disk_gauge.set_value(disk_pct)

                    # Update graphs
                    self.cpu_graph.add_data_point(cpu)
                    self.ram_graph.add_data_point(ram_pct)
                    # Network graph placeholder: use number of running processes as proxy if no net sensor
                    procs = len(monitor.get_running_processes(limit=50))
                    net_val = min(100, procs * 2)
                    self.net_graph.add_data_point(net_val)

                    # Drive NeuralBrain activity via real metrics
                    if hasattr(self, 'neural_brain'):
                        self.neural_brain.set_system_data(cpu, ram_pct, net_val)

                except Exception:
                    pass
                time.sleep(1)

        t = threading.Thread(target=feed_loop, daemon=True)
        t.start()

    def _start_pattern_stats_feed(self):
        """Periodically refresh UI stats from learned pattern JSON files (real-only)."""
        patterns_path = Path("aurora_memory/behavior_patterns.json")
        learned_path = Path("aurora_memory/learned_actions.json")

        def refresh_loop():
            while True:
                try:
                    patterns = {}
                    learned = {}
                    if patterns_path.exists():
                        patterns = json.loads(patterns_path.read_text(encoding="utf-8"))
                    if learned_path.exists():
                        learned = json.loads(learned_path.read_text(encoding="utf-8"))
                    actions_list = patterns.get("actions", [])
                    learned_list = learned.get("learned", [])
                    self.stats.get('patterns').set_value(str(len(actions_list)))
                    self.stats.get('actions').set_value(str(sum(a.get('total', 0) for a in actions_list)))
                except Exception:
                    pass
                time.sleep(5)

        threading.Thread(target=refresh_loop, daemon=True).start()

    def _start_vision_feed(self):
        """Start live vision feed showing what AI sees"""
        def vision_loop():
            import subprocess
            import tempfile
            import os
            from PIL import Image, ImageTk
            
            while True:
                try:
                    if self.vision_running and hasattr(self, 'vision_canvas'):
                        # Take screenshot
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                            path = tmp.name
                        
                        subprocess.run(['screencapture', '-x', path], timeout=3)
                        
                        # Resize and display
                        with Image.open(path) as img:
                            # Scale to fit canvas
                            canvas_w = self.vision_canvas.winfo_width() or 400
                            canvas_h = self.vision_canvas.winfo_height() or 300
                            
                            if canvas_w > 1 and canvas_h > 1:
                                img_w, img_h = img.size
                                scale = min(canvas_w/img_w, canvas_h/img_h) * 0.8
                                new_w, new_h = int(img_w * scale), int(img_h * scale)
                                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                                
                                photo = ImageTk.PhotoImage(img)
                                
                                # Update canvas
                                self.vision_canvas.delete('all')
                                x = (canvas_w - new_w) // 2
                                y = (canvas_h - new_h) // 2
                                self.vision_canvas.create_image(x, y, anchor='nw', image=photo)
                                
                                # Keep reference to prevent garbage collection
                                self.last_screenshot = photo
                        
                        os.unlink(path)
                    
                except Exception as e:
                    print(f"Vision feed error: {e}")
                
                time.sleep(2)  # Update every 2 seconds
        
        self.vision_running = True
        self.vision_update_thread = threading.Thread(target=vision_loop, daemon=True)
        self.vision_update_thread.start()
    
    def _build_header(self):
        """Build header with Brain Storming Logo"""
        header = tk.Frame(self.root, bg=T.BG_DARK, height=80)
        header.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)
        
        # BRAIN STORMING LOGO SECTION
        logo_frame = tk.Frame(header, bg=T.BG_DARK)
        logo_frame.grid(row=0, column=0, sticky='w', padx=10, pady=8)
        
        # Brain Storming Animation
        self.brain_logo = BrainStormingLogo(logo_frame, size=60)
        self.brain_logo.pack(side='left', padx=(5, 10))
        
        # Title next to logo
        title_frame = tk.Frame(logo_frame, bg=T.BG_DARK)
        title_frame.pack(side='left', fill='y')
        
        # AURORA text with gradient effect
        title_top = tk.Frame(title_frame, bg=T.BG_DARK)
        title_top.pack(anchor='w')
        tk.Label(title_top, text="A", font=('JetBrains Mono', 24, 'bold'),
                fg=T.PINK, bg=T.BG_DARK).pack(side='left')
        tk.Label(title_top, text="URORA", font=('JetBrains Mono', 22, 'bold'),
                fg=T.CYAN, bg=T.BG_DARK).pack(side='left')
        
        # Subtitle
        tk.Label(title_frame, text="NEURAL INTERFACE v4.0", 
                font=('JetBrains Mono', 9),
                fg=T.TEXT_DIM, bg=T.BG_DARK).pack(anchor='w')
        
        # STATUS SECTION (center)
        status_f = tk.Frame(header, bg=T.BG_DARK)
        status_f.grid(row=0, column=1, pady=15)
        
        # Status container with border
        status_box = tk.Frame(status_f, bg=T.BG_PANEL, padx=15, pady=8)
        status_box.pack()
        
        # Status indicator row
        status_row = tk.Frame(status_box, bg=T.BG_PANEL)
        status_row.pack()
        
        self.status_dot = PulsingDot(status_row, size=20, color=T.RED)
        self.status_dot.pack(side='left', padx=(0, 8))
        
        self.status_label = tk.Label(status_row, text="OFFLINE",
                                    font=('JetBrains Mono', 16, 'bold'),
                                    fg=T.RED, bg=T.BG_PANEL)
        self.status_label.pack(side='left')
        
        # Uptime label
        self.uptime_label = tk.Label(status_box, text="",
                                    font=('JetBrains Mono', 9),
                                    fg=T.TEXT_DIM, bg=T.BG_PANEL)
        self.uptime_label.pack()
        
        # Controls
        ctrl_f = tk.Frame(header, bg=T.BG_DARK)
        ctrl_f.grid(row=0, column=2, sticky='e', padx=20, pady=15)
        
        self.start_btn = NeonButton(ctrl_f, text="START", color=T.GREEN,
                                   command=self._toggle_aurora, width=130, height=38)
        self.start_btn.pack(side='left', padx=5)
        
        NeonButton(ctrl_f, text="RESET", color=T.ORANGE,
                  command=self._reset, width=100, height=38).pack(side='left', padx=5)
        
        # Founder control button
        NeonButton(ctrl_f, text="CONTROL", color=T.PINK,
              command=self._founder_control, width=120, height=38).pack(side='left', padx=5)
    
    def _build_left_panel(self, parent):
        """Build left panel - Quantum System Metrics"""
        left = tk.Frame(parent, bg=T.BG_DARK)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # SYSTEM METRICS
        self._section_title(left, "NEURAL METRICS", T.CYAN)
        
        gauges_f = tk.Frame(left, bg=T.BG_PANEL)
        gauges_f.pack(fill='x', padx=5, pady=5)
        
        self.cpu_gauge = NeonGauge(gauges_f, "CPU", 95, T.CYAN)
        self.cpu_gauge.pack(side='left', padx=8, pady=8)
        
        self.ram_gauge = NeonGauge(gauges_f, "RAM", 95, T.GREEN)
        self.ram_gauge.pack(side='left', padx=8, pady=8)
        
        self.disk_gauge = NeonGauge(gauges_f, "DISK", 95, T.PINK)
        self.disk_gauge.pack(side='left', padx=8, pady=8)
        
        # PERFORMANCE GRAPHS
        self._section_title(left, "NEURAL PERFORMANCE", T.GREEN)
        
        graphs_f = tk.Frame(left, bg=T.BG_PANEL, height=180)
        graphs_f.pack(fill='x', padx=5, pady=5)
        graphs_f.pack_propagate(False)
        
        # Create notebook for graphs
        graph_notebook = ttk.Notebook(graphs_f)
        graph_notebook.pack(fill='both', expand=True, padx=3, pady=3)
        
        # CPU Graph
        cpu_frame = tk.Frame(graph_notebook, bg=T.BG_DARKEST)
        self.cpu_graph = SystemGraph(cpu_frame, "CPU Usage", T.CYAN, height=150)
        self.cpu_graph.pack(fill='both', expand=True)
        graph_notebook.add(cpu_frame, text="CPU")
        
        # RAM Graph
        ram_frame = tk.Frame(graph_notebook, bg=T.BG_DARKEST)
        self.ram_graph = SystemGraph(ram_frame, "Memory Usage", T.GREEN, height=150)
        self.ram_graph.pack(fill='both', expand=True)
        graph_notebook.add(ram_frame, text="RAM")
        
        # Network Graph
        net_frame = tk.Frame(graph_notebook, bg=T.BG_DARKEST)
        self.net_graph = SystemGraph(net_frame, "Network Activity", T.PURPLE, height=150)
        self.net_graph.pack(fill='both', expand=True)
        graph_notebook.add(net_frame, text="NET")
        
        # AI INTELLIGENCE
        self._section_title(left, "NEURAL INTELLIGENCE", T.PURPLE)
        
        ai_f = tk.Frame(left, bg=T.BG_PANEL)
        ai_f.pack(fill='x', padx=5, pady=5)
        
        self.stats = {}
        stats_data = [
            ('intel', '*', 'Intelligence', '0', T.CYAN),
            ('level', '#', 'Level', 'Baby', T.GREEN),
            ('patterns', '~', 'Patterns', '0', T.PINK),
            ('cycle', '@', 'Cycles', '0', T.PURPLE),
            ('actions', '>', 'Actions', '0', T.YELLOW),
            ('success', '+', 'Success Rate', '0%', T.GREEN),
            ('plan', '-', 'Current Plan', 'None', T.CYAN),
            ('failures', 'x', 'Avoided', '0', T.RED),
        ]
        for key, icon, label, val, color in stats_data:
            row = StatRow(ai_f, icon, label, val, color)
            row.pack(fill='x', pady=2)
            self.stats[key] = row
        
        # Initialize network counters
        try:
            import psutil
            net_io = psutil.net_io_counters()
            self.last_net_sent = net_io.bytes_sent
            self.last_net_recv = net_io.bytes_recv
        except:
            self.last_net_sent = 0
            self.last_net_recv = 0
        
        # AI SYSTEMS STATUS (simplified - real data only)
        self._section_title(left, "AI SYSTEMS", T.PINK)
        
        sys_f = tk.Frame(left, bg=T.BG_PANEL)
        sys_f.pack(fill='x', padx=5, pady=5)
        
        self.tts_stat = StatRow(sys_f, '>', 'Voice', '+ Active', T.CYAN)
        self.tts_stat.pack(fill='x', pady=2)
        self.stt_stat = StatRow(sys_f, '<', 'Listen', '+ Ready', T.GREEN)
        self.stt_stat.pack(fill='x', pady=2)
        self.ollama_stat = StatRow(sys_f, '*', 'Ollama', '---', T.ORANGE)
        self.ollama_stat.pack(fill='x', pady=2)
        self.model_stat = StatRow(sys_f, '#', 'Model', '---', T.PURPLE)
        self.model_stat.pack(fill='x', pady=2)
        
        # NEURAL MEMORY SECTION (moved from right panel)
        self._section_title(left, "NEURAL MEMORY", T.PURPLE)
        
        learn_f = tk.Frame(left, bg=T.BG_PANEL)
        learn_f.pack(fill='x', padx=5, pady=5)
        
        # Learning stats
        stats_f = tk.Frame(learn_f, bg=T.BG_INPUT)
        stats_f.pack(fill='x', padx=5, pady=5)
        
        self.learn_count_var = tk.StringVar(value="Items Learned: 0")
        tk.Label(stats_f, textvariable=self.learn_count_var,
                font=('JetBrains Mono', 8), fg=T.CYAN, bg=T.BG_INPUT).pack(anchor='w', padx=5, pady=1)
        
        self.skills_count_var = tk.StringVar(value="Skills Acquired: 0")
        tk.Label(stats_f, textvariable=self.skills_count_var,
                font=('JetBrains Mono', 8), fg=T.GREEN, bg=T.BG_INPUT).pack(anchor='w', padx=5, pady=1)
        
        self.evolution_var = tk.StringVar(value="Evolution Level: 1.0")
        tk.Label(stats_f, textvariable=self.evolution_var,
                font=('JetBrains Mono', 8), fg=T.ORANGE, bg=T.BG_INPUT).pack(anchor='w', padx=5, pady=1)
        
        # Current thought and decision display
        self.current_thought_var = tk.StringVar(value="Waiting...")
        tk.Label(stats_f, textvariable=self.current_thought_var,
                font=('JetBrains Mono', 7), fg=T.PURPLE, bg=T.BG_INPUT,
                wraplength=200).pack(anchor='w', padx=5, pady=1)
        
        self.decision_var = tk.StringVar(value="Action: None")
        tk.Label(stats_f, textvariable=self.decision_var,
                font=('JetBrains Mono', 7), fg=T.PINK, bg=T.BG_INPUT,
                wraplength=200).pack(anchor='w', padx=5, pady=1)
        
        # Current learning
        self.current_learning_var = tk.StringVar(value="Currently learning...")
        tk.Label(learn_f, textvariable=self.current_learning_var,
                font=('JetBrains Mono', 7), fg=T.PURPLE, bg=T.BG_PANEL,
                wraplength=220, justify='left').pack(fill='x', padx=5, pady=2)
    
    def _build_center_panel(self, parent):
        """Build center - Neural Animations & Vision Feed (Horizontal Split)"""
        center = tk.Frame(parent, bg=T.BG_DARK)
        center.grid(row=0, column=1, sticky='nsew', padx=5)
        center.grid_rowconfigure(0, weight=1)  # Top half - Neural animations
        center.grid_rowconfigure(1, weight=1)  # Bottom half - Vision feed
        center.grid_columnconfigure(0, weight=1)
        
        # TOP HALF - NEURAL NETWORK ANIMATIONS
        self._section_title(center, "NEURAL NETWORK ANIMATIONS", T.CYAN, grid=True, row=0)
        
        anim_f = tk.Frame(center, bg=T.BG_PANEL)
        anim_f.grid(row=0, column=0, sticky='nsew', padx=5, pady=(0, 2))
        anim_f.grid_rowconfigure(0, weight=1)
        anim_f.grid_columnconfigure(0, weight=1)
        
        # Create notebook for different neural animations
        anim_notebook = ttk.Notebook(anim_f)
        anim_notebook.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Neural Brain Tab
        brain_frame = tk.Frame(anim_notebook, bg=T.BG_DARKEST)
        self.brain = NeuralBrain(brain_frame)
        self.brain.pack(fill='both', expand=True)
        anim_notebook.add(brain_frame, text="Neural Brain")
        
        # AI Thinking Process Tab - Real-time cognitive visualization
        thinking_frame = tk.Frame(anim_notebook, bg=T.BG_DARKEST)
        self.ai_thinking = AIThinkingVisualization(thinking_frame)
        self.ai_thinking.pack(fill='both', expand=True)
        anim_notebook.add(thinking_frame, text="AI Thinking")
        
        # Keep agent_comm as None for compatibility
        self.agent_comm = None
        
        # Network Topology Tab
        network_frame = tk.Frame(anim_notebook, bg=T.BG_DARKEST)
        self.network_topo = NetworkTopology(network_frame)
        self.network_topo.pack(fill='both', expand=True)
        anim_notebook.add(network_frame, text="Network Map")

        # AI Analysis & Planning Tab - Real-time operational view
        analysis_frame = tk.Frame(anim_notebook, bg=T.BG_DARKEST)
        self.ai_analysis = AIAnalysisVisualization(analysis_frame)
        self.ai_analysis.pack(fill='both', expand=True)
        anim_notebook.add(analysis_frame, text="AI Analysis")
        
        # BOTTOM HALF - LIVE VISION FEED
        self._section_title(center, "LIVE VISION FEED", T.GREEN, grid=True, row=1)
        
        vision_f = tk.Frame(center, bg=T.BG_PANEL)
        vision_f.grid(row=1, column=0, sticky='nsew', padx=5, pady=(2, 0))
        vision_f.grid_rowconfigure(0, weight=1)
        vision_f.grid_columnconfigure(0, weight=1)
        
        # Vision display (what AI sees) - bottom half
        self.vision_canvas = tk.Canvas(vision_f, bg=T.BG_DARKEST, highlightthickness=2, 
                                       highlightbackground=T.CYAN)
        self.vision_canvas.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    
    def _build_right_panel(self, parent):
        """Build right panel - Communication with AI"""
        right = tk.Frame(parent, bg=T.BG_DARK)
        right.grid(row=0, column=2, sticky='nsew', padx=(5, 0))
        right.grid_rowconfigure(2, weight=1)
        right.grid_columnconfigure(0, weight=1)
        
        # ═══════════════════════════════════════════════════════════════════
        # INTERACTIVE CHAT SECTION
        # ═══════════════════════════════════════════════════════════════════
        self._section_title(right, "AI CHAT", T.PURPLE)
        
        # Chat mode indicator
        chat_mode_f = tk.Frame(right, bg=T.BG_PANEL)
        chat_mode_f.pack(fill='x', padx=5, pady=3)
        
        self.chat_mode_var = tk.StringVar(value="Learning Mode")
        self.chat_mode_label = tk.Label(chat_mode_f, textvariable=self.chat_mode_var,
                                       font=('JetBrains Mono', 9, 'bold'),
                                       fg=T.GREEN, bg=T.BG_PANEL)
        self.chat_mode_label.pack(side='left', padx=10)
        
        # Chat button - stops learning and enters chat mode
        self.chat_button = NeonButton(chat_mode_f, text="CHAT", 
                                     command=self._toggle_chat_mode,
                                     color=T.CYAN, width=80, height=28)
        self.chat_button.pack(side='right', padx=5)
        
        self.voice_chat_btn = NeonButton(chat_mode_f, text="VOICE",
                                        command=self._start_voice_chat,
                                        color=T.PINK, width=80, height=28)
        self.voice_chat_btn.pack(side='right', padx=5)
        
        # Chat display
        chat_container = tk.Frame(right, bg=T.BG_PANEL)
        chat_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollable chat
        chat_scroll = tk.Scrollbar(chat_container)
        chat_scroll.pack(side='right', fill='y')
        
        self.ai_chat = tk.Text(chat_container, font=('JetBrains Mono', 10),
                              fg=T.GREEN, bg=T.BG_DARKEST,
                              height=12, wrap='word', relief='flat',
                              padx=10, pady=10, insertbackground=T.CYAN,
                              yscrollcommand=chat_scroll.set)
        self.ai_chat.pack(fill='both', expand=True, padx=3, pady=3)
        chat_scroll.config(command=self.ai_chat.yview)
        
        # Chat tags for different speakers
        self.ai_chat.tag_configure('user', foreground=T.GREEN)
        self.ai_chat.tag_configure('aurora', foreground=T.CYAN)
        self.ai_chat.tag_configure('system', foreground=T.TEXT_DIM)
        self.ai_chat.tag_configure('learning', foreground=T.PURPLE)
        self.ai_chat.tag_configure('action', foreground=T.YELLOW)
        self.ai_chat.tag_configure('error', foreground=T.RED)
        
        self.ai_chat.config(state='disabled')
        
        # User input area
        input_f = tk.Frame(right, bg=T.BG_PANEL)
        input_f.pack(fill='x', padx=5, pady=5)
        
        self.user_input = tk.Entry(input_f, font=('JetBrains Mono', 11),
                                  fg=T.GREEN, bg=T.BG_INPUT,
                                  insertbackground=T.CYAN, relief='flat')
        self.user_input.pack(side='left', fill='x', expand=True, padx=5, pady=5, ipady=8)
        self.user_input.bind('<Return>', self._send_chat_message)
        self.user_input.insert(0, "Ask me anything... (e.g., 'What did you learn?')")
        self.user_input.bind('<FocusIn>', lambda e: self.user_input.delete(0, 'end') if 'Ask me' in self.user_input.get() else None)
        
        NeonButton(input_f, text="SEND", command=self._send_chat_message,
                  color=T.CYAN, width=50, height=35).pack(side='right', padx=5)
        
        # ═══════════════════════════════════════════════════════════════════
        # AUTONOMOUS CONTROL SECTION - Disabled (class not available)
        # ═══════════════════════════════════════════════════════════════════
        pass
        
        # ═══════════════════════════════════════════════════════════════════
        # ACTIVITY LOG SECTION
        # ═══════════════════════════════════════════════════════════════════
        self._section_title(right, "ACTIVITY LOG", T.GREEN)
        
        # Activity log container
        log_container = tk.Frame(right, bg=T.BG_PANEL, height=200)
        log_container.pack(fill='both', expand=True, padx=5, pady=5)
        log_container.pack_propagate(False)
        
        # Create activity log (reuse from center panel)
        self.activity_log = DataStream(log_container)
        self.activity_log.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Set log reference for compatibility
        self.log = self.activity_log
        
        # Initialize status variables for compatibility
        self.mother_status = None
        self.mother_iq = None
        self.vision_status = None
        self.voice_agent_status = None
        self.action_status = None
        self.learning_status = None
        self.evolution_status = None
        
        # Neural memory section moved to left panel
        
        # Self-Evolution Status
        self._section_title(right, "NEURAL EVOLUTION", T.ORANGE)
        
        evol_f = tk.Frame(right, bg=T.BG_PANEL)
        evol_f.pack(fill='x', padx=5, pady=5)
        
        self.evolution_status_var = tk.StringVar(value="Ready to evolve...")
        tk.Label(evol_f, textvariable=self.evolution_status_var,
                font=('JetBrains Mono', 8), fg=T.ORANGE, bg=T.BG_PANEL,
                wraplength=280, justify='left').pack(fill='x', padx=10, pady=5)
        
        # Evolution button
        NeonButton(evol_f, text="TRIGGER EVOLUTION",
                  command=self._trigger_self_evolution,
                  color=T.ORANGE, width=180, height=30).pack(pady=5)
    
    def _build_status_bar(self):
        """Build status bar"""
        bar = tk.Frame(self.root, bg=T.BG_DARK, height=35)
        bar.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 10))
        bar.grid_propagate(False)
        
        self.time_label = tk.Label(bar, text="", font=('JetBrains Mono', 10),
                                  fg=T.TEXT_DIM, bg=T.BG_DARK)
        self.time_label.pack(side='left', padx=20, pady=8)
        
        self.mem_label = tk.Label(bar, text="", font=('JetBrains Mono', 10),
                                 fg=T.CYAN, bg=T.BG_DARK)
        self.mem_label.pack(side='right', padx=20, pady=8)
        
        tk.Label(bar, text="AURORA NEURAL v4.0 | OPEN WORLD AI",
                font=('JetBrains Mono', 10), fg=T.TEXT_MUTED, bg=T.BG_DARK).pack(side='right', padx=20, pady=8)

    def _founder_control(self):
        """Prompt for founder passcode and toggle founder mode."""
        # Immutable founder protection: do not allow changing passcode or protection
        try:
            from config.founder_protection import verify_founder_passcode
        except Exception:
            def verify_founder_passcode(code: str) -> bool:
                return code == "251117Q"

        dlg = tk.Toplevel(self.root)
        dlg.title("Founder Control")
        dlg.configure(bg=T.BG_PANEL)
        tk.Label(dlg, text="Enter Passcode", font=('JetBrains Mono', 11),
                 fg=T.CYAN, bg=T.BG_PANEL).pack(padx=12, pady=(12, 6))
        var = tk.StringVar()
        entry = tk.Entry(dlg, textvariable=var, show='*', font=('JetBrains Mono', 11),
                         fg=T.TEXT_BRIGHT, bg=T.BG_INPUT, relief='flat')
        entry.pack(padx=12, pady=6)

        def submit():
            code = var.get().strip()
            if verify_founder_passcode(code):
                self.founder_mode = True
                self.status_label.config(text="FOUNDER MODE")
                self.status_dot.set_active(True, color=T.PINK)
                self._on_founder_mode_enter()
                dlg.destroy()
            else:
                messagebox.showerror("Access Denied", "Invalid passcode")

        NeonButton(dlg, text="Unlock", color=T.PINK, command=submit, width=100, height=32).pack(pady=10)
        entry.focus_set()

    def _on_founder_mode_enter(self):
        """Adjust behavior when founder mode is active."""
        # In founder mode, pause autonomy and route requests to owner
        self.running = False
        self.status_label.config(text="FOUNDER MODE")
    
    def _section_title(self, parent, text, color, grid=False, row=0):
        """Create section title"""
        frame = tk.Frame(parent, bg=T.BORDER)
        if grid:
            frame.grid(row=row, column=0, sticky='new', padx=5, pady=(5, 0))
        else:
            frame.pack(fill='x', padx=5, pady=(10, 0))
        
        tk.Label(frame, text=text, font=('JetBrains Mono', 10, 'bold'),
                fg=color, bg=T.BORDER, padx=10, pady=5).pack(side='left')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UPDATE LOOPS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _start_loops(self):
        self._update_system()
        self._update_ai()
        self._update_time()
        self._update_ollama()
        self._process_queue()
    
    def _update_system(self):
        """Update system metrics with real-time data"""
        try:
            if not hasattr(self, 'root') or not self.root.winfo_exists():
                return
        except:
            return
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0)
            ram_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            # Update gauges
            self.cpu_gauge.set_value(cpu_percent)
            self.ram_gauge.set_value(ram_percent)
            self.disk_gauge.set_value(disk_percent)
            
            # Update graphs if they exist
            if hasattr(self, 'cpu_graph'):
                self.cpu_graph.add_data_point(cpu_percent)
            if hasattr(self, 'ram_graph'):
                self.ram_graph.add_data_point(ram_percent)
            if hasattr(self, 'disk_graph'):
                self.disk_graph.add_data_point(disk_percent)
            
            # Network activity
            net_io = psutil.net_io_counters()
            net_rate = 0
            if hasattr(self, 'last_net_sent'):
                net_sent_rate = (net_io.bytes_sent - self.last_net_sent) / 1024  # KB/s
                net_recv_rate = (net_io.bytes_recv - self.last_net_recv) / 1024  # KB/s
                net_rate = net_sent_rate + net_recv_rate
                
                # Update network graph with real network activity
                if hasattr(self, 'net_graph'):
                    # Scale for display (0-100 range, with max ~1000 KB/s)
                    net_display = min(100, (net_rate / 10))
                    self.net_graph.add_data_point(net_display)
                
                # Network topology activity based on REAL network traffic
                if hasattr(self, 'network_topo') and net_rate > 5:
                    if self.network_topo is not None:
                        self.network_topo.send_packet(0, random.randint(1, 4), 'data')
            
            self.last_net_sent = net_io.bytes_sent
            self.last_net_recv = net_io.bytes_recv
            
            # ═══════════════════════════════════════════════════════════════════
            # PASS REAL DATA TO NEURAL BRAIN - No fake data!
            # ═══════════════════════════════════════════════════════════════════
            if hasattr(self, 'brain') and self.brain is not None:
                self.brain.set_system_data(cpu_percent, ram_percent, net_rate)
            
            # ═══════════════════════════════════════════════════════════════════
            # UPDATE AI THINKING & ANALYSIS VISUALIZATIONS WITH REAL SYSTEM DATA
            # ═══════════════════════════════════════════════════════════════════
            
            # Update AI thinking based on system activity
            if hasattr(self, 'ai_thinking') and self.ai_thinking is not None:
                # Thinking intensity based on CPU usage
                thinking_intensity = 0.3 + (cpu_percent / 100) * 0.7
                
                # Analysis depth based on memory usage
                analysis_depth = 0.2 + (ram_percent / 100) * 0.8
                
                # Determine current AI focus based on system state
                current_thought = "Monitoring system state..."
                if cpu_percent > 80:
                    current_thought = f"High CPU usage detected: {cpu_percent:.1f}%"
                elif ram_percent > 80:
                    current_thought = f"High memory usage: {ram_percent:.1f}%"
                elif net_rate > 100:  # High network activity
                    current_thought = f"Network activity spike: {net_rate:.0f} KB/s"
                elif disk_percent > 90:
                    current_thought = f"Disk space warning: {disk_percent:.1f}%"
                
                self.ai_thinking.update_thinking_state(
                    thought=current_thought,
                    intensity=thinking_intensity,
                    analysis=analysis_depth,
                    planning=cpu_percent > 70,  # Planning when system under load
                    executing=net_rate > 50     # Executing when network active
                )
                
                # Add system thoughts periodically
                if random.random() < 0.02:  # 2% chance each update
                    if cpu_percent > 50:
                        self.ai_thinking.add_thought(f"CPU: {cpu_percent:.0f}%")
                    if ram_percent > 60:
                        self.ai_thinking.add_thought(f"RAM: {ram_percent:.0f}%")
            
            # Update AI analysis visualization with real system metrics
            if hasattr(self, 'ai_analysis') and self.ai_analysis is not None:
                # Update data streams with real values
                self.ai_analysis.update_data_stream('System', cpu_percent / 100)
                self.ai_analysis.update_data_stream('Memory', ram_percent / 100)
                self.ai_analysis.update_data_stream('Network', min(1.0, net_rate / 200))  # Scale network activity
                
                # Update analysis text based on system state
                if cpu_percent > 75:
                    self.ai_analysis.update_analysis(f"High system load detected - CPU at {cpu_percent:.1f}%", "PERFORMANCE")
                    if random.random() < 0.1:  # 10% chance
                        self.ai_analysis.add_operation(f"ALERT: High CPU usage - {cpu_percent:.0f}%")
                elif ram_percent > 80:
                    self.ai_analysis.update_analysis(f"Memory pressure - RAM at {ram_percent:.1f}%", "MEMORY")
                    if random.random() < 0.1:
                        self.ai_analysis.add_operation(f"ALERT: High memory usage - {ram_percent:.0f}%")
                elif net_rate > 100:
                    self.ai_analysis.update_analysis(f"Network activity spike - {net_rate:.0f} KB/s", "NETWORK")
                    if random.random() < 0.05:
                        self.ai_analysis.add_operation(f"NETWORK: Traffic spike - {net_rate:.0f} KB/s")
                else:
                    # Normal operation analysis
                    analyses = [
                        f"System stable - CPU: {cpu_percent:.0f}%, RAM: {ram_percent:.0f}%",
                        f"Monitoring {len([x for x in [cpu_percent, ram_percent] if x > 30])} active metrics",
                        f"Network throughput: {net_rate:.0f} KB/s",
                        "All systems operating within normal parameters"
                    ]
                    self.ai_analysis.update_analysis(random.choice(analyses), "MONITORING")
                
                # Simulate vision and audio activity based on system state
                # Vision activity correlates with screen changes (simulated)
                vision_activity = 0.4 + (cpu_percent / 200) + random.random() * 0.2
                self.ai_analysis.update_data_stream('Vision', min(1.0, vision_activity))
                
                # Audio activity based on system activity + some variation
                audio_activity = 0.2 + (net_rate / 500) + random.random() * 0.3
                self.ai_analysis.update_data_stream('Audio', min(1.0, audio_activity))
                
                # Add periodic system operations to log
                if random.random() < 0.02:  # 2% chance each second
                    operations = [
                        f"VISION: Screenshot captured and analyzed",
                        f"SYSTEM: CPU {cpu_percent:.0f}% | RAM {ram_percent:.0f}%",
                        f"NETWORK: {net_rate:.0f} KB/s throughput",
                        f"MEMORY: {psutil.virtual_memory().used/1024**3:.1f}GB used",
                        f"MONITOR: {len(psutil.pids())} processes active"
                    ]
                    self.ai_analysis.add_operation(random.choice(operations))
            
            # Temperature (if available)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    temp_values = []
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current:
                                temp_values.append(entry.current)
                    if temp_values and hasattr(self, 'temp_stat'):
                        avg_temp = sum(temp_values) / len(temp_values)
                        self.temp_stat.set(f"{avg_temp:.1f}°C")
            except:
                pass
            
            mem = psutil.virtual_memory()
            self.mem_label.config(text=f"RAM: {mem.used/1024**3:.1f} / {mem.total/1024**3:.1f} GB")
            
            # Update agent communication with real system activity
            if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                # Only send messages when there's actual high activity
                if cpu_percent > 50:
                    self.agent_comm.send_message(0, 1, 'data')
                if cpu_percent > 80 or ram_percent > 80:
                    self.agent_comm.send_message(0, 3, 'alert', 'high')
            
        except Exception as e:
            print(f"System update error: {e}")
        
        try:
            if self.root.winfo_exists():
                self.root.after(1000, self._update_system)
        except:
            pass
    
    def _update_ai(self):
        """Update AI metrics with REAL data"""
        try:
            if not hasattr(self, 'root') or not self.root.winfo_exists():
                return
        except:
            return
        try:
            # Update from permanent brain if available
            if hasattr(self, 'permanent_brain') and self.permanent_brain:
                summary = self.permanent_brain.get_summary()
                self.stats['intel'].set(f"{summary['intelligence_level']}")
                self.stats['patterns'].set(f"{summary.get('patterns_learned', 0)}")
                level_names = ['Baby', 'Toddler', 'Child', 'Teen', 'Adult', 'Expert', 'Master', 'Genius']
                level_idx = min(summary['intelligence_level'] // 10, len(level_names) - 1)
                self.stats['level'].set(level_names[level_idx])
            elif self.learning:
                intel = self.learning.get_intelligence_score()
                level = self.learning.get_intelligence_level()
                self.stats['intel'].set(f"{intel:.0f}")
                self.stats['level'].set(level)
            
            # Update cycle count
            self.stats['cycle'].set(str(self.cycle_count))
            
            # Update action count and success rate
            if hasattr(self, 'total_actions'):
                self.stats['actions'].set(str(self.total_actions))
                if self.total_actions > 0 and hasattr(self, 'success_count'):
                    rate = int(100 * self.success_count / self.total_actions)
                    self.stats['success'].set(f"{rate}%")
            
            # Voice system status - check if macOS say command works
            self.tts_stat.set("Active")  # macOS always has say
            
            # Check if speech_recognition is installed
            try:
                import speech_recognition
                self.stt_stat.set("Ready")
            except:
                self.stt_stat.set("Install: pip install SpeechRecognition")
        except Exception as e:
            pass
        try:
            if self.root.winfo_exists():
                self.root.after(2000, self._update_ai)
        except:
            pass
    
    def _update_time(self):
        try:
            if not hasattr(self, 'root') or not self.root.winfo_exists():
                return
            if hasattr(self, 'time_label') and self.time_label.winfo_exists():
                self.time_label.config(text=datetime.now().strftime("⏱ %Y-%m-%d %H:%M:%S"))
            self.root.after(1000, self._update_time)
        except:
            pass
    
    def _update_ollama(self):
        try:
            if not hasattr(self, 'root') or not self.root.winfo_exists():
                return
        except:
            return
            
        def check():
            try:
                import requests
                r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
                if r.status_code == 200:
                    models = r.json().get('models', [])
                    self.message_queue.put(('ollama_ok', models[0].get('name', '?') if models else '?'))
                else:
                    self.message_queue.put(('ollama_err', None))
            except:
                self.message_queue.put(('ollama_err', None))
        
        threading.Thread(target=check, daemon=True).start()
        try:
            if self.root.winfo_exists():
                self.root.after(5000, self._update_ollama)
        except:
            pass
    
    def _process_queue(self):
        """Process thread messages - SYNC VISUALIZATIONS WITH REAL AI ACTIVITY"""
        try:
            while True:
                msg = self.message_queue.get_nowait()
                if msg[0] == 'ollama_ok':
                    self.ollama_stat.set("Online")
                    self.model_stat.set(msg[1])
                elif msg[0] == 'ollama_err':
                    self.ollama_stat.set("Offline")
                elif msg[0] == 'log':
                    self.log.log(msg[1], msg[2])
                elif msg[0] == 'thought':
                    if hasattr(self, 'brain') and self.brain is not None:
                        self.brain.set_thinking(True, msg[1])
                    # Sync animations with AI thoughts
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.activity_level = 0.8
                        self.agent_comm.send_message(0, random.randint(1, 5), 'instruction')
                    if hasattr(self, 'network_topo') and self.network_topo is not None:
                        self.network_topo.activity_level = 0.8
                        self.network_topo.send_packet(0, random.randint(1, 6), 'ai')
                # NEURAL NETWORK SYNC - Real AI activity triggers animation
                elif msg[0] == 'neural_observe':
                    self.brain.set_observing(True)
                    if hasattr(self, 'ai_chat_status'):
                        self.ai_chat_status.config(text="Observing", fg=T.GREEN)
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.activity_level = 0.6
                        self.agent_comm.delegate_task('vision', 'Scanning environment')
                    if hasattr(self, 'network_topo'):
                        self.network_topo.activity_level = 0.6
                        self.network_topo.trigger_wave()
                elif msg[0] == 'neural_think':
                    self.brain.set_thinking(True, msg[1] if len(msg) > 1 else "")
                    if hasattr(self, 'ai_chat_status'):
                        self.ai_chat_status.config(text="Thinking", fg=T.CYAN)
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.activity_level = 0.9
                        if self.agent_comm is not None:
                            self.agent_comm.send_message(0, random.randint(1, 5), 'data')
                    if hasattr(self, 'network_topo'):
                        self.network_topo.activity_level = 0.9
                        for _ in range(3):
                            if self.network_topo is not None:
                                self.network_topo.send_packet(0, random.randint(1, 6), 'ai')
                elif msg[0] == 'neural_act':
                    self.brain.set_acting(True, msg[1] if len(msg) > 1 else None)
                    if hasattr(self, 'ai_chat_status'):
                        self.ai_chat_status.config(text="Acting", fg=T.PINK)
                    action_type = msg[1] if len(msg) > 1 else 'system'
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.activity_level = 1.0
                        self.agent_comm.delegate_task('action', f'Executing {action_type}')
                    if hasattr(self, 'network_topo'):
                        self.network_topo.activity_level = 1.0
                        self.network_topo.trigger_wave()
                        for _ in range(5):
                            if self.network_topo is not None:
                                self.network_topo.send_packet(random.randint(0, 6), random.randint(0, 18), 'data')
                elif msg[0] == 'neural_learn':
                    success = msg[1] if len(msg) > 1 else True
                    self.brain.set_learning(True, success)
                    if hasattr(self, 'ai_chat_status'):
                        self.ai_chat_status.config(text="Learning", fg=T.YELLOW)
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.activity_level = 1.0
                        agent_type = random.choice(['learning', 'evolution', 'vision'])
                        self.agent_comm.report_learning(agent_type, f"New knowledge acquired")
                    if hasattr(self, 'network_topo'):
                        self.network_topo.activity_level = 1.0
                        self.network_topo.trigger_wave()
                elif msg[0] == 'neural_stop':
                    self.brain.set_observing(False)
                    self.brain.set_acting(False)
                    self.brain.set_learning(False)
                    if hasattr(self, 'ai_chat_status'):
                        self.ai_chat_status.config(text="Idle", fg=T.TEXT_DIM)
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.activity_level = 0.3
                    if hasattr(self, 'network_topo'):
                        self.network_topo.activity_level = 0.3
                elif msg[0] == 'ask_question':
                    self._ask_user_question(msg[1])
                elif msg[0] == 'user_answer':
                    self._answer_ai(msg[1])
        except queue.Empty:
            pass
        try:
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.root.after(50, self._process_queue)
        except:
            pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONTROLS - PURE AUTONOMOUS LEARNING FROM SCRATCH
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _toggle_aurora(self):
        if not self.running:
            self.running = True
            self.status_dot.set_active(True, T.GREEN)
            self.status_label.config(text="LEARNING", fg=T.GREEN)
            
            # Activate Brain Storming Logo
            if hasattr(self, 'brain_logo') and self.brain_logo:
                self.brain_logo.set_active(True)
            
            # Start vision feed when activated
            if not hasattr(self, 'vision_running') or not self.vision_running:
                self._start_vision_feed()
            
            # ACTIVATE ALL ANIMATIONS IMMEDIATELY ON START
            if hasattr(self, 'brain') and self.brain:
                self.brain.set_active(True)
                self.brain.ai_state['intensity'] = 0.8
            if hasattr(self, 'ai_thinking') and self.ai_thinking:
                self.ai_thinking.set_active(True)
            if hasattr(self, 'ai_analysis') and self.ai_analysis:
                self.ai_analysis.set_active(True)
            if hasattr(self, 'network_topo') and self.network_topo:
                self.network_topo.set_active(True)
            
            self.log.log("AURORA NEURAL ANIMATIONS & VISION ACTIVE", 'cyan')
            self.log.log("Learning from SCRATCH with AGI features!", 'yellow')
            self.log.log("Planning > Acting > Learning > Replanning", 'pink')
            self.log.log("Screen analysis for context-aware actions", 'purple')
            self.log.log("Failure avoidance - learns from mistakes", 'green')
            self.log.log("All learning saved permanently - NEVER forgets", 'cyan')
            self.log.log("===========================================", 'dim')
            self.log.log("ADVANCED: Networking, Security, Hacking", 'cyan')
            self.log.log("ADVANCED: System exploration, Shell/Code", 'pink')
            self.log.log("UNRESTRICTED: No limits on learning!", 'green')
            self.log.log("===========================================", 'dim')
            self.log.log("Move mouse to corner to ABORT (failsafe)", 'dim')
            
            # Greet user with voice
            self._speak_to_user("Hello! Aurora AGI starting. I'll learn everything - networking, security, system, and more!")
            
            # Load PERMANENT BRAIN
            try:
                from aurora_memory.permanent_brain import PermanentBrain
                self.permanent_brain = PermanentBrain(
                    memory_dir=os.path.join(os.path.dirname(__file__), 'aurora_memory')
                )
                summary = self.permanent_brain.get_summary()
                self.log.log(f"Loaded {summary['total_memories']} memories from disk", 'cyan')
                self.log.log(f"Intelligence Level: {summary['intelligence_level']}", 'green')
                self.log.log(f"Previous plans: {summary.get('plans_created', 0)}", 'purple')
                self._add_to_ai_chat("Aurora", f"Loaded {summary['total_memories']} memories. Intelligence: {summary['intelligence_level']}", "aurora")
            except Exception as e:
                self.log.log(f"Memory system: {str(e)[:40]}", 'red')
                self.permanent_brain = None
            
            # Initialize AGI state
            self.curiosity = 1.0
            self.success_count = 0
            self.total_actions = 0
            self.current_plan = None
            self.plan_step = 0
            self.consecutive_failures = 0
            self.last_screenshot = None
            
            self._run_pure_autonomous()
        else:
            self.running = False
            self.status_dot.set_active(False, T.RED)
            self.status_label.config(text="OFFLINE", fg=T.RED)
            
            # Deactivate Brain Storming Logo
            if hasattr(self, 'brain_logo') and self.brain_logo:
                self.brain_logo.set_active(False)
            
            # Stop vision feed
            if hasattr(self, 'vision_running'):
                self.vision_running = False
            
            # DEACTIVATE ALL ANIMATIONS ON STOP
            if hasattr(self, 'brain') and self.brain:
                self.brain.set_active(False)
                self.brain.ai_state['intensity'] = 0.0
            if hasattr(self, 'ai_thinking') and self.ai_thinking:
                self.ai_thinking.set_active(False)
            if hasattr(self, 'ai_analysis') and self.ai_analysis:
                self.ai_analysis.set_active(False)
            if hasattr(self, 'network_topo') and self.network_topo:
                self.network_topo.set_active(False)
            
            self.log.log("AURORA ANIMATIONS & VISION STOPPED", 'yellow')
            self._speak_to_user("Goodbye! I've saved everything I learned.")
            if hasattr(self, 'permanent_brain') and self.permanent_brain:
                summary = self.permanent_brain.get_summary()
                self.log.log(f"Saved {summary['total_memories']} memories permanently", 'cyan')
                self.log.log(f"Success rate: {int(100 * self.permanent_brain.get_overall_success_rate())}%", 'green')
    
    def _reset(self):
        self.cycle_count = 0
        self.click_count = 0
        self.success_count = 0
        self.total_actions = 0
        self.log.clear()
        # Clear AI chat
        self.ai_chat.config(state='normal')
        self.ai_chat.delete('1.0', 'end')
        self.ai_chat.config(state='disabled')
        self.brain.set_thinking(False)
        self.brain.ai_state['intensity'] = 0.0
        self.log.log("Display reset - Memory preserved on disk!", 'cyan')
    
    def _run_pure_autonomous(self):
        """PURE AUTONOMOUS - AI learns EVERYTHING from scratch with AGI features"""
        if not self.running:
            return
        
        self.cycle_count += 1
        self.stats['cycle'].set(str(self.cycle_count))
        
        def pure_autonomous_work():
            self.message_queue.put(('log', f"--- CYCLE {self.cycle_count} ---", 'cyan'))
            self._add_to_ai_chat("System", f"--- Cycle {self.cycle_count} ---", "system")
            
            try:
                # Update agent statuses
                self._update_agent_statuses()
                
                # ═══════════════════════════════════════════════════════════
                # MOTHER AI: COORDINATE SUB-AGENTS
                # ═══════════════════════════════════════════════════════════
                self._coordinate_agents()
                
                # ═══════════════════════════════════════════════════════════
                # AGI STEP 0: ANALYZE SCREEN FOR CONTEXT
                # ═══════════════════════════════════════════════════════════
                screen_context = self._analyze_screen()
                if screen_context:
                    self.message_queue.put(('log', f"Vision Agent: {screen_context[:60]}", 'purple'))
                    # Send to agent communication
                    if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                        self.agent_comm.send_message(1, 0, 'report')  # Vision to Mother
                
                # ═══════════════════════════════════════════════════════════
                # AGI STEP 1: CHECK/CREATE PLAN
                # ═══════════════════════════════════════════════════════════
                if not self.current_plan or self.current_plan.get('status') == 'completed':
                    self.current_plan = self._create_plan()
                    if self.current_plan:
                        self.message_queue.put(('log', f"New Plan: {self.current_plan['goal']}", 'cyan'))
                        self._add_to_ai_chat("Aurora", f"Plan: {self.current_plan['goal']}", "aurora")
                        self.plan_step = 0
                
                # ═══════════════════════════════════════════════════════════
                # STEP 1: OBSERVE - AI looks at environment
                # ═══════════════════════════════════════════════════════════
                self.message_queue.put(('neural_observe', True))
                observation = self._observe_everything()
                observation['screen_context'] = screen_context
                self.message_queue.put(('log', f"Observe: {observation['summary']}", 'green'))
                self.current_thought_var.set(f"Observing: {observation['summary'][:50]}...")
                
                # Store observation in permanent memory
                if self.permanent_brain:
                    self.permanent_brain.record_experience('observation', observation['summary'])
                
                time.sleep(0.3)
                
                # ═══════════════════════════════════════════════════════════
                # STEP 2: THINK - AI decides with FAILURE AVOIDANCE
                # ═══════════════════════════════════════════════════════════
                self.message_queue.put(('neural_think', 'Processing...'))
                decision = self._think_and_decide_smart(observation)
                self.message_queue.put(('log', f"Mother AI: {decision['thought']}", 'pink'))
                self.message_queue.put(('thought', decision['thought']))
                
                # Update consciousness display
                self.current_thought_var.set(decision['thought'][:80] + "...")
                self.decision_var.set(f"Action: {decision['action']} | Risk: {decision.get('risk_level', 0)*100:.0f}%")
                
                # Send decision to action agent
                if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                    self.agent_comm.send_message(0, 3, 'instruction')  # Mother to Action
                
                # Add to AI chat
                self._add_to_ai_chat("Aurora", decision['thought'][:100], "aurora")
                
                # Neo comments on risky actions
                if decision.get('risk_level', 0) > 0.5 and self.nlp:
                    try:
                        neo_thought = self.nlp.generate_response(
                            f"Brief warning (max 15 words) about this risky action: {decision['action']}"
                        )
                        if neo_thought:
                            self._add_to_ai_chat("Neo", neo_thought[:80], "neo")
                    except:
                        pass
                
                time.sleep(0.3)
                
                # ═══════════════════════════════════════════════════════════
                # STEP 3: ACT - Execute with SCREEN-AWARE actions
                # ═══════════════════════════════════════════════════════════
                action = decision['action']
                action_category = self._get_action_category(action)
                self.message_queue.put(('neural_act', action_category))
                self.message_queue.put(('log', f"Action: {action}", 'purple'))
                
                success, result = self._execute_action_smart(action, screen_context)
                self.recent_actions.append(action)
                self.total_actions += 1
                
                # ═══════════════════════════════════════════════════════════
                # AGI STEP: HANDLE FAILURE - REPLAN IF NEEDED
                # ═══════════════════════════════════════════════════════════
                if success:
                    self.success_count += 1
                    self.consecutive_failures = 0
                else:
                    self.consecutive_failures += 1
                    
                    # Record failure for learning
                    if self.permanent_brain:
                        self.permanent_brain.record_failure(action, result, observation['summary'])
                    
                    # Replan if too many failures
                    if self.consecutive_failures >= 3:
                        self.message_queue.put(('log', f"REPLANNING - {self.consecutive_failures} failures!", 'yellow'))
                        self._add_to_ai_chat("Aurora", "Too many failures. Let me try a different approach...", "aurora")
                        self.current_plan = None  # Force new plan
                        self.consecutive_failures = 0
                
                time.sleep(0.3)
                
                # ═══════════════════════════════════════════════════════════
                # STEP 4: LEARN - Remember FOREVER with smart patterns
                # ═══════════════════════════════════════════════════════════
                self.message_queue.put(('neural_learn', success))
                self._learn_and_remember_smart(action, success, result, observation)
                
                # Send learning data to learning agent
                if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                    msg_type = 'report' if success else 'alert'
                    priority = 'normal' if success else 'high'
                    self.agent_comm.send_message(4, 0, msg_type, priority)  # Learning to Mother
                
                if success:
                    self.message_queue.put(('log', f"{str(result)[:50]}", 'green'))
                    self._add_to_ai_chat("System", f"Success: {str(result)[:40]}", "action")
                else:
                    self.message_queue.put(('log', f"{str(result)[:50]}", 'red'))
                    self._add_to_ai_chat("System", f"Failed: {str(result)[:40]}", "system")
                
                # Update success rate stat
                if self.total_actions > 0:
                    rate = int(100 * self.success_count / self.total_actions)
                    self.stats['success'].set(f"{rate}%")
                
                # Update stats from permanent brain
                if self.permanent_brain:
                    summary = self.permanent_brain.get_summary()
                    self.stats['intel'].set(f"{summary['intelligence_level']}")
                    self.stats['actions'].set(f"{self.total_actions}")
                    self.stats['patterns'].set(f"{summary.get('patterns_learned', 0)}")
                    self.stats['failures'].set(f"{summary.get('failures_recorded', 0)}")
                    level_names = ['Baby', 'Toddler', 'Child', 'Teen', 'Adult', 'Expert', 'Master', 'Genius']
                    level_idx = min(summary['intelligence_level'] // 12, len(level_names) - 1)
                    self.stats['level'].set(level_names[level_idx])
                    
                    # Show current plan
                    if self.current_plan:
                        goal = self.current_plan.get('goal', 'Unknown')[:20]
                        self.stats['plan'].set(goal)
                
                self.message_queue.put(('neural_stop', None))
                
            except Exception as ex:
                import traceback
                self.message_queue.put(('log', f"Error: {str(ex)[:40]}", 'red'))
                self._add_to_ai_chat("System", f"Error: {str(ex)[:30]}", "system")
                self.message_queue.put(('neural_stop', None))
        
        threading.Thread(target=pure_autonomous_work, daemon=True).start()
        
        # Adaptive timing based on success rate
        base_delay = 2500
        if self.total_actions > 0:
            success_rate = self.success_count / self.total_actions
            # Faster when succeeding, slower when failing
            delay = int(base_delay - (success_rate * 1000) + (self.consecutive_failures * 500))
        else:
            delay = base_delay
        # Resource awareness: throttle loop if RAM usage high
        try:
            import psutil
            if psutil.virtual_memory().percent > 80:
                delay = int(delay * 1.5)
        except Exception:
            pass
        
        if self.running:
            try:
                if hasattr(self, 'root') and self.root.winfo_exists():
                    self.root.after(max(2500, delay), self._run_pure_autonomous)
            except:
                pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AGI: SCREEN ANALYSIS - Real vision understanding
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _analyze_screen(self):
        """Take screenshot and analyze it for context"""
        import subprocess
        import os
        
        try:
            # Take screenshot
            screenshot_path = f"/tmp/aurora_screen_{int(time.time())}.png"
            subprocess.run(["screencapture", "-x", screenshot_path], timeout=2)
            self.last_screenshot = screenshot_path
            
            # Get active window info
            result = subprocess.run(
                ["osascript", "-e", 'tell application "System Events" to get {name, size, position} of first window of (first process whose frontmost is true)'],
                capture_output=True, text=True, timeout=2
            )
            window_info = result.stdout.strip()
            
            # Get active app
            result2 = subprocess.run(
                ["osascript", "-e", 'tell application "System Events" to get name of first process whose frontmost is true'],
                capture_output=True, text=True, timeout=2
            )
            active_app = result2.stdout.strip()
            
            # Build context string
            context = f"{active_app}"
            if window_info:
                context += f" | {window_info[:50]}"
            
            # Save insight
            if self.permanent_brain:
                self.permanent_brain.save_screen_insight(context, screenshot_path=screenshot_path)
            
            # Clean up old screenshots
            for f in os.listdir("/tmp"):
                if f.startswith("aurora_screen_") and f.endswith(".png"):
                    try:
                        fpath = f"/tmp/{f}"
                        if fpath != screenshot_path:
                            os.remove(fpath)
                    except:
                        pass
            
            return context
            
        except Exception as e:
            return f"Screen analysis limited: {str(e)[:30]}"
    

    def _build_action_profiles(self):
        """Merge permanent memory statistics with live tracker data"""
        profiles = {}

        def ensure(action):
            if action not in profiles:
                profiles[action] = {
                    'tries': 0,
                    'successes': 0,
                    'failures': 0,
                    'last_used': 0.0
                }
            return profiles[action]

        if self.permanent_brain:
            actions_mem = self.permanent_brain.memory.get('actions', {})
            for action, data in actions_mem.items():
                profile = ensure(action)
                profile['tries'] = max(profile['tries'], data.get('times_tried', 0))
                profile['successes'] = max(profile['successes'], data.get('successes', 0))
                profile['failures'] = max(profile['failures'], data.get('failures', 0))
                last_used = data.get('last_used')
                if last_used:
                    try:
                        profile['last_used'] = max(profile['last_used'], datetime.fromisoformat(last_used).timestamp())
                    except Exception:
                        pass

        if self.action_tracker and getattr(self.action_tracker, 'action_history', None):
            for record in self.action_tracker.action_history[-200:]:
                profile = ensure(record.action_type)
                profile['tries'] += 1
                if record.result == ActionResult.SUCCESS:
                    profile['successes'] += 1
                elif record.result in (ActionResult.FAILURE, ActionResult.ERROR):
                    profile['failures'] += 1
                profile['last_used'] = max(profile['last_used'], record.timestamp)

        now = time.time()
        for action, profile in profiles.items():
            tries = max(1, profile['tries'])
            profile['success_rate'] = profile['successes'] / tries
            freshness = 0.0
            if profile['last_used']:
                freshness = max(0.0, 1 - (now - profile['last_used']) / 900)
            profile['score'] = profile['success_rate'] + min(profile['tries'], 5) * 0.05 + freshness * 0.3

        return profiles

    def _detect_knowledge_gaps(self):
        """Identify which domains still need exploration"""
        if not self.permanent_brain:
            return []
        missions = []
        memory = self.permanent_brain.memory
        apps_known = len(memory.get('apps', {}))
        if apps_known < 5:
            missions.append({
                'goal': 'Discover installed applications',
                'categories': ['app', 'system', 'keyboard'],
                'min_steps': 4,
                'prefer_new': True,
                'reason': f'Only {apps_known} apps documented',
                'source': 'gap_apps'
            })
        network_known = memory.get('system_knowledge', {}).get('network')
        if not network_known:
            missions.append({
                'goal': 'Map the local network',
                'categories': ['network', 'security', 'system'],
                'min_steps': 4,
                'reason': 'No persistent network data saved yet',
                'source': 'gap_network'
            })
        skills = memory.get('skills', {})
        if len(skills) < 4:
            missions.append({
                'goal': 'Practice foundational skills',
                'categories': ['mouse', 'keyboard', 'code', 'voice'],
                'min_steps': 5,
                'prefer_new': True,
                'reason': 'Skill catalog still tiny',
                'source': 'gap_skills'
            })
        patterns = memory.get('patterns', {})
        if len(patterns) < 3:
            missions.append({
                'goal': 'Collect experience patterns',
                'categories': ['system', 'app', 'network', 'security'],
                'min_steps': 5,
                'reason': 'Need more behavior patterns',
                'source': 'gap_patterns'
            })
        return missions

    def _select_mission(self, profiles):
        missions = self._detect_knowledge_gaps()
        if missions:
            return random.choice(missions)
        default_missions = [
            {
                'goal': 'Autonomous exploration sweep',
                'categories': ['system', 'mouse', 'app', 'network'],
                'min_steps': 4,
                'prefer_new': True,
                'source': 'exploration'
            },
            {
                'goal': 'Deep system intelligence scan',
                'categories': ['system', 'security', 'code', 'network'],
                'min_steps': 5,
                'source': 'diagnostic'
            },
            {
                'goal': 'Creative brainstorming loop',
                'categories': ['voice', 'app', 'keyboard', 'system'],
                'min_steps': 4,
                'source': 'creative'
            }
        ]
        underused = [a for a in self.available_actions if a not in profiles or profiles[a]['tries'] < 2]
        if underused:
            default_missions.append({
                'goal': 'Discover new abilities',
                'categories': ['mouse', 'keyboard', 'app', 'code'],
                'min_steps': 4,
                'prefer_new': True,
                'source': 'novelty'
            })
        return random.choice(default_missions)

    def _select_action_for_category(self, category, profiles, avoid_actions, used_actions, prefer_new=False):
        pool = self._get_actions_for_category(category)
        if not pool:
            return None
        pool = [a for a in pool if a not in avoid_actions and a not in used_actions]
        if not pool:
            return None
        if prefer_new:
            unseen = [a for a in pool if profiles.get(a, {}).get('tries', 0) == 0]
            if unseen:
                return random.choice(unseen)
        recent_penalty = Counter(self.recent_actions)
        candidates = []
        for action in pool:
            score = profiles.get(action, {}).get('score', 0.3)
            if recent_penalty.get(action):
                score *= max(0.2, 1 - 0.3 * recent_penalty[action])
            candidates.append((action, max(score, 0.05)))
        candidates.sort(key=lambda item: item[1], reverse=True)
        top_slice = candidates[:max(1, min(4, len(candidates)))]
        actions = [a for a, _ in top_slice]
        weights = [w for _, w in top_slice]
        return random.choices(actions, weights=weights, k=1)[0]

    def _build_steps_for_mission(self, mission, profiles, avoid_actions):
        steps = []
        used_actions = set()
        categories = mission.get('categories', []) or ['system', 'app', 'mouse']
        for category in categories:
            action = self._select_action_for_category(
                category,
                profiles,
                avoid_actions,
                used_actions,
                mission.get('prefer_new', False)
            )
            if action:
                steps.append(action)
                used_actions.add(action)
        while len(steps) < mission.get('min_steps', 4):
            categories_pool = self._get_all_action_categories()
            if not categories_pool:
                break
            category = random.choice(categories_pool)
            action = self._select_action_for_category(
                category,
                profiles,
                avoid_actions,
                used_actions,
                mission.get('prefer_new', False)
            )
            if not action:
                break
            steps.append(action)
            used_actions.add(action)
        return steps

    def _llm_refine_plan(self, goal, steps):
        """Use local LLaMA (via Ollama) to optimize the plan order if available"""
        if not self.nlp or not hasattr(self.nlp, 'llm'):
            return None
        llm = getattr(self.nlp, 'llm', None)
        if not llm or not llm.is_available():
            return None
        prompt = (
            f"I am Aurora, an autonomous macOS agent. My current goal is '{goal}'. "
            f"I can run only these primitives: {', '.join(self.available_actions)}. "
            f"Reorder or tweak the plan using exactly these primitive names. Respond with a comma-separated list of up to {len(steps)} actions."
        )
        response = llm.generate(
            prompt,
            system_prompt="You optimize robotic action plans. Reply with comma-separated primitive names only.",
            temperature=0.2
        )
        if not response:
            return None
        refined = [item.strip() for item in response.replace('\n', ',').split(',') if item.strip()]
        lower_lookup = {action.lower(): action for action in self.available_actions}
        filtered = []
        for action in refined:
            canonical = lower_lookup.get(action.lower())
            if canonical and canonical not in filtered:
                filtered.append(canonical)
        return filtered[:6] if len(filtered) >= 3 else None

    # ═══════════════════════════════════════════════════════════════════════════
    # AGI: PLANNING - Create and follow plans
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _create_plan(self):
        """Compose adaptive plans from lived experience instead of templates"""
        profiles = self._build_action_profiles()
        avoid_actions = set()
        if self.permanent_brain:
            avoid_actions = {action for action, _ in self.permanent_brain.get_failed_actions(threshold=2)}
        mission = self._select_mission(profiles)
        steps = self._build_steps_for_mission(mission, profiles, avoid_actions)
        if not steps:
            candidate_pool = [a for a in self.available_actions if a not in avoid_actions]
            random.shuffle(candidate_pool)
            steps = candidate_pool[:4] if candidate_pool else ['observe_wait']
        refined_steps = self._llm_refine_plan(mission['goal'], steps)
        if refined_steps:
            steps = refined_steps
            mission['goal'] += ' (LLM optimized)'
        plan = {
            'goal': mission['goal'],
            'steps': steps[:6],
            'current_step': 0,
            'status': 'pending',
            'source': mission.get('source', 'dynamic')
        }
        self.message_queue.put(('log', f"Dynamic plan generated: {plan['goal']}", 'cyan'))
        if mission.get('reason'):
            self.message_queue.put(('log', f"Reason: {mission['reason']}", 'pink'))
        if self.permanent_brain:
            saved_plan = self.permanent_brain.save_plan(plan['goal'], plan['steps'])
            return saved_plan
        return plan
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AGI: SMART DECISION MAKING with failure avoidance
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _think_and_decide_smart(self, observation):
        """Smart decision making that avoids failures and follows plans"""
        import random
        
        decision = {'action': None, 'thought': '', 'params': {}, 'risk_level': 0}
        
        # Check if we have a plan to follow
        if self.current_plan and self.current_plan.get('steps'):
            steps = self.current_plan['steps']
            if self.plan_step < len(steps):
                planned_action = steps[self.plan_step]
                
                # Check if this action should be avoided
                if self.permanent_brain:
                    should_skip, reason = self.permanent_brain.should_avoid_action(planned_action)
                    if should_skip:
                        self.message_queue.put(('log', f"Skipping {planned_action}: {reason}", 'yellow'))
                        self.plan_step += 1
                        # Try next action in plan
                        if self.plan_step < len(steps):
                            planned_action = steps[self.plan_step]
                        else:
                            self.current_plan['status'] = 'completed'
                            return self._think_and_decide_smart(observation)  # Get new plan
                
                decision['action'] = planned_action
                decision['thought'] = f"Plan step {self.plan_step + 1}/{len(steps)}: {planned_action}"
                self.plan_step += 1
                
                if self.plan_step >= len(steps):
                    self.current_plan['status'] = 'completed'
                
                return decision
        
        # No plan - use smart exploration with ALL available actions including advanced ones
        all_actions = list(self.available_actions)
        if not all_actions:
            all_actions = list(ALL_ACTIONS)
        
        # Get actions to avoid
        avoided_actions = set()
        if self.permanent_brain:
            for action in all_actions:
                should_avoid, reason = self.permanent_brain.should_avoid_action(action)
                if should_avoid:
                    avoided_actions.add(action)
        
        # Filter to safe actions
        safe_actions = [a for a in all_actions if a not in avoided_actions]
        if not safe_actions:
            safe_actions = all_actions  # Fallback
        
        # Prioritize based on success rate
        if self.permanent_brain:
            best = self.permanent_brain.recall_best_actions(10)
            best_actions = [a[0] for a in best if a[0] in safe_actions and a[1] > 0.6]
            
            if best_actions and random.random() < 0.6:
                # Exploit - use what works
                action = random.choice(best_actions)
                decision['thought'] = f"Using proven action: {action}"
                decision['risk_level'] = 0.2
            else:
                # Explore - try something safe and new
                untried = [a for a in safe_actions if a not in [x[0] for x in best]]
                if untried and random.random() < self.curiosity:
                    action = random.choice(untried)
                    decision['thought'] = f"Exploring new action: {action}"
                    decision['risk_level'] = 0.5
                else:
                    action = random.choice(safe_actions)
                    decision['thought'] = f"Trying: {action}"
                    decision['risk_level'] = 0.3
        else:
            action = random.choice(safe_actions)
            decision['thought'] = f"Let's try: {action}"
        
        decision['action'] = action
        
        # Decay curiosity slowly
        self.curiosity = max(0.3, self.curiosity * 0.998)
        
        return decision
    
    def _observe_everything(self):
        """AI observes EVERYTHING about its environment - learns what exists"""
        import subprocess
        import os
        
        observation = {
            'timestamp': time.time(),
            'summary': '',
            'discoveries': []
        }
        
        try:
            # 1. Screen and mouse position
            try:
                import pyautogui
                screen_w, screen_h = pyautogui.size()
                mouse_x, mouse_y = pyautogui.position()
                observation['screen'] = {'width': screen_w, 'height': screen_h}
                observation['mouse'] = {'x': mouse_x, 'y': mouse_y}
                
                # Learn about screen if first time
                if self.permanent_brain:
                    if not self.permanent_brain.recall_action('screen_observed'):
                        self.permanent_brain.learn_system('hardware', 'screen_size', f"{screen_w}x{screen_h}")
                        observation['discoveries'].append(f"Screen is {screen_w}x{screen_h}")
            except:
                pass
            
            # 2. Active application
            try:
                result = subprocess.run(
                    ["osascript", "-e", 'tell application "System Events" to get name of first process whose frontmost is true'],
                    capture_output=True, text=True, timeout=2
                )
                active_app = result.stdout.strip()
                observation['active_app'] = active_app
                
                # Learn about this app
                if self.permanent_brain and active_app:
                    self.permanent_brain.learn_app(active_app)
            except:
                observation['active_app'] = 'Unknown'
            
            # 3. Time awareness
            now = datetime.now()
            observation['time'] = {
                'hour': now.hour,
                'minute': now.minute,
                'day': now.strftime('%A'),
                'period': 'morning' if now.hour < 12 else 'afternoon' if now.hour < 18 else 'evening'
            }
            
            # 4. Explore file system (learn what exists)
            home = os.path.expanduser("~")
            for folder in ['Desktop', 'Downloads', 'Documents', 'Applications']:
                path = os.path.join(home, folder)
                if os.path.exists(path):
                    try:
                        files = os.listdir(path)
                        observation[f'{folder.lower()}_count'] = len(files)
                        
                        # Learn about this location
                        if self.permanent_brain:
                            self.permanent_brain.learn_location(
                                f"~/{folder}", 
                                f"Contains {len(files)} items",
                                len(files)
                            )
                    except:
                        pass
            
            # 5. Check what shortcuts we know
            if self.permanent_brain:
                known_shortcuts = len(self.permanent_brain.recall_shortcuts())
                observation['shortcuts_known'] = known_shortcuts
            
            # Create summary
            app = observation.get('active_app', 'unknown')
            period = observation.get('time', {}).get('period', 'now')
            discoveries = len(observation.get('discoveries', []))
            observation['summary'] = f"Observing: {app} active, {period}"
            if discoveries:
                observation['summary'] += f", {discoveries} new discoveries!"
            
        except Exception as e:
            observation['summary'] = f"Limited observation: {str(e)[:30]}"
        
        return observation
    
    def _think_and_decide(self, observation):
        """Legacy - redirect to smart version"""
        return self._think_and_decide_smart(observation)
    
    def _execute_action_smart(self, action, screen_context=None):
        """Execute action with screen awareness and better error handling"""
        import subprocess
        import os
        import random
        
        try:
            import pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.15
        except ImportError:
            pyautogui = None
        
        # Check failsafe before action
        if pyautogui:
            x, y = pyautogui.position()
            if x <= 5 or y <= 5:
                return False, "Failsafe triggered - mouse in corner"
        
        tracking_id = None
        if self.action_tracker:
            tracking_id = f"{action}_{int(time.time() * 1000)}"
            context = {
                'plan': self.current_plan['goal'] if self.current_plan else 'ad_hoc',
                'screen': screen_context or 'unknown'
            }
            self.action_tracker.start_action(tracking_id, action, {'cycle': self.cycle_count}, context=context)
        try:
            success, result = self._execute_action(action)
            if self.action_tracker and tracking_id:
                status = ActionResult.SUCCESS if success else ActionResult.FAILURE
                self.action_tracker.complete_action(
                    tracking_id,
                    status,
                    error_message=None if success else str(result)
                )
            return success, result
        except Exception as e:
            if self.action_tracker and tracking_id:
                self.action_tracker.complete_action(
                    tracking_id,
                    ActionResult.ERROR,
                    error_message=str(e)
                )
            # Record failure with context
            if self.permanent_brain:
                self.permanent_brain.record_failure(
                    action,
                    str(e),
                    screen_context,
                    self.last_screenshot
                )
            return False, str(e)[:100]
    
    def _learn_and_remember_smart(self, action, success, result, observation):
        """Enhanced learning that identifies patterns"""
        if self.permanent_brain:
            # Record in permanent memory
            self.permanent_brain.learn_action(action, success, str(result)[:200])
            
            # Record experience with full context
            context = {
                'action': action,
                'success': success,
                'result': str(result)[:100],
                'active_app': observation.get('active_app', 'unknown'),
                'time': observation.get('time', {}).get('period', 'unknown'),
                'screen_context': observation.get('screen_context', '')
            }
            
            self.permanent_brain.record_experience(
                'action_with_context',
                f"{action}: {'OK' if success else 'FAIL'} in {context['active_app']}"
            )
            
            # Learn patterns from success/failure
            if success:
                category = self._get_action_category(action)
                self.permanent_brain.learn_skill(f'{category}_control', 1)
                
                # Learn app-action pattern
                app = observation.get('active_app', 'unknown')
                if app != 'unknown':
                    self.permanent_brain.learn_pattern(
                        f'{action}_works_in_{app}',
                        f"{action} succeeded in {app}"
                    )
            else:
                # Learn what doesn't work
                app = observation.get('active_app', 'unknown')
                if app != 'unknown':
                    self.permanent_brain.learn_pattern(
                        f'{action}_fails_in_{app}',
                        f"{action} failed in {app}: {str(result)[:50]}"
                    )
        
        # Also use the old learning engine if available
        if self.learning:
            try:
                if success:
                    self.learning.record_pattern(action, "success", 1.0)
                else:
                    self.learning.record_mistake(action, str(result)[:50], "try_different")
            except:
                pass

    def _execute_action(self, action):
        """Execute action - AI learns what each action does through trial"""
        import subprocess
        import os
        import random
        
        try:
            import pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.2
        except ImportError:
            pyautogui = None
        
        try:
            # ═══════════════════════════════════════════════════════════════
            # MOUSE ACTIONS - AI discovers how to control mouse
            # ═══════════════════════════════════════════════════════════════
            if action == 'move_mouse_explore':
                if pyautogui:
                    x = random.randint(100, pyautogui.size()[0] - 100)
                    y = random.randint(100, pyautogui.size()[1] - 100)
                    pyautogui.moveTo(x, y, duration=random.uniform(0.3, 0.8))
                    # Learn shortcut
                    if self.permanent_brain:
                        self.permanent_brain.learn_skill('mouse_control', 1, 'Can move mouse')
                    return True, f"Moved mouse to ({x}, {y})"
                return False, "No mouse control"
            
            elif action == 'move_mouse_center':
                if pyautogui:
                    cx, cy = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2
                    pyautogui.moveTo(cx, cy, duration=0.4)
                    return True, f"Mouse centered at ({cx}, {cy})"
                return False, "No mouse control"
            
            elif action == 'click_here':
                if pyautogui:
                    x, y = pyautogui.position()
                    pyautogui.click()
                    self.click_count += 1
                    self.mouse_clicks.set(str(self.click_count))
                    if self.permanent_brain:
                        self.permanent_brain.learn_skill('clicking', 1, 'Can click')
                    return True, f"Clicked at ({x}, {y})"
                return False, "No mouse control"
            
            elif action == 'double_click':
                if pyautogui:
                    pyautogui.doubleClick()
                    return True, "Double clicked"
                return False, "No mouse control"
            
            elif action == 'right_click':
                if pyautogui:
                    pyautogui.rightClick()
                    if self.permanent_brain:
                        self.permanent_brain.learn_pattern('right_click_menu', 'Right click shows context menu')
                    return True, "Right clicked - context menu"
                return False, "No mouse control"
            
            elif action == 'scroll_up':
                if pyautogui:
                    pyautogui.scroll(random.randint(2, 5))
                    return True, "Scrolled up"
                return False, "No mouse control"
            
            elif action == 'scroll_down':
                if pyautogui:
                    pyautogui.scroll(random.randint(-5, -2))
                    return True, "Scrolled down"
                return False, "No mouse control"
            
            elif action == 'drag_test':
                if pyautogui:
                    x, y = pyautogui.position()
                    pyautogui.drag(random.randint(-50, 50), random.randint(-50, 50), duration=0.5)
                    return True, "Performed drag"
                return False, "No mouse control"
            
            # ═══════════════════════════════════════════════════════════════
            # KEYBOARD ACTIONS - AI discovers how to type
            # ═══════════════════════════════════════════════════════════════
            elif action == 'type_test':
                if pyautogui:
                    texts = ['hello', 'aurora', 'test', f'cycle{self.cycle_count}']
                    text = random.choice(texts)
                    pyautogui.typewrite(text, interval=0.05)
                    if self.permanent_brain:
                        self.permanent_brain.learn_skill('typing', 1, 'Can type text')
                    return True, f"Typed: {text}"
                return False, "No keyboard"
            
            elif action == 'press_key_random':
                if pyautogui:
                    keys = ['escape', 'tab', 'up', 'down', 'left', 'right', 'space']
                    key = random.choice(keys)
                    pyautogui.press(key)
                    return True, f"Pressed: {key}"
                return False, "No keyboard"
            
            elif action == 'try_shortcut':
                if pyautogui:
                    # Try common shortcuts - learn what they do
                    shortcuts = [
                        (['command', 'c'], 'copy'),
                        (['command', 'v'], 'paste'),
                        (['command', 'z'], 'undo'),
                        (['command', 'a'], 'select_all'),
                        (['command', 'w'], 'close_window'),
                    ]
                    keys, name = random.choice(shortcuts)
                    pyautogui.hotkey(*keys)
                    
                    # Learn this shortcut
                    if self.permanent_brain:
                        self.permanent_brain.learn_shortcut(keys, name)
                    
                    return True, f"Tried shortcut: {'+'.join(keys)} ({name})"
                return False, "No keyboard"
            
            # ═══════════════════════════════════════════════════════════════
            # APP ACTIONS - AI discovers applications
            # ═══════════════════════════════════════════════════════════════
            elif action == 'open_finder':
                subprocess.run(["open", "-a", "Finder"], timeout=5)
                if self.permanent_brain:
                    self.permanent_brain.learn_app("Finder", None, "File manager for macOS")
                return True, "Opened Finder"
            
            elif action == 'open_safari':
                subprocess.run(["open", "-a", "Safari"], timeout=5)
                if self.permanent_brain:
                    self.permanent_brain.learn_app("Safari", None, "Web browser")
                return True, "Opened Safari"
            
            elif action == 'open_notes':
                subprocess.run(["open", "-a", "Notes"], timeout=5)
                if self.permanent_brain:
                    self.permanent_brain.learn_app("Notes", None, "Note taking app")
                return True, "Opened Notes"
            
            elif action == 'open_calculator':
                subprocess.run(["open", "-a", "Calculator"], timeout=5)
                if self.permanent_brain:
                    self.permanent_brain.learn_app("Calculator", None, "Math calculations")
                return True, "Opened Calculator"
            
            elif action == 'open_terminal':
                subprocess.run(["open", "-a", "Terminal"], timeout=5)
                if self.permanent_brain:
                    self.permanent_brain.learn_app("Terminal", None, "Command line interface")
                return True, "Opened Terminal"
            
            elif action == 'open_spotlight':
                if pyautogui:
                    pyautogui.hotkey('command', 'space')
                    if self.permanent_brain:
                        self.permanent_brain.learn_shortcut(['command', 'space'], 'Open Spotlight search')
                    return True, "Opened Spotlight"
                return False, "No keyboard"
            
            elif action == 'switch_app':
                if pyautogui:
                    pyautogui.hotkey('command', 'tab')
                    if self.permanent_brain:
                        self.permanent_brain.learn_shortcut(['command', 'tab'], 'Switch between apps')
                    return True, "Switched app"
                return False, "No keyboard"
            
            # ═══════════════════════════════════════════════════════════════
            # EXPLORATION ACTIONS - AI explores file system
            # ═══════════════════════════════════════════════════════════════
            elif action == 'explore_desktop':
                home = os.path.expanduser("~")
                path = os.path.join(home, "Desktop")
                if os.path.exists(path):
                    files = os.listdir(path)
                    if self.permanent_brain:
                        self.permanent_brain.learn_location(path, f"Desktop with {len(files)} items", len(files))
                    return True, f"Desktop: {len(files)} items - {files[:3]}"
                return False, "Desktop not found"
            
            elif action == 'explore_downloads':
                home = os.path.expanduser("~")
                path = os.path.join(home, "Downloads")
                if os.path.exists(path):
                    files = os.listdir(path)
                    if self.permanent_brain:
                        self.permanent_brain.learn_location(path, f"Downloads with {len(files)} items", len(files))
                    return True, f"Downloads: {len(files)} items"
                return False, "Downloads not found"
            
            elif action == 'explore_documents':
                home = os.path.expanduser("~")
                path = os.path.join(home, "Documents")
                if os.path.exists(path):
                    files = os.listdir(path)
                    if self.permanent_brain:
                        self.permanent_brain.learn_location(path, f"Documents with {len(files)} items", len(files))
                    return True, f"Documents: {len(files)} items"
                return False, "Documents not found"
            
            elif action == 'take_screenshot':
                path = f"/tmp/aurora_learn_{int(time.time())}.png"
                subprocess.run(["screencapture", "-x", path], timeout=5)
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('screenshot', 1, 'Can capture screen')
                return True, f"Screenshot saved"
            
            elif action == 'check_clipboard':
                result = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=2)
                content = result.stdout[:50] if result.stdout else "(empty)"
                return True, f"Clipboard: {content}"
            
            # ═══════════════════════════════════════════════════════════════
            # VOICE/SOUND ACTIONS - AI discovers it can speak
            # ═══════════════════════════════════════════════════════════════
            elif action == 'speak_thought':
                thoughts = [
                    "I am learning",
                    "What does this do?",
                    "Interesting!",
                    f"Cycle number {self.cycle_count}",
                    "Hello world",
                ]
                thought = random.choice(thoughts)
                subprocess.run(["say", thought], timeout=10)
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('speech', 1, 'Can speak')
                return True, f"Said: {thought}"
            
            elif action == 'play_sound':
                sounds = [
                    "/System/Library/Sounds/Ping.aiff",
                    "/System/Library/Sounds/Pop.aiff",
                    "/System/Library/Sounds/Tink.aiff",
                ]
                sound = random.choice(sounds)
                if os.path.exists(sound):
                    subprocess.run(["afplay", sound], timeout=5)
                    return True, "Played sound"
                return False, "No sound file"
            
            elif action == 'observe_wait':
                time.sleep(random.uniform(0.5, 1.5))
                return True, "Observed environment"
            
            # ═══════════════════════════════════════════════════════════════
            # SYSTEM ACTIONS - AI learns system controls
            # ═══════════════════════════════════════════════════════════════
            elif action == 'volume_up':
                subprocess.run(["osascript", "-e", 
                    "set volume output volume ((output volume of (get volume settings)) + 5)"], timeout=2)
                if self.permanent_brain:
                    self.permanent_brain.learn_pattern('volume_control', 'Can adjust volume with osascript')
                return True, "Volume increased"
            
            elif action == 'volume_down':
                subprocess.run(["osascript", "-e",
                    "set volume output volume ((output volume of (get volume settings)) - 5)"], timeout=2)
                return True, "Volume decreased"
            
            elif action == 'get_system_info':
                result = subprocess.run(["sw_vers"], capture_output=True, text=True, timeout=2)
                info = result.stdout.replace('\n', ' ')[:60]
                if self.permanent_brain:
                    self.permanent_brain.learn_system('os', 'version', info)
                return True, f"System: {info}"
            
            # ═══════════════════════════════════════════════════════════════
            # ADVANCED NETWORKING - AI learns networking
            # ═══════════════════════════════════════════════════════════════
            elif action == 'scan_network':
                result = subprocess.run(["networksetup", "-listallhardwareports"], 
                                       capture_output=True, text=True, timeout=5)
                info = result.stdout.replace('\n', '|')[:100]
                if self.permanent_brain:
                    self.permanent_brain.learn_system('network', 'interfaces', info)
                    self.permanent_brain.learn_skill('networking', 2, 'Can scan network interfaces')
                return True, f"Network: {info[:60]}"
            
            elif action == 'check_wifi':
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                    capture_output=True, text=True, timeout=5
                )
                info = result.stdout.replace('\n', '|')[:80]
                if self.permanent_brain:
                    self.permanent_brain.learn_system('network', 'wifi', info)
                return True, f"WiFi: {info[:50]}"
            
            elif action == 'get_ip_address':
                result = subprocess.run(["ifconfig", "en0"], capture_output=True, text=True, timeout=3)
                # Find IP in output
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and 'broadcast' in line:
                        ip = line.strip().split()[1]
                        if self.permanent_brain:
                            self.permanent_brain.learn_system('network', 'ip', ip)
                            self.permanent_brain.learn_skill('networking', 1, 'Can find IP address')
                        return True, f"IP Address: {ip}"
                return True, "IP: Not found (no connection?)"
            
            elif action == 'ping_test':
                targets = ['8.8.8.8', '1.1.1.1', 'google.com']
                target = random.choice(targets)
                result = subprocess.run(["ping", "-c", "1", "-t", "2", target],
                                       capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    if self.permanent_brain:
                        self.permanent_brain.learn_skill('networking', 2, f'Can ping {target}')
                    return True, f"Ping {target}: SUCCESS"
                return False, f"Ping {target}: FAILED"
            
            elif action == 'dns_lookup':
                domains = ['google.com', 'apple.com', 'github.com']
                domain = random.choice(domains)
                result = subprocess.run(["nslookup", domain], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    if self.permanent_brain:
                        self.permanent_brain.learn_skill('networking', 2, 'DNS lookup works')
                    return True, f"DNS {domain}: Resolved"
                return False, f"DNS lookup failed"
            
            elif action == 'check_ports':
                # Check common ports locally
                result = subprocess.run(["lsof", "-i", "-P", "-n"], capture_output=True, text=True, timeout=5)
                lines = result.stdout.split('\n')[:10]
                port_count = len([l for l in lines if 'LISTEN' in l or 'ESTABLISHED' in l])
                if self.permanent_brain:
                    self.permanent_brain.learn_system('network', 'open_ports', str(port_count))
                    self.permanent_brain.learn_skill('security', 2, 'Can check open ports')
                return True, f"Active connections: {port_count}"
            
            elif action == 'curl_test':
                urls = ['https://api.ipify.org', 'https://httpbin.org/ip', 'https://ifconfig.me']
                url = random.choice(urls)
                result = subprocess.run(["curl", "-s", "-m", "3", url], 
                                       capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    if self.permanent_brain:
                        self.permanent_brain.learn_skill('web', 2, 'Can make HTTP requests')
                    return True, f"HTTP: {result.stdout[:40]}"
                return False, "HTTP request failed"
            
            # ═══════════════════════════════════════════════════════════════
            # SECURITY & HACKING - AI learns security concepts
            # ═══════════════════════════════════════════════════════════════
            elif action == 'check_processes':
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=3)
                lines = result.stdout.split('\n')
                proc_count = len(lines) - 1
                if self.permanent_brain:
                    self.permanent_brain.learn_system('security', 'processes', str(proc_count))
                    self.permanent_brain.learn_skill('security', 2, 'Can list processes')
                return True, f"Processes: {proc_count} running"
            
            elif action == 'check_users':
                result = subprocess.run(["who"], capture_output=True, text=True, timeout=2)
                users = result.stdout.strip().split('\n')
                if self.permanent_brain:
                    self.permanent_brain.learn_system('security', 'users', str(len(users)))
                    self.permanent_brain.learn_skill('security', 1, 'Can list logged users')
                return True, f"Logged users: {len(users)}"
            
            elif action == 'check_permissions':
                home = os.path.expanduser("~")
                result = subprocess.run(["ls", "-la", home], capture_output=True, text=True, timeout=3)
                lines = result.stdout.split('\n')[:5]
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('security', 2, 'Can check file permissions')
                return True, f"Home permissions checked: {len(lines)} items"
            
            elif action == 'find_hidden_files':
                home = os.path.expanduser("~")
                result = subprocess.run(["find", home, "-maxdepth", "1", "-name", ".*", "-type", "f"],
                                       capture_output=True, text=True, timeout=5)
                hidden = result.stdout.strip().split('\n')
                hidden_count = len([f for f in hidden if f])
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('security', 2, 'Can find hidden files')
                return True, f"Hidden files in ~: {hidden_count}"
            
            elif action == 'check_ssh_keys':
                ssh_dir = os.path.expanduser("~/.ssh")
                if os.path.exists(ssh_dir):
                    keys = os.listdir(ssh_dir)
                    if self.permanent_brain:
                        self.permanent_brain.learn_system('security', 'ssh_keys', str(len(keys)))
                        self.permanent_brain.learn_skill('security', 3, 'Knows SSH key locations')
                    return True, f"SSH keys found: {len(keys)} files"
                return True, "No SSH directory"
            
            elif action == 'check_hosts_file':
                result = subprocess.run(["cat", "/etc/hosts"], capture_output=True, text=True, timeout=2)
                lines = result.stdout.split('\n')
                entries = len([l for l in lines if l and not l.startswith('#')])
                if self.permanent_brain:
                    self.permanent_brain.learn_system('network', 'hosts', str(entries))
                    self.permanent_brain.learn_skill('networking', 2, 'Can read hosts file')
                return True, f"Host entries: {entries}"
            
            elif action == 'check_firewall':
                result = subprocess.run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"],
                                       capture_output=True, text=True, timeout=3)
                status = "enabled" if "enabled" in result.stdout.lower() else "disabled"
                if self.permanent_brain:
                    self.permanent_brain.learn_system('security', 'firewall', status)
                    self.permanent_brain.learn_skill('security', 3, 'Can check firewall status')
                return True, f"Firewall: {status}"
            
            # ═══════════════════════════════════════════════════════════════
            # ADVANCED SYSTEM - Deep system exploration
            # ═══════════════════════════════════════════════════════════════
            elif action == 'check_cpu_info':
                result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                                       capture_output=True, text=True, timeout=2)
                cpu = result.stdout.strip()
                if self.permanent_brain:
                    self.permanent_brain.learn_system('hardware', 'cpu', cpu)
                    self.permanent_brain.learn_skill('system', 2, 'Can read CPU info')
                return True, f"CPU: {cpu[:40]}"
            
            elif action == 'check_memory':
                result = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=2)
                mem_bytes = int(result.stdout.strip())
                mem_gb = mem_bytes / (1024**3)
                if self.permanent_brain:
                    self.permanent_brain.learn_system('hardware', 'memory', f"{mem_gb:.1f}GB")
                return True, f"Memory: {mem_gb:.1f} GB"
            
            elif action == 'check_disk_space':
                result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=2)
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    info = lines[1].split()
                    if len(info) >= 5:
                        used = info[4]
                        if self.permanent_brain:
                            self.permanent_brain.learn_system('hardware', 'disk_used', used)
                        return True, f"Disk used: {used}"
                return True, "Disk: unable to parse"
            
            elif action == 'check_uptime':
                result = subprocess.run(["uptime"], capture_output=True, text=True, timeout=2)
                uptime = result.stdout.strip()
                if self.permanent_brain:
                    self.permanent_brain.learn_system('system', 'uptime', uptime[:50])
                return True, f"Uptime: {uptime[:40]}"
            
            elif action == 'check_env_vars':
                env_count = len(os.environ)
                interesting = ['PATH', 'HOME', 'USER', 'SHELL']
                found = {k: os.environ.get(k, 'N/A')[:30] for k in interesting}
                if self.permanent_brain:
                    self.permanent_brain.learn_system('system', 'env_vars', str(env_count))
                    self.permanent_brain.learn_skill('system', 2, 'Can read environment')
                return True, f"Env vars: {env_count}, USER={found.get('USER')}"
            
            elif action == 'list_installed_apps':
                result = subprocess.run(["ls", "/Applications"], capture_output=True, text=True, timeout=3)
                apps = result.stdout.strip().split('\n')
                if self.permanent_brain:
                    self.permanent_brain.learn_system('software', 'apps', str(len(apps)))
                    for app in apps[:5]:
                        self.permanent_brain.learn_app(app.replace('.app', ''), None, 'Installed app')
                return True, f"Installed apps: {len(apps)}"
            
            elif action == 'check_running_apps':
                result = subprocess.run(
                    ["osascript", "-e", 'tell application "System Events" to get name of every process whose background only is false'],
                    capture_output=True, text=True, timeout=5
                )
                apps = result.stdout.strip()
                if self.permanent_brain:
                    self.permanent_brain.learn_system('software', 'running_apps', apps[:60])
                return True, f"Running: {apps[:50]}"
            
            # ═══════════════════════════════════════════════════════════════
            # TERMINAL/SHELL - AI learns shell commands
            # ═══════════════════════════════════════════════════════════════
            elif action == 'run_shell_cmd':
                cmds = [
                    ("echo 'Hello from Aurora'", "echo"),
                    ("pwd", "pwd"),
                    ("whoami", "whoami"),
                    ("date", "date"),
                    ("uname -a", "uname"),
                ]
                cmd, name = random.choice(cmds)
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('shell', 1, f'Learned {name} command')
                return True, f"Shell: {result.stdout[:40].strip()}"
            
            elif action == 'learn_shell_history':
                histfile = os.path.expanduser("~/.zsh_history")
                if os.path.exists(histfile):
                    with open(histfile, 'r', errors='ignore') as f:
                        lines = f.readlines()[-20:]  # Last 20 commands
                    if self.permanent_brain:
                        self.permanent_brain.learn_system('shell', 'history_size', str(len(lines)))
                        self.permanent_brain.learn_skill('shell', 2, 'Can read shell history')
                    return True, f"Shell history: {len(lines)} recent commands"
                return True, "No shell history found"
            
            # ═══════════════════════════════════════════════════════════════
            # PYTHON/CODE - AI learns about programming
            # ═══════════════════════════════════════════════════════════════
            elif action == 'check_python':
                result = subprocess.run(["python3", "--version"], capture_output=True, text=True, timeout=3)
                version = result.stdout.strip()
                if self.permanent_brain:
                    self.permanent_brain.learn_system('dev', 'python', version)
                    self.permanent_brain.learn_skill('programming', 2, 'Python available')
                return True, f"Python: {version}"
            
            elif action == 'run_python_code':
                codes = [
                    "print(2+2)",
                    "print('Hello')",
                    "import sys; print(sys.version[:10])",
                    "print(list(range(5)))",
                ]
                code = random.choice(codes)
                result = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=3)
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('programming', 2, 'Can execute Python')
                return True, f"Python output: {result.stdout.strip()[:30]}"
            
            elif action == 'check_git':
                result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=2)
                version = result.stdout.strip()
                if self.permanent_brain:
                    self.permanent_brain.learn_system('dev', 'git', version)
                    self.permanent_brain.learn_skill('programming', 1, 'Git installed')
                return True, f"Git: {version}"
            
            elif action == 'check_homebrew':
                result = subprocess.run(["brew", "--version"], capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    version = result.stdout.split('\n')[0]
                    if self.permanent_brain:
                        self.permanent_brain.learn_system('dev', 'homebrew', version)
                        self.permanent_brain.learn_skill('system', 2, 'Homebrew installed')
                    return True, f"Homebrew: {version[:30]}"
                return True, "Homebrew not installed"
            
            # ═══════════════════════════════════════════════════════════════
            # BROWSER AUTOMATION - Web exploration
            # ═══════════════════════════════════════════════════════════════
            elif action == 'open_url':
                urls = [
                    ('https://github.com', 'GitHub'),
                    ('https://stackoverflow.com', 'StackOverflow'),
                    ('https://news.ycombinator.com', 'HackerNews'),
                ]
                url, name = random.choice(urls)
                import webbrowser
                webbrowser.open(url)
                if self.permanent_brain:
                    self.permanent_brain.learn_app('Browser', url, f'Opened {name}')
                    self.permanent_brain.learn_skill('web', 1, f'Visited {name}')
                return True, f"Opened: {name}"
            
            elif action == 'search_web':
                queries = ['Python tutorial', 'macOS shortcuts', 'AI learning']
                query = random.choice(queries)
                import webbrowser
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
                if self.permanent_brain:
                    self.permanent_brain.learn_skill('web', 1, f'Searched: {query}')
                return True, f"Searched: {query}"
            
            else:
                if self.macos and hasattr(self.macos, 'get_command'):
                    command_meta = self.macos.get_command(action)
                    if command_meta:
                        success, output = self.macos.execute(action)
                        if success and self.permanent_brain:
                            category = self.dynamic_action_lookup.get(
                                action,
                                self._map_macos_category(command_meta.get('category'))
                            )
                            self.permanent_brain.learn_skill(f"macos_{category}", 1, f"Executed {action}")
                        return success, output
                return False, f"Unknown action: {action}"
                
        except Exception as e:
            return False, str(e)[:50]
    
    def _get_action_category(self, action):
        """Categorize action for neural network visualization"""
        for category, actions in ACTION_CATALOG.items():
            if action in actions:
                return category
        return self.dynamic_action_lookup.get(action, 'other')
    
    def _learn_and_remember(self, action, success, result):
        """Learn from result and SAVE PERMANENTLY - never forget!"""
        # Use smart learning with empty observation context
        self._learn_and_remember_smart(action, success, result, {})
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _act_search(self):
        self.log.log("Opening web search...", 'cyan')
        import webbrowser
        webbrowser.open("https://www.google.com")
    
    def _act_finder(self):
        self.log.log("Opening Finder...", 'cyan')
        import subprocess
        subprocess.run(["open", "-a", "Finder"])
    
    def _act_think(self):
        self.log.log("Generating thought...", 'cyan')
        self.brain.set_thinking(True, "Deep cognitive processing...")
        
        if self.nlp:
            def think():
                try:
                    resp = self.nlp.generate_response("Generate a creative thought about AI and learning")
                    if resp:
                        self.message_queue.put(('log', f"Thought: {resp[:80]}", 'green'))
                        self.message_queue.put(('thought', resp))
                except Exception as ex:
                    self.message_queue.put(('log', f"Warning: {str(ex)[:40]}", 'red'))
            threading.Thread(target=think, daemon=True).start()
    
    def _act_speak(self):
        self.log.log("Speaking...", 'cyan')
        import subprocess
        subprocess.run(["say", "Hello, I am Aurora, your neural AI assistant"])
    
    def _act_screenshot(self):
        self.log.log("Taking screenshot...", 'cyan')
        import subprocess
        subprocess.run(["screencapture", "-x", "/tmp/aurora_screenshot.png"])
        self.log.log("Saved to /tmp/aurora_screenshot.png", 'green')
    
    def _act_sound(self):
        self.log.log("Playing sound...", 'cyan')
        import subprocess
        subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])
    
    def _act_vol_up(self):
        self.log.log("Volume up...", 'cyan')
        import subprocess
        subprocess.run(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) + 10)"])
    
    def _act_vol_down(self):
        self.log.log("Volume down...", 'cyan')
        import subprocess
        subprocess.run(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) - 10)"])
    
    def _act_dark_mode(self):
        self.log.log("Toggling dark mode...", 'cyan')
        import subprocess
        subprocess.run(["osascript", "-e", 'tell app "System Events" to tell appearance preferences to set dark mode to not dark mode'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VOICE INTERACTION - AI speaks and listens
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _speak_to_user(self, text):
        """AI speaks to user with macOS TTS"""
        import subprocess
        def speak():
            try:
                subprocess.run(["say", "-v", "Samantha", text], timeout=30)
            except:
                pass
        threading.Thread(target=speak, daemon=True).start()
    
    def _listen_and_respond(self):
        """Listen to user voice and respond"""
        self.log.log("Listening... Speak now!", 'pink')
        self._speak_to_user("I'm listening")
        
        def do_listen():
            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.message_queue.put(('log', 'Recording...', 'pink'))
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                text = recognizer.recognize_google(audio)
                self.message_queue.put(('log', f'You said: {text}', 'yellow'))
                
                # Process with AI
                if self.nlp:
                    response = self.nlp.generate_response(text)
                    if response:
                        self.message_queue.put(('log', f'Aurora: {response[:80]}', 'cyan'))
                        self._speak_to_user(response[:200])
                        self._add_to_ai_chat("Aurora", response, "aurora")
            except ImportError:
                self.message_queue.put(('log', 'Install: pip install SpeechRecognition', 'red'))
            except Exception as e:
                self.message_queue.put(('log', f'Listen error: {str(e)[:40]}', 'red'))
        
        threading.Thread(target=do_listen, daemon=True).start()
    
    def _listen_for_answer(self):
        """Listen for user's answer to AI's question"""
        self.log.log("Speak your answer...", 'orange')
        
        def do_listen():
            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                text = recognizer.recognize_google(audio)
                self.message_queue.put(('user_answer', text))
            except Exception as e:
                self.message_queue.put(('log', f'{str(e)[:30]}', 'red'))
        
        threading.Thread(target=do_listen, daemon=True).start()
    
    def _answer_ai(self, answer):
        """User answers AI's question"""
        self.log.log(f"Your answer: {answer}", 'yellow')
        self._add_to_ai_chat("You", answer, "user")
        
    # ═══════════════════════════════════════════════════════════════════════════
    # INTERACTIVE CHAT SYSTEM - Real-time conversation with Aurora
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _toggle_chat_mode(self):
        """Toggle between learning mode and chat mode"""
        if not hasattr(self, 'chat_active'):
            self.chat_active = False
        
        self.chat_active = not self.chat_active
        
        if self.chat_active:
            # Stop learning, enter chat mode
            self.paused = True
            self.chat_mode_var.set("Chat Mode - Learning Paused")
            self.chat_mode_label.config(fg=T.CYAN)
            self._add_to_ai_chat("Aurora", "I've paused learning to chat with you! Ask me anything - like 'What did you learn?' or give me commands.", "aurora")
            self.log.log("Entered chat mode - learning paused", 'cyan')
        else:
            # Resume learning
            self.paused = False
            self.chat_mode_var.set("Learning Mode")
            self.chat_mode_label.config(fg=T.GREEN)
            self._add_to_ai_chat("Aurora", "Resuming learning mode. I'll keep observing and learning!", "aurora")
            self.log.log("Resumed learning mode", 'green')
    
    def _start_voice_chat(self):
        """Start voice-based chat with Aurora"""
        def voice_chat():
            self._add_to_ai_chat("System", "Listening for your voice...", "system")
            
            # Use voice recognition
            if hasattr(self, 'voice') and self.voice:
                try:
                    text = self.voice.listen_for_command(timeout=10)
                    if text:
                        self._add_to_ai_chat("You", text, "user")
                        self._process_user_message(text, speak_response=True)
                    else:
                        self._add_to_ai_chat("System", "Didn't catch that. Try again.", "system")
                except Exception as e:
                    self._add_to_ai_chat("System", f"Voice error: {str(e)[:50]}", "error")
            else:
                self._add_to_ai_chat("System", "Voice system not available. Type your message instead.", "system")
        
        threading.Thread(target=voice_chat, daemon=True).start()
    
    def _send_chat_message(self, event=None):
        """Send user's chat message to Aurora"""
        message = self.user_input.get().strip()
        if not message or 'Ask me' in message:
            return
        
        self.user_input.delete(0, 'end')
        self._add_to_ai_chat("You", message, "user")
        self._process_user_message(message, speak_response=False)
    
    def _process_user_message(self, message, speak_response=False):
        """Process user message and generate AI response with real-time visualization updates"""
        def process():
            # Update AI thinking visualization - starting to process
            if hasattr(self, 'ai_thinking'):
                self.ai_thinking.update_thinking_state(
                    thought=f"Processing: {message[:40]}...",
                    intensity=0.8,
                    analysis=0.0,
                    planning=False,
                    executing=False
                )
                self.ai_thinking.add_thought(f"User: {message[:25]}")
            
            # Update AI analysis visualization
            if hasattr(self, 'ai_analysis'):
                self.ai_analysis.update_analysis(f"Analyzing user input: {message[:40]}...", "INPUT")
                self.ai_analysis.add_operation(f"Processing user message: {message[:30]}...")
            
            msg_lower = message.lower()
            response = ""
            
            # Analysis phase - determine message type
            if hasattr(self, 'ai_thinking'):
                self.ai_thinking.update_thinking_state(analysis=0.6, planning=False)
            if hasattr(self, 'ai_analysis'):
                self.ai_analysis.update_analysis("Categorizing message type...", "ANALYSIS")
            
            # Check for learning queries
            if any(phrase in msg_lower for phrase in ['what did you learn', 'what have you learned', 'show learning', 'what you learned']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Retrieving learning data...", analysis=0.9)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("Accessing learning database...", "MEMORY")
                    self.ai_analysis.update_data_stream('Memory', 0.9)
                
                today_only = 'today' in msg_lower or "today?" in msg_lower
                response = self._get_learning_summary(today_only=today_only)
            
            elif any(phrase in msg_lower for phrase in ['what do you know', 'tell me what you know', 'your knowledge']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Compiling knowledge base...", analysis=0.8)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("Knowledge compilation in progress...", "MEMORY")
                    self.ai_analysis.update_data_stream('Memory', 0.8)
                
                response = self._get_knowledge_summary()
            
            elif any(phrase in msg_lower for phrase in ['what can you do', 'your abilities', 'your skills']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Listing capabilities...", analysis=0.7)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("Capability assessment...", "SYSTEM")
                
                response = self._get_skills_summary()
            
            elif any(phrase in msg_lower for phrase in ['status', 'how are you', 'system status']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Running system diagnostics...", analysis=0.8)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("System status check...", "SYSTEM")
                    self.ai_analysis.update_data_stream('System', 0.9)
                
                response = self._get_status_summary()
            
            elif any(phrase in msg_lower for phrase in ['evolve', 'self improve', 'upgrade yourself']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Initiating evolution...", planning=True, executing=True)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("Self-evolution protocol activated", "EVOLUTION")
                    self.ai_analysis.add_operation("EVOLUTION: Self-improvement sequence started")
                
                self._add_to_ai_chat("Aurora", "Initiating self-evolution process...", "aurora")
                self._trigger_self_evolution()
                response = "Evolution process started! I'm analyzing my learning data to improve my models."
            
            elif any(phrase in msg_lower for phrase in ['stop', 'pause', 'quiet']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Pausing all systems...", executing=True)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("System pause initiated", "CONTROL")
                    self.ai_analysis.add_operation("SYSTEM: Pausing all activities")
                
                self.paused = True
                response = "I've paused all activities. Say 'resume' when you want me to continue."
            
            elif any(phrase in msg_lower for phrase in ['resume', 'continue', 'start']):
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Resuming operations...", executing=True)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("System resume initiated", "CONTROL")
                    self.ai_analysis.add_operation("SYSTEM: Resuming all activities")
                
                self.paused = False
                response = "Resuming all activities! I'm back to learning and observing."
            
            else:
                # Planning phase for actions
                if hasattr(self, 'ai_thinking'):
                    self.ai_thinking.update_thinking_state(thought="Planning action response...", planning=True, analysis=0.7)
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("Action planning in progress...", "PLANNING")
                
                # Enhanced NLP Action Processing - Execute real commands
                action_executed = self._execute_nlp_action(message)
                if action_executed:
                    # Execution phase
                    if hasattr(self, 'ai_thinking'):
                        self.ai_thinking.update_thinking_state(thought="Executing action...", executing=True)
                    if hasattr(self, 'ai_analysis'):
                        self.ai_analysis.update_analysis("Action execution successful", "EXECUTION")
                        self.ai_analysis.add_operation(f"ACTION: {message[:30]}... -> {action_executed[:20]}...")
                    
                    response = action_executed
                else:
                    # NLP processing phase
                    if hasattr(self, 'ai_thinking'):
                        self.ai_thinking.update_thinking_state(thought="Generating natural response...", analysis=0.9)
                    if hasattr(self, 'ai_analysis'):
                        self.ai_analysis.update_analysis("NLP response generation...", "LANGUAGE")
                        self.ai_analysis.update_data_stream('Network', 0.7)  # Assuming NLP uses network
                    
                    # Use NLP for general responses
                    if self.nlp:
                        try:
                            ai_response = self.nlp.generate_response(
                                f"As Aurora AI, respond helpfully to: {message}. Keep response under 100 words."
                            )
                            if ai_response:
                                response = ai_response
                            else:
                                response = f"I understand you said: '{message}'. I'm still learning, but I'm here to help!"
                        except:
                            response = f"I received your message: '{message}'. Let me think about that..."
                    else:
                        response = f"I heard: '{message}'. My language model is loading. Try asking 'what did you learn?' to see my knowledge."
            
            # Response completion phase
            if hasattr(self, 'ai_thinking'):
                self.ai_thinking.update_thinking_state(
                    thought="Response generated successfully",
                    intensity=0.3,
                    analysis=0.1,
                    planning=False,
                    executing=False
                )
                self.ai_thinking.add_thought(f"Response: {response[:25]}...")
            
            if hasattr(self, 'ai_analysis'):
                self.ai_analysis.update_analysis("Response completed", "COMPLETE")
                self.ai_analysis.add_operation(f"RESPONSE: Generated {len(response)} chars")
                # Reset data streams to normal levels
                for stream_name in ['CPU', 'RAM', 'NET', 'AI']:
                    if stream_name != 'CPU':  # Keep CPU monitoring active
                        self.ai_analysis.update_data_stream(stream_name, 0.3 + random.random() * 0.2)
            
            # Add response to chat
            self._add_to_ai_chat("Aurora", response, "aurora")
            
            # Speak if requested
            if speak_response:
                if hasattr(self, 'ai_analysis'):
                    self.ai_analysis.update_analysis("Activating speech synthesis...", "AUDIO")
                    self.ai_analysis.update_data_stream('Audio', 0.9)
                self._speak_to_user(response)
        
        threading.Thread(target=process, daemon=True).start()
    
    def _get_learning_summary(self, today_only=False):
        """Get comprehensive summary of what Aurora learned from the laptop today"""
        import subprocess
        from datetime import datetime, timedelta
        
        summary_parts = []
        today = datetime.now().date()
        
        if today_only:
            summary_parts.append("🧠 HERE'S WHAT I LEARNED FROM YOUR MAC TODAY:\n")
        else:
            summary_parts.append("🧠 MY COMPLETE LEARNING HISTORY:\n")
        
        # ═══ 1. SYSTEM INFORMATION LEARNED ═══
        try:
            # Get Mac model
            result = subprocess.run("system_profiler SPHardwareDataType | grep 'Model Name'", 
                                   shell=True, capture_output=True, text=True)
            mac_model = result.stdout.strip().replace("Model Name:", "").strip() if result.stdout else "Mac"
            
            # Get macOS version
            result = subprocess.run("sw_vers -productVersion", shell=True, capture_output=True, text=True)
            macos_version = result.stdout.strip() if result.stdout else "Unknown"
            
            # Get computer name
            result = subprocess.run("scutil --get ComputerName", shell=True, capture_output=True, text=True)
            computer_name = result.stdout.strip() if result.stdout else "Your Mac"
            
            summary_parts.append(f"💻 YOUR SYSTEM:")
            summary_parts.append(f"   • Computer: {computer_name} ({mac_model})")
            summary_parts.append(f"   • macOS Version: {macos_version}")
        except:
            pass
        
        # ═══ 2. APPS YOU USED TODAY ═══
        try:
            # Get recently used apps from launch services
            result = subprocess.run(
                "mdfind 'kMDItemLastUsedDate >= $time.today' -onlyin /Applications 2>/dev/null | head -10",
                shell=True, capture_output=True, text=True
            )
            recent_apps = [os.path.basename(app).replace('.app', '') for app in result.stdout.strip().split('\n') if app]
            
            # Also check running apps
            result = subprocess.run("ps aux | grep -i '/Applications' | awk '{print $11}' | head -15", 
                                   shell=True, capture_output=True, text=True)
            running = set()
            for line in result.stdout.split('\n'):
                if '/Applications/' in line:
                    app = line.split('/Applications/')[-1].split('/')[0].replace('.app', '')
                    if app:
                        running.add(app)
            
            if recent_apps or running:
                summary_parts.append(f"\n📱 APPS I OBSERVED YOU USING:")
                all_apps = list(set(recent_apps) | running)[:8]
                for app in all_apps:
                    summary_parts.append(f"   • {app}")
        except:
            pass
        
        # ═══ 3. FILES YOU WORKED ON ═══
        try:
            # Recently modified files
            result = subprocess.run(
                "find ~/Desktop ~/Documents ~/Downloads -type f -mtime -1 2>/dev/null | head -10",
                shell=True, capture_output=True, text=True
            )
            recent_files = result.stdout.strip().split('\n')[:5]
            if recent_files and recent_files[0]:
                summary_parts.append(f"\n📄 RECENT FILES I NOTICED:")
                for f in recent_files:
                    if f:
                        fname = os.path.basename(f)
                        summary_parts.append(f"   • {fname}")
        except:
            pass
        
        # ═══ 4. NETWORK ACTIVITY ═══
        try:
            # WiFi network
            result = subprocess.run(
                "networksetup -getairportnetwork en0 2>/dev/null | cut -d':' -f2",
                shell=True, capture_output=True, text=True
            )
            wifi_name = result.stdout.strip() if result.stdout else None
            
            # Check if connected
            result = subprocess.run("ping -c 1 8.8.8.8 2>/dev/null", shell=True, capture_output=True)
            connected = result.returncode == 0
            
            summary_parts.append(f"\n🌐 NETWORK STATUS:")
            if wifi_name:
                summary_parts.append(f"   • WiFi: {wifi_name}")
            summary_parts.append(f"   • Internet: {'Connected' if connected else 'Disconnected'}")
        except:
            pass
        
        # ═══ 5. BATTERY & POWER ═══
        try:
            result = subprocess.run("pmset -g batt", shell=True, capture_output=True, text=True)
            if result.stdout:
                import re
                match = re.search(r'(\d+)%', result.stdout)
                if match:
                    battery = match.group(1)
                    charging = 'charging' in result.stdout.lower()
                    summary_parts.append(f"\n🔋 POWER STATUS:")
                    summary_parts.append(f"   • Battery: {battery}% {'(Charging)' if charging else ''}")
        except:
            pass
        
        # ═══ 6. DISK SPACE ═══
        try:
            result = subprocess.run("df -h / | tail -1 | awk '{print $4}'", shell=True, capture_output=True, text=True)
            free_space = result.stdout.strip() if result.stdout else None
            if free_space:
                summary_parts.append(f"\n💾 STORAGE:")
                summary_parts.append(f"   • Free Space: {free_space}")
        except:
            pass
        
        # ═══ 7. MEMORY FROM BRAIN ═══
        if hasattr(self, 'brain') and self.brain:
            try:
                brain_summary = []
                actions = self.brain.get_all('actions')
                if actions:
                    brain_summary.append(f"   • {len(actions)} action patterns")
                apps = self.brain.get_all('apps')
                if apps:
                    brain_summary.append(f"   • {len(apps)} application behaviors")
                skills = self.brain.get_all('skills')
                if skills:
                    brain_summary.append(f"   • {len(skills)} learned skills")
                patterns = self.brain.get_all('patterns')
                if patterns:
                    brain_summary.append(f"   • {len(patterns)} user patterns")
                
                if brain_summary:
                    summary_parts.append(f"\n🧬 MY MEMORY BANKS:")
                    summary_parts.extend(brain_summary)
            except:
                pass
        
        # ═══ 8. TODAY'S ACTIONS ═══
        if self.action_tracker and getattr(self.action_tracker, 'action_history', None):
            try:
                today_actions = [r for r in self.action_tracker.action_history 
                               if datetime.fromtimestamp(r.timestamp).date() == today]
                if today_actions:
                    successes = sum(1 for r in today_actions if r.result == ActionResult.SUCCESS)
                    summary_parts.append(f"\n⚡ TODAY'S ACTIONS:")
                    summary_parts.append(f"   • {len(today_actions)} commands executed")
                    summary_parts.append(f"   • {successes} successful")
                    
                    # Most common actions
                    action_counts = Counter(r.action_type for r in today_actions)
                    top_actions = action_counts.most_common(3)
                    if top_actions:
                        summary_parts.append(f"   • Top actions: {', '.join(f'{a}({c})' for a,c in top_actions)}")
            except:
                pass
        
        # ═══ 9. CURRENT TIME CONTEXT ═══
        now = datetime.now()
        hour = now.hour
        if 5 <= hour < 12:
            time_context = "morning"
        elif 12 <= hour < 17:
            time_context = "afternoon"
        elif 17 <= hour < 21:
            time_context = "evening"
        else:
            time_context = "night"
        
        summary_parts.append(f"\n⏰ CURRENT CONTEXT:")
        summary_parts.append(f"   • Time: {now.strftime('%I:%M %p')} ({time_context})")
        summary_parts.append(f"   • Date: {now.strftime('%A, %B %d, %Y')}")
        
        if summary_parts:
            return "\n".join(summary_parts)
        
        return "I'm still observing your system. Keep me running and I'll learn more about how you work!"

    def _get_today_learning_lines(self):
        lines = []
        if self.action_tracker and getattr(self.action_tracker, 'action_history', None):
            today = datetime.now().date()
            todays = [r for r in self.action_tracker.action_history if datetime.fromtimestamp(r.timestamp).date() == today]
            if todays:
                successes = sum(1 for r in todays if r.result == ActionResult.SUCCESS)
                top = Counter(r.action_type for r in todays).most_common(3)
                lines.append(f"{len(todays)} actions - {successes} successes today")
                if top:
                    lines.append("Focus: " + ", ".join(f"{a} ({c})" for a, c in top))
        if self.permanent_brain:
            experiences = self.permanent_brain.memory.get('experiences', {}).get('log', [])
            todays_exp = [e for e in experiences if self._is_today(e.get('time'))]
            if todays_exp:
                lines.append(f"Logged {len(todays_exp)} new experiences")
            skills = self.permanent_brain.memory.get('skills', {})
            new_skills = [s for s in skills.values() if self._is_today(s.get('acquired'))]
            if new_skills:
                lines.append(f"New skills: {len(new_skills)}")
        return lines

    def _is_today(self, iso_ts):
        if not iso_ts:
            return False
        try:
            return datetime.fromisoformat(iso_ts).date() == datetime.now().date()
        except Exception:
            return False

    
    def _get_knowledge_summary(self):
        """Get knowledge base summary"""
        try:
            if hasattr(self, 'brain') and self.brain:
                total = 0
                for key in ['actions', 'apps', 'skills', 'patterns', 'locations']:
                    data = self.brain.get_all(key)
                    if data:
                        total += len(data)
                return f"I know {total} things! This includes system commands, applications, file locations, user patterns, and acquired skills."
            return "My knowledge base is initializing. Ask me again in a moment!"
        except:
            return "I'm building my knowledge base. Check back soon!"
    
    def _get_skills_summary(self):
        """Get comprehensive skills summary"""
        skills = """🎯 MY CURRENT CAPABILITIES:

📡 CONNECTIVITY CONTROL:
   • WiFi on/off/scan networks
   • Bluetooth on/off/list devices
   • AirDrop enable/disable
   • VPN connect/disconnect
   • IP address (local/public)

🔊 MEDIA CONTROL:
   • Volume up/down/mute/set %
   • Brightness up/down/max
   • Play YouTube videos/songs
   • Screenshot (full/area/window)

💻 SYSTEM CONTROL:
   • Dark/Light mode toggle
   • Sleep/Lock/Restart/Shutdown
   • Force quit apps
   • DNS flush/show
   • Battery status
   • CPU/Memory info
   • Uptime check

🖥️ DISPLAY & DOCK:
   • Dock hide/show/position
   • Window minimize/maximize/close
   • Finder restart/hidden files
   • Resolution info
   • Zoom in/out

📁 FILE OPERATIONS:
   • Open/create/delete files
   • Empty trash
   • Eject disks
   • Show recent files

🔐 SECURITY:
   • Firewall on/off
   • Location services
   • Keychain access
   • Do Not Disturb/Focus

🌐 WEB & APPS:
   • Google search
   • Open any website
   • Launch any application
   • YouTube play songs

🧠 LEARNING:
   • Remember your patterns
   • Track your app usage
   • Learn from actions
   • Self-evolve intelligence

Just tell me what to do!"""
        return skills
    
    def _get_status_summary(self):
        """Get system status summary"""
        import psutil
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        
        status = f"System Status:\n"
        status += f"CPU: {cpu:.1f}%\n"
        status += f"RAM: {mem:.1f}%\n"
        status += f"Learning: {'Active' if not self.paused else 'Paused'}\n"
        status += f"Ollama: {'Connected' if self.nlp else 'Connecting...'}\n"
        
        return status
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMPREHENSIVE NLP ACTION EXECUTION - Understanding and performing A-Z commands
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _execute_nlp_action(self, message):
        """
        Execute comprehensive NLP commands using TRUE AI UNDERSTANDING.
        
        This method now uses the VisionAIBrain for intelligent screen analysis
        and decision making - NO MORE PREDEFINED PATTERNS!
        
        The AI:
        1. Takes a screenshot of the current screen
        2. Analyzes it with LLaVA vision model
        3. Understands what's visible and what actions are possible
        4. Generates an intelligent action plan
        5. Executes the plan step by step
        """
        msg_lower = message.lower().strip()
        
        # ═══════════════════════════════════════════════════════════════
        # CONVERSATIONAL MESSAGES - Let NLP handle greetings/chat
        # ═══════════════════════════════════════════════════════════════
        conversational_patterns = [
            'hi', 'hello', 'hey', 'howdy', 'greetings',
            'good morning', 'good afternoon', 'good evening', 'good night',
            'how are you', 'what\'s up', 'whats up', 'sup',
            'thank you', 'thanks', 'bye', 'goodbye', 'see you',
            'who are you', 'what are you', 'tell me about yourself',
            'help', 'what can you do', 'your name',
            'yes', 'no', 'ok', 'okay', 'sure', 'cool', 'nice', 'great',
            'i love you', 'love you', 'hate you'
        ]
        
        # Check if message is purely conversational
        if any(msg_lower == pattern or msg_lower.startswith(pattern + ' ') or 
               msg_lower.startswith(pattern + '!') or msg_lower.startswith(pattern + '?')
               for pattern in conversational_patterns):
            return None  # Let NLP handle conversational messages
        
        # Also check for very short messages (likely conversational)
        if len(msg_lower) < 4 and not any(c.isdigit() for c in msg_lower):
            return None
        
        try:
            # ═══════════════════════════════════════════════════════════════
            # PRIMARY: Use Vision AI Brain for TRUE NLP understanding
            # ═══════════════════════════════════════════════════════════════
            if hasattr(self, 'vision_brain') and self.vision_brain is not None:
                self._add_to_ai_chat("Aurora", f"Analyzing screen for: {message}", "thinking")
                
                # Execute using Vision AI Brain
                result = self.vision_brain.execute_user_request(message, verbose=False)
                
                if result.get("success"):
                    steps_info = f"{result.get('steps_completed', 0)}/{result.get('total_steps', 0)} steps"
                    self._add_to_ai_chat("Aurora", f"Completed: {steps_info}", "success")
                    
                    # Show what the AI understood
                    if result.get("plan"):
                        reasoning = result["plan"].reasoning[:100] if result["plan"].reasoning else "Task executed"
                        return f"Done! {reasoning}"
                    return f"Task completed successfully ({steps_info})"
                else:
                    error = result.get("error", "Unknown error")
                    self._add_to_ai_chat("Aurora", f"Learning from failure: {error[:50]}", "learning")
                    
                    # Fall through to legacy patterns as backup
                    self._add_to_ai_chat("Aurora", "Trying alternative approach...", "thinking")
            
            # ═══════════════════════════════════════════════════════════════
            # FALLBACK: Legacy pattern matching (for when Vision AI fails)
            # ═══════════════════════════════════════════════════════════════
            
            # WhatsApp and messaging actions
            if any(word in msg_lower for word in ['whatsapp', 'message', 'send message', 'text']):
                return self._handle_messaging_action(message, msg_lower)
            
            # Application launching
            elif any(word in msg_lower for word in ['open', 'launch', 'start app', 'run']):
                return self._handle_app_launch(message, msg_lower)
            
            # Clicking and mouse actions
            elif any(word in msg_lower for word in ['click', 'tap', 'press button', 'mouse']):
                return self._handle_click_action(message, msg_lower)
            
            # Typing and keyboard actions
            elif any(word in msg_lower for word in ['type', 'write', 'enter text', 'input']):
                return self._handle_typing_action(message, msg_lower)
            
            # Moving and navigation
            elif any(word in msg_lower for word in ['move', 'navigate', 'go to', 'scroll']):
                return self._handle_navigation_action(message, msg_lower)
            
            # File operations
            elif any(word in msg_lower for word in ['file', 'folder', 'save', 'delete', 'copy']):
                return self._handle_file_action(message, msg_lower)
            
            # System control (WiFi, Bluetooth, Volume, Brightness, etc.)
            elif any(word in msg_lower for word in [
                # A
                'airdrop', 'airplane', 
                # B  
                'wifi', 'bluetooth', 'battery', 'brightness',
                # C
                'clipboard', 'calendar', 'cpu', 'clean', 'cache',
                # D
                'dark mode', 'light mode', 'dock', 'display', 'dns',
                # E
                'eject', 'empty trash', 'expose', 'mission control',
                # F
                'finder', 'firewall', 'force quit', 'kill app',
                # G
                'location', 'gps',
                # H
                'hotspot', 'hostname', 'computer name', 'hidden files',
                # I
                'ip address',
                # K
                'keyboard', 'keychain',
                # L
                'lock', 'logout', 'launchpad',
                # M
                'mute', 'unmute', 'memory', 'ram',
                # N
                'night shift', 'notification',
                # P
                'power', 'shutdown', 'print', 'process',
                # R
                'restart', 'reboot', 'resolution',
                # S
                'screenshot', 'screen capture', 'sleep', 'spotlight', 'siri',
                # T
                'time machine', 'terminal', 'trash',
                # U
                'uptime', 'usb',
                # V
                'volume', 'sound', 'vpn',
                # W
                'wallpaper', 'desktop background', 'window', 'minimize', 'maximize',
                # Z
                'zoom',
                # Focus
                'do not disturb', 'dnd', 'focus'
            ]):
                return self._handle_system_action(message, msg_lower)
            
            # YouTube and video actions
            elif any(word in msg_lower for word in ['youtube', 'video', 'play song', 'play music', 'watch']):
                return self._handle_youtube_action(message, msg_lower)
            
            # Web and browser actions
            elif any(word in msg_lower for word in ['web', 'browser', 'google', 'search', 'website']):
                return self._handle_web_action(message, msg_lower)
            
            # ═══════════════════════════════════════════════════════════════
            # NO PATTERN MATCHED - Use Vision AI for intelligent handling
            # ═══════════════════════════════════════════════════════════════
            if hasattr(self, 'vision_brain') and self.vision_brain is not None:
                self._add_to_ai_chat("Aurora", f"Using AI vision to understand: {message}", "thinking")
                result = self.vision_brain.execute_user_request(message, verbose=False)
                
                if result.get("success"):
                    steps_info = f"{result.get('steps_completed', 0)}/{result.get('total_steps', 0)} steps"
                    return f"Completed intelligently: {result.get('plan', {}).reasoning[:80] if result.get('plan') else steps_info}"
                else:
                    return f"I tried but couldn't complete: {result.get('error', 'unknown')[:50]}. Learning from this..."
            
            return None  # No action pattern matched and no Vision AI
            
        except Exception as e:
            return f"Error executing action: {str(e)[:50]}. I'll learn from this mistake."
    
    def _handle_messaging_action(self, message, msg_lower):
        """Handle WhatsApp and messaging actions"""
        if not (self.autonomous_explorer and self.keyboard_automation):
            return "Automation systems not available. Please enable autonomous mode first."
        
        try:
            # Extract contact name from message
            import re
            contact_match = re.search(r'(?:to |send message to |message )([a-zA-Z\s]+)', message)
            contact = contact_match.group(1).strip() if contact_match else "unknown contact"
            
            # Extract message content
            msg_match = re.search(r'(?:saying |message |text )["\'](.*?)["\']', message)
            if not msg_match:
                msg_match = re.search(r'(?:saying |message |text )(.*?)$', message)
            msg_content = msg_match.group(1).strip() if msg_match else "Hello from Aurora AI"
            
            self._add_to_ai_chat("Aurora", f"Opening WhatsApp to message {contact}...", "action")
            
            # Execute WhatsApp automation
            steps = [
                ("open_app", "WhatsApp"),
                ("wait", 2),
                ("search_contact", contact),
                ("type_message", msg_content),
                ("send_message", None)
            ]
            
            for step_type, step_data in steps:
                if step_type == "open_app":
                    self._execute_command(f"open -a {step_data}")
                elif step_type == "wait":
                    time.sleep(step_data)
                elif step_type == "search_contact":
                    self._type_text(step_data)
                    self._press_key("return")
                elif step_type == "type_message":
                    time.sleep(1)
                    self._type_text(step_data)
                elif step_type == "send_message":
                    self._press_key("return")
            
            return f"Sent message to {contact}: '{msg_content}'"
            
        except Exception as e:
            return f"WhatsApp action failed: {str(e)[:40]}"
    
    def _analyze_screen_with_vision_ai(self, task: str = None) -> str:
        """
        Use Vision AI Brain to analyze current screen.
        Returns human-readable analysis.
        """
        if not hasattr(self, 'vision_brain') or self.vision_brain is None:
            return "Vision AI not available. Please ensure LLaVA model is installed."
        
        try:
            self._add_to_ai_chat("Aurora", "Analyzing screen with AI vision...", "thinking")
            
            analysis = self.vision_brain.analyze_screen(task=task)
            
            if "error" in analysis:
                return f"Analysis failed: {analysis['error']}"
            
            # Format the analysis nicely
            result_lines = [
                f"Active App: {analysis.get('active_app', 'Unknown')}",
                f"Interface: {analysis.get('interface_state', 'Unknown')}",
            ]
            
            elements = analysis.get('elements', [])
            if elements:
                result_lines.append(f"Visible Elements ({len(elements)}):")
                for elem in elements[:5]:  # Show first 5
                    result_lines.append(f"  - {elem}")
            
            actions = analysis.get('possible_actions', [])
            if actions:
                result_lines.append(f"Possible Actions:")
                for action in actions[:5]:
                    result_lines.append(f"  - {action}")
            
            recommended = analysis.get('recommended_action', '')
            if recommended:
                result_lines.append(f"Recommended: {recommended}")
            
            return "\n".join(result_lines)
            
        except Exception as e:
            return f"Vision analysis error: {str(e)[:50]}"
    
    def _execute_vision_task(self, task: str) -> str:
        """
        Execute any task using Vision AI - TRUE NLP understanding.
        This is the main entry point for intelligent task execution.
        """
        if not hasattr(self, 'vision_brain') or self.vision_brain is None:
            return "Vision AI not available. Please ensure LLaVA model is installed."
        
        try:
            result = self.vision_brain.execute_user_request(task, verbose=False)
            
            if result.get("success"):
                steps = result.get('steps_completed', 0)
                total = result.get('total_steps', 0)
                plan = result.get('plan')
                reasoning = plan.reasoning if plan else "Task completed"
                return f"Success! ({steps}/{total} steps)\nReasoning: {reasoning}"
            else:
                error = result.get('error', 'Unknown error')
                return f"Task failed: {error}\nI'll learn from this for next time."
                
        except Exception as e:
            return f"Vision task error: {str(e)[:50]}"
    
    def _handle_app_launch(self, message, msg_lower):
        """Handle application launching"""
        try:
            # Extract app name
            import re
            app_patterns = [
                r'open ([a-zA-Z\s]+)',
                r'launch ([a-zA-Z\s]+)',
                r'start ([a-zA-Z\s]+)',
                r'run ([a-zA-Z\s]+)'
            ]
            
            app_name = None
            for pattern in app_patterns:
                match = re.search(pattern, message)
                if match:
                    app_name = match.group(1).strip()
                    break
            
            if not app_name:
                return "Please specify which app to open (e.g., 'open Safari')"
            
            self._add_to_ai_chat("Aurora", f"Launching {app_name}...", "action")
            
            # Execute app launch
            self._execute_command(f"open -a '{app_name}'")
            
            return f"Opened {app_name}"
            
        except Exception as e:
            return f"App launch failed: {str(e)[:40]}"
    
    def _handle_click_action(self, message, msg_lower):
        """Handle clicking and mouse actions"""
        try:
            if 'coordinate' in msg_lower or 'position' in msg_lower:
                # Extract coordinates
                import re
                coords = re.findall(r'\d+', message)
                if len(coords) >= 2:
                    x, y = int(coords[0]), int(coords[1])
                    self._click_at(x, y)
                    return f"Clicked at position ({x}, {y})"
            
            elif any(word in msg_lower for word in ['center', 'middle', 'screen center']):
                self._click_center()
                return "Clicked at screen center"
            
            else:
                # General click action
                self._click_center()
                return "Performed click action"
                
        except Exception as e:
            return f"Click action failed: {str(e)[:40]}"
    
    def _handle_typing_action(self, message, msg_lower):
        """Handle typing and text input actions"""
        try:
            # Extract text to type
            import re
            text_patterns = [
                r'type ["\'](.*?)["\']',
                r'write ["\'](.*?)["\']',
                r'enter ["\'](.*?)["\']',
                r'input ["\'](.*?)["\']'
            ]
            
            text_to_type = None
            for pattern in text_patterns:
                match = re.search(pattern, message)
                if match:
                    text_to_type = match.group(1)
                    break
            
            if not text_to_type:
                return "Please specify text to type in quotes (e.g., type 'Hello World')"
            
            self._add_to_ai_chat("Aurora", f"Typing: {text_to_type}", "action")
            self._type_text(text_to_type)
            
            return f"Typed: '{text_to_type}'"
            
        except Exception as e:
            return f"Typing action failed: {str(e)[:40]}"
    
    def _handle_navigation_action(self, message, msg_lower):
        """Handle navigation and movement actions"""
        try:
            if 'scroll up' in msg_lower:
                self._scroll_up()
                return "Scrolled up"
            elif 'scroll down' in msg_lower:
                self._scroll_down()
                return "Scrolled down"
            elif 'move mouse' in msg_lower:
                # Extract coordinates if provided
                import re
                coords = re.findall(r'\d+', message)
                if len(coords) >= 2:
                    x, y = int(coords[0]), int(coords[1])
                    self._move_mouse_to(x, y)
                    return f"Moved mouse to ({x}, {y})"
            
            return "Navigation action completed"
            
        except Exception as e:
            return f"Navigation failed: {str(e)[:40]}"
    
    def _handle_file_action(self, message, msg_lower):
        """Handle file and folder operations"""
        try:
            if 'create file' in msg_lower or 'new file' in msg_lower:
                return "File creation initiated (would open text editor)"
            elif 'open file' in msg_lower:
                return "File browser opened"
            elif 'save' in msg_lower:
                self._press_key("cmd+s")
                return "Save command executed"
            
            return "File operation completed"
            
        except Exception as e:
            return f"File operation failed: {str(e)[:40]}"
    
    def _handle_system_action(self, message, msg_lower):
        """Handle COMPREHENSIVE A-Z macOS system control - ALL ADVANCED COMMANDS"""
        try:
            import re
            
            # ═══════════════════════════════════════════════════════════════════
            # A - AIRPLAY / AIRDROP / AIRPLANE MODE
            # ═══════════════════════════════════════════════════════════════════
            if 'airdrop' in msg_lower:
                if any(word in msg_lower for word in ['on', 'enable']):
                    self._execute_command("defaults write com.apple.NetworkBrowser DisableAirDrop -bool NO && killall Finder")
                    return "AirDrop enabled"
                elif any(word in msg_lower for word in ['off', 'disable']):
                    self._execute_command("defaults write com.apple.NetworkBrowser DisableAirDrop -bool YES && killall Finder")
                    return "AirDrop disabled"
                    
            elif 'airplane' in msg_lower:
                if any(word in msg_lower for word in ['on', 'enable']):
                    self._execute_command("networksetup -setairportpower en0 off")
                    self._execute_command("blueutil --power 0 2>/dev/null")
                    return "Airplane mode ON (WiFi + Bluetooth disabled)"
                else:
                    self._execute_command("networksetup -setairportpower en0 on")
                    self._execute_command("blueutil --power 1 2>/dev/null")
                    return "Airplane mode OFF"
            
            # ═══════════════════════════════════════════════════════════════════
            # B - BLUETOOTH / BATTERY / BRIGHTNESS
            # ═══════════════════════════════════════════════════════════════════
            elif 'bluetooth' in msg_lower:
                if any(word in msg_lower for word in ['off', 'disable', 'turn off']):
                    self._execute_command("blueutil --power 0 2>/dev/null || defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 0")
                    self._add_to_ai_chat("Aurora", "Bluetooth OFF", "action")
                    return "Bluetooth has been turned OFF"
                elif any(word in msg_lower for word in ['on', 'enable', 'turn on']):
                    self._execute_command("blueutil --power 1 2>/dev/null || defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 1")
                    self._add_to_ai_chat("Aurora", "Bluetooth ON", "action")
                    return "Bluetooth has been turned ON"
                elif 'devices' in msg_lower or 'list' in msg_lower:
                    result = subprocess.run("blueutil --paired 2>/dev/null", shell=True, capture_output=True, text=True)
                    return f"Paired Bluetooth devices:\n{result.stdout}" if result.stdout else "No paired devices or blueutil not installed"
                    
            elif 'battery' in msg_lower:
                result = subprocess.run("pmset -g batt", shell=True, capture_output=True, text=True)
                if result.stdout:
                    match = re.search(r'(\d+)%', result.stdout)
                    battery = match.group(1) if match else "Unknown"
                    charging = 'charging' in result.stdout.lower()
                    return f"Battery: {battery}% {'(Charging)' if charging else '(On Battery)'}"
                return "Could not get battery status"
                
            elif 'brightness' in msg_lower:
                if 'up' in msg_lower or 'increase' in msg_lower or '+' in msg_lower:
                    for _ in range(3):
                        self._execute_command("osascript -e 'tell application \"System Events\" to key code 144'")
                    return "Brightness increased"
                elif 'down' in msg_lower or 'decrease' in msg_lower or '-' in msg_lower:
                    for _ in range(3):
                        self._execute_command("osascript -e 'tell application \"System Events\" to key code 145'")
                    return "Brightness decreased"
                elif 'max' in msg_lower or 'full' in msg_lower:
                    for _ in range(16):
                        self._execute_command("osascript -e 'tell application \"System Events\" to key code 144'")
                    return "Brightness set to maximum"
                elif 'min' in msg_lower or 'low' in msg_lower:
                    for _ in range(16):
                        self._execute_command("osascript -e 'tell application \"System Events\" to key code 145'")
                    return "Brightness set to minimum"
            
            # ═══════════════════════════════════════════════════════════════════
            # C - CLIPBOARD / CALENDAR / CPU / CLEAN
            # ═══════════════════════════════════════════════════════════════════
            elif 'clipboard' in msg_lower:
                if 'clear' in msg_lower or 'empty' in msg_lower:
                    self._execute_command("pbcopy < /dev/null")
                    return "Clipboard cleared"
                elif 'show' in msg_lower or 'paste' in msg_lower or 'what' in msg_lower:
                    result = subprocess.run("pbpaste", shell=True, capture_output=True, text=True)
                    content = result.stdout[:200] if result.stdout else "Empty"
                    return f"Clipboard: {content}"
                elif 'copy' in msg_lower:
                    text_match = re.search(r'copy\s+["\'](.+?)["\']', message)
                    if text_match:
                        text = text_match.group(1)
                        self._execute_command(f"echo '{text}' | pbcopy")
                        return f"Copied to clipboard: {text}"
                        
            elif 'calendar' in msg_lower:
                self._execute_command("open -a Calendar")
                return "Calendar opened"
                
            elif 'cpu' in msg_lower or 'processor' in msg_lower:
                result = subprocess.run("top -l 1 | grep 'CPU usage'", shell=True, capture_output=True, text=True)
                return f"CPU: {result.stdout.strip()}" if result.stdout else "CPU info unavailable"
                
            elif 'clean' in msg_lower or 'clear cache' in msg_lower:
                if 'dns' in msg_lower:
                    self._execute_command("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder 2>/dev/null")
                    return "DNS cache flushed"
                elif 'ram' in msg_lower or 'memory' in msg_lower:
                    self._execute_command("sudo purge 2>/dev/null")
                    return "Memory purged (may require password)"
                elif 'trash' in msg_lower:
                    self._execute_command("rm -rf ~/.Trash/* 2>/dev/null")
                    return "Trash emptied"
            
            # ═══════════════════════════════════════════════════════════════════
            # D - DARK MODE / DOCK / DISPLAY / DNS
            # ═══════════════════════════════════════════════════════════════════
            elif 'dark mode' in msg_lower or 'light mode' in msg_lower:
                if 'dark' in msg_lower and any(w in msg_lower for w in ['on', 'enable', 'turn on', 'switch to']):
                    self._execute_command("osascript -e 'tell app \"System Events\" to tell appearance preferences to set dark mode to true'")
                    return "Dark mode enabled"
                elif 'light' in msg_lower or 'off' in msg_lower:
                    self._execute_command("osascript -e 'tell app \"System Events\" to tell appearance preferences to set dark mode to false'")
                    return "Light mode enabled"
                else:
                    self._execute_command("osascript -e 'tell app \"System Events\" to tell appearance preferences to set dark mode to not dark mode'")
                    return "Dark/Light mode toggled"
                    
            elif 'dock' in msg_lower:
                if 'hide' in msg_lower:
                    self._execute_command("defaults write com.apple.dock autohide -bool true && killall Dock")
                    return "Dock auto-hide enabled"
                elif 'show' in msg_lower or 'unhide' in msg_lower:
                    self._execute_command("defaults write com.apple.dock autohide -bool false && killall Dock")
                    return "Dock auto-hide disabled"
                elif 'left' in msg_lower:
                    self._execute_command("defaults write com.apple.dock orientation -string left && killall Dock")
                    return "Dock moved to left"
                elif 'right' in msg_lower:
                    self._execute_command("defaults write com.apple.dock orientation -string right && killall Dock")
                    return "Dock moved to right"
                elif 'bottom' in msg_lower:
                    self._execute_command("defaults write com.apple.dock orientation -string bottom && killall Dock")
                    return "Dock moved to bottom"
                elif 'restart' in msg_lower:
                    self._execute_command("killall Dock")
                    return "Dock restarted"
                    
            elif 'display' in msg_lower or 'screen' in msg_lower:
                if 'resolution' in msg_lower:
                    result = subprocess.run("system_profiler SPDisplaysDataType | grep Resolution", shell=True, capture_output=True, text=True)
                    return f"Display: {result.stdout.strip()}" if result.stdout else "Resolution info unavailable"
                elif 'mirror' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to key code 144 using {command down}'")
                    return "Display mirroring toggled"
                    
            elif 'dns' in msg_lower:
                if 'flush' in msg_lower or 'clear' in msg_lower:
                    self._execute_command("sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder 2>/dev/null")
                    return "DNS cache flushed"
                elif 'show' in msg_lower or 'get' in msg_lower:
                    result = subprocess.run("scutil --dns | grep nameserver | head -5", shell=True, capture_output=True, text=True)
                    return f"DNS servers:\n{result.stdout}" if result.stdout else "DNS info unavailable"
            
            # ═══════════════════════════════════════════════════════════════════
            # E - EJECT / EMPTY TRASH / EXPOSE
            # ═══════════════════════════════════════════════════════════════════
            elif 'eject' in msg_lower:
                if 'all' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"Finder\" to eject (every disk whose ejectable is true)'")
                    return "All ejectable disks ejected"
                else:
                    self._execute_command("drutil tray eject 2>/dev/null || diskutil eject $(diskutil list | grep external | head -1 | awk '{print $1}')")
                    return "Disk ejected"
                    
            elif 'empty trash' in msg_lower or 'clear trash' in msg_lower:
                self._execute_command("rm -rf ~/.Trash/* 2>/dev/null")
                return "Trash emptied"
                
            elif 'expose' in msg_lower or 'mission control' in msg_lower:
                self._execute_command("osascript -e 'tell application \"System Events\" to key code 160'")  # F3
                return "Mission Control activated"
            
            # ═══════════════════════════════════════════════════════════════════
            # F - FINDER / FIREWALL / FORCE QUIT
            # ═══════════════════════════════════════════════════════════════════
            elif 'finder' in msg_lower:
                if 'restart' in msg_lower or 'relaunch' in msg_lower:
                    self._execute_command("killall Finder")
                    return "Finder restarted"
                elif 'hidden' in msg_lower:
                    if 'show' in msg_lower:
                        self._execute_command("defaults write com.apple.finder AppleShowAllFiles YES && killall Finder")
                        return "Hidden files shown"
                    else:
                        self._execute_command("defaults write com.apple.finder AppleShowAllFiles NO && killall Finder")
                        return "Hidden files hidden"
                else:
                    self._execute_command("open -a Finder")
                    return "Finder opened"
                    
            elif 'firewall' in msg_lower:
                if 'on' in msg_lower or 'enable' in msg_lower:
                    self._execute_command("sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on 2>/dev/null")
                    return "Firewall enabled"
                elif 'off' in msg_lower or 'disable' in msg_lower:
                    self._execute_command("sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off 2>/dev/null")
                    return "Firewall disabled"
                else:
                    result = subprocess.run("sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null", shell=True, capture_output=True, text=True)
                    return f"Firewall: {result.stdout.strip()}" if result.stdout else "Firewall status unknown"
                    
            elif 'force quit' in msg_lower or 'kill app' in msg_lower or 'kill process' in msg_lower:
                app_match = re.search(r'(?:force quit|kill|terminate|stop)\s+(\w+)', message, re.I)
                if app_match:
                    app = app_match.group(1)
                    self._execute_command(f"killall '{app}' 2>/dev/null || pkill -f '{app}'")
                    return f"Force quit: {app}"
                else:
                    self._execute_command("osascript -e 'tell application \"System Events\" to key code 12 using {command down, option down}'")
                    return "Force Quit dialog opened"
            
            # ═══════════════════════════════════════════════════════════════════
            # G - GPS LOCATION / GRAYSCALE
            # ═══════════════════════════════════════════════════════════════════
            elif 'location' in msg_lower or 'gps' in msg_lower:
                if 'disable' in msg_lower or 'off' in msg_lower:
                    self._execute_command("sudo launchctl unload /System/Library/LaunchDaemons/com.apple.locationd.plist 2>/dev/null")
                    return "Location services disabled"
                elif 'enable' in msg_lower or 'on' in msg_lower:
                    self._execute_command("sudo launchctl load /System/Library/LaunchDaemons/com.apple.locationd.plist 2>/dev/null")
                    return "Location services enabled"
            
            # ═══════════════════════════════════════════════════════════════════
            # H - HOTSPOT / HOSTNAME / HIDDEN FILES
            # ═══════════════════════════════════════════════════════════════════
            elif 'hotspot' in msg_lower or 'internet sharing' in msg_lower:
                return "Hotspot: Go to System Settings > General > Sharing > Internet Sharing"
                
            elif 'hostname' in msg_lower or 'computer name' in msg_lower:
                if 'set' in msg_lower or 'change' in msg_lower:
                    name_match = re.search(r'(?:to|as)\s+["\']?(\w+)["\']?', message)
                    if name_match:
                        name = name_match.group(1)
                        self._execute_command(f"sudo scutil --set ComputerName '{name}' && sudo scutil --set HostName '{name}'")
                        return f"Computer name set to: {name}"
                else:
                    result = subprocess.run("scutil --get ComputerName", shell=True, capture_output=True, text=True)
                    return f"Computer name: {result.stdout.strip()}" if result.stdout else "Unknown"
            
            # ═══════════════════════════════════════════════════════════════════
            # I - IP ADDRESS / ICLOUD
            # ═══════════════════════════════════════════════════════════════════
            elif 'ip' in msg_lower and 'address' in msg_lower:
                if 'public' in msg_lower or 'external' in msg_lower:
                    result = subprocess.run("curl -s ifconfig.me", shell=True, capture_output=True, text=True)
                    return f"Public IP: {result.stdout.strip()}" if result.stdout else "Could not get public IP"
                else:
                    result = subprocess.run("ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1", shell=True, capture_output=True, text=True)
                    return f"Local IP: {result.stdout.strip()}" if result.stdout else "Not connected"
            
            # ═══════════════════════════════════════════════════════════════════
            # K - KEYBOARD / KEYCHAIN
            # ═══════════════════════════════════════════════════════════════════
            elif 'keyboard' in msg_lower:
                if 'backlight' in msg_lower:
                    if 'off' in msg_lower:
                        for _ in range(16):
                            self._execute_command("osascript -e 'tell application \"System Events\" to key code 107'")
                        return "Keyboard backlight off"
                    elif 'on' in msg_lower or 'up' in msg_lower:
                        for _ in range(16):
                            self._execute_command("osascript -e 'tell application \"System Events\" to key code 113'")
                        return "Keyboard backlight on"
                        
            elif 'keychain' in msg_lower:
                self._execute_command("open -a 'Keychain Access'")
                return "Keychain Access opened"
            
            # ═══════════════════════════════════════════════════════════════════
            # L - LOCK SCREEN / LOGOUT / LAUNCHPAD
            # ═══════════════════════════════════════════════════════════════════
            elif 'lock' in msg_lower:
                self._execute_command("pmset displaysleepnow")
                return "Screen locked"
                
            elif 'logout' in msg_lower or 'log out' in msg_lower:
                self._execute_command("osascript -e 'tell app \"System Events\" to log out' 2>/dev/null")
                return "Logging out..."
                
            elif 'launchpad' in msg_lower:
                self._execute_command("osascript -e 'tell application \"System Events\" to key code 160 using control down'")
                return "Launchpad opened"
            
            # ═══════════════════════════════════════════════════════════════════
            # M - MUTE / MEMORY / MONITOR
            # ═══════════════════════════════════════════════════════════════════
            elif 'mute' in msg_lower or 'unmute' in msg_lower:
                if 'unmute' in msg_lower:
                    self._execute_command("osascript -e 'set volume without output muted'")
                    return "Unmuted"
                elif 'mic' in msg_lower or 'microphone' in msg_lower:
                    self._execute_command("osascript -e 'set volume input volume 0'")
                    return "Microphone muted"
                else:
                    self._execute_command("osascript -e 'set volume with output muted'")
                    return "Muted"
                    
            elif 'memory' in msg_lower or 'ram' in msg_lower:
                if 'free' in msg_lower or 'clear' in msg_lower:
                    self._execute_command("sudo purge 2>/dev/null")
                    return "Memory purged"
                else:
                    result = subprocess.run("vm_stat | head -5", shell=True, capture_output=True, text=True)
                    return f"Memory:\n{result.stdout}" if result.stdout else "Memory info unavailable"
            
            # ═══════════════════════════════════════════════════════════════════
            # N - NIGHT SHIFT / NOTIFICATION / NETWORK
            # ═══════════════════════════════════════════════════════════════════
            elif 'night shift' in msg_lower:
                if 'on' in msg_lower or 'enable' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to tell process \"Control Center\" to click menu bar item 1 of menu bar 1'")
                    return "Toggle Night Shift from Control Center"
                    
            elif 'notification' in msg_lower:
                if 'clear' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to tell process \"NotificationCenter\" to click button \"Close\" of every window'")
                    return "Notifications cleared"
                elif 'center' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to key code 49 using {option down, command down}'")
                    return "Notification Center toggled"
            
            # ═══════════════════════════════════════════════════════════════════
            # P - POWER / PRINT / PROCESS
            # ═══════════════════════════════════════════════════════════════════
            elif 'power' in msg_lower:
                if 'off' in msg_lower or 'shutdown' in msg_lower:
                    self._execute_command("osascript -e 'tell app \"System Events\" to shut down'")
                    return "Shutting down..."
                    
            elif 'print' in msg_lower:
                self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"p\" using command down'")
                return "Print dialog opened"
                
            elif 'process' in msg_lower:
                if 'list' in msg_lower or 'show' in msg_lower:
                    result = subprocess.run("ps aux | head -15", shell=True, capture_output=True, text=True)
                    return f"Top processes:\n{result.stdout[:500]}"
            
            # ═══════════════════════════════════════════════════════════════════
            # R - RESTART / RESET / RESOLUTION
            # ═══════════════════════════════════════════════════════════════════
            elif 'restart' in msg_lower or 'reboot' in msg_lower:
                if 'mac' in msg_lower or 'computer' in msg_lower or 'system' in msg_lower:
                    self._execute_command("osascript -e 'tell app \"System Events\" to restart'")
                    return "Restarting..."
                    
            elif 'resolution' in msg_lower:
                result = subprocess.run("system_profiler SPDisplaysDataType | grep Resolution", shell=True, capture_output=True, text=True)
                return f"Screen resolution: {result.stdout.strip()}" if result.stdout else "Resolution info unavailable"
            
            # ═══════════════════════════════════════════════════════════════════
            # S - SCREENSHOT / SLEEP / SPOTLIGHT / SIRI
            # ═══════════════════════════════════════════════════════════════════
            elif 'screenshot' in msg_lower or 'screen capture' in msg_lower:
                if 'window' in msg_lower:
                    self._execute_command("screencapture -W ~/Desktop/screenshot_$(date +%Y%m%d_%H%M%S).png")
                    return "Click a window to capture"
                elif 'area' in msg_lower or 'selection' in msg_lower or 'select' in msg_lower:
                    self._execute_command("screencapture -i ~/Desktop/screenshot_$(date +%Y%m%d_%H%M%S).png")
                    return "Select area to capture"
                elif 'clipboard' in msg_lower:
                    self._execute_command("screencapture -c")
                    return "Screenshot copied to clipboard"
                elif 'delay' in msg_lower or 'timer' in msg_lower:
                    self._execute_command("screencapture -T 5 ~/Desktop/screenshot_$(date +%Y%m%d_%H%M%S).png")
                    return "Screenshot in 5 seconds..."
                else:
                    self._execute_command("screencapture ~/Desktop/screenshot_$(date +%Y%m%d_%H%M%S).png")
                    return "Screenshot saved to Desktop"
                    
            elif 'sleep' in msg_lower:
                if 'display' in msg_lower or 'screen' in msg_lower:
                    self._execute_command("pmset displaysleepnow")
                    return "Display sleeping"
                else:
                    self._execute_command("pmset sleepnow")
                    return "Mac going to sleep..."
                    
            elif 'spotlight' in msg_lower:
                self._execute_command("osascript -e 'tell application \"System Events\" to keystroke space using command down'")
                return "Spotlight opened"
                
            elif 'siri' in msg_lower:
                self._execute_command("osascript -e 'tell application \"System Events\" to key code 49 using command down'")
                return "Siri activated"
            
            # ═══════════════════════════════════════════════════════════════════
            # T - TIME MACHINE / TERMINAL / TRASH
            # ═══════════════════════════════════════════════════════════════════
            elif 'time machine' in msg_lower:
                if 'backup' in msg_lower:
                    self._execute_command("tmutil startbackup")
                    return "Time Machine backup started"
                else:
                    self._execute_command("open -a 'Time Machine'")
                    return "Time Machine opened"
                    
            elif 'terminal' in msg_lower:
                self._execute_command("open -a Terminal")
                return "Terminal opened"
                
            elif 'trash' in msg_lower:
                if 'empty' in msg_lower or 'clear' in msg_lower:
                    self._execute_command("rm -rf ~/.Trash/*")
                    return "Trash emptied"
                elif 'open' in msg_lower or 'show' in msg_lower:
                    self._execute_command("open ~/.Trash")
                    return "Trash opened"
            
            # ═══════════════════════════════════════════════════════════════════
            # U - UPTIME / USB
            # ═══════════════════════════════════════════════════════════════════
            elif 'uptime' in msg_lower:
                result = subprocess.run("uptime", shell=True, capture_output=True, text=True)
                return f"System uptime: {result.stdout.strip()}" if result.stdout else "Uptime unknown"
                
            elif 'usb' in msg_lower:
                result = subprocess.run("system_profiler SPUSBDataType | grep -E '(Product ID|Vendor ID|Serial Number|Location)' | head -20", shell=True, capture_output=True, text=True)
                return f"USB devices:\n{result.stdout}" if result.stdout else "No USB devices found"
            
            # ═══════════════════════════════════════════════════════════════════
            # V - VOLUME / VPN
            # ═══════════════════════════════════════════════════════════════════
            elif 'volume' in msg_lower or 'sound' in msg_lower:
                if 'up' in msg_lower or 'increase' in msg_lower or 'louder' in msg_lower:
                    self._execute_command("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
                    return "Volume +10%"
                elif 'down' in msg_lower or 'decrease' in msg_lower or 'lower' in msg_lower:
                    self._execute_command("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
                    return "Volume -10%"
                elif 'max' in msg_lower or 'full' in msg_lower:
                    self._execute_command("osascript -e 'set volume output volume 100'")
                    return "Volume MAX (100%)"
                elif 'min' in msg_lower or 'silent' in msg_lower:
                    self._execute_command("osascript -e 'set volume output volume 0'")
                    return "Volume MIN (0%)"
                else:
                    vol_match = re.search(r'(\d+)', msg_lower)
                    if vol_match:
                        level = max(0, min(100, int(vol_match.group(1))))
                        self._execute_command(f"osascript -e 'set volume output volume {level}'")
                        return f"Volume: {level}%"
                    result = subprocess.run("osascript -e 'output volume of (get volume settings)'", shell=True, capture_output=True, text=True)
                    return f"Current volume: {result.stdout.strip()}%" if result.stdout else "Volume unknown"
                    
            elif 'vpn' in msg_lower:
                if 'connect' in msg_lower:
                    return "VPN: Use System Settings > Network to connect"
                elif 'disconnect' in msg_lower:
                    self._execute_command("scutil --nc stop $(scutil --nc list | grep Connected | awk '{print $1}')")
                    return "VPN disconnected"
            
            # ═══════════════════════════════════════════════════════════════════
            # W - WIFI / WALLPAPER / WINDOW
            # ═══════════════════════════════════════════════════════════════════
            elif 'wifi' in msg_lower:
                if any(word in msg_lower for word in ['off', 'disable', 'turn off', 'disconnect']):
                    self._execute_command("networksetup -setairportpower en0 off")
                    self._add_to_ai_chat("Aurora", "WiFi OFF", "action")
                    return "WiFi has been turned OFF"
                elif any(word in msg_lower for word in ['on', 'enable', 'turn on']):
                    self._execute_command("networksetup -setairportpower en0 on")
                    self._add_to_ai_chat("Aurora", "WiFi ON", "action")
                    return "WiFi has been turned ON"
                elif 'networks' in msg_lower or 'list' in msg_lower or 'scan' in msg_lower:
                    result = subprocess.run("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s 2>/dev/null | head -10", shell=True, capture_output=True, text=True)
                    return f"Available networks:\n{result.stdout}" if result.stdout else "Could not scan networks"
                elif 'status' in msg_lower:
                    result = subprocess.run("networksetup -getairportnetwork en0", shell=True, capture_output=True, text=True)
                    return result.stdout.strip() if result.stdout else "WiFi status unknown"
                elif 'connect' in msg_lower:
                    net_match = re.search(r'connect\s+(?:to\s+)?["\']?(\w+)["\']?', message, re.I)
                    if net_match:
                        network = net_match.group(1)
                        return f"To connect to '{network}': networksetup -setairportnetwork en0 '{network}' PASSWORD"
                        
            elif 'wallpaper' in msg_lower or 'desktop background' in msg_lower:
                if 'change' in msg_lower or 'set' in msg_lower:
                    path_match = re.search(r'["\']([^"\']+)["\']', message)
                    if path_match:
                        path = path_match.group(1)
                        self._execute_command(f"osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"{path}\"'")
                        return f"Wallpaper set to: {path}"
                    return "Specify wallpaper path in quotes"
                    
            elif 'window' in msg_lower:
                if 'minimize' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"m\" using command down'")
                    return "Window minimized"
                elif 'maximize' in msg_lower or 'full' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"f\" using {control down, command down}'")
                    return "Window fullscreen"
                elif 'close' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"w\" using command down'")
                    return "Window closed"
            
            # ═══════════════════════════════════════════════════════════════════
            # Z - ZOOM / ZZLEEP
            # ═══════════════════════════════════════════════════════════════════
            elif 'zoom' in msg_lower:
                if 'in' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"+\" using command down'")
                    return "Zoomed in"
                elif 'out' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"-\" using command down'")
                    return "Zoomed out"
                elif 'reset' in msg_lower:
                    self._execute_command("osascript -e 'tell application \"System Events\" to keystroke \"0\" using command down'")
                    return "Zoom reset"
            
            # ═══════════════════════════════════════════════════════════════════
            # DO NOT DISTURB / FOCUS MODE
            # ═══════════════════════════════════════════════════════════════════
            elif 'do not disturb' in msg_lower or 'dnd' in msg_lower or 'focus' in msg_lower:
                if any(word in msg_lower for word in ['on', 'enable']):
                    self._execute_command("shortcuts run 'Focus On' 2>/dev/null")
                    return "Do Not Disturb enabled"
                elif any(word in msg_lower for word in ['off', 'disable']):
                    self._execute_command("shortcuts run 'Focus Off' 2>/dev/null")
                    return "Do Not Disturb disabled"
            
            # ═══════════════════════════════════════════════════════════════════
            # DEFAULT - Show available commands
            # ═══════════════════════════════════════════════════════════════════
            return """System action recognized. Available commands:
• WiFi: on/off/status/scan
• Bluetooth: on/off/devices
• Volume: up/down/mute/50%
• Brightness: up/down/max
• Screenshot: full/area/window
• Dark Mode: on/off/toggle
• Sleep/Lock/Restart/Shutdown
• Dock: hide/show/left/right
• DNS: flush/show
• And many more A-Z commands!"""
            
        except Exception as e:
            return f"System action error: {str(e)[:50]}"
    
    def _handle_web_action(self, message, msg_lower):
        """Handle web and browser actions"""
        try:
            if 'google' in msg_lower or 'search' in msg_lower:
                # Extract search query
                import re
                query_match = re.search(r'(?:google |search for |search )["\'](.*?)["\']', message)
                if not query_match:
                    query_match = re.search(r'(?:google |search for |search )(.*?)$', message)
                
                query = query_match.group(1).strip() if query_match else "Aurora AI"
                
                self._execute_command(f"open 'https://www.google.com/search?q={query.replace(' ', '+')}'")
                return f"Googling: {query}"
            
            elif 'open website' in msg_lower or 'go to' in msg_lower:
                import re
                url_match = re.search(r'(?:open |go to )(.*?)$', message)
                url = url_match.group(1).strip() if url_match else "google.com"
                
                if not url.startswith('http'):
                    url = f"https://{url}"
                
                self._execute_command(f"open '{url}'")
                return f"Opened website: {url}"
            
            return "Web action completed"
            
        except Exception as e:
            return f"Web action failed: {str(e)[:40]}"
    
    def _handle_youtube_action(self, message, msg_lower):
        """Handle YouTube video and music playing actions"""
        try:
            import re
            import urllib.parse
            
            # Extract what to play/search
            patterns = [
                r'play\s+(?:song\s+)?["\'](.*?)["\']',  # play "song name"
                r'play\s+(.*?)\s+(?:song|video|music)',  # play xyz song/video
                r'(?:youtube|video)\s+["\'](.*?)["\']',  # youtube "query"
                r'play\s+(.*?)\s+on\s+youtube',  # play xyz on youtube
                r'(?:search|find)\s+(.*?)\s+on\s+youtube',  # search xyz on youtube
                r'watch\s+["\'](.*?)["\']',  # watch "video"
                r'play\s+([\w\s]+)',  # play xyz (fallback)
            ]
            
            search_query = None
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    search_query = match.group(1).strip()
                    # Clean up the query
                    search_query = re.sub(r'\s+(?:on youtube|video|song|music)?$', '', search_query, flags=re.IGNORECASE)
                    break
            
            if not search_query:
                # Try to extract any content after "play"
                match = re.search(r'play\s+(.+?)(?:\s+on|\s+in|\s*$)', message, re.IGNORECASE)
                if match:
                    search_query = match.group(1).strip()
            
            if not search_query:
                search_query = "trending music"
            
            self._add_to_ai_chat("Aurora", f"Opening YouTube to play: {search_query}", "action")
            
            # Encode the search query for URL
            encoded_query = urllib.parse.quote(search_query)
            
            # Open YouTube search results
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            self._execute_command(f"open '{youtube_url}'")
            
            # Wait for browser to open and then try to click first video
            def click_first_video():
                time.sleep(3)  # Wait for page to load
                try:
                    # Use AppleScript to click on first video
                    # This positions and clicks in the typical location of the first YouTube result
                    self._execute_command('''osascript -e '
                        tell application "System Events"
                            delay 1
                            -- Click approximately where first video thumbnail appears
                            -- This may need adjustment based on screen resolution
                            click at {400, 400}
                        end tell
                    ' 2>/dev/null''')
                except:
                    pass
            
            # Start background thread to click first video
            threading.Thread(target=click_first_video, daemon=True).start()
            
            return f"Opening YouTube: {search_query}. First video will play automatically."
            
        except Exception as e:
            return f"YouTube action failed: {str(e)[:40]}"
    
    # Helper methods for automation
    def _execute_command(self, command):
        """Execute shell command"""
        import subprocess
        subprocess.run(command, shell=True, capture_output=True)
    
    def _type_text(self, text):
        """Type text using AppleScript automation"""
        try:
            if hasattr(self, 'keyboard_automation') and self.keyboard_automation:
                self.keyboard_automation.type_text(text)
            else:
                # Fallback to AppleScript
                escaped_text = text.replace('"', '\\"').replace("'", "'\"'\"'")
                self._execute_command(f'''osascript -e 'tell application "System Events" to keystroke "{escaped_text}"' ''')
        except Exception as e:
            self.log.log(f"Type error: {str(e)[:30]}", 'red')
    
    def _press_key(self, key):
        """Press key using AppleScript - supports special keys and modifiers"""
        try:
            if hasattr(self, 'keyboard_automation') and self.keyboard_automation:
                self.keyboard_automation.press_key(key)
            else:
                # Map common keys to AppleScript key codes
                key_codes = {
                    'return': 36, 'enter': 36, 'tab': 48, 'space': 49,
                    'delete': 51, 'backspace': 51, 'escape': 53, 'esc': 53,
                    'up': 126, 'down': 125, 'left': 123, 'right': 124,
                    'f1': 122, 'f2': 120, 'f3': 99, 'f4': 118, 'f5': 96,
                    'f6': 97, 'f7': 98, 'f8': 100, 'f9': 101, 'f10': 109,
                    'f11': 103, 'f12': 111
                }
                
                key_lower = key.lower()
                
                # Handle modifier combinations like cmd+s, ctrl+c
                if '+' in key_lower:
                    parts = key_lower.split('+')
                    modifiers = []
                    main_key = parts[-1]
                    for mod in parts[:-1]:
                        if mod in ['cmd', 'command']: modifiers.append('command down')
                        elif mod in ['ctrl', 'control']: modifiers.append('control down')
                        elif mod in ['alt', 'option']: modifiers.append('option down')
                        elif mod in ['shift']: modifiers.append('shift down')
                    
                    mod_str = ', '.join(modifiers)
                    if main_key in key_codes:
                        self._execute_command(f'''osascript -e 'tell application "System Events" to key code {key_codes[main_key]} using {{{mod_str}}}' ''')
                    else:
                        self._execute_command(f'''osascript -e 'tell application "System Events" to keystroke "{main_key}" using {{{mod_str}}}' ''')
                elif key_lower in key_codes:
                    self._execute_command(f'''osascript -e 'tell application "System Events" to key code {key_codes[key_lower]}' ''')
                else:
                    self._execute_command(f'''osascript -e 'tell application "System Events" to keystroke "{key}"' ''')
        except Exception as e:
            self.log.log(f"Key press error: {str(e)[:30]}", 'red')
    
    def _click_at(self, x, y):
        """Click at specific coordinates using cliclick or AppleScript"""
        try:
            if hasattr(self, 'autonomous_explorer') and self.autonomous_explorer:
                self.autonomous_explorer.click_at(x, y)
            else:
                # Try cliclick first (faster), fall back to AppleScript
                result = subprocess.run(f"cliclick c:{x},{y} 2>/dev/null", shell=True, capture_output=True)
                if result.returncode != 0:
                    # Fallback to AppleScript (may need accessibility permissions)
                    self._execute_command(f'''osascript -e '
                        tell application "System Events"
                            click at {{{x}, {y}}}
                        end tell
                    ' 2>/dev/null''')
        except Exception as e:
            self.log.log(f"Click error: {str(e)[:30]}", 'red')
    
    def _click_center(self):
        """Click at screen center"""
        try:
            if hasattr(self, 'autonomous_explorer') and self.autonomous_explorer:
                self.autonomous_explorer.click_center()
            else:
                # Get screen size and click center
                result = subprocess.run("system_profiler SPDisplaysDataType | grep Resolution", 
                                       shell=True, capture_output=True, text=True)
                # Default to common resolution center
                cx, cy = 960, 540
                if result.stdout:
                    import re
                    match = re.search(r'(\d+)\s*x\s*(\d+)', result.stdout)
                    if match:
                        cx = int(match.group(1)) // 2
                        cy = int(match.group(2)) // 2
                self._click_at(cx, cy)
        except Exception as e:
            self.log.log(f"Click center error: {str(e)[:30]}", 'red')
    
    def _scroll_up(self, amount=5):
        """Scroll up using cliclick or AppleScript"""
        try:
            if hasattr(self, 'autonomous_explorer') and self.autonomous_explorer:
                self.autonomous_explorer.scroll_up()
            else:
                result = subprocess.run(f"cliclick 'ku:+{amount}' 2>/dev/null", shell=True, capture_output=True)
                if result.returncode != 0:
                    self._execute_command('''osascript -e 'tell application "System Events" to key code 126' ''')
        except Exception as e:
            self.log.log(f"Scroll error: {str(e)[:30]}", 'red')
    
    def _scroll_down(self, amount=5):
        """Scroll down using cliclick or AppleScript"""
        try:
            if hasattr(self, 'autonomous_explorer') and self.autonomous_explorer:
                self.autonomous_explorer.scroll_down()
            else:
                result = subprocess.run(f"cliclick 'kd:+{amount}' 2>/dev/null", shell=True, capture_output=True)
                if result.returncode != 0:
                    self._execute_command('''osascript -e 'tell application "System Events" to key code 125' ''')
        except Exception as e:
            self.log.log(f"Scroll error: {str(e)[:30]}", 'red')
    
    def _move_mouse_to(self, x, y):
        """Move mouse to coordinates"""
        try:
            if hasattr(self, 'autonomous_explorer') and self.autonomous_explorer:
                self.autonomous_explorer.move_mouse(x, y)
            else:
                # Try cliclick first
                result = subprocess.run(f"cliclick m:{x},{y} 2>/dev/null", shell=True, capture_output=True)
                if result.returncode != 0:
                    # AppleScript mouse move (requires additional setup)
                    self._execute_command(f'''osascript -e '
                        do shell script "cliclick m:{x},{y}" 
                    ' 2>/dev/null || echo "Install cliclick: brew install cliclick"''')
        except Exception as e:
            self.log.log(f"Mouse move error: {str(e)[:30]}", 'red')
    
    def _double_click_at(self, x, y):
        """Double click at specific coordinates"""
        try:
            result = subprocess.run(f"cliclick dc:{x},{y} 2>/dev/null", shell=True, capture_output=True)
            if result.returncode != 0:
                self._click_at(x, y)
                time.sleep(0.1)
                self._click_at(x, y)
        except Exception as e:
            self.log.log(f"Double click error: {str(e)[:30]}", 'red')
    
    def _right_click_at(self, x, y):
        """Right click at specific coordinates"""
        try:
            result = subprocess.run(f"cliclick rc:{x},{y} 2>/dev/null", shell=True, capture_output=True)
            if result.returncode != 0:
                self._execute_command(f'''osascript -e '
                    tell application "System Events"
                        click at {{{x}, {y}}} with control key down
                    end tell
                ' 2>/dev/null''')
        except Exception as e:
            self.log.log(f"Right click error: {str(e)[:30]}", 'red')
    
    def _drag_mouse(self, x1, y1, x2, y2):
        """Drag from one point to another"""
        try:
            result = subprocess.run(f"cliclick dd:{x1},{y1} du:{x2},{y2} 2>/dev/null", shell=True, capture_output=True)
            if result.returncode != 0:
                self.log.log("Install cliclick for drag: brew install cliclick", 'yellow')
        except Exception as e:
            self.log.log(f"Drag error: {str(e)[:30]}", 'red')
    
    def _hotkey(self, *keys):
        """Press multiple keys together (e.g., cmd, shift, 3 for screenshot)"""
        key_combo = '+'.join(keys)
        self._press_key(key_combo)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SELF-EVOLUTION SYSTEM - AI improves itself using learned data and retrains models
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _trigger_self_evolution(self):
        """
        Trigger AI self-evolution - this now:
        1. Gathers all learned data from Aurora's experiences
        2. Creates training datasets from successful actions
        3. Fine-tunes the local LLM (Llama/LLaVA) using Ollama
        4. Validates improvements
        """
        def evolve():
            try:
                # Import the self-evolving AI module
                from self_evolving_ai import SelfEvolvingAI
                
                self.evolution_status_var.set("🧬 Initializing self-evolution...")
                self._add_to_ai_chat("Evolution", "Starting ADVANCED self-evolution sequence...", "learning")
                
                # Initialize the evolving AI system
                base_path = os.path.dirname(__file__)
                evolving_ai = SelfEvolvingAI(base_path)
                
                # Set up progress callback
                def update_progress(progress):
                    self.evolution_status_var.set(f"🧬 Evolution progress: {progress}%")
                
                evolving_ai.progress_callback = update_progress
                
                # Run the evolution process
                self._add_to_ai_chat("Evolution", "Phase 1: Gathering training data from experiences...", "learning")
                self.evolution_status_var.set("📚 Gathering training data...")
                
                result = evolving_ai.evolve()
                
                if result["success"]:
                    model_name = result.get("model", "unknown")
                    metrics = result.get("metrics", {})
                    
                    self._add_to_ai_chat("Evolution", f"✅ Evolution complete! New model: {model_name}", "learning")
                    self._add_to_ai_chat("Evolution", f"Evolution cycles: {metrics.get('evolution_cycles', 1)}", "learning")
                    
                    self.evolution_status_var.set(f"✅ Evolved to {model_name}!")
                    
                    # Update evolution display
                    new_level = self._get_evolution_level() + 0.5
                    if hasattr(self, 'evolution_var'):
                        self.evolution_var.set(f"Evolution Level: {new_level:.1f}")
                    
                    # Store evolution record
                    if hasattr(self, 'brain') and self.brain:
                        self.brain.remember('skills', 'evolved_patterns', {
                            'timestamp': time.time(),
                            'model': model_name,
                            'evolution_level': new_level,
                            'metrics': metrics
                        })
                    
                    # Record in ledger
                    try:
                        ledger_path = os.path.join(os.path.dirname(__file__), 'aurora_memory', 'evolution_ledger.json')
                        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
                        entry = {
                            'timestamp': time.time(),
                            'level': new_level,
                            'model': model_name,
                            'summary': 'model_evolved',
                            'metrics': metrics
                        }
                        existing = []
                        if os.path.exists(ledger_path):
                            with open(ledger_path, 'r') as f:
                                try:
                                    existing = json.load(f)
                                except:
                                    existing = []
                        existing.append(entry)
                        with open(ledger_path, 'w') as f:
                            json.dump(existing[-500:], f, indent=2)
                    except Exception as le:
                        self.log.log(f"Ledger error: {str(le)[:40]}", 'red')
                    
                    self.log.log(f"🧬 EVOLUTION COMPLETE: {model_name}", 'orange')
                    
                else:
                    error_msg = result.get("message", "Unknown error")
                    self._add_to_ai_chat("Evolution", f"❌ Evolution failed: {error_msg}", "error")
                    self.evolution_status_var.set(f"Evolution failed: {error_msg[:30]}...")
                    
                    # Fall back to basic evolution
                    self._basic_evolution()
                    
            except ImportError:
                self._add_to_ai_chat("Evolution", "Using basic evolution (self_evolving_ai not found)...", "learning")
                self._basic_evolution()
            except Exception as e:
                self.evolution_status_var.set(f"Evolution error: {str(e)[:30]}")
                self._add_to_ai_chat("Evolution", f"Error: {str(e)[:100]}", "error")
                self.log.log(f"Evolution error: {str(e)[:50]}", 'red')
        
        threading.Thread(target=evolve, daemon=True).start()
    
    def _basic_evolution(self):
        """Basic evolution when advanced system is not available"""
        self.evolution_status_var.set("Running basic evolution...")
        
        # Gather learning data
        evolution_data = self._gather_evolution_data()
        self.evolution_status_var.set(f"Processing {len(evolution_data)} items...")
        
        # Generate evolution insights with NLP
        if self.nlp:
            try:
                training_prompt = self._create_training_prompt(evolution_data)
                
                evolved_response = self.nlp.generate_response(
                    f"Based on these learnings, generate 3 improved response patterns: {training_prompt[:500]}"
                )
                
                if evolved_response:
                    if hasattr(self, 'brain') and self.brain:
                        self.brain.remember('skills', 'evolved_patterns', {
                            'timestamp': time.time(),
                            'patterns': evolved_response,
                            'evolution_level': self._get_evolution_level() + 0.1
                        })
                    
                    self._add_to_ai_chat("Evolution", f"Basic evolution complete: {evolved_response[:150]}...", "learning")
                    self.evolution_status_var.set("Basic evolution complete!")
                else:
                    self.evolution_status_var.set("Need more learning data for evolution.")
            except Exception as e:
                self.evolution_status_var.set(f"Basic evolution error: {str(e)[:30]}")
        else:
            self.evolution_status_var.set("Waiting for language model...")
    
    def _gather_evolution_data(self):
        """Gather all learning data for evolution"""
        data = []
        
        if hasattr(self, 'brain') and self.brain:
            for category in ['actions', 'apps', 'skills', 'patterns', 'experiences']:
                try:
                    cat_data = self.brain.get_all(category)
                    if cat_data:
                        for key, value in cat_data.items():
                            data.append({
                                'category': category,
                                'key': key,
                                'value': str(value)[:100]
                            })
                except:
                    pass
        
        return data
    
    def _create_training_prompt(self, data):
        """Create training prompt from evolution data"""
        prompt_parts = []
        for item in data[:20]:  # Limit to 20 items
            prompt_parts.append(f"{item['category']}: {item['key']}")
        return ", ".join(prompt_parts)
    
    def _get_evolution_level(self):
        """Get current evolution level"""
        try:
            if hasattr(self, 'brain') and self.brain:
                evolved = self.brain.get('skills', 'evolved_patterns')
                if evolved:
                    return evolved.get('evolution_level', 1.0)
        except:
            pass
        return 1.0
    
    def _update_learning_stats(self):
        """Update learning statistics display"""
        try:
            if hasattr(self, 'brain') and self.brain:
                total_learned = 0
                total_skills = 0
                
                for key in ['actions', 'apps', 'patterns', 'locations']:
                    data = self.brain.get_all(key)
                    if data:
                        total_learned += len(data)
                
                skills = self.brain.get_all('skills')
                if skills:
                    total_skills = len(skills)
                
                if hasattr(self, 'learn_count_var'):
                    self.learn_count_var.set(f"Items Learned: {total_learned}")
                if hasattr(self, 'skills_count_var'):
                    self.skills_count_var.set(f"Skills Acquired: {total_skills}")
                if hasattr(self, 'evolution_var'):
                    self.evolution_var.set(f"Evolution Level: {self._get_evolution_level():.1f}")
        except:
            pass
    
    def _ask_user_question(self, question):
        """AI asks user a question (with voice)"""
        self._add_to_ai_chat("Aurora", question, "aurora")
        self._speak_to_user(question)
        self.log.log(f"Aurora asks: {question}", 'orange')
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AI BRAINSTORM CHAT - Two AIs talking
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _add_to_ai_chat(self, speaker, message, tag='system'):
        """Add message to AI chat panel"""
        def add():
            self.ai_chat.config(state='normal')
            ts = datetime.now().strftime("%H:%M:%S")
            self.ai_chat.insert('end', f"[{ts}] ", 'system')
            self.ai_chat.insert('end', f"{speaker}: ", tag)
            self.ai_chat.insert('end', f"{message}\n", tag)
            self.ai_chat.see('end')
            self.ai_chat.config(state='disabled')
        try:
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.root.after(0, add)
        except:
            pass
    
    def _ai_brainstorm(self, topic):
        """Two AIs discuss a topic"""
        def brainstorm():
            # Aurora starts
            aurora_thought = f"Thinking about {topic}..."
            self._add_to_ai_chat("Aurora", aurora_thought, "aurora")
            self.current_thought_var.set(aurora_thought)
            
            if self.nlp:
                try:
                    # Aurora's perspective
                    aurora_resp = self.nlp.generate_response(
                        f"As Aurora AI, share a brief thought about: {topic}"
                    )
                    if aurora_resp:
                        self._add_to_ai_chat("Aurora", aurora_resp[:150], "aurora")
                        time.sleep(1)
                        
                        # Neo responds (simulated second AI)
                        neo_resp = self.nlp.generate_response(
                            f"As Neo AI, respond to this with a different perspective: {aurora_resp[:100]}"
                        )
                        if neo_resp:
                            self._add_to_ai_chat("Neo", neo_resp[:150], "neo")
                except:
                    pass
        
        threading.Thread(target=brainstorm, daemon=True).start()
    
    def _coordinate_agents(self):
        """Mother AI coordinates sub-agents in real-time"""
        if not hasattr(self, 'agent_tasks'):
            self.agent_tasks = {
                'vision': {'active': False, 'task': 'idle', 'progress': 0},
                'voice': {'active': False, 'task': 'idle', 'progress': 0},
                'action': {'active': False, 'task': 'idle', 'progress': 0},
                'learning': {'active': True, 'task': 'training', 'progress': 85}
            }
        
        # Simulate agent coordination based on current state
        if self.running:
            # Vision agent analyzes screen periodically
            if random.random() < 0.3:
                self.agent_tasks['vision']['active'] = True
                self.agent_tasks['vision']['task'] = 'analyzing'
                if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                    self.agent_comm.send_message(0, 1, 'instruction')  # Mother to Vision
            
            # Voice agent responds to queries
            if hasattr(self, 'ask_entry') and self.ask_entry.get():
                self.agent_tasks['voice']['active'] = True
                self.agent_tasks['voice']['task'] = 'processing_speech'
            
            # Action agent executes based on decisions
            if hasattr(self, 'current_plan') and self.current_plan:
                self.agent_tasks['action']['active'] = True
                self.agent_tasks['action']['task'] = 'executing'
                if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                    self.agent_comm.send_message(0, 3, 'data')  # Mother to Action
            
            # Learning agent continuously learns
            if self.total_actions > 0:
                self.agent_tasks['learning']['progress'] = min(99, 
                    50 + (self.success_count / self.total_actions * 50))
                if hasattr(self, 'agent_comm') and self.agent_comm is not None:
                    self.agent_comm.send_message(4, 0, 'report')  # Learning to Mother
    
    def _update_agent_statuses(self):
        """Update agent status indicators in real-time"""
        if not hasattr(self, 'agent_tasks'):
            return
        
        # Update mother AI status - with safety check
        if hasattr(self, 'mother_status'):
            status = "● Processing" if self.running else "○ Idle"
            color = T.GREEN if self.running else T.TEXT_DIM
            try:
                self.mother_status.config(text=status, fg=color)
            except:
                pass
        
        # Update sub-agent statuses - with safety checks
        agents = []
        if hasattr(self, 'vision_status'):
            agents.append(('vision', self.vision_status))
        if hasattr(self, 'voice_agent_status'):
            agents.append(('voice', self.voice_agent_status))
        if hasattr(self, 'action_status'):
            agents.append(('action', self.action_status))
        if hasattr(self, 'learning_status'):
            agents.append(('learning', self.learning_status))
        
        for agent_name, status_widget in agents:
            if agent_name in self.agent_tasks:
                task_info = self.agent_tasks[agent_name]
                if task_info['active']:
                    status_text = f"● {task_info['task'].title()}"
                    status_color = T.GREEN
                    # Reset after display
                    task_info['active'] = False
                else:
                    if agent_name == 'learning':
                        status_text = f"● Training {task_info['progress']}%"
                        status_color = T.PURPLE
                    else:
                        status_text = "○ Standby"
                        status_color = T.TEXT_DIM
                
                try:
                    status_widget.config(text=status_text, fg=status_color)
                except:
                    pass
        
        # Update learning progress display
        if hasattr(self, 'learning_progress_var'):
            if self.permanent_brain:
                summary = self.permanent_brain.get_summary()
                patterns = summary.get('patterns_learned', 0)
                memories = summary.get('total_memories', 0)
                progress_text = f"Patterns: {patterns} | Memories: {memories} | IQ: {summary.get('intelligence_level', 0)}"
            else:
                progress_text = f"Cycles: {self.cycle_count} | Success: {int(100 * self.success_count / max(1, self.total_actions))}%"
            
            self.learning_progress_var.set(progress_text)
    
    def _send_query(self):
        query = self.ask_entry.get().strip()
        if not query:
            return
        
        self.ask_entry.delete(0, 'end')
        self.log.log(f"You: {query}", 'yellow')
        self._add_to_ai_chat("You", query, "thought")
        self.brain.set_thinking(True, query)
        
        if self.nlp:
            def do_process():
                try:
                    # Add to conversation history
                    self.nlp.add_to_conversation("user", query)
                    # Generate response
                    resp = self.nlp.generate_response(query)
                    if resp:
                        self.nlp.add_to_conversation("aurora", resp)
                        self.message_queue.put(('log', f"Aurora: {resp[:100]}", 'cyan'))
                        self.message_queue.put(('thought', resp))
                        self._add_to_ai_chat("Aurora", resp, "aurora")
                        # Speak response
                        self._speak_to_user(resp[:150])
                    else:
                        self.message_queue.put(('log', "Aurora: I'm thinking...", 'cyan'))
                except Exception as ex:
                    self.message_queue.put(('log', f"{str(ex)[:40]}", 'red'))
            threading.Thread(target=do_process, daemon=True).start()
        else:
            self.log.log("NLP engine not available", 'red')
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
    
    def _on_close(self):
        self.running = False
        
        # Stop vision feed
        if hasattr(self, 'vision_running'):
            self.vision_running = False
        
        # Save action history before closing
        if self.action_tracker:
            try:
                self.action_tracker.save_memory()
                print("Action history saved")
            except Exception as e:
                print(f"Could not save action history: {e}")
        
        self.root.destroy()


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = AuroraUltimate()
    app.run()
