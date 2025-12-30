# AltPippiBot

A Telegram bot for osu!droid — profile cards, pp calculations, top plays, graphs and more.

## Requirements

- Python 3.11+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Copy the example env and fill values locally (do NOT commit `.env`):

```bash
cp .env.example .env
# then edit .env
```

Required environment variables (examples are in `.env.example`):
- `BOT_TOKEN` — Telegram bot token
- `API_BASE` — backend API base URL used by the bot
- `API_ID`, `API_HASH` — Telegram API credentials
- `OSU_API_KEY`, `OSU_CLIENT_ID`, `OSU_CLIENT_SECRET` — osu! API credentials
- `DROID_TOKEN` — optional (leaderboard API)

## Run locally

Start the bot with:

```bash
python bot.py
```

Use `screen`/`tmux` or a process manager (systemd, pm2, supervisor) for production deployments.

## Tests

Run the test-suite locally:

```bash
pytest -q
```

## Release checklist

- Update `VERSION` and add notes to `CHANGELOG.md` under a new version heading
- Run tests and linters in CI
- Create a signed tag and a GitHub Release
- Rotate any secrets that were exposed (BOT token, API keys)

## Security

- Do not commit `.env` or any secret files. Use GitHub Secrets for CI and environment variables on hosting services.
- After removing secrets from history, rotate keys immediately.
- Make the repository private if you don't want public visibility.

## Contributing

PRs are welcome. Please add tests for new features and keep changes small and focused.

