"""Dynamic resume - Streamlit application.

Run with:  streamlit run resume_app.py

All content comes from resume_data.py, the same file that generates the static
resume.html page.  Nothing is written twice.

The point of this app is the Role Fit tab.  A printed CV is a one-way claim:
the candidate says "I can do X" and the reader has to take it on trust.  Here
the recruiter sets the requirements and the page scores the candidate against
them, showing the exact piece of work behind every rating.

Constraints followed: no classes, no lambdas, no pandas.
"""

import base64

import streamlit as st

import resume_data

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=resume_data.PROFILE["name"] + " - Dynamic Resume",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Entrance motion. Streamlit has no animation API, so this is a small CSS
# injection - styling only, still no JavaScript anywhere in the project.
MOTION_CSS = """
<style>
@keyframes riseIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: none; }
}
[data-testid="stMetric"] {
  animation: riseIn .55s cubic-bezier(.2,.7,.3,1) both;
  /* an accent rule rather than a full box, so the note underneath still
     reads as part of the same figure */
  border-left: 3px solid #2b4ecc;
  padding-left: 14px;
}
[data-testid="stColumn"]:nth-of-type(1) [data-testid="stMetric"] { animation-delay: .05s; }
[data-testid="stColumn"]:nth-of-type(2) [data-testid="stMetric"] { animation-delay: .16s; }
[data-testid="stColumn"]:nth-of-type(3) [data-testid="stMetric"] { animation-delay: .27s; }
[data-testid="stMetricValue"] { font-weight: 700; }
[data-testid="stTabPanel"] { animation: riseIn .45s ease-out both; }
[data-testid="stHeading"] { animation: riseIn .5s ease-out both; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
"""

# Rating bands used by the Role Fit verdict.
STRONG_MATCH = 80
GOOD_MATCH = 65
PARTIAL_MATCH = 50

# A rating below this counts as a development area rather than a strength.
GAP_LEVEL = 3


# ---------------------------------------------------------------------------
# Small helpers over the data file
# ---------------------------------------------------------------------------
def skill_by_key(key):
    """Return the skill dictionary for a key, or None if it does not exist."""
    for skill in resume_data.SKILLS:
        if skill["key"] == key:
            return skill
    return None


def key_for_name(name):
    """Turn a display name shown in the picker back into its key."""
    for skill in resume_data.SKILLS:
        if skill["name"] == name:
            return skill["key"]
    return ""


def all_skill_names():
    names = []
    for skill in resume_data.SKILLS:
        names.append(skill["name"])
    return names


def names_for_keys(keys):
    """Turn a list of skill keys into the names the picker displays."""
    names = []
    for key in keys:
        skill = skill_by_key(key)
        if skill is not None:
            names.append(skill["name"])
    return names


def default_skill_names():
    """The requirements of the default role, used as the starting selection."""
    return names_for_keys(resume_data.TARGET_ROLE["required"])


def preset_titles():
    titles = []
    for preset in resume_data.ROLE_PRESETS:
        titles.append(preset["title"])
    return titles


def preset_by_title(title):
    for preset in resume_data.ROLE_PRESETS:
        if preset["title"] == title:
            return preset
    return None


def apply_preset():
    """Load the chosen job template into the requirement picker.

    Streamlit calls this when the template dropdown changes. It runs before the
    picker is drawn again, which is why the selection can be replaced here.
    """
    preset = preset_by_title(st.session_state.get("preset_choice", ""))
    if preset is not None:
        st.session_state["requirement_names"] = names_for_keys(preset["required"])


def roles_using(key):
    """Every role whose work evidences this skill."""
    found = []
    for role in resume_data.EXPERIENCE:
        if key in role["skills"]:
            found.append(role)
    return found


def read_file_bytes(path):
    """Read a file for the download button; return None if it is not there."""
    try:
        handle = open(path, "rb")
        content = handle.read()
        handle.close()
        return content
    except Exception:
        return None


def photo_data_uri():
    raw = read_file_bytes(resume_data.PROFILE["photo"])
    if raw is None:
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii")


# ---------------------------------------------------------------------------
# The scoring engine behind the Role Fit tab
# ---------------------------------------------------------------------------
def compute_fit(selected_keys, importance):
    """Weighted match score.

    Each requirement contributes level x importance out of a possible
    5 x importance, so a skill marked "critical" moves the score more than a
    "nice to have" one.
    """
    earned = 0
    possible = 0
    for key in selected_keys:
        skill = skill_by_key(key)
        if skill is None:
            continue
        weight = importance.get(key, 3)
        earned = earned + skill["level"] * weight
        possible = possible + 5 * weight
    if possible == 0:
        return 0.0
    return earned * 100.0 / possible


