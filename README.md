# Automated Testing Suite

This repository contains Python-based automated tests for the Petfinder API and web UI, including API, performance (Locust), and UI (pytest-bdd with Selenium) tests, orchestrated via Docker and GitHub Actions.

## Setup Instructions


1. **Install Python dependencies**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```


2. **Start Docker services for UI tests**
   ```bash
   docker-compose up -d
   ```
   This will start Selenoid (for browser sessions) and MySQL (for tests).

3. **(Optional) Install Allure CLI**  
   ```bash
   npm install -g allure-commandline --save-dev
   ```

## Running Tests

### API Tests
```bash
pytest api_tests/ --html=report.html --self-contained-html --alluredir=allure-results
```

### Performance Tests
```bash
locust -f performance_tests/test_petfinder_real.py --headless -u 10 -r 2 -t 3m --host https://api.petfinder.com
```
Results will be saved in `load-test-results/`.

### UI Automation Tests
```bash
pytest -v --maxfail=1 --disable-warnings --alluredir=allure-results --html=report.html -n auto
```
- Ensure Docker Compose is running.
- Video recordings and logs are stored in `./selenoid/video` and `./selenoid/logs`.

## 

## Assumptions & Decisions

- Python 3.9 is the target runtime for consistency with GitHub Actions.
- Locust used for lightweight performance testing; headless execution for CI.
- Selenoid chosen over standalone Selenium Grid for video recording support.
- Tests configured to be idempotent; CSV test data is loaded per-test.

## Tools & Resources

- **Python** 3.9
- **pytest** / pytest-bdd / pytest-html / allure-pytest
- **Selenium** 4.8.0 + Selenoid
- **Locust** 2.16.0
- **GitHub Actions** for CI
- **Docker Compose** for UI test infrastructure
- **Allure** for advanced reporting
- **Requests** / **Requests-Mock** for API interactions

