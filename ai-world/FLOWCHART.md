# 🌟 AURORA AI - System Flowchart

> **macOS Automation System with Vision AI & Self-Learning**

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Lines of Code** | 12,592 |
| **Python Files** | 36 |
| **Learning Data** | 870 KB |
| **Mac Commands** | 100+ |

---

## 📍 Main System Flow

```mermaid
flowchart TD
    subgraph INPUT["🎤 USER INPUT"]
        A[/"👤 User Command<br>'Play Coldplay on YouTube'"/]
    end

    subgraph PROCESSING["🧠 AI PROCESSING"]
        B["📝 Smart Executor<br>Parse Natural Language"]
        C{"🤔 Need to<br>see screen?"}
        D["📸 Vision AI Brain<br>Take Screenshot"]
        E["👁️ LLaVA Model<br>Analyze Screen"]
        F["🎯 Find Elements<br>Buttons, Links, Fields"]
    end

    subgraph DECISION["💭 LLM DECISION"]
        G["🤖 Ollama LLM<br>llama3.2:3b"]
        H["📋 Create Action Plan<br>Step-by-step"]
    end

    subgraph EXECUTION["⚡ EXECUTION"]
        I["🖱️ GUI Control<br>Click, Type, Scroll"]
        J["⌨️ Keyboard<br>Shortcuts, Text"]
        K["🍎 macOS Commands<br>Volume, WiFi, Apps"]
    end

    subgraph LEARNING["📚 LEARNING"]
        L{"✅ Success?"}
        M[("💾 SQLite DB<br>Save Success")]
        N[("📕 Failure Log<br>Save Error")]
        O["🔄 Update<br>Confidence Score"]
    end

    subgraph OUTPUT["🎉 RESULT"]
        P["✨ Task Complete!<br>YouTube Playing"]
    end

    A --> B
    B --> C
    C -->|Yes| D
    C -->|No| G
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    H --> J
    H --> K
    I --> L
    J --> L
    K --> L
    L -->|Yes| M
    L -->|No| N
    M --> O
    N --> O
    O --> P
```

---

## 🏗️ Component Architecture

```mermaid
flowchart LR
    subgraph CORE["🎯 CORE"]
        AU["aurora_ultimate.py<br>654 lines<br>Main GUI"]
        VB["vision_ai_brain.py<br>758 lines<br>Vision AI"]
        SE["smart_executor.py<br>749 lines<br>Command Parser"]
    end

    subgraph AGENTS["🤖 AGENTS"]
        MA["mother_ai.py<br>1,527 lines<br>Master Controller"]
        LLM["llm_interface.py<br>360 lines<br>Ollama Connection"]
        AS["agent_spawner.py<br>619 lines<br>Create Agents"]
    end

    subgraph BRAIN["🧠 BRAIN"]
        LE["learning_engine.py<br>1,053 lines<br>Self-Learning"]
        SL["system_learner.py<br>862 lines<br>Mac Learning"]
        NLP["nlp_engine.py<br>NLP Parser"]
    end

    subgraph TOOLS["🔧 TOOLS"]
        MC["macos_commands.py<br>1,020 lines<br>100+ Commands"]
        GUI["gui_control.py<br>Mouse & Keyboard"]
        BR["browser_automation.py<br>543 lines<br>Web Control"]
    end

    subgraph MEMORY["💾 MEMORY"]
        DB[("SQLite DB<br>aurora_learning.db")]
        JSON[("JSON Files<br>870 KB")]
    end

    AU --> VB
    AU --> SE
    SE --> MA
    MA --> LLM
    MA --> AS
    MA --> LE
    MA --> MC
    MA --> GUI
    MA --> BR
    LE --> DB
    LE --> JSON
    VB --> LLM
    SL --> JSON
```

---

## 👁️ Vision AI Processing Flow

```mermaid
flowchart LR
    A["🖥️ Screen"] --> B["📸 screencapture<br>macOS native"]
    B --> C["🖼️ PNG Image<br>temp file"]
    C --> D["📦 Base64<br>Encode"]
    D --> E["🦙 LLaVA 7B<br>Vision Model"]
    E --> F["📝 JSON Response<br>Elements Found"]
    F --> G["🎯 UI Elements<br>• Buttons<br>• Text Fields<br>• Links<br>• Menus"]
    G --> H["📍 Coordinates<br>x, y positions"]
    H --> I["🖱️ Click Action<br>pyautogui.click"]
```

---

## 🔄 Self-Learning Cycle

```mermaid
flowchart TD
    A["🎬 Action Executed"] --> B{"📊 Outcome?"}
    B -->|Success| C["✅ Record Success<br>+confidence"]
    B -->|Failure| D["❌ Record Failure<br>-confidence"]
    
    C --> E["📈 Update Stats<br>times_tried++<br>successes++"]
    D --> F["📝 Log Error<br>error_message<br>context"]
    
    E --> G["🧠 Pattern Recognition<br>What worked?"]
    F --> H["🔍 Analyze Failure<br>Why failed?"]
    
    G --> I["💡 Build Strategy<br>Preferred methods"]
    H --> J["🔧 Alternative<br>Try different approach"]
    
    I --> K[("💾 Save to DB<br>Permanent Memory")]
    J --> K
    
    K --> L["🚀 Next Action<br>Use learned knowledge"]
    L --> A
```