def verdict_for(score):
    """Turn a number into the sentence a recruiter actually wants."""
    if score >= STRONG_MATCH:
        return "Strong match", "Ready to contribute from week one."
    if score >= GOOD_MATCH:
        return "Good match", "Covers the core of the role with room to grow."
    if score >= PARTIAL_MATCH:
        return "Partial match", "Solid on several requirements, developing on others."
    return "Limited match", "This role leans on skills I am still building."


def coverage_by_role(selected_keys):
    """How many of the selected requirements each role can evidence."""
    orgs = []
    counts = []
    pairs = []
    for role in resume_data.EXPERIENCE:
        hits = 0
        for key in selected_keys:
            if key in role["skills"]:
                hits = hits + 1
        pairs.append((hits, role["org"]))
    pairs.sort(reverse=True)
    for pair in pairs:
        counts.append(pair[0])
        orgs.append(pair[1])
    return {"Role": orgs, "Requirements evidenced": counts}


# ---------------------------------------------------------------------------
# Sidebar - the recruiter's controls
# ---------------------------------------------------------------------------
def render_sidebar():
    """The recruiter's panel: what does your vacancy actually need?"""
    profile = resume_data.PROFILE
    uri = photo_data_uri()
    if uri != "":
        st.sidebar.markdown(
            '<div style="text-align:center">'
            '<img src="' + uri + '" style="width:130px;height:130px;border-radius:50%;'
            'object-fit:cover;box-shadow:0 0 0 3px #2b4ecc"></div>',
            unsafe_allow_html=True,
        )
    st.sidebar.markdown("### " + profile["name"])
    st.sidebar.write(profile["headline"])
    st.sidebar.caption(profile["tagline"])
    st.sidebar.write(profile["location"])
    st.sidebar.write(profile["email"])
    st.sidebar.write("[" + profile["linkedin_label"] + "](" + profile["linkedin_url"] + ")")
    st.sidebar.divider()

    st.sidebar.subheader("What does your role need?")
    st.sidebar.caption(
        "This panel is for you, the reader. Set the requirements of the job you "
        "are hiring for, and the **Role fit** tab scores me against them - with "
        "the evidence behind every score."
    )

    # Step 1 - start from a template so the first interaction is one click
    st.sidebar.markdown("**Step 1 - pick a job template**")
    if "preset_choice" not in st.session_state:
        st.session_state["preset_choice"] = resume_data.TARGET_ROLE["title"]
    st.sidebar.selectbox(
        "Job template",
        preset_titles(),
        key="preset_choice",
        on_change=apply_preset,
        label_visibility="collapsed",
    )
    chosen_preset = preset_by_title(st.session_state["preset_choice"])
    if chosen_preset is not None:
        st.sidebar.caption(chosen_preset["blurb"])

    # Step 2 - adjust the list by hand
    st.sidebar.markdown("**Step 2 - add or remove requirements**")
    if "requirement_names" not in st.session_state:
        st.session_state["requirement_names"] = default_skill_names()

    # The reset control is drawn before the picker, because Streamlit will not
    # let a widget's value be rewritten after that widget has been created.
    if st.sidebar.button("Reset to the template", width="stretch"):
        apply_preset()

    chosen_names = st.sidebar.multiselect(
        "Requirements",
        all_skill_names(),
        key="requirement_names",
        label_visibility="collapsed",
    )

    selected_keys = []
    for name in chosen_names:
        key = key_for_name(name)
        if key != "":
            selected_keys.append(key)

    # Step 3 - weighting is optional, so it stays folded away
    st.sidebar.markdown("**Step 3 - how much does each one matter?** *(optional)*")
    importance = {}
    expander = st.sidebar.expander("Set importance (all start at 3/5)", expanded=False)
    if len(selected_keys) == 0:
        expander.caption("Choose some requirements first.")
    for key in selected_keys:
        skill = skill_by_key(key)
        importance[key] = expander.slider(
            skill["name"], 1, 5, 3, key="importance_" + key,
            help="1 = nice to have, 5 = critical",
        )
    return selected_keys, importance


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
def render_entry_cards(container, entries, title_field, subtitle_field):
    """Render roles or projects as expanders, in the same shape on every tab."""
    position = 0
    for entry in entries:
        header = entry[title_field] + "  -  " + entry[subtitle_field] + "  (" + entry["period"] + ")"
        box = container.expander(header, expanded=(position == 0))
        box.caption(entry["summary"])
        left, right = box.columns([1.15, 0.85])
        left.markdown("**Key responsibilities**")
        for bullet in entry["bullets"]:
            left.write("- " + bullet)
        right.markdown("**Impact & achievements**")
        right.info(entry["impact"])
        tags = []
        for key in entry["skills"]:
            skill = skill_by_key(key)
            if skill is not None:
                tags.append("`" + skill["name"] + "`")
        right.caption("Skills evidenced: " + " ".join(tags))
        position = position + 1


