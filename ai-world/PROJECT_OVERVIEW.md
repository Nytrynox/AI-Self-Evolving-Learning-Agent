# 🌟 AURORA AI - Project Overview

## What Does This Project Do? (Simple English)

**Aurora is a personal AI assistant that can control your Mac computer like a human would.**

Imagine having a robot friend sitting at your computer who can:
- **See your screen** (takes screenshots and understands what's on screen)
- **Click buttons** and type on keyboard
- **Understand your commands** in plain English like "open YouTube and play music"
- **Learn from mistakes** - if something fails, it remembers and tries differently next time
- **Control your Mac** - volume, brightness, WiFi, apps, files, everything!

### In One Sentence:
> Aurora is an AI that **SEES your screen**, **UNDERSTANDS what you want**, and **DOES it for you** - learning and improving each time.

---

## 🔄 How It Works - Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           AURORA AI WORKFLOW                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

                              YOU (User)
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │    "Play Coldplay on       │
                    │     YouTube"                │
                    │   (Natural Language Input)  │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      SMART EXECUTOR         │
                    │   (Natural Language Parser) │
                    │                             │
                    │  • Understands intent       │
                    │  • Breaks into steps        │
                    │  • Plans the execution      │
                    └──────────────┬──────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│   LLM BRAIN     │   │   VISION SYSTEM     │   │   macOS COMMANDS    │
│  (Ollama)       │   │                     │   │                     │
│                 │   │  • Takes screenshot │   │  • 100+ commands    │
│  • llama3.2:3b  │   │  • Sends to LLaVA   │   │  • Volume/WiFi      │
│    (text)       │   │  • Finds buttons,   │   │  • Open apps        │
│  • llava:7b     │   │    links, fields    │   │  • System control   │
│    (vision)     │   │  • Returns x,y      │   │  • Keyboard/Mouse   │
│                 │   │    coordinates      │   │                     │
└────────┬────────┘   └──────────┬──────────┘   └──────────┬──────────┘
         │                       │                         │
         └───────────────────────┼─────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     ACTION EXECUTOR     │
                    │                         │
                    │  • Click at x,y         │
                    │  • Type text            │
                    │  • Press keys           │
                    │  • Run AppleScript      │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   LEARNING ENGINE       │
                    │   (SQLite Database)     │
                    │                         │
                    │  • Was it successful?   │
                    │  • Record outcome       │
                    │  • Update confidence    │
                    │  • Remember for next    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │       RESULT            │
                    │                         │
                    │  ✅ Success: YouTube    │
                    │     opens, plays song   │
                    │                         │
                    │  ❌ Fail: Learn why,    │
                    │     try different way   │
                    └─────────────────────────┘
```

---

## 🏗️ Project Architecture

```
ai-world/
├── aurora_ultimate.py      ◄── MAIN GUI (Start Here!)
│                               The window you see, type commands here
│
├── vision_ai_brain.py      ◄── CORE AI BRAIN
│                               Screenshot → LLaVA → Understanding → Action
│
├── smart_executor.py       ◄── COMMAND PROCESSOR
│                               "turn on wifi" → wifi_on action
│
├── action_tracker.py       ◄── SUCCESS/FAILURE TRACKING
│                               Records what worked, what didn't
│
├── autonomous_explorer.py  ◄── AUTO-PILOT MODE
│                               AI explores screen on its own
│
├── agents/
│   ├── mother_ai.py        ◄── MASTER AI (1,527 lines!)
│   │                           Controls everything, makes decisions
│   ├── llm_interface.py    ◄── OLLAMA CONNECTION
│   │                           Talks to local AI models
│   ├── agent_spawner.py    ◄── CREATE HELPER AGENTS
│   │                           Spawn mini-AIs for specific tasks
│   └── event_bus.py        ◄── AGENT COMMUNICATION
│                               Agents talk to each other
│
├── brain/
│   ├── learning_engine.py  ◄── SELF-LEARNING (SQLite DB)
│   │                           Remembers everything forever
│   ├── system_learner.py   ◄── LEARNS YOUR MAC
│   │                           Discovers apps, shortcuts, files
│   ├── nlp_engine.py       ◄── LANGUAGE UNDERSTANDING
│   │                           Parses natural language
│   ├── memory_system.py    ◄── MEMORY STORAGE
│   ├── state_tracker.py    ◄── CURRENT STATE
│   ├── goal_generator.py   ◄── GOAL PLANNING
│   ├── priority_system.py  ◄── TASK PRIORITIES
│   └── resource_tracker.py ◄── SYSTEM RESOURCES (CPU/RAM)
│
├── tools/
│   ├── macos_commands.py   ◄── 100+ MAC COMMANDS
│   │                           Volume, WiFi, Apps, Files, etc.
│   ├── actions/
│   │   ├── gui_control.py  ◄── MOUSE & KEYBOARD
│   │   ├── browser_automation.py ◄── WEB BROWSER CONTROL
│   │   ├── file_ops.py     ◄── FILE OPERATIONS
│   │   ├── web_tools.py    ◄── WEB REQUESTS
│   │   └── code_executor.py ◄── RUN CODE
│   │
│   └── sensors/
│       ├── vision.py       ◄── SCREEN CAPTURE
│       ├── system_monitor.py ◄── CPU/RAM/DISK
│       ├── voice_system.py ◄── SPEAK & LISTEN
│       └── audio.py        ◄── AUDIO OUTPUT
│
├── config/
│   ├── settings.py         ◄── ALL SETTINGS
│   └── founder_protection.py ◄── OWNER SECURITY
│
└── aurora_memory/          ◄── PERSISTENT MEMORY (JSON files)
    ├── learned_actions.json    (90 KB - what actions work)
    ├── action_history.json     (172 KB - all past actions)
    ├── behavior_patterns.json  (176 KB - learned patterns)
    ├── experiences_log.json    (218 KB - all experiences)
    └── ... more memory files
```

---

## 📊 Real Project Data

### Code Statistics
| Metric | Value |
|--------|-------|
| **Total Lines of Code** | 12,592 |
| **Number of Files** | 36 Python files |
| **Project Size** | 1.8 MB |
| **Memory Data** | ~870 KB (learning data) |

### Top 5 Largest Files
| File | Lines | Purpose |
|------|-------|---------|
| `agents/mother_ai.py` | 1,527 | Master AI controller |
| `brain/learning_engine.py` | 1,053 | Self-learning system |
| `tools/macos_commands.py` | 1,020 | 100+ Mac commands |
| `brain/system_learner.py` | 862 | System learning |
| `vision_ai_brain.py` | 758 | Vision AI processing |

### AI Models Used
| Model | Size | Purpose |
|-------|------|---------|
| `llama3.2:3b` | ~2GB | Text understanding, reasoning |
| `llava:7b` | ~4GB | Vision - screen understanding |

### Real Learned Data (from aurora_memory/)

**Acquired Skills:**
| Skill | Practice Count | First Learned |
|-------|---------------|---------------|
| System Control | 283 times | Nov 29, 2025 |
| App Control | 243 times | Nov 29, 2025 |
| Keyboard Control | 151 times | Nov 29, 2025 |
| Other Control | 114 times | Nov 29, 2025 |
| Try Shortcut | 51 times (100% success) | Nov 29, 2025 |
| Clicking | 42 times | Nov 29, 2025 |
| Screenshot | 29 times | Nov 29, 2025 |
| Speech | 28 times | Nov 29, 2025 |

**Memory Files Size:**
| File | Size | Contains |
|------|------|----------|
| experiences_log.json | 218 KB | All experiences |
| behavior_patterns.json | 176 KB | Learned behaviors |
| action_history.json | 172 KB | Every action taken |
| plans_history.json | 144 KB | Planning history |
| learned_actions.json | 90 KB | Successful actions |
| screen_analysis.json | 47 KB | Screen understanding |
| failure_log.json | 9 KB | What failed |

---

## 🎯 Where Can This Project Be Used?

### 1. **Personal Automation Assistant**
- Automate repetitive tasks on your Mac
- "Open Chrome, go to Gmail, check new emails"
- "Download all images from this webpage"

### 2. **Accessibility Tool**
- Help people with disabilities control their computer
- Voice commands → Computer actions
- Screen reader alternative with AI understanding

### 3. **Testing & QA Automation**
- Automated UI testing for macOS apps
- Record and replay user actions
- Detect UI changes with vision AI

### 4. **Workflow Automation**
- Complex multi-step workflows
- "Every morning: Open email, summarize new messages, read them to me"
- "When I say 'meeting mode', mute notifications, open Zoom, share calendar"

### 5. **Educational Tool**
- Learn how AI computer vision works
- Understand NLP command processing
- Study autonomous agent architecture

### 6. **Research Platform**
- AI agent research and development
- Human-computer interaction studies
- Multimodal AI (vision + text + audio)

---

## 🚀 Future Scope & Improvements

### Short Term (1-3 months)
| Feature | Description | Difficulty |
|---------|-------------|------------|
| Multi-Monitor Support | Handle 2+ screens | Medium |
| Better OCR | Read text from screen more accurately | Medium |
| Voice Activation | "Hey Aurora" wake word | Easy |
| Action Recording | Record your actions, replay later | Medium |

### Medium Term (3-6 months)
| Feature | Description | Difficulty |
|---------|-------------|------------|
| Cross-App Workflows | "Copy from Chrome, paste in Word" | Hard |
| Context Memory | Remember what we talked about | Medium |
| Natural Conversations | Multi-turn dialog support | Medium |
| Browser Extension | Deep Chrome/Safari integration | Medium |
| API Integrations | Connect to Slack, Email, Calendar | Medium |

### Long Term (6-12 months)
| Feature | Description | Difficulty |
|---------|-------------|------------|
| iOS Companion App | Control Mac from iPhone | Hard |
| Cloud Sync | Sync learning across devices | Hard |
| Plugin System | Community-created actions | Hard |
| Windows/Linux Port | Cross-platform support | Very Hard |
| Fine-tuned Models | Train custom AI for your workflow | Very Hard |

### Dream Features (12+ months)
| Feature | Description |
|---------|-------------|
| **Predictive Actions** | AI predicts what you want before you ask |
| **Proactive Assistance** | "I noticed you always check email at 9am..." |
| **Natural Collaboration** | Work alongside you, not just execute commands |
| **Multi-Agent Teams** | Multiple AI agents working together on complex tasks |
| **Real-time Learning** | Learn from watching you work |

---

## 🔧 Technical Requirements

### Hardware (Optimized for)
- **Mac**: MacBook Air/Pro M1/M2
- **RAM**: 8GB minimum (models swap to save memory)
- **Storage**: 10GB free (for models + memory)

### Software
- **Python**: 3.9+
- **Ollama**: Local AI runtime
- **Models**: llama3.2:3b, llava:7b
- **macOS**: 12.0+ (Monterey or newer)

### Python Dependencies
```
pyautogui      # Mouse/keyboard control
opencv-python  # Image processing
numpy          # Data processing
requests       # HTTP requests
sqlite3        # Database (built-in)
```

---

## 🏃 How to Run

```bash
# 1. Install Ollama (if not installed)
brew install ollama

# 2. Download AI models
ollama pull llama3.2:3b
ollama pull llava:7b

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start Aurora
python aurora_ultimate.py
```

---

## 🎓 Summary

**Aurora AI** is a sophisticated **macOS automation system** that combines:

1. **Computer Vision** (LLaVA) - Sees and understands your screen
2. **Natural Language Processing** - Understands plain English commands
3. **Self-Learning** - Remembers what works, learns from failures
4. **Full Mac Control** - 100+ commands for complete automation

It's like having an intelligent assistant who can actually USE your computer, not just talk about it!

---

*Project Created by: Karthik*  
*Last Updated: December 2025*  
*Lines of Code: 12,592*  
*Learning Data: 870+ KB accumulated*
