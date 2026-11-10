# Claude Experiments — Tracking Log

> Personal learning journal: experiments with Claude to work more efficiently as a developer.
> Each entry has a status, objective, notes and key learnings.

---

## How to use this file

| Status | Meaning |
|--------|---------|
| ⬜ To do | Not started |
| 🔄 In progress | Currently experimenting |
| ✅ Done | Completed, learnings captured |
| ⏸ Paused | On hold |

---

## Level 1 — Immediate productivity

### EXP-01 · Refactor legacy code
- **Status:** ⬜ To do
- **Goal:** Paste real PHP or C# legacy code and ask Claude to modernise it. Compare the result with the original.
- **Suggested prompt:** *"Refactor this PHP function following modern best practices. Keep the same behaviour but improve readability, structure and performance."*
- **Notes:**
- **Learnings:**

---

### EXP-02 · SQL query optimisation
- **Status:** ⬜ To do
- **Goal:** Take a slow or complex SQL query (MySQL or SQL Server) and ask Claude to optimise it. Explain the difference in strategy.
- **Suggested prompt:** *"Analyse this SQL query, identify performance bottlenecks and propose an optimised version with an explanation of each change."*
- **Notes:**
- **Learnings:**

---

### EXP-03 · Generate unit tests for existing code
- **Status:** ⬜ To do
- **Goal:** Give Claude a function without tests and ask it to generate a complete test suite (PHPUnit or xUnit).
- **Suggested prompt:** *"Write unit tests for this function. Cover the happy path, edge cases and error scenarios."*
- **Notes:**
- **Learnings:**

---

### EXP-04 · Auto-generate documentation
- **Status:** ⬜ To do
- **Goal:** Ask Claude to add PHPDoc / XML Doc comments to undocumented functions.
- **Suggested prompt:** *"Add complete PHPDoc comments to these functions: parameters, return types, exceptions and a brief description."*
- **Notes:**
- **Learnings:**

---

## Level 2 — AI-assisted workflow

### EXP-05 · Automated code review
- **Status:** ⬜ To do
- **Goal:** Paste a git diff or a file and ask Claude to review it as a senior developer would.
- **Suggested prompt:** *"Review this code as a senior developer. Look for bugs, security issues, performance problems and style inconsistencies. Be direct."*
- **Notes:**
- **Learnings:**

---

### EXP-06 · Generate realistic test data
- **Status:** ⬜ To do
- **Goal:** Ask Claude to generate SQL INSERT scripts or fixtures for a specific schema.
- **Suggested prompt:** *"Generate 20 rows of realistic test data for this MySQL table. Use plausible values, not Lorem Ipsum."*
- **Notes:**
- **Learnings:**

---

### EXP-07 · Cross-language migration
- **Status:** ⬜ To do
- **Goal:** Take a PHP function with business logic and ask Claude to rewrite it in C# (or vice versa). Analyse the differences.
- **Suggested prompt:** *"Migrate this PHP class to C# keeping the same business logic. Use idiomatic C# patterns."*
- **Notes:**
- **Learnings:**

---

### EXP-08 · Database schema design
- **Status:** ⬜ To do
- **Goal:** Describe a business problem in plain English and ask Claude to propose the relational model (tables, keys, indexes).
- **Suggested prompt:** *"Design a MySQL schema for a survey management system. Include tables, relationships, primary/foreign keys and suggested indexes."*
- **Notes:**
- **Learnings:**

---

## Level 3 — AI inside your own projects

### EXP-09 · Integrate Claude API in a PHP app
- **Status:** ⬜ To do
- **Goal:** Build a minimal PHP script that calls the Claude API and processes a response. First real integration.
- **Suggested prompt:** *(Code exercise — no prompt needed, build it)*
- **Resources:** [Claude API docs](https://docs.anthropic.com)
- **Notes:**
- **Learnings:**

---

### EXP-10 · Prompt engineering — systematic testing
- **Status:** ⬜ To do
- **Goal:** For the same task, test 3 different prompts (zero-shot, few-shot, chain-of-thought). Document which works best and why.
- **Task to test on:** SQL optimisation or code review
- **Notes:**
- **Learnings:**

---

### EXP-11 · AI agent for data analysis
- **Status:** ⬜ To do
- **Goal:** Given a CSV or SQL result, ask Claude to analyse it, find patterns and generate a summary report. Relevant for your ERP/reporting background.
- **Suggested prompt:** *"Analyse this dataset. Identify trends, anomalies and key insights. Format the output as an executive summary."*
- **Notes:**
- **Learnings:**

---

### EXP-12 · Automate a repetitive dev task
- **Status:** ⬜ To do
- **Goal:** Identify a task you do manually and repeatedly (generating boilerplate, writing migration scripts, formatting data) and ask Claude to build a script that automates it.
- **Task identified:**
- **Notes:**
- **Learnings:**

---

## Level 4 — Spec Driven Development

### EXP-13 · SDD — Write a spec, implement from it
- **Status:** ✅ Done
- **Goal:** Write a full spec for a small feature using `specs/_TEMPLATE.md`, have Claude review it, then implement and generate tests from it. Practice the full SDD loop.
- **Suggested prompt (spec review):** *"Review this spec as a senior developer. Identify: missing requirements, ambiguous statements, untestable criteria, and anything that would cause problems during implementation."*
- **Suggested prompt (implementation):** *"Implement this feature strictly following the spec. For each functional requirement, add a comment referencing its ID (FR-01, etc.). Do not add anything not in the spec."*
- **Suggested prompt (test generation):** *"Generate unit tests based on the acceptance criteria in this spec. Each scenario maps to at least one test. Name the tests after the scenario."*
- **Spec file:** `specs/exp-13-gbp-eur-converter.md`
- **Implementation:** `exp-13-gbp-eur-converter/converter.py`
- **Notes:** Built a GBP→EUR historical converter using frankfurter.app API. Generates a self-contained HTML report with daily rates for the first trading day of each month, color-coded by above/below average rate. Implemented and tested entirely from VS Code local using Claude Code.
- **Learnings:**
  - SDD forces you to think through edge cases before writing code — the spec caught validation requirements (FR-07, FR-08) that would have been easy to miss
  - Claude generates tests directly mapped to acceptance criteria when the spec uses Given/When/Then format
  - Working locally in VS Code is faster for iteration than cloud sessions — no push/pull needed between edits
  - `frankfurter.app` is a solid free API for currency data with no API key required

---

### EXP-14 · SDD — Claude reviews and improves a spec
- **Status:** ⬜ To do
- **Goal:** Write a deliberately incomplete or vague spec and ask Claude to identify gaps, contradictions and untestable requirements. Learn what makes a good spec.
- **Suggested prompt:** *"This spec has intentional flaws. Act as a QA engineer and find: missing edge cases, contradictory requirements, acceptance criteria that cannot be tested, and requirements that are too vague to implement."*
- **Notes:**
- **Learnings:**

---

## General notes & patterns

> Use this section to note cross-experiment observations: prompt styles that work well, common mistakes, time saved, etc.

---

## Progress summary

| Level | Total | Done | In progress |
|-------|-------|------|-------------|
| Level 1 — Immediate productivity | 4 | 0 | 0 |
| Level 2 — AI-assisted workflow | 4 | 0 | 0 |
| Level 3 — AI inside projects | 4 | 0 | 0 |
| Level 4 — Spec Driven Development | 2 | 1 | 0 |
| **Total** | **14** | **1** | **0** |