def render_profile():
    st.subheader("About")
    st.write(resume_data.PROFILE["summary"])
    st.subheader("Impact in numbers")
    columns = st.columns(3)
    position = 0
    for item in resume_data.HIGHLIGHTS:
        column = columns[position % 3]
        column.metric(item["label"], item["value"], help=item["note"])
        column.caption(item["note"])
        position = position + 1

    st.divider()
    left, right = st.columns(2)
    left.subheader("Education")
    for entry in resume_data.EDUCATION:
        left.markdown("**" + entry["school"] + "** - " + entry["degree"])
        left.caption(entry["period"])
        for note in entry["notes"]:
            left.write("- " + note)
    right.subheader("Honours & awards")
    for award in resume_data.AWARDS:
        right.write("- " + award)
    right.subheader("Languages")
    for language in resume_data.LANGUAGES:
        right.write("- " + language)


def render_experience():
    st.subheader("Experience")
    names = all_skill_names()
    chosen = st.multiselect(
        "Filter by skill (leave empty to see everything)", names, default=[]
    )
    wanted = []
    for name in chosen:
        wanted.append(key_for_name(name))

    kept = []
    for role in resume_data.EXPERIENCE:
        keep = True
        for key in wanted:
            if key not in role["skills"]:
                keep = False
        if keep:
            kept.append(role)

    if len(kept) == 0:
        st.warning("No single role covers that whole combination. Try fewer filters.")
    else:
        render_entry_cards(st, kept, "role", "org")

    st.divider()
    st.subheader("Projects")
    st.caption("Work I started myself, from the first line of the spec to acceptance testing.")
    render_entry_cards(st, resume_data.PROJECTS, "org", "role")

    st.divider()
    st.subheader("Campus & research experience")
    render_entry_cards(st, resume_data.CAMPUS, "org", "role")


def render_publications():
    st.subheader("Publications & working papers")
    st.write(resume_data.RESEARCH_STATEMENT)
    for paper in resume_data.PUBLICATIONS:
        box = st.container(border=True)
        # an inline badge rather than a full-width status box, which drowned
        # out the citation it was meant to label
        if paper["status"] in ("Published", "In press"):
            colour = "green"
        else:
            colour = "blue"
        box.markdown(
            ":" + colour + "-background[**" + paper["status"] + "**]"
            "  \u00b7  " + paper["role"]
        )
        box.markdown("**" + paper["citation"] + "**")
        box.write(paper["detail"])
        if paper["link"] != "":
            box.markdown("[" + paper["link_label"] + "](" + paper["link"] + ")")


