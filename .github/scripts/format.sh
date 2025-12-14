#!/bin/bash
set -e

uv sync

uv run ruff format --check
