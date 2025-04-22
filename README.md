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

- **Synchronous waits**: Simple `time.sleep()` calls are used for demo; can be replaced with explicit WebDriver waits.
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


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from urllib3.exceptions import MaxRetryError
from selenium.common.exceptions import WebDriverException

def before_all(context):
    os.makedirs("screenshots", exist_ok=True)

    hub = os.getenv("SELENIUM_HUB_URL", "http://selenium-hub:4444/wd/hub")
    browser = os.getenv("BROWSER_NAME", "chrome").upper()

    try:
        caps = getattr(DesiredCapabilities, browser).copy()
    except AttributeError:
        raise ValueError(f"Unsupported browser: {browser}. Use CHROME or FIREFOX.")

    max_retries = 5
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            context.driver = webdriver.Remote(command_executor=hub, desired_capabilities=caps)
            context.driver.maximize_window()
            break
        except (MaxRetryError, WebDriverException) as e:
            if attempt == max_retries - 1:
                raise
            print(f"Connection attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

def after_all(context):
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()