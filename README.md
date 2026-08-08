# SHB CLI

> An AI-powered command-line assistant built during the GDG Hackathon.

---

## About the Project

SHB CLI (Second-Hand Bot CLI) is an intelligent command-line assistant developed as part of a hackathon project. It demonstrates how Large Language Models (LLMs) can interact with a local system through a secure and user-friendly terminal interface.

Unlike a traditional chatbot, SHB CLI can understand natural language instructions and perform real tasks such as executing shell commands, managing files, retrieving information from the web, and assisting developers directly from the terminal. It can even make sense out of images.

To ensure safety, every potentially sensitive operation requires explicit user confirmation before execution.

---

## Features

- AI-powered command-line assistant using Google Gemini
- Execute shell commands with user confirmation
- Create, edit, and manage local files
- Make sense out of images
- Retrieve and summarize web content
- Rich Markdown output in the terminal
- Automatic API key failover support
- Lightweight and developer-friendly
- Cross-platform support (Linux, Windows, and Android via Termux)

---

## Tech Stack

- Python 3.10+
- Google Gemini API
- Rich
- BeautifulSoup4
- Prompt Toolkit
- python-dotenv

---

# Installation Guide

> **Note**
>
> Google Gemini APIs are subject to rate limits, are not free, or forever. Be sure to update it from time to time. You can change the model by editing the variable `model_name` near the top of `app.py`.
>
> Rate Limits:
> https://ai.google.dev/gemini-api/docs/rate-limits

---

## Clone the Repository

### Linux

```bash
git clone https://github.com/ProRick2358Y/SHB_CLI.git
cd SHB_CLI
```

### Windows

```cmd
git clone https://github.com/ProRick2358Y/SHB_CLI.git
cd SHB_CLI
```

---

## Existing Project

If you already have the project files instead of cloning the repository, ensure the following files are present in the project directory:

```
.env
app.py
constitution.md
requirements.txt
```

---

## Enter Gemini Keys

Go to the root directory of the project and edit the filename of `.env.example` to `.env` and add actual Gemini Keys inside the placeholders of the keys inside the file. Here is an overview of the `.env.example`:

```
# Put actual Gemini Keys in the placeholders before running app.py. You need at least 1 key, and can add as many as you wish as long as they are legit.
gemini_api="AIzaSyD...Key1, AIzaSyD...Key2"

```

### **Note:
 If you are having trouble changing the filename, you can try the same using CLI -


**Linux & Android (Termux):**
```bash
mv .env.example .env
```

**Windows (Command Prompt):**
```cmd
ren .env.example .env
```

**Windows (PowerShell):**
```powershell
Rename-Item .env.example .env
```

---

## Linux Installation

**Tested on Ubuntu 26.04 and Fedora 44**

### Install Python and Virtual Environment

```bash
sudo apt install python3 python3-venv python3-pip -y
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Bot

```bash
python3 app.py
```

### Stop the Bot

```text
Ctrl + C
```

### Deactivate the Virtual Environment

```bash
deactivate
```

To completely remove the virtual environment:

```bash
rm -rf venv
```

---

## Windows Installation

**Tested on Windows 11 25H2**

Install Python 3.10 or later from:

https://www.python.org/

Or the Microsoft Store.

During installation, enable **"Add Python to PATH."**

Open Command Prompt or PowerShell inside the project directory.

### Create a Virtual Environment

```powershell
python -m venv venv
```

### Activate (PowerShell)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

### Activate (Command Prompt)

```cmd
venv\Scripts\activate.bat
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the Bot

```bash
python app.py
```

### Stop the Bot

```text
Ctrl + C
```

---

## Android (Termux)

**Tested on Android 16**

Install Termux.

Grant storage permission:

```bash
termux-setup-storage
```

Skip virtual environment creation.

### Install Required Packages

```bash
pkg update && pkg upgrade

pkg install binutils python-pip rust build-essential openssl libffi

pip install --upgrade pip setuptools wheel

pkg install python-cryptography

export ANDROID_API_LEVEL=24
export CARGO_BUILD_TARGET=aarch64-linux-android
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Bot

```bash
python3 app.py
```

### Stop the Bot

```text
Ctrl + C
```

---

## Project Structure

```
SHB_CLI/
│
├── app.py
├── requirements.txt
├── constitution.md
├── .env
├── LICENSE
├── README.md
├── ARCHITECTURE.md
├── PRD.md
├── TASK_BREAKDOWN.md
└── tests/
```

---

## Future Improvements

- Additional AI tools
- Plugin support
- Better file management and file support
- More automation capabilities
- Improved terminal interface
- Expanded platform support

---

## Hackathon Project

This project was developed during a hackathon to explore how AI can be integrated into the command line to create a powerful and secure assistant. We tried to stick to the **Knowledge and Compliance Agents** path of the Hackathon, but the Bot surely is compliant with the other paths of **Developer Productivity Tools** and **Business Process Automation** as it can assist the developers for the former, and can write scripts for the latter one.

The primary objective was to build a practical CLI tool capable of understanding natural language, having a computer vision, and interacting with the local system while maintaining user safety through explicit confirmation before sensitive operations.

---

## Credits

Developed by the SHB CLI Team.

Special thanks to everyone who contributed ideas, testing, and feedback during the hackathon.

---

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.
