# Sprint 2 — From Prototype to Functional MVP

**Project:** EO Data Finder  
**Student:** Adama SAMAKE  
**Group:** M80-103CB-26  
**University:** Moscow Aviation Institute (MAI)  
**Period:** October 19 – November 1, 2026

## 1. Sprint Goal

Transform the Sprint 1 prototype into a functional MVP by connecting React to a Python FastAPI backend and a SQLite database.

## 2. Completed Tasks

- Improved the React user interface.
- Developed the FastAPI backend.
- Integrated SQLite using SQLAlchemy.
- Implemented satellite product searches with date and cloud coverage filters.
- Added product selection and an analysis preview.
- Created 14 automated API tests using Pytest.
- Prepared and published the Sprint 2 demo video.

## 3. Sprint Review and Testing

The application now uses the following architecture:

**React → FastAPI → SQLite**

Users can search for satellite products, apply filters, and select a product for analysis.

**Testing result: 14 tests passed.**

The satellite catalogue uses demonstration records, and environmental indicators remain simulated.

## 4. Sprint Retrospective

**What went well:**

- Successfully connected the frontend, backend, and database.
- Completed the planned features and automated tests.

**What was difficult:**

Everything went well during Sprint 2. No major difficulties were encountered.

**Next sprint improvements:**

- Integrate real satellite catalogue data.
- Continue testing new features.
- Continue improve interface.

## 5. Clean Code — Reading and Application

During Sprint 2, I read selected chapters of Robert C. Martin's *Clean Code* and applied these principles:

- **Meaningful names:** Used clear function names such as `get_products` and `handleSearch`.
- **Code organization:** Separated the API, database, and frontend.
- **Error handling:** Added validation for dates and cloud coverage.
- **Testing:** Created 14 automated tests using Pytest.

These practices helped me write more readable, organized, and testable code.

**Book Reference:**  
Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship* (2008).  
https://www.pearson.com/en-us/subject-catalog/p/Martin-Clean-Code-A-Handbook-of-Agile-Software-Craftsmanship/P200000009044

## 6. Sprint 2 Deliverables

**Source code:**  
https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/tree/s2-prep

**Demo video:**  
https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/releases/tag/sprint-2

**Agile Board:**  
https://github.com/users/samake3699-ctrl/projects/1/views/1
