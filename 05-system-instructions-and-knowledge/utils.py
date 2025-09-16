import os
import glob


def load_system_instructions():
    """Load system instructions from system-instructions.md file."""
    try:
        with open("system-instructions.md", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("⚠️  system-instructions.md not found, using default instructions")
        return "You are a helpful AI assistant."


def load_knowledge_base():
    """Load all markdown files from data directory as knowledge base."""
    knowledge_base = ""
    data_dir = "data"

    if os.path.exists(data_dir):
        # Get all .md files in data directory
        md_files = glob.glob(os.path.join(data_dir, "*.md"))

        if md_files:
            knowledge_base += "\n\n# KNOWLEDGE BASE:\n"
            for file_path in sorted(md_files):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read().strip()
                        filename = os.path.basename(file_path)
                        knowledge_base += f"\n## {filename}:\n{content}\n"
                except Exception as e:
                    print(f"⚠️  Could not read {file_path}: {e}")
        else:
            print("⚠️  No .md files found in data directory")
    else:
        print("⚠️  Data directory not found")

    return knowledge_base