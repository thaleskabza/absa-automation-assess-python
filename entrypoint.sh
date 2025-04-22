#!/usr/bin/env bash
# start Xvfb in background
Xvfb :99 -screen 0 1920x1080x24 &

# now hand off to pytest (preserving exit code)
pytest "$@"
