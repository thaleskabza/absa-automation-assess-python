## README.md

# Python UI Automation for Web Tables

This repository contains a Python/Behave/Selenium automation suite for testing the Web Tables example on `http://www.way2automation.com/angularjs-protractor/webtables/`.

## Setup Instructions

### Prerequisites

- Python 3.9 or later
- pip (Python package manager)
- Docker & Docker Compose (optional, for containerized execution)
- A running Selenium Grid (via Docker Compose or external)

### Installing Dependencies

```bash
pip install --no-cache-dir -r requirements.txt
```

```bash
docker build -t absa-auto-python .


#

```bash
docker compose up -d  

#

```bash
docker compose down -v   

### Running Tests Locally

1. Ensure a Selenium Hub is available at `SELENIUM_HUB_URL` (default: `http://localhost:4444/wd/hub`).
2. Start a browser node or use Docker Compose (see below).
3. Execute:
   ```bash
   behave --format pretty
   ```

### Running Tests with Docker Compose

```bash
docker-compose up -d --build  # starts hub, node, and test-runner
# tests will run automatically in test-runner
# once complete, bring down the grid:
docker-compose down -v
```

## Project Structure



## Assumptions & Decisions

- **Synchronous waits**: Simple `time.sleep()` 
- **Unique usernames**: CSV-driven scenarios assume unique `UserName` fields or generate timestamped suffixes.
- **Default hub URL**: Uses `SELENIUM_HUB_URL` env var, falling back to `http://selenium-hub-G:4444/wd/hub`.
- **Containerized grid**: Docker Compose spins up a Hub + Chrome node for isolated CI runs.

## Tools & Resources Used

- **Language**: Python 3.9
- **Automation**: Selenium WebDriver 4.x
- **BDD**: Behave 1.2+
- **Docker**: `selenium/hub` & `selenium/node-chrome` images
- **CI/CD**: GitHub Actions
- **Test Data**: CSV file (`src/test/resources/testdata/users.csv`)
- **Browser Drivers**: Managed via remote Selenium Grid

---

## Directory Structure
```
.
