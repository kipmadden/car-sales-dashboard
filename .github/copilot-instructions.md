# GitHub Copilot Instructions for Car Sales Dashboard

## Project Objective

This repository aims to deliver an interactive car sales forecasting dashboard:
- **Backend**: Python ML models (SARIMAX) for time series forecasting, supporting exogenous variable manipulation.
- **Frontend**: React-based UI with dynamic controls for exogenous factors, visualizing forecast results in real time.
- **Data**: Clean, well-structured car sales time series data, with provisions for ingesting additional exogenous variables (e.g., economic indicators, promotions, etc.).
- **User Experience**: Users must be able to adjust exogenous variables and immediately see changes reflected in the forecasted car sales.

---

## Copilot Coding Guidelines

### 1. **Backend (Python)**
- Use **SARIMAX** from `statsmodels` for time series forecasting.
- Code must support:
  - Loading historical sales and exogenous data.
  - Training and serializing SARIMAX models.
  - RESTful endpoints for:
    - Fetching forecasts based on user-provided exogenous variables.
    - Retrieving available exogenous variable options and historical values.
- Ensure modularity:
  - Separate model training, serving, and data handling logic.
- Always include **type hints** and **docstrings** for all public functions and classes.
- Ensure **error handling** for invalid input (e.g., missing or malformed exogenous variable data).

### 2. **Frontend (React)**
- Use **TypeScript** for type safety.
- Prioritize a modular, component-driven approach:
  - Interactive controls (sliders, dropdowns, etc.) for exogenous variables.
  - Dynamic visualization (charts/graphs) to display forecast updates instantly.
- All API interactions should be in a separate `api` module.
- Display loading and error states.
- Maintain accessibility (ARIA tags for interactive elements).

### 3. **Integration**
- Minimize latency for interactive feedback:
  - Backend endpoints should be optimized for quick response.
  - Frontend should debounce user input to avoid flooding API with requests.
- Use JSON for all data exchange between frontend and backend.

### 4. **Testing**
- Backend: Provide unit tests for data ingestion, model training, and API endpoints.
- Frontend: Use Jest/React Testing Library for component and API integration tests.

### 5. **Documentation**
- Every module must include concise docstrings (Python) or JSDoc (TypeScript).
- README must include:
  - Clear setup instructions.
  - Example data schema for both sales and exogenous data.
  - API documentation (endpoints, input/output formats).
  - Screenshot/gif of the dashboard once available.

### 6. **General Practices**
- Use meaningful variable and function names reflecting their domain role (e.g., `train_sarimax_model`, `updateExogenousVariable`).
- Follow PEP8 for Python and Airbnb style guide for React.
- Use comments to explain business logic, especially for data transformations and model parameter selection.
- Avoid hardcoding values; use configuration files where possible.
- Prefer open-source, well-maintained libraries.

---

## Special Instructions for Copilot
- When suggesting code, prefer **completeness** over brevity—include imports, error handling, and basic tests where possible.
- When generating examples, use realistic car sales and exogenous variable data.
- When suggesting UI components, include clear prop interfaces and sample usage.
- Always assume this is a collaborative, production-quality project—write code that is easy for others to review and extend.

