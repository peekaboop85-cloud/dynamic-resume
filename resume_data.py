"""Single source of truth for the resume.

Everything shown on the static HTML page and in the Streamlit app is defined
here and nowhere else.  To update the resume, edit this file only:

    * change a number      -> edit it once, both pages follow
    * add a role           -> append one dictionary to EXPERIENCE
    * add a skill          -> append one dictionary to SKILLS
    * re-generate the page -> python build_static_html.py

No classes, no lambdas, no pandas - plain dictionaries and lists only.
"""

# ---------------------------------------------------------------------------
# Contact details.
# Phone number and postal address are deliberately omitted, and the personal
# mailbox was replaced with the university address, because the old local part
# was the phone number itself.
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Zhan Wenqian",
    # The line under the name says who I am academically; the tagline carries
    # the positioning and is used where there is room for a second line.
    "headline": "MSc Business Analytics, Nanyang Technological University",
    "tagline": "Turning messy operational data into decisions",
    "location": "Singapore",
    "email": "ZHAN0820@e.ntu.edu.sg",
    "linkedin_url": "https://www.linkedin.com/in/wenqian-zhan-36076641b",
    "linkedin_label": "linkedin.com/in/wenqian-zhan-36076641b",
    "photo": "assets/photo.jpg",
    "summary": (
        "I am an MSc Business Analytics student at NTU with four analytics internships behind me "
        "at ByteDance, L'Oreal, Roland Berger and Western Securities. What connects them is the "
        "same habit: I do not trust a number until I have checked where it came from. At ByteDance "
        "that meant rebuilding the quality checks on six core tables before anyone reported on them; "
        "at Roland Berger it meant turning 200+ open-ended survey answers into five findings a "
        "partner could act on. I am looking for an e-commerce analyst role where the data is messy, "
        "the questions are commercial, and someone has to own both ends."
    ),
}

# ---------------------------------------------------------------------------
# Headline numbers.  These drive the metric strip on both pages.
# ---------------------------------------------------------------------------
HIGHLIGHTS = [
    {"value": "99.2%", "label": "Data usability", "note": "lifted from 92.5% across 6 core tables"},
    {"value": "12", "label": "Power BI dashboards", "note": "built for daily GMV / product / user monitoring"},
    {"value": "+63%", "label": "Conversion peak found", "note": "20:00 slot vs. daily average, ByteDance"},
    {"value": "500+", "label": "Data points maintained", "note": "electronics industry database, Western Securities"},
    {"value": "200+", "label": "Survey responses analysed", "note": "management diagnostic, Roland Berger"},
    {"value": "30+", "label": "Expert interviews structured", "note": "unstructured notes to research conclusions"},
]

