#!/usr/bin/env python3
import os
import re

# Problematic / Exception files excluded from the general generator script
PROBLEM_FILES = [
    "physics/class-11-2/11-2-chapter-14-waves.html",
    "mathematics/class-10/10-chapter-14-probability.html",
    "mathematics/class-9/09-chapter-03-the-world-of-numbers.html",
    "physics/class-11-2/11-2-chapter-11-thermodynamics.html",
    "genr.html"
]

FOOTER_HTML = """
  <!-- NCERT Site Footer -->
  <footer class="site-footer" style="margin-top: 3rem; padding: 1.5rem 0; border-top: 1px solid #e2e8f0; text-align: center; color: #64748b; font-size: 0.875rem; font-family: system-ui, -apple-system, sans-serif;">
      <p><strong>NCERT Notes Reference Library</strong> | Maintained &amp; published via <a href="https://ventpipe.blog/2026/06/01/ncert-textbooks-short-notes/" target="_blank" rel="noopener noreferrer" style="color: #0284c7; text-decoration: none; font-weight: 500;">ventpipe.blog</a></p>
  </footer>
"""

def inject_exception_footers():
    print("🛠️ Processing exception files (repairing & injecting footer)...\n")

    for rel_path in PROBLEM_FILES:
        if not os.path.exists(rel_path):
            print(f"  ⚠️ File not found: {rel_path}")
            continue

        with open(rel_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Repair broken LaTeX if present (\right split across line breaks)
        content = re.sub(r'\\right\s*\n\s*ight\)', r'\\right)', content)
        content = re.sub(r'\^Might\)', r'\\right)', content)

        # 2. Inject footer if not already present
        if 'class="site-footer"' not in content and 'ncert-textbooks-short-notes' not in content:
            if '</body>' in content:
                # Safely split at the last </body> tag only
                parts = content.rsplit('</body>', 1)
                content = parts[0] + f'\n{FOOTER_HTML}\n</body>' + parts[1]
            else:
                content += f'\n{FOOTER_HTML}\n'

        with open(rel_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Exception file processed: {rel_path}")

    print("\n🎉 Exception processing complete!")

if __name__ == "__main__":
    inject_exception_footers()
