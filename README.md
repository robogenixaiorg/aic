# AgentBalu - AI Commit Message Generator

AgentBalu is a Python-based tool that uses AI to generate concise and informative Git commit messages based on staged changes. It's designed to simplify the commit process and improve commit quality for developers.

---

## Features

- Automatically analyzes staged Git changes to generate meaningful commit messages.
- Utilizes a remote AI model for commit message generation.
- Lightweight and easy to integrate into any development workflow.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/AgentBalu.git
   cd AgentBalu

2. **Setup environment variables for API_KEY and API_URL**:
    * For linux/MacOS:
        1. setup environment variables
        `export AI_API_KEY="your_api_key_here"`
        `export AI_API_URL="https://your.api.url"`

        2. reload shell
        `source ~/.bashrc`

    * For Windows(Powershell):
        1. setup environment variables
        `$env:AI_API_KEY="your_api_key_here"`
        `$env:AI_API_URL="https://your.api.url"`


2. **Setup the Package**:
    ```bash
    make setup

3. 