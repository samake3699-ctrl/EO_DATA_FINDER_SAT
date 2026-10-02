# Sprint 1 - Local Interface Prototype

## Sprint Goal

Build and validate the first local web prototype of EO Data Finder.

The prototype must allow a user to enter satellite-search criteria, view demonstration Sentinel-2 products, select one product, and open a preview of the future drought-risk analysis module.

## Sprint duration

Two weeks.

## Sprint Backlog

| Task | Status |
| --- | --- |
| Install Node.js, npm, pnpm, Git, and Visual Studio Code | Done |
| Create the React project with Vite | Done |
| Initialize the Git repository | Done |
| Create the EO Data Finder page | Done |
| Create the search form | Done |
| Add pilot area, dates, cloud coverage, and analysis module | Done |
| Add form validation | Done |
| Display demonstration Sentinel-2 products | Done |
| Allow the user to select one product | Done |
| Add a preview of the drought-risk module | Done |
| Add responsive CSS styling | Done |
| Perform manual acceptance tests | To validate |
| Create the final S1 Git commit | To validate |

## S1 acceptance criteria

- The application starts locally.
- The EO Data Finder title is visible.
- The user can select a pilot area.
- The user can enter a start date and an end date.
- The user can enter a maximum cloud coverage.
- The drought-risk monitoring module is visible in the form.
- Missing fields produce an error.
- An invalid date range produces an error.
- Invalid cloud coverage produces an error.
- A valid search displays demonstration products.
- The user can select one product.
- The user can open the drought-analysis preview.
- The preview clearly states that the indicators are simulated.
- The application works on desktop and small screens.
- The code is saved in Git.

## Sprint Review

The S1 demonstration shows the complete future user journey at interface level:

1. Select a pilot area.
2. Enter the search period.
3. Enter the cloud coverage limit.
4. Search for demonstration Sentinel-2 products.
5. Select one product.
6. Open the experimental drought-risk preview.
7. View a simulated NDVI map, rainfall anomaly, and drought-risk level.

No real Copernicus request, image processing, NDVI calculation, rainfall calculation, or prediction is performed during S1.

## Sprint Retrospective

### What went well

- The development environment was installed successfully.
- The React application was created and launched locally.
- The form, validation, results table, and styling were developed progressively.
- Git was used to save the first working version.
- The difference between interface data and real scientific data was clarified.

### What was difficult

- Choosing between JavaScript and TypeScript caused some initial confusion.
- The project scope changed when the drought-analysis module was added.
- It was necessary to distinguish a demonstration result from a real prediction.

### What will be improved in Sprint 2

- Keep each technical task small and testable.
- Add Python without removing the existing React interface.
- Create a small FastAPI backend.
- Replace demonstration products with real Copernicus metadata.
- Keep the drought indicators simulated until the real processing pipeline is validated.

## Definition of Done

Sprint 1 is complete when:

- all acceptance criteria pass;
- the application builds without an error;
- the full user scenario works locally;
- the S1 documentation is present;
- the final S1 commit is created.
