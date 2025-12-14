#!/bin/bash
set -e

uv run pytest -rP -v --ignore=databricks
