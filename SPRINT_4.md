# Sprint 4 — Environmental Analytics

**Project:** EO Data Finder — Finding Satellite Data  
**Student:** Adama SAMAKE  
**Group:** M80-103CB-26  
**University:** Moscow Aviation Institute (MAI)  
**Sprint period:** November 16–29, 2026  
**Sprint status:** Core features implemented and tested; demo video pending.

## 1. Sprint Goal

Extend EO Data Finder with real Sentinel-2 vegetation analysis and historical CHIRPS rainfall indicators for the Sikasso pilot area, while improving testing and delivery practices.

## 2. Implemented Features

- Connected product selection in React to the Sentinel-2 processing workflow through FastAPI.
- Retrieved B04 (red), B08 (near-infrared), `dataMask`, and SCL for the selected Sentinel-2 Level-2A product, using a small fixed pilot area near Sikasso.
- Calculated NDVI with Python and excluded unsuitable pixels using the data mask and SCL classes 4 and 5.
- Generated a product-specific NDVI GeoTIFF, preview image, and statistical results (minimum, maximum, mean, and valid pixels).
- Processed real CHIRPS v3 historical rainfall data, comparing October 2025 precipitation at the Sikasso pilot point with the 1991–2020 and 1995–2024 reference periods.
- Displayed the NDVI map, mean NDVI, rainfall anomaly, and CHIRPS comparison chart in the React Analysis Workspace.
- Documented Python dependencies and prepared `.env.example` while keeping credentials and downloaded raster data outside Git.

**Data interpretation:** The NDVI analysis follows the satellite product selected by the user. The Sprint 4 CHIRPS comparison is based on a fixed October 2025 pilot dataset; it is not automatically linked to the selected satellite acquisition date. Drought-risk estimation is not part of the completed Sprint 4 functionality.

## 3. Validation Results

- **Python tests:** 26 passed in 5.12 seconds, including three scientific calculation tests and five tests for selected-product API errors.
- **Test warning:** One non-blocking Starlette/httpx compatibility deprecation warning.
- **Frontend production build:** `pnpm run build` completed successfully in 1.04 seconds.
- **Sentinel-2 processing:** Real selected products were processed and checked locally; NDVI maps and statistics varied by product.
- **CHIRPS analysis:** October 2025 rainfall at the pilot point was approximately **38.25 mm**, compared with a **96.08 mm** mean for October 1991–2020, giving an anomaly of approximately **−60.19%**.
- **Interface:** Satellite search, product selection, analysis navigation, and display of the NDVI and CHIRPS results were checked manually.

## 4. Lessons from *The DevOps Handbook*

**Flow:** Delivering the satellite retrieval, NDVI calculation, rainfall analysis, and frontend integration in small steps helped keep progress visible and problems easier to isolate.

**Feedback:** Automated Pytest checks and manual tests with real satellite products helped detect errors early. Adding dedicated numerical tests improved confidence in the scientific calculations.

**Continual learning:** Testing different satellite scenes and refining the processing workflow helped improve data selection, pixel filtering, and presentation of the results.

These practices are useful because EO Data Finder depends on external data sources and needs reproducible, verifiable results. Automated GitHub CI has not yet been set up.

**Book reference:** Gene Kim, Jez Humble, Patrick Debois, and John Willis, *The DevOps Handbook*, IT Revolution.

## 5. Sprint Retrospective

**What went well:** Real satellite imagery and historical rainfall data were integrated into the application. The selected-product NDVI workflow worked in local tests, and all 26 Python tests passed.

**Challenges:** Matching a selected Copernicus product to its actual image data and filtering invalid pixels required additional verification. The rainfall and vegetation indicators also have different temporal and spatial coverage.

**Experiments for the next sprint:**

1. Automate the existing backend tests and frontend build checks during development.
2. Check how rainfall periods and satellite acquisition dates should be aligned before producing an experimental risk indicator.

## 6. Next Steps

- Complete and publish the Sprint 4 English demonstration video.
- Finalize the MVP during Sprint 5, including the planned **experimental Low/Moderate/High drought-risk estimate** and result export.
- Improve verification and prepare the final demonstration and Agile reflection.

## 7. Sprint 4 Deliverables

**Source code:**  
https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/tree/s4-prep

**Agile Project Board:**  
https://github.com/users/samake3699-ctrl/projects/1/views/1

**Demo video:** Pending recording and publication on GitHub Releases.
