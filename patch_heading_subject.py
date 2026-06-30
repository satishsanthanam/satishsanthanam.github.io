#!/usr/bin/env python3
import os
import re

TARGET_DIR = "."
EXCLUDE_DIRS = {'.git', '.github', 'node_modules', 'factory-builds', 'pagefind'}

def bulk_inject_subjects():
    print("🚀 Initiating global <h1> subject injection pass...")
    updated_count = 0

    # Walk through the directories
    for root, dirs, files in os.walk(TARGET_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        rel_path = os.path.relpath(root, TARGET_DIR)
        if rel_path == ".":
            continue
            
        path_parts = rel_path.split(os.sep)
        # We need at least the subject directory level
        if len(path_parts) >= 1:
            # Format directory name to clean subject (e.g., "social-sciences" -> "Social Sciences")
            subject_name = path_parts[0].replace('-', ' ').title()
            
            for file in files:
                if file.endswith(".html") and file != "index.html" and file != "search.html":
                    filepath = os.path.join(root, file)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Target <h1> tags that don't already have the subject prefix
                    # This protects the script if you accidentally run it twice (Idempotence)
                    h1_pattern = r'<h1>(?!' + re.escape(subject_name) + r':)'
                    
                    if re.search(h1_pattern, content):
                        # Replace <h1> with <h1>Subject Name: 
                        updated_content = re.sub(h1_pattern, f'<h1>{subject_name}: ', content)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        updated_count += 1

    print(f"✅ Successfully patched {updated_count} sub-pages with clean subject headers.")

if __name__ == "__main__":
    bulk_inject_subjects()
