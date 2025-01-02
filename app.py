import os
import subprocess
import sys
import ollama


commands = {
    "is_git_repo": ["git", "rev-parse", "--git-dir"],
    "clear_screen": ["cls" if os.name == "nt" else "clear"],
    "commit": ["git", "commit", "-m"],
    "get_stashed_changes": ["git", "diff", "--cached"],
}


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
        print("\nStaged Changes:\n")
        print(staged_changes)

    except KeyboardInterrupt:
        print("\n\n❌ AI commit exited.")


if __name__ == "__main__":
    run()
