# Self-Evolving Agent

## Overview
An experimental AI agent designed with recursive self-improvement capabilities. This agent can modify its own code or prompt strategies based on performance feedback, theoretically enabling it to adapt to increasingly complex tasks over time.

## Features
-   **Code Modification**: Ability to read and rewrite its own source files.
-   **Performance Loop**: continuous evaluation of task success rates.
-   **Safety Sandbox**: Execution environment to prevent uncontrolled divergence.
-   **Version Control**: Auto-commits changes to track evolutionary history.

## Technology Stack
-   **LLM**: GPT-4 / Claude 3 (via API).
-   **Language**: Python.
-   **System**: Docker for sandboxing.

## Usage Flow
1.  **Initialize**: Agent starts with a base set of capabilities.
2.  **Task**: User assigns a complex goal (e.g., "Optimize your sorting algorithm").
3.  **Reflect**: Agent analyzes its current code and plans an upgrade.
4.  **Evolve**: Agent rewrites the target module and tests it.

## Quick Start
```bash
# Clone the repository
git clone "https://github.com/Nytrynox/Self-Evolv-Agent.git"

# Install dependencies
pip install -r requirements.txt

# Run the agent
python evolve.py
```

## License
MIT License

## Author
**Karthik Idikuda**
