# Commands

AltPippiBot provides a comprehensive set of commands for osu!droid and osu! gameplay tracking.

## Language & Settings

### /lang
Set your preferred language (ru/en).
```
/lang ru
/lang en
```

### /bind
Bind your osu!droid account to access personalized commands.
```
/bind <username>
```
Example: `/bind Lift`

---

## Map Information

### /map
Get detailed information about a beatmap from a link.
```
/map <link>
```
Examples:
- `/map https://osu.ppy.sh/beatmapsets/1234567#osu/2569829`
- `/map https://osu.ppy.sh/b/2569829`

Returns: map card with difficulty, artist, creator, and pp buttons.

### /dw
Download a beatmap (.osz file).
```
/dw <link>
```
Example: `/dw https://osu.ppy.sh/beatmapsets/1234567`

### /sr
Search for beatmaps by query.
```
/sr <query>
```
Example: `/sr metal remix`

Returns: paginated search results with difficulty ratings.

### /top
Browse ranked beatmaps leaderboard.
```
/top
```

---

## PP & Difficulty Calculation

### /pp
Calculate PP for a beatmap with custom mods and accuracy.
```
/pp #osu/<map_id> [+mods] [accuracy%]
```
Examples:
- `/pp #osu/2569829` — default 100% NM
- `/pp #osu/2569829 +HD` — Hidden mod
- `/pp #osu/2569829 +HDDT 98%` — HD+DT at 98% accuracy

### /stars
Get difficulty rating of a beatmap.
```
/stars #osu/<map_id>
```
Example: `/stars #osu/2569829`

### /fc
Calculate PP for a Full Combo (100% accuracy, no misses).
```
/fc #osu/<map_id> [+mods]
```
Example: `/fc #osu/2569829 +HD`

### /dpp
Calculate osu!droid-specific PP (DPP).
```
/dpp <beatmap_id_or_url> [mods] [accuracy]
```
Examples:
- `/dpp 2569829`
- `/dpp 2569829 HD 98`

---

## Player Profiles

### /prpic
Generate a profile card for a player.
```
/prpic [username] [text|photo]
```
Examples:
- `/prpic` — your bound account as photo
- `/prpic Lift photo` — another player
- `/prpic text` — text-only version (stats)

### /topplays or /pr
View a player's top 50 plays with sorting options.
```
/topplays [username]
/pr [username]
```
Examples:
- `/topplays` — your bound account
- `/topplays Lift` — another player

Buttons: sort by PP or date, navigate between plays.

### /ppgraph
Plot a player's PP progress over last 30 days.
```
/ppgraph [username]
```
Example: `/ppgraph Lift`

### /accuracygraph
Plot a player's accuracy trend over last 30 days.
```
/accuracygraph [username]
```
Example: `/accuracygraph Lift`

### /compare
Compare stats between two players.
```
/compare <username1> <username2>
```
Example: `/compare Lift Cookiezi`

### /comparepic
Generate a comparison card (visual) between two players.
```
/comparepic <username1> <username2>
```
Example: `/comparepic Lift Cookiezi`

### /recommend
Get beatmap recommendations based on a player's top plays.
```
/recommend [username]
```
Example: `/recommend Lift`

### /milestone
Check progress towards common milestones (PP, playcount, accuracy).
```
/milestone [username]
```
Example: `/milestone Lift`

---

## Statistics

### /modstats
Show mod distribution in a player's top 50 plays.
```
/modstats <username>
```
Example: `/modstats Lift`

### /toplist
Browse global leaderboard (by score or pp).
```
/toplist <score|pp>
```
Examples:
- `/toplist pp` — top pp players
- `/toplist score` — top score players

Paginated with navigation buttons.

### /server
Get osu!droid server statistics (online users, registration count).
```
/server
```

Returns: stats card and activity trend graph.

---

## Replay Analysis

### Upload a .osr file
Send a replay file (.osr) to get:
- Player username & mods
- Achieved PP at your accuracy
- FC PP (full combo)
- PP difference

---

## Customization

### /setgr
Set a custom gradient color for your profile card.
```
/setgr <hex_color>
```
Example: `/setgr #8A2BE2` (purple)

### /setfr
Set a custom frame color around your avatar.
```
/setfr <hex_color>
```
Example: `/setfr #FF0000` (red)

### /resetfr
Remove your custom frame.
```
/resetfr
```

---

## Fun

### /yn
Get a random yes/no answer.
```
/yn
```

### /roll
Roll dice (random number).
```
/roll [max]
/roll [min] [max]
```
Examples:
- `/roll` — 1–100
- `/roll 20` — 1–20
- `/roll 5 15` — 5–15

---

## Tips

- Use `/bind <username>` first to enable personalized commands (topplays, prpic, etc.).
- Change language with `/lang` (ru/en).
- Customize colors with `/setgr` and `/setfr`.
- Upload .osr replay files for instant analysis.
- Explore leaderboards with `/toplist` and `/top`.

Enjoy! 🎮
