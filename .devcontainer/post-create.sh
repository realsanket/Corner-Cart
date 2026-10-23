#!/usr/bin/env bash
# Runs once when the codespace is created: the tools the labs need beyond the base image.
set -euo pipefail

sudo apt-get update -y
sudo apt-get install -y --no-install-recommends postgresql-client   # psql
sudo npm install -g azurite                                          # local storage for Functions triggers
pip install --no-cache-dir -r requirements.txt -r requirements-labs.txt                     # the app, its tests and the linter
python data/generate.py                                              # the demo data (fixed seed)
python scripts/check_tools.py || true                                # show the bench; red lines are fixed in the lab
