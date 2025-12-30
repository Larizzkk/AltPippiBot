osu-bot
=======

Minimal instructions to run the bot locally and prepare for release.

Requirements
------------
- Python 3.11+
- Install dependencies:

```bash
pip install -r requirements.txt
```

Environment variables (set in `.env` or environment):
- `BOT_TOKEN` (Telegram bot token)
- `API_BASE` (backend API base URL used by the bot)
- `API_ID`, `API_HASH` (Telegram API credentials)
- `OSU_API_KEY`, `OSU_CLIENT_ID`, `OSU_CLIENT_SECRET` (osu! API credentials)
- `DROID_TOKEN` (optional, for leaderboard)

Run locally
-----------
Create `.env` with required keys, then:

```bash
python testppy.py
```

Tests
-----
Run tests with:

```bash
pytest -q
```

Release checklist
-----------------
- Ensure `requirements.txt` is up to date
- Bump `VERSION` and update `CHANGELOG.md`
- Run tests and linters in CI
- Tag the commit and create GitHub Release (or use CI to publish)