# ---------------------------------------------------------------------------
# Experience.  Order is by relevance to analytics roles, not strictly by date.
# "impact" is the one line that stays visible when the card is collapsed.
# "skills" holds the keys defined in SKILLS below - this is what powers the
# Role Fit scoring and the evidence trail.
# ---------------------------------------------------------------------------
EXPERIENCE = [
    {
        "id": "bytedance",
        "org": "ByteDance",
        "role": "User Growth | Business Analysis Intern",
        "period": "Jan 2025 - Feb 2025",
        "impact": "Raised data usability from 92.5% to 99.2% and found the 20:00 conversion peak that reshaped campaign scheduling.",
        "bullets": [
            "Owned quality monitoring and cleaning for 6 core tables (user behaviour, transaction records); built an AI-assisted QA workflow for missing-value detection, outlier flagging and date-format validation, lifting data usability from 92.5% to 99.2%.",
            "Built 12 Power BI dashboards - GMV trend heatmaps, product-rating boxplots, user-activity time-series - covering daily monitoring across the transaction, product and user workstreams.",
            "Through user-activity and conversion analysis, identified a conversion-rate peak at 20:00 running 63% above the daily average, providing the quantitative basis for optimising campaign scheduling.",
        ],
        "skills": ["data_quality", "power_bi", "python", "conversion_analysis", "dataviz", "ai_workflow"],
    },
    {
        "id": "loreal",
        "org": "L'Oreal (China)",
        "role": "Business Analysis Intern",
        "period": "Apr 2024 - Jun 2024",
        "impact": "Competitor benchmarking that fed 3 market opportunities into the Q3 category plan and informed 3 major promotional campaigns.",
        "bullets": [
            "Benchmarked Chando and Proya across product portfolio, pricing and promotional activity; consolidated 10+ competitor datasets (e-commerce sell-through, promotions) in Excel pivot tables to quantify relative strengths - delivering 3 market opportunities and several risk flags that were adopted into the Q3 category plan with written recognition from the department, and informed 3 major promotional campaigns.",
            "Researched CRM practices in the beauty industry - membership structure, repurchase behaviour and digital touchpoint deployment - authoring a ~20,000-character industry report with strategic recommendations.",
        ],
        "skills": ["benchmarking", "excel", "ecommerce", "business_writing", "stats"],
    },
    {
        "id": "western",
        "org": "Western Securities",
        "role": "Research Intern, Electronics & Semiconductors",
        "period": "Dec 2025 - Mar 2026",
        "impact": "Maintained a 500+ data point industry database and structured 30+ expert interviews into research conclusions at scale.",
        "bullets": [
            "Used LLM agents to decompose and consolidate 30+ expert interviews and site-visit notes, converting unstructured text into structured research conclusions at scale; deployed AI agents to pre-read filings and broker reports for automated first-pass screening.",
            "Built and maintained the core electronics industry database (global semiconductor sales, fab utilisation, key product pricing), updating 500+ data points under a standardised collection and refresh process.",
            "Supported in-depth semiconductor company reports (30-50 pages each), covering value-chain mapping and competitive landscape for foundry, foldable-display and AI-chip sub-sectors.",
        ],
        "skills": ["ai_workflow", "database", "industry_research", "business_writing", "data_quality"],
    },
    {
        "id": "roland_berger",
        "org": "Roland Berger",
        "role": "Consulting Project Team, Intern",
        "period": "Nov 2025 - Feb 2026",
        "impact": "Turned 200+ survey responses into 5 core findings and screened 10+ robotics companies for a cross-industry M&A deck.",
        "bullets": [
            "Designed a management diagnostic survey (strategy execution, organisational structure); processed 200+ valid responses with multi-dimensional cross-tabulation and AI-agent topic clustering of open-ended feedback, quantifying unstructured input into 5 core findings.",
            "On an automotive cross-industry M&A project, used AI research agents to map the robotics value chain and ran fundamental analysis on 10+ companies (patent counts, R&D intensity, supply-chain stability), contributing to a 15+ page market-entry deck.",
        ],
        "skills": ["survey", "stats", "ai_workflow", "industry_research", "business_writing"],
    },
]

