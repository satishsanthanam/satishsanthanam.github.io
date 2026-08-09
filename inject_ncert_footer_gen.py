#!/usr/bin/env python3
import os

TARGET_DIR = "."

# Standard system/utility excludes
EXCLUDE_DIRS = {'.git', '.github', '_pagefind', 'node_modules', 'res'}

# Files to exclude entirely from general script processing
EXCLUDE_FILES = {
    'search.html', 
    '404.html',
    # Problematic / Exception files handled separately
    'genr.html',
    'physics/class-11-2/11-2-chapter-11-thermodynamics.html',
    'physics/class-11-2/11-2-chapter-14-waves.html',
    'mathematics/class-10/10-chapter-14-probability.html',
    'mathematics/class-9/09-chapter-03-the-world-of-numbers.html'
}

FOOTER_HTML = """
  <!-- NCERT Site Footer -->
  <footer class="site-footer" style="margin-top: 3rem; padding: 1.5rem 0; border-top: 1px solid #e2e8f0; text-align: center; color: #64748b; font-size: 0.875rem; font-family: system-ui, -apple-system, sans-serif;">
      <p><strong>NCERT Notes Reference Library</strong> | Maintained &amp; published via <a href="https://ventpipe.blog/2026/06/01/ncert-textbooks-short-notes/" target="_blank" rel="noopener noreferrer" style="color: #0284c7; text-decoration: none; font-weight: 500;">ventpipe.blog</a></p>
  </footer>
"""

def inject_standard_footers():
    processed = 0
    skipped = 0

    print("🚀 Running general NCERT footer injection...\n")

    for root, dirs, files in os.walk(TARGET_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.html'):
                continue

            file_path = os.path.normpath(os.path.join(root, file))
            
            # Skip base filenames or relative paths present in EXCLUDE_FILES
            if file in EXCLUDE_FILES or file_path in EXCLUDE_FILES:
                skipped += 1
                print(f"  ⏭️ Excluded exception file: {file_path}")
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if site footer is already present
            if 'class="site-footer"' in content or 'ncert-textbooks-short-notes' in content:
                skipped += 1
                continue

            # Standard replacement using rsplit to target ONLY the last </body>
            if '</body>' in content:
                parts = content.rsplit('</body>', 1)
                updated_content = parts[0] + f'\n{FOOTER_HTML}\n</body>' + parts[1]
            else:
                updated_content = content + f'\n{FOOTER_HTML}\n'

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            processed += 1
            print(f"  ✅ Added footer: {file_path}")

    print(f"\n🎉 Standard run complete! Processed {processed} files ({skipped} skipped/excluded).")

if __name__ == "__main__":
    inject_standard_footers()
