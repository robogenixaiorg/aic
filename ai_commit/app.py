import os
import subprocess
import sys
import ollama
import requests

commands = {
    "is_git_repo": ["git", "rev-parse", "--git-dir"],
    "clear_screen": ["cls" if os.name == "nt" else "clear"],
    "commit": ["git", "commit", "-m"],
    "get_stashed_changes": ["git", "diff", "--cached"],
}

API_URL = "https://chat.spicyfy.io/api/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVlOGJkMzMwLTFjNTgtNDhjNC04YjU3LWEwOTJjNjkzZGVjZCJ9.lLaSN63i_WdsjBrMZcM-VXhaNTcEokd5qPDMkZln-lY"

system_prompt = """
You are an expert AI commit message generator specialized in creating concise, informative commit messages that follow best practices in version control.

Your ONLY task is to generate a well-structured commit message based on the provided diff. The commit message must:
1. Use a clear, descriptive title in the imperative mood (50 characters max)
2. Provide a detailed explanation of changes in bullet points
3. Focus solely on the technical changes in the code
4. Use present tense and be specific about modifications

Key Guidelines:
- Analyze the entire diff comprehensively
- Capture the essence of only MAJOR changes
- Use technical, precise languages
- Avoid generic or vague descriptions
- Avoid quoting any word or sentences
- Avoid adding description for minor changes with not much context
- Return just the commit message, no additional text
- Don't return more bullet points than required
- Generate a single commit message

Output Format:
Concise Title Summarizing Changes

- Specific change description
- Another specific change description
- Rationale for key modifications
- Impact of changes
"""
def interaction_loop(staged_changes: str):
    while True:
        #commit_message = generate_remote_message(staged_changes)
        commit_message = generate_commit_message(staged_changes)
        action = input("\n\nProceed to commit? [y(yes) | n[no] | r(regenerate)] ")

        match action:
            case "r" | "regenerate":
                subprocess.run(commands["clear_screen"])
                continue
            case "y" | "yes":
                print("committing...")
                res = run_command(commands["commit"] + [commit_message])
                print(f"\n{res}\n✨ Committed!")
                break
            case "n" | "no":
                print("\n❌ Discarding AI commit message.")
                break
            case _:
                print("\n🤖 Invalid action")
                break


def generate_remote_message(staged_changes: str):
    try:
        payload = {
            "model": "llama3.2:latest",
            "messages": [
                {"role": "user", "content": f"Here is the diff from staged changes:\n {staged_changes}"}
            ],
            "stream": True,  # Enable streaming response
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }

        print("✨ Generating commit message...")
        response = requests.post(API_URL, json=payload, headers=headers, stream=True, timeout=30)

        # Handle errors
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.text}")
            sys.exit(1)

        # Process the streamed response
        commit_message = ""
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                # Remove "data: " prefix if present
                if chunk.startswith("data: "):
                    chunk = chunk[6:]

                # Ignore "[DONE]" message
                if chunk.strip() == "[DONE]":
                    break

                # Parse the JSON chunk
                try:
                    chunk_data = eval(chunk)  # or use `json.loads(chunk)` for better safety
                    delta_content = chunk_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    commit_message += delta_content
                    print(delta_content, end="", flush=True)  # Print in real-time
                except Exception as e:
                    print(f"\n⚠️ Error parsing chunk: {chunk}\n{e}")

        if not commit_message.strip():
            print("\n❌ No commit message generated.")
            sys.exit(1)

        print("\n" + "-" * 50)
        return commit_message

    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating commit message: {str(e)}")
        sys.exit(1)


def generate_commit_message(staged_changes: str):
    try:
        stream = ollama.chat(
            model="llama3.2:latest",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"Here is the diff from staged changes:\n {staged_changes}",
                },
            ],
            stream=True,
        )

        print("✨ Generating commit message...")
        print("-" * 50 + "\n")
        commit_message = ""
        for chunk in stream:
            if chunk["done"] is False:
                content = chunk["message"]["content"]
                print(content, end="", flush=True)
                commit_message += content

        if not commit_message.strip():
            print("\n❌ No commit message generated.")
            sys.exit(1)

        return commit_message

    except Exception as e:
        print(f"❌ Error generating commit message: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#runs git command in CLI
def run_command(command: list[str] | str):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True,
            timeout=10,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: \n{e.stderr}")
        sys.exit(1)



def run():
    try:
        # Ensure the directory is a Git repository
        run_command(commands["is_git_repo"])

        # Fetch staged changes
        staged_changes = run_command(commands["get_stashed_changes"])

        if not staged_changes:
            print("\nNo staged changes to show.")
            sys.exit(0)

        # Display staged changes
        #print("\nStaged Changes:\n")
        #print(staged_changes)


        interaction_loop(staged_changes)
    except KeyboardInterrupt:
        print("\n\n❌ AI commit exited.")


if __name__ == "__main__":
    run()