# ---------------------------------------------------------------------------
# Skills.
#   level    - honest self-rating out of 5
#   evidence - the exact resume line that backs the rating, so every claim on
#              the Role Fit tab can be traced to a piece of work
# ---------------------------------------------------------------------------
SKILLS = [
    {
        "key": "data_quality",
        "name": "Data Quality & QA Monitoring",
        "group": "Data Engineering & Preparation",
        "level": 5,
        "evidence": [
            {"org": "ByteDance", "detail": "Rebuilt QA on 6 core tables - missing values, outliers, date formats - usability 92.5% to 99.2%."},
            {"org": "Western Securities", "detail": "Standardised collection and refresh process for 500+ database data points."},
        ],
    },
    {
        "key": "excel",
        "name": "Excel (Pivot Tables, Modelling)",
        "group": "Data Engineering & Preparation",
        "level": 5,
        "evidence": [
            {"org": "L'Oreal (China)", "detail": "Consolidated 10+ competitor datasets in pivot tables to quantify relative strengths."},
        ],
    },
    {
        "key": "python",
        "name": "Python for Data Analysis",
        "group": "Data Engineering & Preparation",
        "level": 4,
        "evidence": [
            {"org": "ByteDance", "detail": "Cleaning and quality checks across user behaviour and transaction tables."},
            {"org": "Coursework", "detail": "Python for Data Analysis (BJTU); AI & Big Data in Business (NTU MSc)."},
        ],
    },
    {
        "key": "sql",
        "name": "SQL",
        "group": "Data Engineering & Preparation",
        "level": 3,
        "evidence": [
            {"org": "Coursework", "detail": "Querying and joins; no production project metric on the resume yet - an area I am actively building."},
        ],
    },
    {
        "key": "database",
        "name": "Database Building & Maintenance",
        "group": "Data Engineering & Preparation",
        "level": 4,
        "evidence": [
            {"org": "Western Securities", "detail": "Built and maintained the core electronics industry database; 500+ data points refreshed on a standard cycle."},
        ],
    },
    {
        "key": "power_bi",
        "name": "Power BI",
        "group": "Analytics & Visualisation",
        "level": 4,
        "evidence": [
            {"org": "ByteDance", "detail": "12 dashboards - GMV trend heatmaps, product-rating boxplots, user-activity time-series."},
        ],
    },
    {
        "key": "tableau",
        "name": "Tableau",
        "group": "Analytics & Visualisation",
        "level": 3,
        "evidence": [
            {"org": "Coursework", "detail": "Dashboard building for coursework; Power BI is currently my stronger tool."},
        ],
    },
    {
        "key": "dataviz",
        "name": "Dashboard Design & Data Visualisation",
        "group": "Analytics & Visualisation",
        "level": 4,
        "evidence": [
            {"org": "ByteDance", "detail": "Designed daily monitoring views for three workstreams - transaction, product and user."},
        ],
    },
    {
        "key": "conversion_analysis",
        "name": "User Behaviour & Conversion Analysis",
        "group": "Analytics & Visualisation",
        "level": 4,
        "evidence": [
            {"org": "ByteDance", "detail": "Found a 20:00 conversion peak 63% above the daily average; became the basis for campaign scheduling."},
        ],
    },
    {
        "key": "stats",
        "name": "Statistics & Cross-Tabulation",
        "group": "Analytics & Visualisation",
        "level": 4,
        "evidence": [
            {"org": "Roland Berger", "detail": "Multi-dimensional cross-tabulation of 200+ survey responses into 5 core findings."},
            {"org": "Coursework", "detail": "Business Statistics, Managerial Statistics, Market Research & Data Analysis; SPSS."},
        ],
    },
    {
        "key": "ai_workflow",
        "name": "AI / LLM Agent Workflows",
        "group": "AI Applications",
        "level": 5,
        "evidence": [
            {"org": "Western Securities", "detail": "LLM agents to structure 30+ expert interviews; agents pre-read filings for first-pass screening."},
            {"org": "Roland Berger", "detail": "AI-agent topic clustering of open-ended survey feedback; AI research agents to map the robotics value chain."},
            {"org": "ByteDance", "detail": "AI-assisted QA workflow for missing values, outliers and format validation."},
        ],
    },
    {
        "key": "benchmarking",
        "name": "Competitor Benchmarking",
        "group": "Business & Commercial",
        "level": 4,
        "evidence": [
            {"org": "L'Oreal (China)", "detail": "Benchmarked Chando and Proya on portfolio, pricing and promotions; 3 opportunities adopted into the Q3 category plan."},
        ],
    },
    {
        "key": "ecommerce",
        "name": "E-Commerce & Promotions Analytics",
        "group": "Business & Commercial",
        "level": 4,
        "evidence": [
            {"org": "L'Oreal (China)", "detail": "E-commerce sell-through and promotion datasets; findings informed 3 major promotional campaigns."},
            {"org": "ByteDance", "detail": "GMV trend monitoring across the transaction workstream."},
        ],
    },
    {
        "key": "survey",
        "name": "Survey Design & Scale Analysis",
        "group": "Business & Commercial",
        "level": 4,
        "evidence": [
            {"org": "Roland Berger", "detail": "Designed a management diagnostic survey covering strategy execution and organisational structure."},
        ],
    },
    {
        "key": "industry_research",
        "name": "Industry & Equity Research",
        "group": "Business & Commercial",
        "level": 4,
        "evidence": [
            {"org": "Western Securities", "detail": "Supported 30-50 page semiconductor reports on foundry, foldable display and AI chips."},
            {"org": "Roland Berger", "detail": "Fundamental analysis on 10+ robotics companies for a market-entry deck."},
        ],
    },
    {
        "key": "business_writing",
        "name": "Business Writing & Stakeholder Reporting",
        "group": "Business & Commercial",
        "level": 4,
        "evidence": [
            {"org": "L'Oreal (China)", "detail": "~20,000-character CRM industry report with strategic recommendations."},
            {"org": "Roland Berger", "detail": "Contributed to a 15+ page market-entry deck."},
        ],
    },
]

