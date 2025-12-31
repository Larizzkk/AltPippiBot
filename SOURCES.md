# Sources & References

This project integrates with several external APIs and resources.

## APIs & Documentation

### osu!droid
- **API Docs**: https://new.osudroid.moe/api2/frontend/docs/#/
- **Source Code**: https://github.com/osudroid/osu-droid

Main backend for player profiles, top plays, stats, and leaderboards.

### osu!
- **API v1 & v2 (OAuth)**: https://osu.ppy.sh/home/account/edit

osu! API credentials for beatmap queries and authentication.

### Difficulty & PP Calculation
- **DPP Calculator**: https://droidpp.osudroid.moe/calculate

Droid PP (Difficulty-adjusted Performance Points) calculation for custom mods and accuracy.

## Libraries & Tools

- **Pyrogram**: Telegram bot framework
- **pyttanko**: osu! difficulty and pp calculation
- **osrparse**: Replay file parsing (.osr format)
- **PIL (Pillow)**: Image generation for profile cards and graphs
- **matplotlib**: Graph rendering (pp history, accuracy trends)
- **aiohttp**: Async HTTP client for API calls
- **pycountry**: Country code/name lookup

## Font

- You can use any font, but sometimes it won't fit and you'll have to change the font size.

- (I'm using the TORUS LIGHT font)

- Be sure to rename the font file to font.ttf

## Development

For local testing and CI setup, see [README.md](README.md) and [CHANGELOG.md](CHANGELOG.md).
