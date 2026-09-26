"""Generate resume.html from resume_data.py.

The static page contains no JavaScript at all - every interactive behaviour is
pure HTML/CSS:

    * collapsible roles      -> the native <details> element
    * section navigation     -> anchor links + scroll-behavior + :target
    * skill bars             -> inline widths written by this script
    * dark mode              -> prefers-color-scheme
    * print to PDF           -> a dedicated @media print block

Run:  python build_static_html.py
"""

import base64
import datetime

import resume_data

OUTPUT_FILE = "resume.html"

# Characters that must not be handed to the browser raw.
ESCAPES = [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;")]


def esc(text):
    """Escape the characters that would otherwise break the markup."""
    result = str(text)
    for original, replacement in ESCAPES:
        result = result.replace(original, replacement)
    return result


def skill_lookup():
    """Build a key -> skill dictionary so roles can name their skills."""
    lookup = {}
    for skill in resume_data.SKILLS:
        lookup[skill["key"]] = skill
    return lookup


def embed_photo(path):
    """Read the portrait and return it as a data URI.

    Embedding the image keeps resume.html a single self-contained file: it can
    be e-mailed, zipped or opened from any folder and the photo still shows.
    If the file is missing we fall back to the ordinary relative path.
    """
    try:
        handle = open(path, "rb")
        raw = handle.read()
        handle.close()
        encoded = base64.b64encode(raw).decode("ascii")
        return "data:image/jpeg;base64," + encoded
    except Exception:
        print("Note: could not embed " + path + ", linking to it instead.")
        return path


# ---------------------------------------------------------------------------
# Inline SVG icons. Inline so the page stays a single file with no requests,
# and no icon font or script is needed.
# ---------------------------------------------------------------------------
ICONS = {
    "chart": '<path d="M3 3v18h18"/><path d="M7 15l3-4 3 3 4-6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
    "chip": '<rect x="7" y="7" width="10" height="10" rx="1.6"/><path d="M10 3v3M14 3v3M10 18v3M14 18v3M3 10h3M3 14h3M18 10h3M18 14h3"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.4-3 8-7 9-4-1-7-4.6-7-9V6z"/><path d="M9.2 12.2l2 2 3.6-4"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "robot": '<rect x="4" y="8" width="16" height="11" rx="2.5"/><path d="M12 4v4M8.5 13h.01M15.5 13h.01M9 19v2M15 19v2"/>',
    "leaf": '<path d="M20 4c0 9-5.5 14-13 14"/><path d="M4 20c0-8 5-13 13-13"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 5h11l-2 3 2 3H5z"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M17 11.5a2.8 2.8 0 1 0-1.6-5.1M18 20c0-2.2-.8-3.9-2.2-4.9"/>',
    "bullseye": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20v3H6.5"/>',
}


def icon_svg(name, css_class):
    """Return one inline SVG glyph, or an empty circle if the name is unknown."""
    body = ICONS.get(name, '<circle cx="12" cy="12" r="8"/>')
    return ('<svg class="' + css_class + '" viewBox="0 0 24 24" aria-hidden="true">'
            + body + '</svg>')


# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------

def build_css():
    return """
:root {
  --bg: #ffffff;
  --card: #ffffff;
  --line: #e4e9f2;
  --ink: #101826;
  --navy: #0f2350;
  --muted: #55627a;
  --accent: #2b4ecc;
  --pill: #e9eef9;
  --shadow: 0 1px 2px rgba(16, 24, 38, .04), 0 10px 30px rgba(16, 24, 38, .06);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0b111c;
    --card: #141d2e;
    --line: #26314a;
    --ink: #e9eef7;
    --navy: #dbe5f8;
    --muted: #9aa7bd;
    --accent: #7ea2ff;
    --pill: #1e293f;
    --shadow: 0 1px 2px rgba(0, 0, 0, .3), 0 10px 30px rgba(0, 0, 0, .35);
  }
}

* { box-sizing: border-box; }

/* The page is a document, not an application: nothing here moves, folds or
   responds to a click. The only interactive elements are the two contact
   links, because a reader needs a way to reply. */
body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  background-color: #f4f7fd;
  background-image:
    radial-gradient(1100px 560px at 8% -6%, rgba(43, 78, 204, .13), transparent 62%),
    radial-gradient(860px 480px at 96% 4%, rgba(124, 92, 222, .11), transparent 62%),
    radial-gradient(760px 700px at 50% 108%, rgba(32, 160, 190, .09), transparent 60%),
    linear-gradient(180deg, #fdfdff 0%, #f5f8fd 42%, #eef3fb 100%);
  background-attachment: fixed;
}

@media (prefers-color-scheme: dark) {
  body {
    background-color: #0b111c;
    background-image:
      radial-gradient(1100px 560px at 8% -6%, rgba(78, 118, 255, .16), transparent 62%),
      radial-gradient(860px 480px at 96% 4%, rgba(150, 110, 255, .12), transparent 62%),
      radial-gradient(760px 700px at 50% 108%, rgba(32, 190, 200, .08), transparent 60%),
      linear-gradient(180deg, #0a1018 0%, #0c1421 48%, #101a2c 100%);
  }
}

.wrap { max-width: 940px; margin: 0 auto; padding: 0 24px; }

a { color: var(--accent); text-decoration: none; }

/* ---------- header ---------- */
.hero { display: flex; gap: 28px; align-items: center; padding: 56px 0 30px; }

.avatar {
  width: 124px; height: 124px; border-radius: 50%; object-fit: cover;
  flex-shrink: 0; border: 3px solid var(--card);
  box-shadow: 0 0 0 2px var(--accent), var(--shadow);
}

.hero h1 { margin: 0 0 6px; font-size: 2.1rem; letter-spacing: -.02em; line-height: 1.15; color: var(--navy); }
.headline { margin: 0 0 2px; color: var(--ink); font-size: 1.02rem; font-weight: 600; }
.tagline { margin: 0 0 14px; color: var(--muted); font-size: .97rem; }

.contact { list-style: none; display: flex; flex-wrap: wrap; gap: 8px; margin: 0; padding: 0; font-size: .9rem; }

.contact li {
  background: var(--card); border: 1px solid var(--line); border-radius: 999px;
  padding: 4px 13px; color: var(--muted); overflow-wrap: anywhere;
}

/* ---------- sections ---------- */
section { padding: 34px 0 6px; }

h2 {
  font-size: .78rem; text-transform: uppercase; letter-spacing: .13em;
  color: var(--muted); margin: 0 0 18px; padding-bottom: 10px;
  border-bottom: 1px solid var(--line); break-after: avoid;
}

.section-note { margin: -6px 0 18px; color: var(--muted); font-size: .92rem; }
.summary { margin: 0; font-size: 1.04rem; color: var(--ink); max-width: 68ch; }

/* ---------- metrics ---------- */
.metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); gap: 14px; }

.metric { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; box-shadow: var(--shadow); }
.metric b { display: block; font-size: 1.72rem; line-height: 1.1; letter-spacing: -.02em; color: var(--accent); }
.metric span { display: block; font-weight: 600; font-size: .92rem; margin-top: 4px; }
.metric small { display: block; color: var(--muted); font-size: .8rem; margin-top: 3px; }

/* ---------- the role / project card ---------- */
.card {
  display: block;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: var(--shadow);
  margin-bottom: 16px;
  padding: 24px 26px;
  break-inside: avoid;
}

.card-top { display: flex; gap: 18px; align-items: flex-start; }

.card-icon {
  width: 52px; height: 52px; border-radius: 50%;
  background: var(--navy);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

@media (prefers-color-scheme: dark) { .card-icon { background: var(--accent); } }

.card-icon svg { width: 24px; height: 24px; stroke: var(--card); fill: none; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }

.card-titles { flex: 1; min-width: 0; }
.card-role { margin: 0; font-size: 1.4rem; font-weight: 800; letter-spacing: -.02em; color: var(--navy); line-height: 1.2; }
.card-org { margin: 3px 0 0; font-size: 1.04rem; font-weight: 700; color: var(--navy); }

.card-period {
  background: var(--pill); color: var(--navy);
  border-radius: 999px; padding: 6px 15px;
  font-size: .8rem; font-weight: 700; white-space: nowrap; flex-shrink: 0;
}

.card-summary { margin: 16px 0 0; color: var(--muted); font-size: .98rem; }

.card-cols { display: grid; grid-template-columns: 1.15fr .85fr; gap: 34px; margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--line); }

.col-title { display: flex; align-items: center; gap: 9px; font-size: 1.02rem; font-weight: 700; color: var(--ink); margin: 0 0 14px; }
.col-title svg { width: 19px; height: 19px; fill: none; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
.col-title.resp svg { stroke: var(--navy); }
.col-title.impact svg { stroke: #d9a300; }

.card-cols ul { margin: 0; padding-left: 20px; }
.card-cols li { margin-bottom: 11px; font-size: .95rem; color: var(--muted); }
.card-impact { margin: 0; font-size: .97rem; color: var(--muted); }

/* ---------- publications ---------- */
.pub {
  background: var(--card); border: 1px solid var(--line); border-radius: 14px;
  padding: 20px 22px; margin-bottom: 14px; box-shadow: var(--shadow); break-inside: avoid;
}

.pub-head { display: flex; flex-wrap: wrap; gap: 10px; align-items: baseline; margin-bottom: 8px; }

.badge {
  font-size: .72rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;
  border-radius: 999px; padding: 3px 11px; background: var(--pill); color: var(--navy);
}

.badge.live { background: #dff3e6; color: #17603a; }

@media (prefers-color-scheme: dark) { .badge.live { background: #14361f; color: #7fd9a6; } }

.pub-role { font-size: .82rem; color: var(--muted); }
.pub-cite { margin: 0 0 8px; font-size: .97rem; color: var(--ink); }
.pub-detail { margin: 0; font-size: .91rem; color: var(--muted); }
.pub-link { display: inline-block; margin-top: 8px; font-size: .85rem; }

/* ---------- education / awards ---------- */
.edu { margin-bottom: 20px; }
.edu-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; }
.edu-school { font-weight: 700; }
.edu-degree { color: var(--muted); font-size: .95rem; }
.edu-period { margin-left: auto; color: var(--muted); font-size: .84rem; }
.edu ul, .awards { margin: 8px 0 0; padding-left: 20px; }
.edu li, .awards li { font-size: .93rem; margin-bottom: 6px; color: var(--muted); }

.languages { color: var(--muted); font-size: .93rem; margin: 14px 0 0; }

footer { margin-top: 44px; padding: 22px 0 46px; border-top: 1px solid var(--line); color: var(--muted); font-size: .82rem; }

/* ---------- small screens ---------- */
@media (max-width: 860px) {
  .card-cols { grid-template-columns: 1fr; gap: 22px; }
}

@media (max-width: 720px) {
  .hero { flex-direction: column; text-align: center; padding-top: 38px; gap: 18px; }
  .contact { justify-content: center; }
  .avatar { width: 104px; height: 104px; }
  .hero h1 { font-size: 1.75rem; }
  .edu-period { margin-left: 0; width: 100%; }
  .card { padding: 20px; }
  .card-top { flex-wrap: wrap; }
  .card-period { margin-left: 70px; }
  .card-role { font-size: 1.22rem; }
}

/* ---------- print ---------- */
@media print {
  :root {
    --bg: #ffffff; --card: #ffffff; --line: #cfd6e2;
    --ink: #000000; --navy: #14307a; --muted: #3f4a5c; --accent: #14307a;
    --pill: #eef1f7; --shadow: none;
  }

  @page { margin: 13mm; }

  body { font-size: 9.2pt; line-height: 1.32; background: #fff !important; background-image: none !important; }
  .wrap { max-width: none; padding: 0; }
  .hero { padding: 0 0 12px; gap: 18px; }
  .avatar { width: 84px; height: 84px; box-shadow: none; border: 1px solid var(--line); }
  section { padding: 10px 0 0; }
  h2 { margin-bottom: 8px; padding-bottom: 4px; }
  .section-note { margin: -4px 0 10px; }
  .summary { max-width: none; }
  .metrics { gap: 9px; }
  .metric { padding: 10px 13px; box-shadow: none; }
  .metric b { font-size: 1.4rem; }
  .card, .pub { box-shadow: none; margin-bottom: 9px; }
  .card { padding: 12px 14px; }
  .card-summary { margin-top: 10px; }
  .card-cols { margin-top: 10px; padding-top: 9px; gap: 18px; }
  .card-cols li { margin-bottom: 3px; }
  .card-role { font-size: 1.05rem; }
  .col-title { margin-bottom: 8px; font-size: .95rem; }
  .card-icon { width: 32px; height: 32px; background: var(--navy) !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .pub { padding: 12px 14px; }
  .pub-head { margin-bottom: 5px; }
  .edu { margin-bottom: 12px; }
}
"""


# ---------------------------------------------------------------------------
# Page fragments
# ---------------------------------------------------------------------------
def build_hero():
    profile = resume_data.PROFILE
    parts = []
    parts.append('<header class="hero">')
    parts.append('<img class="avatar" src="' + embed_photo(profile["photo"]) +
                 '" alt="Portrait of ' + esc(profile["name"]) + '">')
    parts.append('<div>')
    parts.append('<h1>' + esc(profile["name"]) + '</h1>')
    parts.append('<p class="headline">' + esc(profile["headline"]) + '</p>')
    parts.append('<p class="tagline">' + esc(profile["tagline"]) + '</p>')
    parts.append('<ul class="contact">')
    # each chip fades in just after the one before it
    chips = [
        esc(profile["location"]),
        '<a href="mailto:' + esc(profile["email"]) + '">' + esc(profile["email"]) + '</a>',
        '<a href="' + esc(profile["linkedin_url"]) + '">' + esc(profile["linkedin_label"]) + '</a>',
    ]
    for chip in chips:
        parts.append('<li>' + chip + '</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('</header>')
    return "\n".join(parts)


def build_highlights():
    parts = ['<section id="impact"><h2>Impact in Numbers</h2><div class="metrics">']
    for item in resume_data.HIGHLIGHTS:
        parts.append('<div class="metric">')
        parts.append('<b>' + esc(item["value"]) + '</b>')
        parts.append('<span>' + esc(item["label"]) + '</span>')
        parts.append('<small>' + esc(item["note"]) + '</small>')
        parts.append('</div>')
    parts.append('</div></section>')
    return "\n".join(parts)


def build_card(entry, title_field, subtitle_field):
    """Render one role or project as a plain, fully visible card.

    There is nothing to click: the whole entry is on the page from the moment
    it loads, which is what a resume should do.
    """
    parts = []
    parts.append('<article class="card">')
    parts.append('<div class="card-top">')
    parts.append('<span class="card-icon">' + icon_svg(entry.get("icon", ""), "") + '</span>')
    parts.append('<div class="card-titles">')
    parts.append('<h3 class="card-role">' + esc(entry[title_field]) + '</h3>')
    parts.append('<p class="card-org">' + esc(entry[subtitle_field]) + '</p>')
    parts.append('</div>')
    parts.append('<span class="card-period">' + esc(entry["period"]) + '</span>')
    parts.append('</div>')
    parts.append('<p class="card-summary">' + esc(entry["summary"]) + '</p>')

    parts.append('<div class="card-cols">')
    parts.append('<div>')
    parts.append('<p class="col-title resp">' + icon_svg("people", "") + 'Key Responsibilities</p>')
    parts.append('<ul>')
    for bullet in entry["bullets"]:
        parts.append('<li>' + esc(bullet) + '</li>')
    parts.append('</ul></div>')

    parts.append('<div>')
    parts.append('<p class="col-title impact">' + icon_svg("bullseye", "") + 'Impact &amp; Achievements</p>')
    parts.append('<p class="card-impact">' + esc(entry["impact"]) + '</p>')
    parts.append('</div>')

    parts.append('</div></article>')
    return "\n".join(parts)


def build_card_section(anchor, heading, note, entries, title_field, subtitle_field):
    parts = ['<section id="' + anchor + '"><h2>' + esc(heading) + '</h2>']
    if note != "":
        parts.append('<p class="section-note">' + esc(note) + '</p>')
    for entry in entries:
        parts.append(build_card(entry, title_field, subtitle_field))
    parts.append('</section>')
    return "\n".join(parts)


def build_experience():
    return build_card_section(
        "experience", "Experience",
        "Four analytics internships.",
        resume_data.EXPERIENCE, "role", "org")


def build_projects():
    return build_card_section(
        "projects", "Projects",
        "Work I started myself, from the first line of the spec to acceptance testing.",
        resume_data.PROJECTS, "org", "role")


def build_campus():
    return build_card_section(
        "campus", "Campus & Research Experience", "",
        resume_data.CAMPUS, "org", "role")


def build_publications():
    parts = ['<section id="publications"><h2>Publications &amp; Working Papers</h2>']
    parts.append('<p class="section-note">' + esc(resume_data.RESEARCH_STATEMENT) + '</p>')
    for paper in resume_data.PUBLICATIONS:
        badge_class = "badge live" if paper["status"] in ("Published", "In press") else "badge"
        parts.append('<article class="pub">')
        parts.append('<div class="pub-head">')
        parts.append('<span class="' + badge_class + '">' + esc(paper["status"]) + '</span>')
        parts.append('<span class="pub-role">' + esc(paper["role"]) + '</span>')
        parts.append('</div>')
        parts.append('<p class="pub-cite">' + esc(paper["citation"]) + '</p>')
        parts.append('<p class="pub-detail">' + esc(paper["detail"]) + '</p>')
        if paper["link"] != "":
            parts.append('<a class="pub-link" href="' + esc(paper["link"]) + '">'
                         + esc(paper["link_label"]) + '</a>')
        parts.append('</article>')
    parts.append('</section>')
    return "\n".join(parts)


def build_education():
    parts = ['<section id="education"><h2>Education</h2>']
    for entry in resume_data.EDUCATION:
        parts.append('<div class="edu"><div class="edu-head">')
        parts.append('<span class="edu-school">' + esc(entry["school"]) + '</span>')
        parts.append('<span class="edu-degree">' + esc(entry["degree"]) + '</span>')
        parts.append('<span class="edu-period">' + esc(entry["period"]) + '</span>')
        parts.append('</div><ul>')
        for note in entry["notes"]:
            parts.append('<li>' + esc(note) + '</li>')
        parts.append('</ul></div>')
    parts.append('<p class="languages">Languages: ' + esc(" | ".join(resume_data.LANGUAGES)) + '</p>')
    parts.append('</section>')
    return "\n".join(parts)


def build_awards():
    parts = ['<section id="awards"><h2>Honours &amp; Awards</h2><ul class="awards">']
    for award in resume_data.AWARDS:
        parts.append('<li>' + esc(award) + '</li>')
    parts.append('</ul></section>')
    return "\n".join(parts)


def build_page():
    today = datetime.date.today().strftime("%d %b %Y")
    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="en">')
    parts.append('<head>')
    parts.append('<meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append('<title>' + esc(resume_data.PROFILE["name"]) + ' - Business Analytics</title>')
    parts.append('<meta name="description" content="' + esc(resume_data.PROFILE["headline"]) + '">')
    parts.append('<style>' + build_css() + '</style>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append('<div class="wrap">')
    parts.append(build_hero())
    parts.append('</div>')
    parts.append('<main class="wrap">')
    parts.append('<section id="about"><h2>About</h2><p class="summary">' +
                 esc(resume_data.PROFILE["summary"]) + '</p></section>')
    parts.append(build_highlights())
    parts.append(build_experience())
    parts.append(build_projects())
    parts.append(build_publications())
    parts.append(build_campus())
    parts.append(build_education())
    parts.append(build_awards())
    parts.append('</main>')
    parts.append('<footer class="wrap">Generated from resume_data.py on ' + today +
                 ' &middot; no JavaScript, no tracking &middot; press Ctrl/Cmd + P for a print-ready PDF</footer>')
    parts.append('</body>')
    parts.append('</html>')
    return "\n".join(parts)


def main():
    try:
        page = build_page()
        output = open(OUTPUT_FILE, "w", encoding="utf-8")
        output.write(page)
        output.close()
        print("Wrote " + OUTPUT_FILE + " (" + str(len(page)) + " characters)")
    except Exception as error:
        print("Could not generate the page: " + str(error))


main()