# Ready-made requirement profiles, so a recruiter can start from one click
# instead of ticking sixteen boxes. The first one is the default on load.
ROLE_PRESETS = [
    {
        "title": "E-Commerce Analyst Intern",
        "blurb": "The role this resume is written for: messy transaction data, daily reporting, promotion analysis.",
        "required": ["sql", "python", "excel", "power_bi", "conversion_analysis", "ecommerce", "data_quality", "dataviz"],
    },
    {
        "title": "Data / BI Analyst",
        "blurb": "Heavier on the pipeline and the dashboard than on the commercial question.",
        "required": ["sql", "python", "power_bi", "tableau", "dataviz", "data_quality", "database", "stats"],
    },
    {
        "title": "Market & Consumer Research",
        "blurb": "Survey design, competitor work and the write-up that goes to the client.",
        "required": ["survey", "stats", "benchmarking", "excel", "industry_research", "business_writing"],
    },
    {
        "title": "Strategy / Consulting Analyst",
        "blurb": "Industry mapping, benchmarking and deck-ready conclusions at speed.",
        "required": ["industry_research", "benchmarking", "business_writing", "stats", "ai_workflow", "excel"],
    },
]

# The default requirement profile used when the app first loads.
TARGET_ROLE = ROLE_PRESETS[0]

EDUCATION = [
    {
        "school": "Nanyang Technological University",
        "degree": "MSc, Business Analytics",
        "period": "Aug 2026 - Present",
        "notes": ["Key courses: Analytics Strategy; AI & Big Data in Business; Strategies for Digital Transformation in Business"],
    },
    {
        "school": "Beijing Jiaotong University",
        "degree": "BBA, Business Administration",
        "period": "Sep 2022 - Jun 2026",
        "notes": [
            "GPA 3.74 / 4.0",
            "Key courses: Python for Data Analysis, Business Statistics, Managerial Statistics, Market Research & Data Analysis, Strategic Management, Operations & Supply Chain Management",
        ],
    },
]

AWARDS = [
    "1st Prize, Shandong Province - 15th \"Zhengda Cup\" National Market Research & Analysis Competition (2025)",
    "Silver Award, Beijing Region - \"Challenge Cup\" National Entrepreneurship Plan Competition (2024)",
    "1st Prize, University level - National E-Commerce \"Innovation, Creativity & Entrepreneurship\" Challenge (2023)",
    "Academic Excellence Scholarship (2nd Class), BJTU (2022-23, 2023-24)",
    "\"Merit Student\", BJTU (2023)",
]

LANGUAGES = [
    "Mandarin - native",
    "English - IELTS 7.0, CET-6",
]

# Order in which skill groups appear on both pages.
SKILL_GROUPS = [
    "Data Engineering & Preparation",
    "Analytics & Visualisation",
    "AI Applications",
    "Business & Commercial",
]
