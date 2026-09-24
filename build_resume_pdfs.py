"""Turn the sanitised markdown in resume_sources/ into print-ready PDFs.

    python build_resume_pdfs.py

Each file in resume_sources/ becomes a PDF in resumes/, which is what the
Download tab of the Streamlit app hands out. The markdown is the source, so a
change there flows straight through to the downloadable file.

Rendering uses headless Chrome, which every machine running this already has.
No classes, no lambdas, no pandas.
"""

import os
import subprocess

SOURCE_DIR = "resume_sources"
OUTPUT_DIR = "resumes"

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "/usr/bin/google-chrome",
]

ESCAPES = [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")]

PAGE_CSS = """
@page { margin: 16mm 15mm; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  color: #14181f; font-size: 10.2pt; line-height: 1.45; margin: 0;
}
h1 { font-size: 21pt; margin: 0 0 4px; letter-spacing: -.02em; color: #0f2350; }
.contact { color: #4a566b; font-size: 9.4pt; margin: 0 0 14px; }
h2 {
  font-size: 8.6pt; text-transform: uppercase; letter-spacing: .13em; color: #5d6b82;
  border-bottom: 1px solid #d9e0ec; padding-bottom: 5px; margin: 17px 0 9px; break-after: avoid;
}
h3 { font-size: 10.6pt; margin: 11px 0 1px; color: #0f2350; break-after: avoid; }
.period { color: #5d6b82; font-size: 9pt; margin: 0 0 5px; }
ul { margin: 5px 0 0; padding-left: 17px; }
li { margin-bottom: 4px; break-inside: avoid; }
p { margin: 4px 0; }
a { color: #14307a; text-decoration: none; }
"""


def esc(text):
    result = text
    for original, replacement in ESCAPES:
        result = result.replace(original, replacement)
    return result


def inline(text):
    """Handle the only inline markup these files use: **bold** and *italic*."""
    result = esc(text)
    while result.count("**") >= 2:
        result = result.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return result


def find_chrome():
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    return ""


def markdown_to_html(text):
    """Convert the small markdown subset these resumes use."""
    parts = []
    in_list = False
    line_number = 0
    for raw in text.split("\n"):
        line = raw.strip()
        line_number = line_number + 1

        if line.startswith("- "):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append("<li>" + inline(line[2:]) + "</li>")
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False

        if line == "" or line == "---":
            continue
        if line.startswith("### "):
            parts.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("## "):
            parts.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("# "):
            parts.append("<h1>" + inline(line[2:]) + "</h1>")
        elif line.startswith("*") and line.endswith("*") and len(line) > 2:
            parts.append('<p class="period">' + inline(line[1:-1]) + "</p>")
        elif line_number == 3:
            parts.append('<p class="contact">' + inline(line) + "</p>")
        else:
            parts.append("<p>" + inline(line) + "</p>")

    if in_list:
        parts.append("</ul>")

    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            "<style>" + PAGE_CSS + "</style></head><body>"
            + "\n".join(parts) + "</body></html>")


def main():
    chrome = find_chrome()
    if chrome == "":
        print("Could not find Chrome. Install it, or add its path to CHROME_PATHS.")
        return

    if not os.path.isdir(SOURCE_DIR):
        print("No " + SOURCE_DIR + " folder to read.")
        return
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    names = os.listdir(SOURCE_DIR)
    names.sort()
    for name in names:
        if not name.endswith(".md"):
            continue
        source = os.path.join(SOURCE_DIR, name)
        handle = open(source, encoding="utf-8")
        text = handle.read()
        handle.close()

        temp_html = os.path.join(OUTPUT_DIR, name[:-3] + ".tmp.html")
        out = open(temp_html, "w", encoding="utf-8")
        out.write(markdown_to_html(text))
        out.close()

        pdf_path = os.path.join(OUTPUT_DIR, name[:-3] + ".pdf")
        try:
            subprocess.run(
                [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                 "--print-to-pdf=" + os.path.abspath(pdf_path),
                 "file://" + os.path.abspath(temp_html)],
                check=True, capture_output=True, timeout=120,
            )
            print("Wrote " + pdf_path)
        except Exception as error:
            print("Could not render " + name + ": " + str(error))
        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)


main()
