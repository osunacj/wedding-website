# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Django 4.2 wedding guest management system. Python 3.12. Single-app structure: `guests/` handles all guest/RSVP logic; `bigday/` is the Django project root.

## Development

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver         # http://localhost:8000
```

Run tests:

```bash
python manage.py test              # discovers tests under guests/tests/
```

## Deployment (Docker)

```bash
docker-compose up --build          # starts Postgres + Django on port 8080
```

The Docker entrypoint (`deploy/entrypoint.sh`) runs collectstatic, migrate, and optional superuser creation automatically.

Required env vars for Docker:

- `SECRET_KEY` — must be changed from the default in settings.py
- `DEBUG` — set to `False` in production
- `POSTGRES_SERVER`, `POSTGRES_USER`, `POSTGRES_DB`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`

## Configuration

Settings are layered: `bigday/settings.py` → `bigday/localsettings.py` (gitignored, optional) → `.env` (read via django-environ if present). Copy `bigday/localsettings.py.template` to create a local override.

Email backend is toggled with `MAIL_BACKEND`: `"console"` (default, logs to stdout) or `"smtp"` (real sending). Wedding-specific values (couple names, date, location, website URL) live in `localsettings.py`.

## Guest Management Commands

```bash
python manage.py import_guests <csv_file>        # CSV must follow exact column order
python manage.py send_save_the_dates --send --mark-sent
python manage.py send_invitations --send --mark-sent
python manage.py wipe_guest_list                 # destructive — resets all guest data
```

CSV import expects columns in this order: `party_name, first_name, last_name, party_type, is_child, category, is_invited, email`.

## Git Workflow

Use feature branches and PRs for non-trivial changes; direct commits to master is fine for small fixes.

## Gotchas

- `Party.type` is hardcoded as `formal/fun/dimagi` — not a configurable enum.
- The `docker-compose.yml` uses no named volumes; database data lives inside the container. Back up the database before any container teardown in production.
- The Fabric-based `fabfile.py` (`fab production deploy`) is a legacy deployment path targeting `czue.org`. Docker is the preferred path going forward.
- Invitation URLs use hex-encoded UUIDs stored in `Party.invitation_id`. Do not regenerate these after invitations are sent.
