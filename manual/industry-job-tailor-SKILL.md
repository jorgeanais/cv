---
name: industry-job-tailor
description: Translates academic experience and long-form CVs into tailored, high-impact industry resumes (1-2 pages), ATS-optimized profiles, and recruiter outreach pitches.
tools:
  - bash
  - read_file
  - write_file
---

# Industry Job Search & Resume Tailoring Skill

## Purpose
Bridge the gap between academic research/teaching and industry hiring requirements (Data Science, Machine Learning Engineering, AI Research, and Technical Leadership).

## Capabilities
1. **JD Analysis & Keyword Extraction**: Parse a target Job Description (JD) to identify core technical requirements, leadership traits, and domain keywords.
2. **Academic-to-Industry Translation**: Rewrite academic bullet points into the Google XYZ format: *"Accomplished [X], as measured by [Y], by doing [Z]"*.
3. **Resume Generation**: Produce clean, 1-to-2-page industry-standard Markdown or LaTeX resumes customized for specific roles.
4. **ATS Gap Scoring**: Compare the source CV against the JD to calculate match percentage and suggest missing technical/soft skill keywords.
5. **Recruiter Pitch Generation**: Create short LinkedIn/email messages tailored for agency headhunters and corporate talent acquisition.

---

## Translation Rules

### 1. Phrasing Equivalencies
| Academic Activity | Industry Translation |
| :--- | :--- |
| PhD / Postdoc Research | End-to-end R&D, Machine Learning pipelines, statistical modeling, algorithmic optimization |
| Telescope / Lab Data Reduction | Data pipeline engineering, ETL, quality assurance, petabyte/terabyte-scale big data processing |
| University Lecturing / Teaching | Technical mentorship, stakeholder communication, cross-functional training, curriculum design |
| Grant Writing & PI Duties | Project management, resource allocation, funding acquisition, roadmap delivery |
| First-author / Peer-reviewed Papers | Technical documentation, white papers, production-ready algorithm development |

### 2. Bullet Point Structuring Formula
- **Avoid:** "Studied the distribution of stars using unsupervised clustering algorithms."
- **Adopt:** "Engineered unsupervised clustering pipelines in Python/SciPy, identifying 3 novel high-density target clusters across dense astronomical survey datasets."

---

## Workflow Modes

### Mode 1: ATS Gap Analysis
```bash
# Run comparison between target JD and base CV
opencode run industry-job-tailor --analyze --jd="path/to/job_description.txt" --cv="path/to/cv.md"
```
**Output:**
- Match Score (0–100%)
- Matched hard/soft skills
- Critical missing keywords
- Recommendations for repositioning

### Mode 2: Targeted 1-2 Page Resume Builder
```bash
# Generate a role-specific industry resume
opencode run industry-job-tailor --generate --role="Senior Machine Learning Engineer" --format="latex"
```
**Output:**
- Compiled `resume_targeted.tex` (or `.md`)
- Highlighting production frameworks (PyTorch, Docker, PostgreSQL, Python), cloud/ETL pipelines, and quantifiable metrics over chronological lists of publications.

### Mode 3: Recruiter Outreach Generator
```bash
# Generate elevator pitches for LinkedIn / Headhunter messages
opencode run industry-job-tailor --pitch --recipient="Tech Recruiter" --company="Target Company"
```
**Output:**
- 100-word concise note highlighting 5+ years of ML/DL expertise, real-world data processing experience, and technical leadership.