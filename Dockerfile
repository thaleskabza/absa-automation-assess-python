FROM python:3.9-slim

WORKDIR /app

# install system deps for Chrome/Firefox if you need headless locally
# (omit if only using remote grid)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl \
      default-jre \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run pytest by default
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v", "--alluredir=allure-results"]