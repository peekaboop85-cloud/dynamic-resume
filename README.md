# Dynamic Resume - AN6100 Assignment Part 1

A static HTML resume and a Streamlit application, both generated from one data file.

## Files

| File | What it is |
| --- | --- |
| `resume_data.py` | The only place the resume content lives |
| `build_static_html.py` | Reads the data and writes `resume.html` |
| `resume.html` | The static page (self-contained, no JavaScript) |
| `resume_app.py` | The Streamlit application |
| `assets/photo.jpg` | Portrait, embedded into `resume.html` at build time |

## How to run it in VS Code

Open this folder in VS Code, then open a terminal (Terminal > New Terminal) and run:

**1. Create the environment and install Streamlit (first time only)**

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

On Windows use `.venv\Scripts\pip` instead of `.venv/bin/pip`.

**2. Rebuild the static page**

```
.venv/bin/python build_static_html.py
```

This writes `resume.html`. Open it by double-clicking, or right-click it in VS Code
and choose "Open with Live Server" / "Reveal in Finder".

**3. Run the Streamlit app**

```
.venv/bin/streamlit run resume_app.py
```

The app opens at http://localhost:8501. Press Ctrl+C in the terminal to stop it.

> Tip: select the `.venv` interpreter in VS Code (Cmd+Shift+P > "Python: Select
> Interpreter") and you can then just run `streamlit run resume_app.py`.

## How to update the resume

Edit `resume_data.py` only, then re-run step 2. Both the static page and the
Streamlit app read the same file, so they never drift apart.

> **Restart Streamlit after editing `resume_data.py`.** Streamlit re-runs
> `resume_app.py` on save, but an imported module stays cached in memory, so the
> old content keeps showing until you stop the server (Ctrl+C) and start it
> again. Editing `resume_app.py` itself does hot-reload normally.

* new internship - append a dictionary to `EXPERIENCE`
* new skill - append a dictionary to `SKILLS` and reference its `key` from a role
* new headline figure - append a dictionary to `HIGHLIGHTS`

## Assignment constraints respected

* No JavaScript anywhere in `resume.html`
* No `class`, no `lambda`, no `pandas` in any `.py` file
* No phone number, ID number or street address on either page
