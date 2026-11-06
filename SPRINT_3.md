# Sprint 3 — Growth

**Project:** EO Data Finder — Finding Satellite Data  
**Student:** Adama SAMAKE
**Group:** M80-103CB-26
**University:** Moscow Aviation Institute (MAI)
**Sprint period:** November 2–15, 2026  
**Sprint status:** Technical implementation validated; documentation and demonstration pending.

## 1. Sprint Goal

Connect EO Data Finder to the real Copernicus Sentinel-2 catalogue, enable satellite product metadata retrieval and local database persistence, and validate the application through automated tests and end-to-end checks.

## 2. Implemented Features

- Integrated real Sentinel-2 Level-2A product search using the Copernicus Data Space catalogue.
- Applied acquisition date and maximum cloud coverage filters to the Sikasso pilot area in Mali.
- Displayed real satellite product metadata in the React interface.
- Enabled users to select a satellite product.
- Implemented metadata persistence in SQLite through FastAPI and SQLAlchemy.
- Added duplicate detection for previously saved products.
- Connected product selection to the analysis workspace.
- Updated interface messages to distinguish real catalogue data from simulated drought-risk indicators.

## 3. Validation Results

- Backend automated tests: 18 passed.
- Copernicus connectivity: successful.
- Real catalogue search: three Sentinel-2 products retrieved during the manual check.
- Product metadata saving: successful.
- React catalogue and analysis navigation: verified.
- Production build: successful.
- Oxlint: zero warnings and zero errors.

## 4. Current Limitations

- Catalogue searches currently focus on the Sikasso pilot area.
- Satellite image bands are not yet downloaded or processed.
- Vegetation and drought-risk indicators remain demonstrations, not scientific predictions.
- The current database stores product metadata rather than complete satellite imagery.

## 5. Lessons from Designing Data-Intensive Applications

**Reliability:** Automated tests help verify application behavior, but real integration checks are also necessary when the application depends on external services such as Copernicus.

**Storage and Retrieval:** Structured product metadata is stored in SQLite. Large satellite data files will be handled separately in a later development stage, with their references linked to the stored metadata.

These principles support the current prototype architecture and help identify improvements for future development.

## 6. Sprint Retrospective

**What went well:** Real catalogue integration, database persistence, and frontend navigation were successfully validated.

**Challenges:** Moving from demonstration data to real external API responses required integration checks beyond isolated automated tests.

**Improvements for the next sprint:** Continue using incremental implementation, automated testing, and real-data validation. Improve satellite data retrieval and processing while keeping the application architecture manageable.

## 7. Next Steps

- Finalize Sprint 3 documentation and GitHub Project Board.
- Prepare the Sprint 3 demonstration video.
- Begin Sprint 4 development in a separate branch.

## 8. Sprint 3 Deliverables

**Source code:**
https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/tree/s3-prep

**Agile Project Board:**
https://github.com/users/samake3699-ctrl/projects/1/views/1

**Demo video:**
Pending recording and publication.

**Book Reference:**
Martin Kleppmann, Designing Data-Intensive Applications,
O'Reilly Media, 2017.