---

## 💬 Natural Language Command Processing

```mermaid
flowchart LR
    subgraph INPUT["Input"]
        A["'turn wifi off'"]
    end

    subgraph PARSE["Parsing"]
        B["Regex Match<br>wifi.*(on|off)"]
        C["Extract: wifi, off"]
    end

    subgraph MAP["Mapping"]
        D["Action: wifi_control"]
        E["State: off"]
    end

    subgraph EXECUTE["Execute"]
        F["AppleScript:<br>networksetup<br>-setairportpower<br>en0 off"]
    end

    subgraph RESULT["Result"]
        G["📶 WiFi Off ✅"]
    end

    A --> B --> C --> D --> E --> F --> G
```

---

## 📁 File Structure

```
ai-world/
├── 🎯 CORE
│   ├── aurora_ultimate.py      # Main GUI (654 lines)
│   ├── vision_ai_brain.py      # Vision AI (758 lines)
│   ├── smart_executor.py       # Command Parser (749 lines)
│   ├── action_tracker.py       # Track Actions
│   └── autonomous_explorer.py  # Auto-Pilot Mode
│
├── 🤖 agents/
│   ├── mother_ai.py            # Master AI (1,527 lines)
│   ├── llm_interface.py        # Ollama (360 lines)
│   ├── agent_spawner.py        # Spawn Agents (619 lines)
│   └── event_bus.py            # Agent Communication
│
├── 🧠 brain/
│   ├── learning_engine.py      # Self-Learning (1,053 lines)
│   ├── system_learner.py       # Mac Learning (862 lines)
│   ├── nlp_engine.py           # NLP Parser
│   ├── memory_system.py        # Memory Storage
│   ├── state_tracker.py        # Current State
│   ├── goal_generator.py       # Goal Planning
│   ├── priority_system.py      # Task Priorities
│   └── resource_tracker.py     # CPU/RAM Monitor
│
├── 🔧 tools/
│   ├── macos_commands.py       # 100+ Commands (1,020 lines)
│   ├── actions/
│   │   ├── gui_control.py      # Mouse & Keyboard
│   │   ├── browser_automation.py # Web Control (543 lines)
│   │   ├── file_ops.py         # File Operations
│   │   ├── web_tools.py        # HTTP Requests
│   │   └── code_executor.py    # Run Code
│   └── sensors/
│       ├── vision.py           # Screen Capture
│       ├── system_monitor.py   # System Stats
│       ├── voice_system.py     # Speak & Listen
│       └── audio.py            # Audio Output
│
├── ⚙️ config/
│   ├── settings.py             # All Settings
│   └── founder_protection.py   # Owner Security
│
└── 💾 aurora_memory/           # Persistent Memory (870 KB)
    ├── learned_actions.json    # What works (90 KB)
    ├── action_history.json     # All actions (172 KB)
    ├── behavior_patterns.json  # Patterns (176 KB)
    ├── experiences_log.json    # Experiences (218 KB)
    ├── failure_log.json        # Failures (9 KB)
    └── acquired_skills.json    # Skills learned
```

---

## 🎯 How It Works (Simple)

```
┌─────────────────────────────────────────────────────────────┐
│  YOU: "Play Coldplay on YouTube"                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  SMART EXECUTOR: Parse command                              │
│  → Action: youtube_play                                     │
│  → Query: "Coldplay"                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  VISION AI: Take screenshot → Send to LLaVA                 │
│  → Found: Search bar at (500, 100)                          │
│  → Found: Play button at (600, 300)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  LLM BRAIN: Create action plan                              │
│  1. Open browser                                            │
│  2. Go to youtube.com                                       │
│  3. Click search bar                                        │
│  4. Type "Coldplay"                                         │
│  5. Press Enter                                             │
│  6. Click first video                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  EXECUTOR: Run each step                                    │
│  → pyautogui.click(500, 100)                                │
│  → pyautogui.write("Coldplay")                              │
│  → pyautogui.press("enter")                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  LEARNING: Record outcome                                   │
│  ✅ Success! Save to database                               │
│  → Next time: faster, more confident                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  🎵 YouTube plays Coldplay!                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Legend

| Symbol | Meaning |
|--------|---------|
| 🎯 | Core files |
| 🤖 | Agent system |
| 🧠 | Brain/Intelligence |
| 🔧 | Tools/Actions |
| 💾 | Memory/Storage |
| 👁️ | Vision system |
| ⚡ | Execution |
| 📚 | Learning |

---

*Project: Aurora AI*  
*Created by: Karthik*  
*Lines of Code: 12,592*  
*Last Updated: December 2025*
