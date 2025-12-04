"""
WorldView - 3D World Visualization for Aurora AI
=================================================
Provides a visual representation of Aurora's understanding of the world.
"""

import tkinter as tk
import math
import random
from collections import deque


class WorldView(tk.Canvas):
    """
    3D World Visualization Canvas
    Shows Aurora's perception of the digital world with:
    - Floating nodes representing apps, files, processes
    - Connections between related entities
    - Real-time updates from AI activity
    """
    
    def __init__(self, parent, **kwargs):
        # Default styling
        kwargs.setdefault('bg', '#050510')
        kwargs.setdefault('highlightthickness', 0)
        super().__init__(parent, **kwargs)
        
        self.width = 0
        self.height = 0
        self.time = 0
        
        # World state
        self.nodes = []
        self.connections = []
        self.particles = []
        self.is_active = False
        
        # Colors
        self.colors = {
            'node': '#00ffff',
            'connection': '#1a3a5a',
            'highlight': '#ff66aa',
            'text': '#ffffff',
            'dim': '#3a4a5a'
        }
        
        # Animation settings
        self.rotation_speed = 0.005
        self.pulse_phase = 0
        
        self.bind('<Configure>', self._on_resize)
        self._init_world()
        self._animate()
    
    def _on_resize(self, event):
        """Handle canvas resize"""
        self.width = event.width
        self.height = event.height
        self._init_world()
    
    def _init_world(self):
        """Initialize world with default nodes"""
        if self.width < 50 or self.height < 50:
            return
            
        self.nodes = []
        cx, cy = self.width // 2, self.height // 2
        
        # Create orbital nodes
        categories = [
            ('Apps', '#00ffff', 80),
            ('Files', '#00ff88', 120),
            ('System', '#ff66aa', 160),
            ('Network', '#ffaa00', 100),
            ('Memory', '#aa66ff', 140),
        ]
        
        for i, (name, color, radius) in enumerate(categories):
            angle = (i / len(categories)) * math.pi * 2
            self.nodes.append({
                'name': name,
                'x': cx + math.cos(angle) * radius,
                'y': cy + math.sin(angle) * radius,
                'base_angle': angle,
                'radius': radius,
                'color': color,
                'size': 20,
                'pulse': random.random() * math.pi * 2,
                'activity': 0.5
            })
    
    def set_active(self, active):
        """Set active state"""
        self.is_active = active
    
    def add_node(self, name, category='default', activity=0.5):
        """Add a new node to the world"""
        if self.width > 0:
            cx, cy = self.width // 2, self.height // 2
            angle = random.random() * math.pi * 2
            radius = 60 + random.random() * 100
            
            colors = ['#00ffff', '#00ff88', '#ff66aa', '#ffaa00', '#aa66ff']
            
            self.nodes.append({
                'name': name[:15],
                'x': cx + math.cos(angle) * radius,
                'y': cy + math.sin(angle) * radius,
                'base_angle': angle,
                'radius': radius,
                'color': random.choice(colors),
                'size': 15,
                'pulse': random.random() * math.pi * 2,
                'activity': activity
            })
    
    def add_connection(self, node1_name, node2_name, strength=0.5):
        """Add connection between nodes"""
        self.connections.append({
            'from': node1_name,
            'to': node2_name,
            'strength': strength,
            'life': 1.0
        })
    
    def update_node_activity(self, name, activity):
        """Update activity level of a node"""
        for node in self.nodes:
            if node['name'] == name:
                node['activity'] = min(1.0, max(0.0, activity))
                break
    
    def spawn_particle(self, x=None, y=None, color=None):
        """Spawn a particle at position"""
        if self.width > 0:
            self.particles.append({
                'x': x or self.width // 2,
                'y': y or self.height // 2,
                'vx': (random.random() - 0.5) * 4,
                'vy': (random.random() - 0.5) * 4,
                'color': color or '#00ffff',
                'size': 3,
                'life': 1.0
            })
    
    def _animate(self):
        """Main animation loop"""
        try:
            if not self.winfo_exists():
                return
        except:
            return
        
        if self.width > 0 and self.height > 0:
            self.delete('all')
            self.time += 0.02
            self.pulse_phase += 0.05
            
            cx, cy = self.width // 2, self.height // 2
            
            # Draw background grid
            self._draw_grid()
            
            # Draw connections
            self._draw_connections()
            
            # Update and draw nodes
            for node in self.nodes:
                # Orbital motion when active
                if self.is_active:
                    node['base_angle'] += self.rotation_speed
                
                # Calculate position
                node['x'] = cx + math.cos(node['base_angle']) * node['radius']
                node['y'] = cy + math.sin(node['base_angle']) * node['radius']
                
                # Draw node
                self._draw_node(node)
            
            # Update and draw particles
            self._update_particles()
            
            # Draw central core
            self._draw_core(cx, cy)
            
            # Draw title
            self._draw_title()
        
        try:
            if self.winfo_exists():
                self.after(33, self._animate)
        except:
            pass
    
    def _draw_grid(self):
        """Draw background grid"""
        cx, cy = self.width // 2, self.height // 2
        
        # Concentric circles
        for r in range(40, 200, 40):
            alpha = 0.3 if self.is_active else 0.1
            self.create_oval(cx - r, cy - r, cx + r, cy + r,
                           outline='#1a2a3a', width=1)
        
        # Radial lines
        for i in range(8):
            angle = (i / 8) * math.pi * 2
            x = cx + math.cos(angle) * 180
            y = cy + math.sin(angle) * 180
            self.create_line(cx, cy, x, y, fill='#1a2a3a', width=1)
    
    def _draw_connections(self):
        """Draw connections between nodes"""
        new_connections = []
        for conn in self.connections:
            conn['life'] -= 0.01
            if conn['life'] > 0:
                # Find nodes
                from_node = next((n for n in self.nodes if n['name'] == conn['from']), None)
                to_node = next((n for n in self.nodes if n['name'] == conn['to']), None)
                
                if from_node and to_node:
                    self.create_line(
                        from_node['x'], from_node['y'],
                        to_node['x'], to_node['y'],
                        fill='#1a3a5a', width=1
                    )
                new_connections.append(conn)
        self.connections = new_connections
    
    def _draw_node(self, node):
        """Draw a single node"""
        x, y = node['x'], node['y']
        size = node['size']
        color = node['color']
        
        # Pulse effect
        pulse = 1 + node['activity'] * 0.2 * math.sin(self.pulse_phase + node['pulse'])
        size *= pulse
        
        # Glow
        if self.is_active:
            for i in range(3, 0, -1):
                glow_size = size + i * 4
                self.create_oval(
                    x - glow_size, y - glow_size,
                    x + glow_size, y + glow_size,
                    outline=color, width=1
                )
        
        # Main node
        self.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill='#0a1520' if self.is_active else '#101520',
            outline=color if self.is_active else '#3a4a5a',
            width=2
        )
        
        # Label
        self.create_text(
            x, y + size + 12,
            text=node['name'],
            font=('JetBrains Mono', 8),
            fill=color if self.is_active else '#5a6a7a'
        )
    
    def _draw_core(self, cx, cy):
        """Draw central core"""
        pulse = 1 + 0.1 * math.sin(self.pulse_phase * 2)
        size = 25 * pulse
        
        # Glow
        if self.is_active:
            for i in range(4, 0, -1):
                glow_size = size + i * 6
                self.create_oval(
                    cx - glow_size, cy - glow_size,
                    cx + glow_size, cy + glow_size,
                    outline='#00ffff', width=1
                )
        
        # Core
        self.create_oval(
            cx - size, cy - size,
            cx + size, cy + size,
            fill='#00ffff' if self.is_active else '#1a2a3a',
            outline='#ffffff' if self.is_active else '#3a4a5a',
            width=2
        )
        
        # Label
        self.create_text(
            cx, cy,
            text='AI',
            font=('JetBrains Mono', 10, 'bold'),
            fill='#000000' if self.is_active else '#5a6a7a'
        )
    
    def _update_particles(self):
        """Update and draw particles"""
        new_particles = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
            p['size'] *= 0.98
            
            if p['life'] > 0 and p['size'] > 0.5:
                self.create_oval(
                    p['x'] - p['size'], p['y'] - p['size'],
                    p['x'] + p['size'], p['y'] + p['size'],
                    fill=p['color'], outline=''
                )
                new_particles.append(p)
        
        self.particles = new_particles[:100]
    
    def _draw_title(self):
        """Draw title"""
        color = '#00ffff' if self.is_active else '#3a4a5a'
        self.create_text(
            self.width // 2, 15,
            text='WORLD VIEW',
            font=('JetBrains Mono', 10, 'bold'),
            fill=color
        )
        
        status = 'ACTIVE' if self.is_active else 'STANDBY'
        self.create_text(
            self.width // 2, self.height - 15,
            text=status,
            font=('JetBrains Mono', 8),
            fill=color
        )


# For standalone testing
if __name__ == '__main__':
    root = tk.Tk()
    root.title('World View Test')
    root.geometry('600x400')
    root.configure(bg='#050510')
    
    wv = WorldView(root)
    wv.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Test activation
    def toggle():
        wv.is_active = not wv.is_active
        root.after(3000, toggle)
    
    root.after(1000, toggle)
    root.mainloop()
