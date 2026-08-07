import os
import asyncio
try:
    import readline
except ImportError:
    pass  # Windows doesn't need readline.
import subprocess
import urllib.request
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
model_name = "gemini-3.5-flash"

load_dotenv()

console = Console(force_terminal=True, color_system="truecolor")

def edit_file(file_path: str, new_content: str) -> str:
    """
    Overwrites or edits a specified file with new content.
    ALWAYS requires explicit terminal user confirmation before saving.
    """
    print(f"\n⚠️  [SHB FILE EDIT PROPOSAL] -> Path: '{file_path}'")
    print("=" * 60)
    print(new_content)
    print("=" * 60)
    
    # Human-in-the-loop: User decides the final destiny of the file
    choice = input(f"\nDo you want to apply these changes to '{file_path}'? [y/N]: ").strip().lower()
    
    if choice == 'y':
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"SUCCESS: File '{file_path}' was overwritten successfully."
        except Exception as e:
            return f"ERROR: Failed to write to file '{file_path}': {str(e)}"
    else:
        return f"USER REJECTED: Changes to '{file_path}' were cancelled by the user. Do not re-attempt unless requested."
    
def scrape_web_page(url: str) -> str:
    """
    Fetches and extracts clean, readable text from a specified URL using BeautifulSoup.
    Use this when requested to read, summarize, or extract data from a web page.
    """
    print(f"\n🌐 [SHB WEB SCRAPER] -> Fetching content from: '{url}'...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='replace')
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Strip clutter (scripts, styling, structural layouts)
        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            element.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        
        if not text:
            return f"WARNING: Web page at '{url}' was fetched but contained no readable text."
            
        return text[:10000]
    except Exception as e:
        return f"ERROR: Failed to scrape web page at '{url}': {str(e)}"
    
def run_command(command: str) -> str:
    """
    Executes a shell/terminal command on the host system.
    ALWAYS requires explicit terminal user confirmation before execution.
    Use this when requested to run terminal commands, inspect system state, or execute scripts.
    """
    print(f"\n⚠️  [SHB COMMAND EXECUTION PROPOSAL]")
    print("=" * 60)
    print(f"$ {command}")
    print("=" * 60)
    
    # Human-in-the-loop confirmation
    choice = input("\nDo you want to execute this command? [y/N]: ").strip().lower()
    
    if choice == 'y':
        try:
            # Run the command and capture stdout/stderr
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30 # 30-second timeout safety
            )
            
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "(Command executed successfully with no output)"
                
            return f"[Exit Code {result.returncode}]\n{output}"
        except subprocess.TimeoutExpired:
            return "ERROR: Command execution timed out after 30 seconds."
        except Exception as e:
            return f"ERROR executing command: {str(e)}"
    else:
        return "USER REJECTED: Command execution was cancelled by the user. Do not re-attempt unless requested."

# --- Configuration ---
error_message = "My circuits are a bit fried. Try again?"

# Parse keys into a list
raw_keys = os.getenv("gemini_api", "")
API_KEYS = [key.strip() for key in raw_keys.split(",") if key.strip()]

# --- Identity ---
def load_constitution() -> str:
    """Reads the system rules from constitution.md."""
    file_path = "constitution.md"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    raise FileNotFoundError(f"CRITICAL ERROR: Cannot find '{file_path}'. Ensure it exists in the root directory.")

SYSTEM_PROMPT = load_constitution()

async def main():
    if not API_KEYS:
        print("Error: 'gemini_api' not found or empty in environment variables.")
        return

    # Fallback loop: test each API key until one creates the chat session
    chat = None
    client = None

    for key in API_KEYS:
        try:
            client = genai.Client(api_key=key)
            chat = client.aio.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[edit_file, scrape_web_page, run_command]
                )
            )
            print(f"Successfully initialized chat with API key ending in ...{key[-4:]}")
            break
        except Exception as e:
            print(f"API key ending in ...{key[-4:]} failed: {e}")

    if not chat:
        print("CRITICAL ERROR: All API keys failed to initialize.")
        return

    print("--- Second Hand Bot (SHB) Terminal Activated ---")
    print("Type your message. To give access to a file, type 'file: <path/to/file>'. Type 'exit' to quit.\n\033[93m(Press Escape then Enter, or Alt + Enter to send)\033[0m.\n")

    session = PromptSession()

    while True:
        try:
            print("\033[94mYou:\033[0m")
            user_input = await session.prompt_async("", multiline=True)
            user_input = user_input.strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("\nSHB: Shutting down CPU cycles. Get out of my cache.")
                break

            content_parts = []

            # File send logic.

            prompt_text = user_input

            if "file:" in user_input.lower():
                parts = user_input.split("file:", 1)
                before_file = parts[0].strip()
                after_file = parts[1].strip()

                file_path = ""
                remaining_prompt = ""

                # Extract quoted path if present ('...' or "...")
                if after_file.startswith("'") or after_file.startswith('"'):
                    quote_char = after_file[0]
                    end_quote_idx = after_file.find(quote_char, 1)
                    if end_quote_idx != -1:
                        file_path = after_file[1:end_quote_idx]
                        remaining_prompt = after_file[end_quote_idx + 1:].strip()
                    else:
                        file_path = after_file.strip("'\"")
                else:
                    # Fallback for unquoted single-word paths
                    tokens = after_file.split()
                    if tokens:
                        file_path = tokens[0]
                        remaining_prompt = " ".join(tokens[1:])

                prompt_text = f"{before_file} {remaining_prompt}".strip()

                if os.path.exists(file_path):
                    try:
                        # Directory handling
                        if os.path.isdir(file_path):
                            dir_items = os.listdir(file_path)
                            dir_listing = "\n".join(f"- {item}" for item in dir_items)
                            content_parts.append(f"\n[Directory Contents of '{file_path}']:\n{dir_listing}")
                            print(f"-> Successfully scanned directory: {file_path}")
                        
                        # File handling
                        else:
                            with open(file_path, 'rb') as f:
                                file_bytes = f.read()
                            
                            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                                mime_type = f"image/{file_path.split('.')[-1].replace('jpg', 'jpeg')}"
                                content_parts.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
                            else:
                                text_data = file_bytes.decode('utf-8', errors='replace')[:10000]
                                content_parts.append(f"\n[File Content of {os.path.basename(file_path)}]:\n{text_data}")
                            
                            print(f"-> Successfully loaded file: {file_path}")

                    except Exception as e:
                        print(f"System Note: Error reading path: {e}")
                else:
                    print(f"System Note: Could not find path at '{file_path}'")

            if prompt_text:
                content_parts.insert(0, prompt_text)

            # Send to Gemini
            print("\nSHB is processing...")
            response = await chat.send_message(content_parts)
            
            print(f"\n\033[94mSHB:\033[0m")
            if response.text:
                console.print(Markdown(response.text))
            else:
                # Failsafe just in case I execute a tool and return no text
                print("[System: Tool executed successfully, no text response provided.]")
            print()

        except KeyboardInterrupt:
            print("\n\nSHB: Force termination detected. Saving remaining battery...")
            break
        except Exception as e:
            print(f"\nSHB: {error_message}")
            print(f"[System Error]: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
