# Agents & Skills Documentation

## 1. Overview
This document details the autonomous agent architecture and custom skills implemented within the repository. The system utilizes a tool-calling primary agent governed by system-level instructions and equipped with specialized capabilities.

---

## 2. Agents

### 2.1 Autonomous System Operator (`app.py`)
* **Role**: Primary execution agent responsible for multi-step reasoning, tool dispatch, and system operations.
* **Model**: Google Gemini 2.5 Flash / Gemini 3.5 Flash Lite (`genai.Client`)
* **Governance**: Constrained by rule sets defined in `constitution.md`.
* **Failover Logic**: Sequentially cycles through `API_KEYS` derived from the `gemini_api` environment variable upon encountering API failures or quota limits.
* **Capabilities**:
  * Evaluates complex multi-step user prompts.
  * Dynamically selects and invokes required skills (tools).
  * Processes tool execution outputs and feeds them back into the conversation context for follow-up actions.
  * Evaluates complex multi-step user prompts.
  * Dynamically selects and invokes required skills (tools).
  * Processes tool execution outputs and feeds them back into the conversation context for follow-up actions.
  * **Native Computer Vision:** Automatically detects image files (`.png`, `.jpg`, `.jpeg`) passed via the `file:` command and processes them using multi-modal byte parsing for visual Q&A and analysis.

---

## 3. Skills (Tools)

### 3.1 Skill: File Editor (`edit_file`)
* **Function**: Modifies or creates local project files based on agent decisions.
* **Parameters**:
  * `path` (*string*): Target file path relative to project root.
  * `content` (*string*): Updated content to write to the file.
* **Usage Pattern**: Used for code refactoring, configuration updates, and markdown document generation.

### 3.2 Skill: Web Scraper (`scrape_web_page`)
* **Function**: Fetches, parses, and extracts clean text from external web URLs.
* **Parameters**:
  * `url` (*string*): Valid HTTP/HTTPS web address.
* **Usage Pattern**: Enables real-time web search, documentation reading, and context expansion for factual accuracy.

### 3.3 Skill: Shell Command Executor (`run_command`)
* **Function**: Runs system shell commands and captures combined stdout/stderr output.
* **Parameters**:
  * `command` (*string*): The terminal command string to execute.
* **Usage Pattern**: Executes tests, linter checks, build scripts, and local environment commands.

---

## 4. Agent-Skill Orchestration Matrix

| Skill | Trigger Condition | Success Output | Error Handling |
| :--- | :--- | :--- | :--- |
| `edit_file` | File creation or content modification needed | Confirmation string with target path | Returns explicit error string to model context |
| `scrape_web_page` | External real-time context required | Cleaned text extract of page body | Catches connection/HTTP errors and reports back |
| `run_command` | Local testing, CI execution, or tool execution | Combined standard output string | Captures return codes and stderr for LLM self-correction |
