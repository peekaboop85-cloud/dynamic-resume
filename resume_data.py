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
        "summary": "Data quality and business reporting for the User Growth team, across user behaviour and transaction data.",
        "icon": "chart",
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
        "summary": "Competitor benchmarking and CRM research for the beauty category team.",
        "icon": "target",
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
        "summary": "Sell-side equity research covering the electronics and semiconductor sector.",
        "icon": "chip",
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
        "summary": "Consulting project team, on a management diagnostic and a cross-industry M&A study.",
        "icon": "briefcase",
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
{
        "key": "product",
        "name": "Product Definition & 0-to-1 Delivery",
        "group": "AI Applications",
        "level": 4,
        "evidence": [
            {"org": "BaoBeiCang", "detail": "PRD covering 6 modules, 27 pages, P0-P3 priorities, a five-stage release plan and the pricing ladder; shipped and accepted on a real device."},
            {"org": "Wengua", "detail": "Defined the product, the trust mechanisms and the compliance red lines before any feature was built."},
        ],
    },
    {
        "key": "rag",
        "name": "RAG & LLM Application Engineering",
        "group": "AI Applications",
        "level": 4,
        "evidence": [
            {"org": "BaoBeiCang", "detail": "Six-stage OCR-to-LLM pipeline; only one stage left to the model, the rest rule-coded. 10 hard prompt constraints written against a real hallucination failure."},
            {"org": "RAG Agents Project", "detail": "Two retrieval-augmented agents on Coze, tuned against a 1,000-comment hand-labelled evaluation set."},
        ],
    },
    {
        "key": "ml",
        "name": "Machine Learning & SEM",
        "group": "Analytics & Visualisation",
        "level": 4,
        "evidence": [
            {"org": "Chia Tai Cup Project", "detail": "K-means segmentation plus a structural equation model of satisfaction, cross-validated against random forest and XGBoost feature importance."},
        ],
    },
    {
        "key": "econometrics",
        "name": "Panel Econometrics & Causal Inference",
        "group": "Research Methods",
        "level": 4,
        "evidence": [
            {"org": "Published research", "detail": "28,473 firm-year panel with industry and year fixed effects; mediation via the KZ index; Altman Z-score and Merton distance-to-default as alternative measures."},
            {"org": "Working paper", "detail": "Moderated-mediation design with entropy balancing, IPW, propensity-score matching and placebo tests."},
        ],
    },
    {
        "key": "qualitative",
        "name": "Qualitative & Case Research",
        "group": "Research Methods",
        "level": 4,
        "evidence": [
            {"org": "Undergraduate dissertation", "detail": "Longitudinal single-case study of CIMC Group; Gioia method with 41 first-order concepts, 15 themes and 4 aggregate dimensions; CiteSpace across 539 publications."},
            {"org": "CATL working paper", "detail": "Executive interviews triangulated against disclosures, patent portfolio and industry coverage."},
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
    "Research Methods",
]


# ---------------------------------------------------------------------------
# Projects I started myself, rather than work I was assigned.
# Same shape as EXPERIENCE so both render through the same card.
# ---------------------------------------------------------------------------
PROJECTS = [
    {
        "id": "baobeicang",
        "summary": "Photograph an insurance policy, get an AI check-up report in three minutes - score, radar chart and risk list - then hand off to a human expert.",
        "icon": "shield",
        "org": "BaoBeiCang - AI Insurance Policy Check-up",
        "role": "Product Owner & Solo Developer (0 to 1)",
        "period": "Apr 2026 - Jul 2026",
        "impact": "Shipped and accepted on a real device: 73 commits, ~15,200 lines of product code and 5,600 lines of tests, with 119 backend and 80 frontend tests passing.",
        "bullets": [
            "Ran demand research across users, agents and engineering and concluded the market gap was neutral policy interpretation, not more selling. Wrote the PRD - 6 modules, 27 pages, P0-P3 priorities, a five-stage release plan - and the pricing ladder from a free check-up to a paid expert review, membership and an annual managed plan.",
            "Designed a six-stage pipeline: batch upload, OCR, content validation, deterministic fact extraction, LLM scoring, then de-duplication. Anything that could be expressed as a rule was taken out of the model, leaving one stage to the LLM. Settings were split by job - temperature 0.2 with enforced JSON for scoring, 0.7 with a follow-up protocol for advisory chat, handing over to a human at the third turn.",
            "Wrote 10 hard prompt constraints after a real failure in which the model asserted a user had no critical-illness cover when they had only uploaded a summary screenshot: coverage bands locked to an enumeration, no penalty for content that was never shown, and an explicit 'insufficient information' answer with product recommendations forbidden in that case. Set a 90% recognition-accuracy gate below which the product would not be promoted at all.",
        ],
        "skills": ["product", "rag", "ai_workflow", "python", "data_quality"],
    },
    {
        "id": "wengua",
        "summary": "BaZi charting, I Ching hexagram casting and practitioner sessions, in a category dominated by fortune-telling apps with poor reputations.",
        "icon": "compass",
        "org": "Wengua - Chinese Culture & Emotional Companion App",
        "role": "Founder, product definition and prototype (0 to 1)",
        "period": "Jul 2026 - Present",
        "impact": "Core demo working end to end, with the hardest domain logic built first and the business model argued only after it ran.",
        "bullets": [
            "Set a dual value anchor - classical Chinese culture plus emotional support for women - and made every product decision answer to it: conversations follow empathise, then interpret, then advise; scenarios centre on relationships rather than fortune or wealth. The positioning also resolves the category's compliance problem, because cultural companionship makes no claims about anyone's fate.",
            "Designed the trust mechanisms, because the thing that kills credibility in this category is a result that looks arbitrary. The daily draw is seeded from user ID plus date, so re-entering the same day cannot reroll it; hexagram casting uses cryptographically secure randomness, with the cast and its seed stored so any reading can be reproduced and audited afterwards.",
            "Fixed the content red lines before the feature list: the product describes itself only as cultural and emotional companionship, never as regulated counselling, and no script may promise to change or avert anyone's fortune. These became the review standard for practitioner scripts.",
        ],
        "skills": ["product", "ai_workflow", "python"],
    },
    {
        "id": "rag_agents",
        "summary": "Two retrieval-augmented agents: one for automated analytical reporting, one for sentiment classification of customer feedback.",
        "icon": "robot",
        "org": "RAG-Enhanced Agents for Market Research",
        "role": "Independent Developer",
        "period": "Feb 2025 - Jun 2025",
        "impact": "Two retrieval-augmented agents delivered end to end, measured against hand-labelled data rather than impressions.",
        "bullets": [
            "Built two Retrieval-Augmented Generation agents on the Coze platform - one for automated analytical reporting, one for semantic sentiment classification of customer feedback - with a domain knowledge base and vector store to beat a general-purpose LLM baseline on retrieval relevance.",
            "Assembled a 1,000-comment manually annotated evaluation set and iterated the knowledge base and prompts against it until agreement with the human labels stabilised. Ran the whole cycle alone: workflow design, prompt engineering, testing and delivery.",
        ],
        "skills": ["rag", "ai_workflow", "python"],
    },
    {
        "id": "chiatai",
        "summary": "A national market research competition entry on how tourists adopt digital travel services.",
        "icon": "chart",
        "org": "Tourist Segmentation - 15th 'Chia Tai Cup' National Competition",
        "role": "Group Leader",
        "period": "Jan 2025 - Apr 2025",
        "impact": "First Prize, Shandong Provincial Division.",
        "bullets": [
            "Designed the survey instrument and led the quantitative workflow: collected and cleaned 550 valid responses on tourists' adoption of digital services in Python, segmented respondents with K-means, and specified a structural equation model of satisfaction in which digital service quality, transport accessibility and interactive engagement carried the strongest path effects.",
            "Cross-checked the SEM path structure against random forest and XGBoost feature importance, and corroborated the findings with automated text clustering and a RoBERTa sentiment classifier run over open-ended responses and web reviews.",
        ],
        "skills": ["ml", "stats", "survey", "python", "dataviz"],
    },
]

# ---------------------------------------------------------------------------
# University research and programmes.
# ---------------------------------------------------------------------------
CAMPUS = [
    {
        "id": "iigf",
        "summary": "Research assistant at a green finance institute, building the policy and standards base its research ran on.",
        "icon": "leaf",
        "org": "International Institute of Green Finance, CUFE",
        "role": "Research Assistant",
        "period": "Feb 2024 - May 2025",
        "impact": "Built the reference base the institute's downstream green-finance research ran on.",
        "bullets": [
            "Built and maintained a structured repository of international agreements, national policies and disclosure standards in green finance, including the Paris Agreement and the G20 sustainable finance agendas.",
            "Co-drafted research reports and policy briefs, authoring literature review and policy comparison sections and running preliminary descriptive analysis.",
            "Delivered outputs in both Chinese and English, keeping terminology consistent across the institute's bilingual publications.",
        ],
        "skills": ["industry_research", "business_writing", "database"],
    },
    {
        "id": "innovation_program",
        "summary": "A nationally funded undergraduate research project on how state-owned enterprises realign ESG strategy under digital transformation.",
        "icon": "flag",
        "org": "National Innovation & Entrepreneurship Training Programme",
        "role": "Team Leader - SOE ESG Strategy in the Digital Era",
        "period": "May 2023 - May 2024",
        "impact": "Nationally funded undergraduate research project, led from proposal to final framework.",
        "bullets": [
            "Led a nationally funded project on how Chinese state-owned enterprises realign ESG strategy as digital transformation and regulatory stringency advance together.",
            "Content-coded 50 national policy directives issued from 2000 onwards into a longitudinal regulatory timeline, identifying five institutional turning points that redefined state expectations of disclosure and governance.",
            "Synthesised qualitative and archival evidence into a stage-based framework showing how SOEs reconcile compliance mandates with technological innovation.",
        ],
        "skills": ["qualitative", "industry_research", "business_writing"],
    },
]

# ---------------------------------------------------------------------------
# Publications and working papers.
#   status drives the badge colour on both pages
# ---------------------------------------------------------------------------
PUBLICATIONS = [
    {
        "status": "Published",
        "citation": "Zhan, W., & Jiang, L. (2024). The impact of ESG information disclosure on corporate financial risk - evidence from Chinese enterprises. Highlights in Business, Economics and Management, 44, 299-310.",
        "role": "First and corresponding author",
        "link": "https://doi.org/10.54097/r0p5dx61",
        "link_label": "doi.org/10.54097/r0p5dx61",
        "detail": "Ran the full empirical pipeline alone on 28,473 A-share firm-year observations from 2012 to 2022. ESG disclosure is associated with significantly lower financial risk (b = -0.035, p < 0.01); financing constraints measured by the KZ index carry the effect; and the association is stronger among more digitalised firms (interaction b = -0.008, p < 0.01). Default risk was measured with Altman Z-scores and checked against a Merton distance-to-default model.",
    },
    {
        "status": "In press",
        "citation": "Jiang, L., & Zhan, W. (in press). Impact of ESG ratings on corporate innovation efficiency: evidence from Chinese listed companies. Highlights in Business, Economics and Management.",
        "role": "Co-author",
        "link": "",
        "link_label": "",
        "detail": "Co-designed the conceptual model and identification strategy; led the literature synthesis, panel cleaning and variable construction across CSMAR and patent databases; ran the baseline regressions and robustness checks.",
    },
    {
        "status": "In progress",
        "citation": "Zhan, W. How does executive attention to artificial intelligence translate into firm value? The roles of firm resilience and board network centrality.",
        "role": "Sole author",
        "link": "",
        "link_label": "",
        "detail": "Sequential mixed-methods study of Chinese A-share firms. Executive AI attention is measured from annual-report MD&A text with a purpose-built keyword dictionary; resilience combines return volatility and three-year sales growth; firm value is Tobin's Q. Controlling for AI patent stock separates managerial attention from existing capability - symbolic disclosure from substantive building. A moderated-mediation design reports conditional indirect effects, with entropy balancing, IPW, propensity-score matching and placebo tests as selection checks.",
    },
    {
        "status": "Under revision",
        "citation": "Zhan, W. Research on the multi-actor collaborative governance mechanism of AI-driven management.",
        "role": "Sole author - Outstanding Undergraduate Dissertation",
        "link": "",
        "link_label": "",
        "detail": "Treats AI systems as socio-technical governance regimes that reallocate decision rights and accountability. CiteSpace bibliometric analysis across 539 CNKI and Web of Science publications, then a longitudinal single-case study of CIMC Group across three stages - exploration, platformisation and deep AI embedding - triangulating executive interviews, site notes, archival reports and 80+ regulatory documents. The Gioia method produced 41 first-order concepts, 15 second-order themes and 4 aggregate dimensions.",
    },
    {
        "status": "Working paper",
        "citation": "Zhan, W. The catch-up mechanism of Chinese latecomer enterprises under digitalisation: the case of CATL.",
        "role": "Principal investigator",
        "link": "",
        "link_label": "",
        "detail": "Semi-structured interviews with two senior executives of CATL subsidiaries, triangulated against annual disclosures, the patent portfolio and industry coverage. Thematic coding across interview and operational data delineates five mechanisms linking digital transformation to catch-up advantage.",
    },
]

RESEARCH_STATEMENT = (
    "I study how managerial attention and governance structures decide whether firms turn "
    "emerging technology - particularly AI - into real organisational capability rather than "
    "an announcement. The work combines panel econometrics and text-based measurement with "
    "inductive case research."
)


# ---------------------------------------------------------------------------
# The three tailored resumes offered on the Download tab.
# Built by build_resume_pdfs.py from the markdown in resume_sources/, with the
# phone number and the old mailbox stripped out - neither belongs on a page
# anyone on the internet can open.
# ---------------------------------------------------------------------------
RESUME_DOWNLOADS = [
    {
        "key": "business_analytics",
        "title": "Business Analytics",
        "blurb": "Data quality, dashboards and conversion analysis. The version behind this site.",
        "file": "resumes/business_analytics.pdf",
        "download_name": "Zhan_Wenqian_Business_Analytics.pdf",
    },
    {
        "key": "consulting",
        "title": "Consulting & Equity Research",
        "blurb": "Industry mapping, company fundamentals and the write-up that reaches the client.",
        "file": "resumes/consulting_equity_research.pdf",
        "download_name": "Zhan_Wenqian_Consulting_Equity_Research.pdf",
    },
    {
        "key": "strategy",
        "title": "Strategy & Management Trainee",
        "blurb": "Competitor benchmarking, management diagnostics and cross-functional projects.",
        "file": "resumes/strategy_management_trainee.pdf",
        "download_name": "Zhan_Wenqian_Strategy_Management_Trainee.pdf",
    },
]
