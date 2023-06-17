#!/usr/bin/env bash
poetry run black $@ bin src tests --exclude="src/database/alembic"