def render_fit(selected_keys, importance):
    st.subheader("Role fit")
    st.write(
        "**A CV only ever argues one side.** I claim a skill, you decide whether "
        "to believe me. This tab turns that around: you set the bar, and I get "
        "scored against it."
    )

    step1, step2, step3 = st.columns(3)
    step1.info("**1. You define the job**\n\nUse the panel on the left to set the "
               "skills your vacancy needs.")
    step2.info("**2. I get scored**\n\nEach requirement is compared with my own "
               "rating out of 5, weighted by how much you need it.")
    step3.info("**3. You check my working**\n\nEvery score opens up to show the "
               "employer, the task and the number behind it.")

    if len(selected_keys) == 0:
        st.warning(
            "No requirements selected yet. Pick a job template in the left-hand "
            "panel - or press **Reset to the template** - to see the score."
        )
        return

    score = compute_fit(selected_keys, importance)
    label, sentence = verdict_for(score)
    preset = preset_by_title(st.session_state.get("preset_choice", ""))
    role_name = "your role"
    if preset is not None:
        role_name = preset["title"]

    st.divider()
    st.markdown("#### The result")
    st.caption(
        "Scoring me against the **" + str(len(selected_keys)) +
        " requirements** you selected for **" + role_name + "**."
    )

    left, right = st.columns([1, 2])
    left.metric("Match score", str(int(round(score))) + "%")
    left.progress(int(round(score)))
    right.markdown("### " + label)
    right.write(sentence)
    right.caption(
        "The score is the weighted average of my ratings: "
        "sum(my level x your importance) / sum(5 x your importance)."
    )

    st.divider()
    st.markdown("#### Requirement by requirement")
    st.caption(
        "Two different numbers here, so read them carefully: **you need it** is "
        "how important you said the skill is; **my level** is how strong I am at "
        "it. Open a panel to see the work behind my rating."
    )

    head_left, head_mid, head_right = st.columns([3, 4, 1])
    head_left.caption("**REQUIREMENT**")
    head_mid.caption("**MY LEVEL**")
    head_right.caption("**/5**")

    gaps = []
    for key in selected_keys:
        skill = skill_by_key(key)
        weight = importance.get(key, 3)

        # A requirement is a gap either because the rating is low, or because
        # nothing but coursework backs it. Claiming a skill with no project
        # behind it is exactly what falls apart in an interview.
        backed_by_work = len(roles_using(key)) > 0
        if skill["level"] < GAP_LEVEL:
            gaps.append((skill, "rated " + str(skill["level"]) + "/5"))
        elif not backed_by_work:
            gaps.append((skill, "coursework only, no project to point to yet"))

        name_col, bar_col, level_col = st.columns([3, 4, 1])
        name_col.write("**" + skill["name"] + "**")
        name_col.caption("You need it: " + str(weight) + "/5")
        bar_col.progress(skill["level"] * 20)
        if backed_by_work:
            bar_col.caption("Proven on the job")
        else:
            bar_col.caption("Coursework only")
        level_col.write("**" + str(skill["level"]) + "**/5")

        evidence_box = st.expander("Show the evidence for " + skill["name"], expanded=False)
        for item in skill["evidence"]:
            evidence_box.markdown("**" + item["org"] + "** - " + item["detail"])
        related = roles_using(key)
        if len(related) > 0:
            orgs = []
            for role in related:
                orgs.append(role["org"])
            evidence_box.caption("Used on the job at: " + ", ".join(orgs))
        else:
            evidence_box.caption("Coursework only so far - no client project to point to yet.")

    st.divider()
    chart_left, chart_right = st.columns(2)
    chart_left.markdown("#### Which job taught me this")
    chart_left.caption(
        "How many of your " + str(len(selected_keys)) +
        " requirements each internship can actually evidence."
    )
    chart_left.bar_chart(
        coverage_by_role(selected_keys),
        x="Role",
        y="Requirements evidenced",
        horizontal=True,
    )

    chart_right.markdown("#### What I cannot back up")
    chart_right.caption("The requirements where I would be overselling myself.")
    if len(gaps) == 0:
        chart_right.success(
            "Every requirement you selected is rated 3/5 or above and backed by "
            "work I was actually paid to do."
        )
    else:
        chart_right.warning(
            "I would rather say this now than be found out in week two."
        )
        for entry in gaps:
            chart_right.write("- **" + entry[0]["name"] + "** - " + entry[1])


def render_download():
    st.subheader("Take a resume with you")
    st.write(
        "Three versions, tailored to three different kinds of role. Every one of "
        "them is built from the same underlying record - only the emphasis changes."
    )

    columns = st.columns(len(resume_data.RESUME_DOWNLOADS))
    position = 0
    for item in resume_data.RESUME_DOWNLOADS:
        column = columns[position]
        box = column.container(border=True)
        box.markdown("**" + item["title"] + "**")
        box.caption(item["blurb"])
        content = read_file_bytes(item["file"])
        if content is None:
            box.warning("Not generated yet.")
        else:
            box.download_button(
                "Download PDF",
                data=content,
                file_name=item["download_name"],
                mime="application/pdf",
                key="download_" + item["key"],
                width="stretch",
            )
        position = position + 1

    st.divider()
    page = read_file_bytes("resume.html")
    if page is not None:
        st.download_button(
            "Or take this whole page as a single HTML file",
            data=page,
            file_name="Zhan_Wenqian_Resume.html",
            mime="text/html",
        )
        st.caption(
            "Self-contained - the photo is embedded, there is no JavaScript and "
            "nothing loads from the internet. Open it and press Ctrl/Cmd + P for a "
            "print-ready PDF."
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    selected_keys, importance = render_sidebar()

    st.markdown(MOTION_CSS, unsafe_allow_html=True)
    st.title(resume_data.PROFILE["name"])
    st.write(
        resume_data.PROFILE["headline"] + "  \u00b7  " + resume_data.PROFILE["tagline"]
    )

    profile_tab, experience_tab, research_tab, fit_tab, download_tab = st.tabs(
        ["Profile", "Experience & projects", "Research", "Role fit", "Download"]
    )
    with profile_tab:
        render_profile()
    with experience_tab:
        render_experience()
    with research_tab:
        render_publications()
    with fit_tab:
        render_fit(selected_keys, importance)
    with download_tab:
        render_download()


main()
