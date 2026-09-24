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
# Stylesheet
# ---------------------------------------------------------------------------
def build_css():
    return """
:root {
  --bg: #ffffff;
  --surface: #f7f9fc;
  --line: #e4e9f2;
  --ink: #101826;
  --muted: #5d6b82;
  --accent: #2b4ecc;
  --accent-soft: #eef2ff;
  --shadow: 0 1px 2px rgba(16, 24, 38, .05), 0 8px 24px rgba(16, 24, 38, .05);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d131f;
    --surface: #151d2c;
    --line: #253148;
    --ink: #e9eef7;
    --muted: #97a4ba;
    --accent: #7ea2ff;
    --accent-soft: #1a2440;
    --shadow: 0 1px 2px rgba(0, 0, 0, .3), 0 8px 24px rgba(0, 0, 0, .35);
  }
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.wrap { max-width: 880px; margin: 0 auto; padding: 0 24px; }

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ---------- header ---------- */
.hero {
  display: flex;
  gap: 28px;
  align-items: center;
  padding: 56px 0 36px;
}

.avatar {
  width: 124px;
  height: 124px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 3px solid var(--bg);
  box-shadow: 0 0 0 2px var(--accent), var(--shadow);
}

.hero h1 {
  margin: 0 0 6px;
  font-size: 2.1rem;
  letter-spacing: -.02em;
  line-height: 1.15;
}

.headline {
  margin: 0 0 2px;
  color: var(--ink);
  font-size: 1.02rem;
  font-weight: 600;
}

.tagline {
  margin: 0 0 14px;
  color: var(--muted);
  font-size: .97rem;
}

.contact {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
  padding: 0;
  font-size: .9rem;
}

.contact li {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 4px 13px;
  color: var(--muted);
  overflow-wrap: anywhere;
}

/* ---------- nav ---------- */
.nav {
  position: sticky;
  top: 0;
  z-index: 20;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.nav ul {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin: 0;
  padding: 10px 0;
  font-size: .88rem;
}

.nav a {
  display: block;
  padding: 5px 12px;
  border-radius: 7px;
  color: var(--muted);
}

.nav a:hover { background: var(--accent-soft); color: var(--accent); text-decoration: none; }

/* ---------- sections ---------- */
section { padding: 42px 0 8px; scroll-margin-top: 62px; }

h2 {
  font-size: .78rem;
  text-transform: uppercase;
  letter-spacing: .13em;
  color: var(--muted);
  margin: 0 0 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
  transition: color .3s ease, border-color .3s ease;
  break-after: avoid;
}

/* the section you jumped to announces itself - no JavaScript needed */
section:target h2 { color: var(--accent); border-color: var(--accent); }

.summary { margin: 0; font-size: 1.04rem; color: var(--ink); max-width: 68ch; }

/* ---------- metrics ---------- */
.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(255px, 1fr));
  gap: 14px;
}

.metric {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 16px 18px;
}

.metric b {
  display: block;
  font-size: 1.72rem;
  line-height: 1.1;
  letter-spacing: -.02em;
  color: var(--accent);
}

.metric span { display: block; font-weight: 600; font-size: .92rem; margin-top: 4px; }
.metric small { display: block; color: var(--muted); font-size: .8rem; margin-top: 3px; }

/* ---------- experience ---------- */
.role {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  margin-bottom: 14px;
  overflow: hidden;
}

.role summary {
  list-style: none;
  cursor: pointer;
  padding: 18px 46px 18px 20px;
  position: relative;
}

.role summary::-webkit-details-marker { display: none; }

.role summary::after {
  content: "";
  position: absolute;
  right: 22px;
  top: 27px;
  width: 8px;
  height: 8px;
  border-right: 2px solid var(--muted);
  border-bottom: 2px solid var(--muted);
  transform: rotate(45deg);
  transition: transform .2s ease;
}

.role[open] summary::after { transform: rotate(-135deg); }
.role summary:hover { background: var(--accent-soft); }

.role-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10px;
}

.role-org { font-weight: 700; font-size: 1.06rem; }
.role-title { color: var(--muted); font-size: .95rem; }

.role-period {
  margin-left: auto;
  color: var(--muted);
  font-size: .84rem;
  white-space: nowrap;
}

.role-impact { margin: 7px 0 0; font-size: .95rem; color: var(--ink); }

.role-body { padding: 0 20px 18px; border-top: 1px solid var(--line); }
.role-body ul { margin: 16px 0 0; padding-left: 20px; }
.role-body li { margin-bottom: 10px; font-size: .95rem; }

.tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }

.tag {
  font-size: .76rem;
  background: var(--accent-soft);
  color: var(--accent);
  border-radius: 6px;
  padding: 3px 9px;
}

/* ---------- skills ---------- */
.skill-group { margin-bottom: 26px; }

.skill-group h3 {
  font-size: .9rem;
  margin: 0 0 12px;
  color: var(--ink);
}

.skill {
  display: grid;
  grid-template-columns: 1fr 160px 34px;
  align-items: center;
  gap: 14px;
  padding: 7px 0;
  font-size: .93rem;
}

.track {
  height: 7px;
  background: var(--line);
  border-radius: 99px;
  overflow: hidden;
}

.fill {
  display: block;
  height: 100%;
  background: var(--accent);
  border-radius: 99px;
  animation: grow .9s ease-out both;
}

@keyframes grow { from { width: 0; } }

/* ---------- entrance motion (CSS only - there is no JavaScript here) ------- */
@keyframes rise {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: none; }
}

@keyframes pop {
  from { opacity: 0; transform: scale(.88); }
  to   { opacity: 1; transform: none; }
}

@keyframes sweep {
  from { opacity: 0; transform: scaleX(0); }
  to   { opacity: 1; transform: none; }
}

.avatar { animation: pop .7s cubic-bezier(.2,.8,.3,1) both; }
.hero h1 { animation: rise .6s cubic-bezier(.2,.7,.3,1) .08s both; }
.headline { animation: rise .6s cubic-bezier(.2,.7,.3,1) .16s both; }
.tagline { animation: rise .6s cubic-bezier(.2,.7,.3,1) .22s both; }
.contact li { animation: rise .5s cubic-bezier(.2,.7,.3,1) both; }
.nav { animation: rise .5s ease-out .45s both; }
.summary { animation: rise .6s ease-out .5s both; }
.metric { animation: rise .55s cubic-bezier(.2,.7,.3,1) both; }
h2 { transform-origin: left; animation: sweep .5s ease-out both; }

/* Anyone who has asked their system to reduce motion gets none of it. */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}

.level { color: var(--muted); font-size: .8rem; text-align: right; }

.languages { color: var(--muted); font-size: .88rem; margin: 4px 0 0; }

/* ---------- education / awards ---------- */
.edu { margin-bottom: 20px; }

.edu-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10px;
}

.edu-school { font-weight: 700; }
.edu-degree { color: var(--muted); font-size: .95rem; }
.edu-period { margin-left: auto; color: var(--muted); font-size: .84rem; }
.edu ul, .awards { margin: 8px 0 0; padding-left: 20px; }
.edu li, .awards li { font-size: .93rem; margin-bottom: 6px; color: var(--muted); }

footer {
  margin-top: 52px;
  padding: 22px 0 46px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: .82rem;
}

/* ---------- small screens ---------- */
@media (max-width: 720px) {
  .hero { flex-direction: column; text-align: center; padding-top: 38px; gap: 18px; }
  .contact { justify-content: center; }
  .avatar { width: 104px; height: 104px; }
  .hero h1 { font-size: 1.75rem; }
  .role-period, .edu-period { margin-left: 0; width: 100%; }
  .skill { grid-template-columns: 1fr 88px 32px; gap: 10px; }
}

/* ---------- print: one keystroke turns this page into a PDF ---------- */
@media print {
  :root {
    --bg: #ffffff;
    --surface: #ffffff;
    --line: #cfd6e2;
    --ink: #000000;
    --muted: #444444;
    --accent: #14307a;
    --accent-soft: #ffffff;
    --shadow: none;
  }

  @page { margin: 14mm; }

  body { font-size: 10pt; line-height: 1.4; }
  .nav, .role summary::after { display: none; }
  .wrap { max-width: none; padding: 0; }
  .hero { padding: 0 0 14px; gap: 18px; }
  .avatar { width: 88px; height: 88px; box-shadow: none; border: 1px solid var(--line); }
  section { padding: 14px 0 0; }
  h2 { margin-bottom: 12px; padding-bottom: 6px; }
  .metric { padding: 10px 13px; }
  .metric b { font-size: 1.4rem; }
  .role summary { padding-top: 12px; padding-bottom: 12px; }
  .role-body { padding-bottom: 12px; }
  .role-body ul { margin-top: 10px; }
  .role-body li { margin-bottom: 6px; }
  .skill { padding: 3px 0; }

  /* two columns of skills instead of one long list */
  .skill-group { display: grid; grid-template-columns: 1fr 1fr; gap: 0 30px; margin-bottom: 14px; }
  .skill-group h3 { grid-column: 1 / -1; }
  .metric, .role { box-shadow: none; break-inside: avoid; }
  .fill, .avatar, .hero h1, .headline, .tagline, .contact li,
  .summary, .metric, h2 { animation: none !important; opacity: 1 !important; transform: none !important; }

  /* every collapsed role is forced open so nothing is lost on paper */
  .role[open] .role-body, .role .role-body { display: block !important; }
  details::details-content { content-visibility: visible !important; block-size: auto !important; }
  .role summary { padding-right: 20px; }
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
    chip_index = 0
    for chip in chips:
        delay = 0.28 + chip_index * 0.07
        parts.append('<li style="animation-delay:' + str(round(delay, 2)) + 's">' + chip + '</li>')
        chip_index = chip_index + 1
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('</header>')
    return "\n".join(parts)


def build_nav():
    links = [
        ("about", "About"),
        ("impact", "Impact"),
        ("experience", "Experience"),
        ("skills", "Skills"),
        ("education", "Education"),
        ("awards", "Awards"),
    ]
    parts = ['<nav class="nav"><div class="wrap"><ul>']
    for anchor, label in links:
        parts.append('<li><a href="#' + anchor + '">' + label + '</a></li>')
    parts.append('</ul></div></nav>')
    return "\n".join(parts)


def build_highlights():
    parts = ['<section id="impact"><h2>Impact in Numbers</h2><div class="metrics">']
    card_index = 0
    for item in resume_data.HIGHLIGHTS:
        # the generator writes the stagger, so the cards arrive one after another
        delay = 0.06 * card_index
        parts.append('<div class="metric" style="animation-delay:' + str(round(delay, 2)) + 's">')
        card_index = card_index + 1
        parts.append('<b>' + esc(item["value"]) + '</b>')
        parts.append('<span>' + esc(item["label"]) + '</span>')
        parts.append('<small>' + esc(item["note"]) + '</small>')
        parts.append('</div>')
    parts.append('</div></section>')
    return "\n".join(parts)


def build_experience():
    lookup = skill_lookup()
    parts = ['<section id="experience"><h2>Experience</h2>']
    position = 0
    for role in resume_data.EXPERIENCE:
        # the most relevant role starts expanded, the rest stay tidy
        if position == 0:
            parts.append('<details class="role" open>')
        else:
            parts.append('<details class="role">')
        parts.append('<summary>')
        parts.append('<div class="role-head">')
        parts.append('<span class="role-org">' + esc(role["org"]) + '</span>')
        parts.append('<span class="role-title">' + esc(role["role"]) + '</span>')
        parts.append('<span class="role-period">' + esc(role["period"]) + '</span>')
        parts.append('</div>')
        parts.append('<p class="role-impact">' + esc(role["impact"]) + '</p>')
        parts.append('</summary>')
        parts.append('<div class="role-body"><ul>')
        for bullet in role["bullets"]:
            parts.append('<li>' + esc(bullet) + '</li>')
        parts.append('</ul>')
        parts.append('<div class="tags">')
        for key in role["skills"]:
            parts.append('<span class="tag">' + esc(lookup[key]["name"]) + '</span>')
        parts.append('</div></div></details>')
        position = position + 1
    parts.append('</section>')
    return "\n".join(parts)


def build_skills():
    parts = ['<section id="skills"><h2>Skills</h2>']
    for group in resume_data.SKILL_GROUPS:
        parts.append('<div class="skill-group"><h3>' + esc(group) + '</h3>')
        for skill in resume_data.SKILLS:
            if skill["group"] != group:
                continue
            width = skill["level"] * 20
            parts.append('<div class="skill">')
            parts.append('<span>' + esc(skill["name"]) + '</span>')
            parts.append('<span class="track"><span class="fill" style="width:' + str(width) + '%"></span></span>')
            parts.append('<span class="level">' + str(skill["level"]) + '/5</span>')
            parts.append('</div>')
        parts.append('</div>')
    parts.append('<p class="languages">Languages: ' + esc(" | ".join(resume_data.LANGUAGES)) + '</p>')
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
    parts.append(build_nav())
    parts.append('<main class="wrap">')
    parts.append('<section id="about"><h2>About</h2><p class="summary">' +
                 esc(resume_data.PROFILE["summary"]) + '</p></section>')
    parts.append(build_highlights())
    parts.append(build_experience())
    parts.append(build_skills())
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
