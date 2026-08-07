# Second Hand Bot (SHB)

Second Hand Bot is a terminal-based AI assistant that uses Google Gemini to help with coding and system tasks. It can read files, scrape web pages, and propose shell commands or file edits, while keeping the user in control through confirmation prompts.

## Overview

SHB is implemented as an interactive CLI application in [app.py](app.py). The bot is guided by a constitution-style system prompt in [constitution.md](constitution.md) and can:

- chat with a Gemini model from the terminal
- read local files and directories when you include a path like `file: ./app.py`
- scrape readable text from web pages
- propose file edits and shell commands for explicit user approval

## What the project does

This repository is a lightweight autonomous agent prototype with a human-in-the-loop workflow. The main agent behavior is centered around three tool-like capabilities:

- File editing via `edit_file`
- Web scraping via `scrape_web_page`
- Shell command execution via `run_command`

These capabilities are wired into the Gemini chat session in [app.py](app.py), and the system prompt in [constitution.md](constitution.md) instructs the agent to use them when appropriate.

## Project structure

- [app.py](app.py) - Main CLI application and tool wiring
- [constitution.md](constitution.md) - System instructions for the agent
- [PRD.md](PRD.md) - Product requirements and user stories
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture notes and skill orchestration
- [AGENTS_AND_SKILLS.md](AGENTS_AND_SKILLS.md) - Agent and skill documentation
- [tests/test_ui.py](tests/test_ui.py) - Current smoke test for a browser UI expectation
- [pyproject.toml](pyproject.toml) - Poetry project metadata and dependencies
- [requirements.txt](requirements.txt) - Runtime dependencies

## Requirements

The project expects Python 3.13+ and the following packages:

- google-genai
- python-dotenv
- beautifulsoup4
- rich
- prompt_toolkit

You can install them via Poetry or pip.

## Installation

### Clone the repository

#### Linux

```bash
git clone https://github.com/ProRick2358Y/SHB_CLI && cd SHB_CLI/
```

#### Windows

```powershell
git clone https://github.com/ProRick2358Y/SHB_CLI
cd SHB_CLI
```

### With Poetry

```bash
poetry install
```

### With pip

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your Gemini API key:

```env
gemini_api=your_api_key_here
```

The app also supports a comma-separated list of API keys for fallback behavior:

```env
gemini_api=key_one,key_two,key_three
```

## Running the app

### With Poetry

```bash
poetry run python app.py
```

### With Python directly

```bash
python app.py
```

## API cost and model notes

Keep in mind that Gemini API usage is not free and may change over time. Review pricing and usage limits regularly, especially if you plan to use the bot frequently.

You can change the model by editing the `model_name` variable near the top of [app.py](app.py).

For current rate limits and model-specific details, check:

- https://ai.google.dev/gemini-api/docs/rate-limits

## Local hosting guides

### Linux (Debian/Ubuntu-based)

```bash
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

To stop the bot, use `exit` or press `Ctrl + C`.

To deactivate the virtual environment:

```bash
deactivate
```

To remove the virtual environment, delete the `venv` folder.

### Windows

```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If you are using Command Prompt instead of PowerShell:

```cmd
venv\Scripts\activate.bat
```

### Android (Termux)

```bash
termux-setup-storage
pkg update && pkg upgrade
pkg install binutils python-pip rust build-essential openssl libffi
pip install --upgrade pip setuptools wheel
pkg install python-cryptography
export ANDROID_API_LEVEL=24
export CARGO_BUILD_TARGET=aarch64-linux-android
pip install -r requirements.txt
python3 app.py
```

## Minimal files required in the bot directory

At minimum, keep these files in the project root:

- `.env`
- `app.py`
- `constitution.md`
- `requirements.txt`
