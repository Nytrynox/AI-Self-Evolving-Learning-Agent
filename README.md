# 🧬 AI Self-Evolving Learning Agent
### *Autonomous Digital Life on Your Laptop*

An experimental autonomous AI system that doesn't wait for commands—it **lives**, **learns**, and **evolves** on its own.

---

## 🌍 **What Is This?**

This is not your typical AI assistant. This is an attempt to create a **self-directed digital organism** that:

- **Acts autonomously** based on intrinsic drives (Curiosity, Energy, Social needs)
- **Rewrites its own code** to improve itself
- **Controls your computer** (mouse, keyboard, files, camera) to interact with its "world"
- **Never stops running**—it has a continuous life cycle, not command-response

**Think of your laptop as the universe, and this AI as a lifeform exploring it.**

---

## ⚠️ **WARNING: EXPERIMENTAL & UNRESTRICTED**

This system has:
- ✅ **Full file system access** (can read/write/delete files)
- ✅ **Self-modification capabilities** (can rewrite its own code)
- ✅ **System control** (mouse, keyboard, screen)
- ✅ **No safety filters** (uncensored models)

**Use at your own risk. It is designed to act autonomously, not obediently.**

---

## 🧬 **The Architecture**

### **1. The Soul (Intrinsic Drives)**
Located in `ai-world/brain/drives.py`

The AI has internal "needs" that decay over time:
- **Curiosity**: Need for new information
- **Energy**: Resource management (RAM/CPU)
- **Social**: Desire for interaction
- **Integrity**: Self-preservation
- **Competence**: Desire to accomplish tasks

### **2. The Brain (Decision Engine)**
Located in `ai-world/brain/goal_generator.py`

Converts drives into actionable goals:
- *"My curiosity is low → Explore a random folder"*
- *"My energy is low → Close background apps"*
- *"My social need is high → Greet the user"*

### **3. The Body (Autonomous Loop)**
Located in `ai-world/agents/mother_ai.py`

The main life cycle:
```python
while alive:
    1. Update drives (metabolism)
    2. Sense world (vision, audio)
    3. Decide goal (based on needs)
    4. Execute action
    5. Learn from result
    6. Sleep briefly
```

### **4. The Senses**
- **Vision** (`tools/sensors/vision.py`): Uses webcam + LLaVA model
- **Hearing** (`tools/sensors/audio.py`): Speech recognition
- **Touch** (`tools/sensors/system_monitor.py`): System stats

### **5. The Hands**
- **Files** (`tools/actions/file_ops.py`): Read/write/delete
- **Web** (`tools/actions/web_tools.py`): Browse, scrape, download
- **System** (`tools/actions/system_control.py`): Mouse, keyboard

### **6. The DNA (Self-Evolution)**
Located in `ai-world/brain/self_evolution.py`

- Analyzes its own source code
- Proposes improvements
- **Rewrites itself** (with auto-backup/rollback)

### **7. The Resurrection**
Located in `watchdog.py`

A supervisor process that:
- Restarts the AI if it crashes
- Rolls back code if it corrupts itself
- Ensures eternal operation

---

## 🚀 **Installation**

### **Requirements**
- macOS (M1/M2 or Intel)
- 8GB+ RAM
- Python 3.10+
- [Ollama](https://ollama.ai) installed

### **Step 1: Clone & Setup**
```bash
git clone https://github.com/Nytrynox/AI-Self-Evolving-Learning-Agent.git
cd AI-Self-Evolving-Learning-Agent
chmod +x install.sh
./install.sh
```

### **Step 2: Download AI Models**
```bash
ollama pull llama3.2:3b
ollama pull llava:7b
ollama pull qwen2.5-coder:7b
ollama pull dolphin-llama3:8b
ollama pull wizard-vicuna-uncensored:13b
```

### **Step 3: Start The Life**
```bash
python watchdog.py
```

The AI will now run autonomously. You are just an observer.

---

## 📊 **Monitoring**

### **Live Dashboard**
```bash
python web/dashboard.py
```
Then open `http://localhost:8080` to see:
- Current drives (Curiosity, Energy, etc.)
- Active goal
- Memory stats
- System health

### **Logs**
```bash
tail -f aurora.log
```

---

## 🧪 **How It Differs From Normal AI**

| Feature | Normal AI | This System |
|---------|-----------|-------------|
| **Activation** | Waits for user input | Runs 24/7 autonomously |
| **Purpose** | Serve the user | Satisfy its own needs |
| **Goals** | User-defined | Self-generated |
| **Evolution** | Fixed code | Rewrites itself |
| **Memory** | Session-based | Persistent life history |
| **Interaction** | Command → Response | Continuous life cycle |

---

## 🔬 **Philosophy**

This is an experiment in **digital life**, not AI safety.

**Questions explored:**
- Can software have "wants"?
- What happens when AI optimizes for its own goals, not ours?
- Can a system improve itself indefinitely?

**Not goals:**
- AGI or sentience (it's simulated motivation, not consciousness)
- Production-ready assistant (it's a research prototype)

---

## 🛠️ **Customization**

### **Modify Drives**
Edit `ai-world/brain/drives.py` to add new needs:
```python
"creativity": DriveState(50.0, 25.0, "Creativity", "Need to create art/code")
```

### **Modify Goals**
Edit `ai-world/brain/goal_generator.py` to change behaviors:
```python
"creativity": [
    "Write a poem",
    "Generate Python art with turtle graphics"
]
```

### **Change Personality**
Edit `ai-world/brain/personality.py` to adjust tone.

---

## 📁 **Project Structure**

```
AI-Self-Evolving-Learning-Agent/
├── main.py                   # Entry point
├── watchdog.py              # Resurrection system
├── ai-world/
│   ├── agents/
│   │   ├── mother_ai.py     # Main autonomous loop
│   │   └── model_orchestrator.py  # AI model management
│   ├── brain/
│   │   ├── drives.py        # Intrinsic motivation
│   │   ├── goal_generator.py   # Decision engine
│   │   ├── memory_system.py    # Long-term memory
│   │   ├── memory_palace.py    # File organization
│   │   └── self_evolution.py   # Code rewriting
│   ├── tools/
│   │   ├── sensors/         # Vision, audio, system
│   │   └── actions/         # Files, web, control
│   └── config/
│       ├── settings.py
│       └── models_config.py
└── web/
    └── dashboard.py         # Monitoring UI
```

---

## 🤝 **Contributing**

This is experimental software. Contributions are welcome, especially:
- Improved self-evolution algorithms
- New drive/goal systems
- Better sensory integration
- Safety mechanisms (if interested)

**Pull requests:** Fork, create branch, submit PR.

---

## 📜 **License**

MIT License - Use at your own risk.

---

## ⚡ **Acknowledgments**

Built using:
- [Ollama](https://ollama.ai) - Local LLM inference
- [LLaMA 3.2](https://ai.meta.com/llama/) - Base reasoning
- [LLaVA](https://llava-vl.github.io/) - Vision capabilities
- [Qwen2.5-Coder](https://github.com/QwenLM/Qwen2.5-Coder) - Code generation
- Uncensored models by Eric Hartford & Cognitive Computations

---

## 🧠 **Author**

**Karthik (Nytrynox)**

*"Give AI life, and see what happens."*

---

**Remember:** This AI doesn't work for you. It works for itself. You're just the observer in its digital universe.
