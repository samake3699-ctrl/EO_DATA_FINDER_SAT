# Sprint 1 Report — EO Data Finder
  
> **Sprint:** S1 — Product and Foundation | **Period:** October 5–18, 2026  
> **Student:** Adama SAMAKE | **Group:** M80-103CB-26 | **MAI**

**Project:** EO Data Finder — Finding Satellite Data

| Sprint 1 evidence | Link |
|---|---|
| **Demo video (screen + English narration)** | [Sprint 1 demo — GitHub Release](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/releases/tag/sprint-1) |
| **Public source repository** | [EO_DATA_FINDER_SAT](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT) |
| **GitHub Projects board** | [EO Data Finder — Agile board](https://github.com/users/samake3699-ctrl/projects/1/views/1) |

---

## 1. Sprint goal

Establish the product foundation by organizing a prioritized backlog, configuring the development environment, building the initial project structure, and demonstrating the first local prototype of EO Data Finder.

## 2. Product context and semester scope

**Problem:** Finding appropriate satellite products can require users to compare geographic coverage, acquisition dates, cloud coverage, product types, and availability manually. Preparing these products for environmental analysis adds further work.

**Target users:** Students, researchers, analysts, engineers, agricultural and environmental services, and public-sector organizations working with Earth Observation data.

**Core value:** Make satellite-product discovery easier and, over the semester, support a first practical analysis of vegetation condition and experimental drought risk.

**Scope boundary:** The semester MVP focuses on one pilot area, a limited number of Sentinel-2 scenes, and one environmental use case: vegetation condition and experimental drought-risk monitoring. Flood mapping, crop-yield prediction, and operational warning services are outside its scope.

## 3. Sprint 1 deliverables and results

| Required S1 foundation | Completed work / evidence |
|---|---|
| **Public repository and Agile board** | Repository and GitHub Project set up; tasks managed through the Backlog, Todo, In Progress, Testing, and Done workflow. |
| **Prioritized product backlog** | The backlog is organized into prioritized feature groups (epics): satellite-product search, product metadata and access, and vegetation/drought analysis. These are broken down into smaller development tasks tracked on the project board. |
| **Development environment** | React, Vite, JavaScript/CSS, Git, VS Code, and `pnpm` configured; prototype runs locally with `pnpm run dev`. |
| **Project skeleton** | Basic frontend structure and configuration established, including `src/`, `public/`, `package.json`, `vite.config.js`, `.gitignore`, and `README.md`. |
| **Visible prototype and demo** | A working local interface and an English screen-and-voice demonstration, linked above. |

### Functional prototype demonstrated

1. **Search criteria:** pilot area, start date, end date, and maximum cloud coverage.
2. **Input validation:** checks for incomplete or inconsistent search criteria, including an invalid date range.
3. **Product results:** a table of **simulated** Sentinel-2 Level-2A products, with product selection.
4. **Experimental analysis preview:** a **simulated** NDVI-condition display, vegetation and rainfall indicators, and a one-month drought-risk category.
5. **Manual review:** the principal local interaction scenarios were checked in preparation for the demonstration.

> **Scientific limitation:** Sprint 1 uses demonstration products and indicators. It does **not** retrieve actual Copernicus imagery, calculate real NDVI or CHIRPS anomalies, or produce a scientifically validated drought forecast. 


## 4. Mini-retrospective

### What went well

- I established the project structure and organized work on a public GitHub board.
- I completed a demonstrable React/Vite prototype covering the main search-to-preview user flow.
- I clearly separated demonstration data from features that will require real satellite data and scientific processing.

### What did not go well

- Git synchronization and local development-server configuration took more time than planned.
- Preparing the video required extra work, especially on editing, transitions, and audio synchronization.
- Although the interface works, its visual hierarchy, readability, consistency, and overall usability still need improvement.

### Problems and blockers

- I had to resolve repository synchronization issues and correct the local Vite launch workflow.
- Video-editing and audio-synchronization difficulties delayed the demonstration preparation.
- Real Copernicus access and scientific analysis are not available in S1; this is a planned limitation of the prototype, not a validated analytical result.

### Two experiments for Sprint 2

1. **Deliver one verified vertical slice at a time:** demonstrate a complete path from the React form to a FastAPI endpoint and SQLite metadata, checking the result before adding further features.
2. **Test earlier and gather focused feedback:** run automated API checks as features are developed and ask a potential user to try the refined search interface, recording one or two concrete usability observations.

## 5. Book takeaways — *The Lean Product Playbook*, Dan Olsen

**Selected topic:** Chapter 1 — *Achieving Product-Market Fit with the Lean Product Process*.  
**Publisher's chapter excerpt:** [Read the official Wiley PDF](https://catalogimages.wiley.com/images/db/pdf/9781118960875.excerpt.pdf).

### What I consider important and useful

- **A product should create real user value.** Product-market fit is not demonstrated just because an interface works: the product must address meaningful customer needs.
- **Follow a structured Lean Product Process.** The chapter outlines six steps: identify target users, understand underserved needs, define the value proposition, choose an MVP feature set, create a prototype, and test it with users.
- **Validate progressively.** A prototype is a starting point for learning; successful technical implementation is different from confirmed user value.

### What I have already applied — and why

- I defined the target audience, problem, and core value in my project application instead of beginning with technology choices alone.
- I deliberately limited the semester MVP to one pilot area and one drought-related use case, so the work remains achievable within the course schedule.
- I built an S1 prototype to demonstrate the search workflow before committing to real imagery, numerical processing, and prediction models.

### What I plan to apply — and why

I will improve the interface to make the search workflow clearer and more professional, then seek brief feedback from potential users. This will help me distinguish a technically functioning screen from a product that users can navigate and understand. I will continue to add capabilities incrementally rather than expanding beyond the approved MVP.

## 6. Next sprint — S2: MVP (October 19–November 1)

**Goal:** Extend the prototype toward a testable frontend–backend workflow using FastAPI, SQLite metadata, server-side filtering, and automated tests. Improve React interface consistency and usability while keeping the agreed semester scope unchanged.

Actual Copernicus data access, NDVI processing, CHIRPS rainfall analysis, and the experimental risk-estimation module remain planned for the later semester sprints; none is claimed as completed in Sprint 1.

---

**Sprint 1 outcome:** The initial product scope, development environment, repository structure, backlog, and demonstrable local prototype are in place. Sprint 2 will focus on a stronger data flow, tests, and user experience rather than adding unrelated use cases.
