# just deleted /dw functions and OSU_COOKIE

import os
import re
import aiohttp
import asyncio
import pyttanko
import logging
import pycountry
import time
import json
import random
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tempfile
from pyrogram import types
from functools import partial
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from osrparse import Replay
from dotenv import load_dotenv
load_dotenv()

# ============ LOGGING SETUP ============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
log = logging.getLogger("osu-bot")

# ============ ENVIRONMENT VARIABLES ============
API_ID = 
API_HASH = 
BOT_TOKEN = 
OSU_API_KEY = 
OSU_CLIENT_ID = 
OSU_CLIENT_SECRET =
DROID_TOKEN = 
API_BASE =

# cached oauth token
OSU_TOKEN_CACHE 

# ============ REGEX PATTERNS ============
RE_MAPSET = re.compile(r"beatmapsets/(\d+)")
RE_BID = re.compile(r"#osu/(\d+)")
RE_ACC = re.compile(r"(\d+\.?\d*)%")
RE_MODS = re.compile(r"\+([A-Z]+)")
RE_URL_BID = re.compile(r"osu\.ppy\.sh/(?:b/|beatmapsets/\d+#osu/)(\d+)")
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")

# ============ GLOBAL STATE ============
session = None
USER_LANGUAGES = {}
USER_BACKGROUNDS = {}
USER_FRAMES = {}
GRADIENT_CACHE = {}
BIND_CACHE = {}
TOPPLAYS_CACHE = {}
SEARCH_CACHE = {}
TOP_CACHE = {}
COOLDOWN = {}
PP_HISTORY_CACHE = {}

# ============ CONSTANTS ============
LIMIT = 5
CD_SECONDS = 3
DPP_API_URL = "https://droidpp.osudroid.moe/api/ppboard/calculatebeatmap"

# ============ TRANSLATIONS ============
TRANSLATIONS = {
    "ru": {
        "pp": "{stars:.2f}✦ | {pp:.2f}pp",
        "replay": "{user}\nReplay: {p1:.2f}pp ({s1:.2f}★)\nFC: {p2:.2f}pp ({s2:.2f}★)\n-{diff:.2f}pp",
        "invalid_link": "Неверная ссылка",
        "downloading": "Скачивание карты...",
        "download_error": "Ошибка при скачивании: {e}",
        "not_replay": "Это не replay файл (.osr)",
        "map_not_found": "Ошибка: карта не найдена",
        "replay_error": "Ошибка обработки replay",
        "dw_help": "Использование: /dw <ссылка на beatmap>",
        "pp_help": "Использование: /pp #osu/<id> [+mods] [acc%]",
        "stars_help": "Использование: /stars #osu/<id>",
        "fc_help": "Использование: /fc #osu/<id> [+mods]",
        "map_help": "Использование: /map <ссылка>",
        "api_error": "Ошибка API",
        "search_help": "Использование: /sr <query>",
        "not_found": "Не найдено",
        "download": "Скачать",
        "bind_help": "Использование: /bind <osu!droid username>",
        "bind_success": "Аккаунт привязан.\nUsername: {username}\nUID: {uid}",
        "bind_error": "Профиль не найден.",
        "bind_fail": "Ошибка при привязке аккаунта.",
        "not_bound": "Аккаунт не привязан. Используй /bind <username>",
        "profile_not_found": "Профиль не найден.",
        "no_topplays": "Top plays отсутствуют.",
        "gradient_help": "Использование: /setgr <hex_color>\nПример: /setgr #8A2BE2",
        "gradient_invalid": "Неверный формат hex. Пример: #8A2BE2",
        "gradient_set": "Градиент изменён на #{color}",
        "gradient_error": "Ошибка: {e}",
        "frame_help": "Использование: /setfr <hex_color>\nПример: /setfr #FF0000",
        "frame_invalid": "Неверный формат hex. Пример: #FF0000",
        "frame_set": "Frame изменён на #{color}",
        "frame_reset": "Frame удалён",
        "frame_not_set": "Кастомный frame не установлен",
        "compare_help": "Использование: /compare <username1> <username2>",
        "compare_header": "Сравнение игроков:",
        "compare_not_found": "Один из профилей не найден.",
        "modstats_help": "Использование: /modstats <username>",
        "modstats_header": "Статистика модов для {username}:",
        "toplist_help": "Использование: /toplist <score|pp>",
        "toplist_invalid": "Допустимые типы: score, pp",
        "toplist_error": "Ошибка получения топ-листа. Статус: {status}",
        "toplist_empty": "Топ-лист пуст.",
        "toplist_header": "Топ-лист ({type}) - страница {page}",
        "dpp_help": "/dpp <beatmap_id_or_url> [mods] [acc]",
        "dpp_error": "Ошибка расчёта DPP: {e}",
        "dpp_error_response": "Ошибка расчёта DPP",
        "wait": "Подождите немного...",
        "lang_set": "Язык установлен: {lang}",
        "lang_help": "Использование: /lang <ru|en>",
        "lang_invalid": "Допустимые языки: ru, en",
        "top_play": "Top play {idx}/{total}",
        "player_info": "Player: {username}\nUID: {uid}\nGlobal Rank: #{global_rank}\nCountry Rank: #{country_rank}\nPP: {pp}\nPlaycount: {playcount}\nAccuracy: {acc}%",
        "prpic_help": "Использование: /prpic [username] [text|photo]",
        "back": "⬅️ Назад",
        "next": "➡️ Вперед",
        "sort_score": "Сортировать по Score",
        "sort_pp": "Сортировать по PP",
        "sort_date": "Сортировать по Дате",
        "region": "Регион",
    },
    "en": {
        "pp": "{stars:.2f}✦ | {pp:.2f}pp",
        "replay": "{user}\nReplay: {p1:.2f}pp ({s1:.2f}★)\nFC: {p2:.2f}pp ({s2:.2f}★)\n-{diff:.2f}pp",
        "invalid_link": "Invalid link",
        "downloading": "Downloading map...",
        "download_error": "Download error: {e}",
        "not_replay": "This is not a replay file (.osr)",
        "map_not_found": "Error: map not found",
        "replay_error": "Replay processing error",
        "dw_help": "Usage: /dw <beatmap link>",
        "pp_help": "Usage: /pp #osu/<id> [+mods] [acc%]",
        "stars_help": "Usage: /stars #osu/<id>",
        "fc_help": "Usage: /fc #osu/<id> [+mods]",
        "map_help": "Usage: /map <link>",
        "api_error": "API Error",
        "search_help": "Usage: /sr <query>",
        "not_found": "Not found",
        "download": "Download",
        "bind_help": "Usage: /bind <osu!droid username>",
        "bind_success": "Account bound.\nUsername: {username}\nUID: {uid}",
        "bind_error": "Profile not found.",
        "bind_fail": "Error binding account.",
        "not_bound": "Account not bound. Use /bind <username>",
        "profile_not_found": "Profile not found.",
        "no_topplays": "No top plays.",
        "gradient_help": "Usage: /setgr <hex_color>\nExample: /setgr #8A2BE2",
        "gradient_invalid": "Invalid hex format. Example: #8A2BE2",
        "gradient_set": "Gradient changed to #{color}",
        "gradient_error": "Error: {e}",
        "frame_help": "Usage: /setfr <hex_color>\nExample: /setfr #FF0000",
        "frame_invalid": "Invalid hex format. Example: #FF0000",
        "frame_set": "Frame changed to #{color}",
        "frame_reset": "Frame removed",
        "frame_not_set": "No custom frame set",
        "compare_help": "Usage: /compare <username1> <username2>",
        "compare_header": "Player comparison:",
        "compare_not_found": "One of the profiles not found.",
        "modstats_help": "Usage: /modstats <username>",
        "modstats_header": "Mod statistics for {username}:",
        "toplist_help": "Usage: /toplist <score|pp>",
        "toplist_invalid": "Available types: score, pp",
        "toplist_error": "Error getting leaderboard. Status: {status}",
        "toplist_empty": "Leaderboard is empty.",
        "toplist_header": "Leaderboard ({type}) - page {page}",
        "dpp_help": "/dpp <beatmap_id_or_url> [mods] [acc]",
        "dpp_error": "DPP calculation error: {e}",
        "dpp_error_response": "DPP calculation error",
        "wait": "Please wait...",
        "lang_set": "Language set to: {lang}",
        "lang_help": "Usage: /lang <ru|en>",
        "lang_invalid": "Available languages: ru, en",
        "top_play": "Top play {idx}/{total}",
        "player_info": "Player: {username}\nUID: {uid}\nGlobal Rank: #{global_rank}\nCountry Rank: #{country_rank}\nPP: {pp}\nPlaycount: {playcount}\nAccuracy: {acc}%",
        "prpic_help": "Usage: /prpic [username] [text|photo]",
        "back": "⬅️ Back",
        "next": "➡️ Next",
        "sort_score": "Sort by Score",
        "sort_pp": "Sort by PP",
        "sort_date": "Sort by Date",
        "region": "Region",
    }
}

# ============ HELPER FUNCTIONS ============
def get_lang(user_id):
    return USER_LANGUAGES.get(user_id, "en")

def t(user_id, key, **kwargs):
    """Get translated text"""
    lang = get_lang(user_id)
    text = TRANSLATIONS.get(lang, {}).get(key, key)
    try:
        return text.format(**kwargs)
    except:
        return text

async def get_session():
    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession(headers=HEADERS, cookies=COOKIES)
    return session

async def fetch(url, params=None):
    s = await get_session()
    log.info(f"HTTP GET {url}")
    try:
        async with s.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as r:
            log.info(f"HTTP {r.status} {url}")
            if r.status == 404:
                log.warning(f"URL not found: {url}")
                return r, None
            if r.status >= 400:
                log.warning(f"HTTP error {r.status} for {url}")
                return r, None
            data = await r.read()
            return r, data
    except asyncio.TimeoutError:
        log.error(f"Timeout for {url}")
        return None, None
    except Exception as e:
        log.error(f"Fetch error for {url}: {e}")
        return None, None

async def beatmap_id_from_hash(hash_code):
    _, data = await fetch("https://osu.ppy.sh/api/get_beatmaps", {
        "k": OSU_API_KEY, "h": hash_code
    })
    js = json.loads(data)
    return js[0]["beatmap_id"] if js else None

def parse_replay(path):
    r = Replay.from_path(path)
    total = r.count_300 + r.count_100 + r.count_50 + r.count_miss
    acc = ((300*r.count_300 + 100*r.count_100 + 50*r.count_50) / (300*total)) * 100 if total > 0 else 0
    return {
        "username": r.username,
        "mods": r.mods.name,
        "combo": r.max_combo,
        "misses": r.count_miss,
        "acc": acc,
        "hash": r.beatmap_hash
    }

def load_beatmap(path):
    p = pyttanko.parser()
    with open(path, encoding="utf-8", errors="ignore") as f:
        return p.map(f)

def calc_pp_from_osu(path, mods="", acc=100.0, combo=None, misses=0):
    bm = load_beatmap(path)
    mods_val = pyttanko.mods_from_str(mods) if mods else 0
    stars = pyttanko.diff_calc().calc(bm, mods_val)
    combo = combo or bm.max_combo()
    n300, n100, n50 = pyttanko.acc_round(acc, len(bm.hitobjects), misses)
    pp, *_ = pyttanko.ppv2(
        aim_stars=stars.aim, speed_stars=stars.speed, bmap=bm, mods=mods_val,
        combo=combo, n300=n300, n100=n100, n50=n50, nmiss=misses
    )
    return stars.total, pp

async def download_with_progress(url, path=None):
    _, data = await fetch(url)
    if data is None:
        return None
    if path:
        with open(path, "wb") as f:
            f.write(data)
        return path
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(url)[1] or '')
    tf.write(data)
    tf.close()
    return tf.name

async def get_osu_token():
    now = time.time()
    if OSU_TOKEN_CACHE.get("token") and OSU_TOKEN_CACHE.get("expiry", 0) > now + 10:
        return OSU_TOKEN_CACHE["token"]

    s = await get_session()
    async with s.post("https://osu.ppy.sh/oauth/token", json={
        "grant_type": "client_credentials",
        "client_id": OSU_CLIENT_ID,
        "client_secret": OSU_CLIENT_SECRET,
        "scope": "public"
    }) as r:
        js = await r.json()
        token = js.get("access_token")
        expires = js.get("expires_in", 3600)
        OSU_TOKEN_CACHE["token"] = token
        OSU_TOKEN_CACHE["expiry"] = now + expires
        return token

async def search_beatmaps_v2(query, mode=0, limit=10, sort="ranked"):
    token = await get_osu_token()
    s = await get_session()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "m": mode, "sort": sort, "limit": limit}
    async with s.get("https://osu.ppy.sh/api/v2/beatmapsets/search",
                     params=params, headers=headers) as r:
        data = await r.json()
        res = []
        for s_map in data.get("beatmapsets", []):
            stars = max([b["difficulty_rating"] for b in s_map.get("beatmaps", [{"difficulty_rating": 0}])])
            res.append({
                "id": s_map["id"],
                "title": s_map["title"],
                "artist": s_map["artist"],
                "creator": s_map.get("creator", "Unknown"),
                "stars": f"{stars:.2f}"
            })
        return res

async def get_map_info_api(beatmap_id):
    try:
        r, data = await fetch("https://osu.ppy.sh/api/get_beatmaps", {
            "k": OSU_API_KEY, "b": beatmap_id
        })
        if r is None or data is None:
            return None
        js = json.loads(data)
        return js[0] if js else None
    except Exception as e:
        log.error(f"get_map_info_api failed: {e}")
        return None
    
def create_beatmap_card(bg_data, info):
    W, H = 960, 280
    try:
        img = Image.open(BytesIO(bg_data)).convert("RGBA")
    except:
        img = Image.new("RGBA", (W, H), (20, 20, 20, 255))

    ratio = max(W/img.width, H/img.height)
    img = img.resize((int(img.width*ratio), int(img.height*ratio)), Image.LANCZOS)
    img = img.crop(((img.width-W)//2, (img.height-H)//2, (img.width+W)//2, (img.height+H)//2))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for i in range(300):
        alpha = int(180 * (1 - i/300))
        draw_ov.line([(i, 0), (i, H)], fill=(0, 0, 0, alpha))
    
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    def get_f(s, default_s):
        try:
            return ImageFont.truetype("font.ttf", s)
        except:
            return ImageFont.load_default()

    draw.text((50, 15), info.get('title', 'Unknown')[:40], font=get_f(62, 60), fill=(255, 255, 255))
    draw.text((50, 85), f"{info.get('artist')} // {info.get('creator')}", font=get_f(33, 30), fill=(220, 220, 220))
    draw.text((50, 135), f"[{info.get('version', 'Normal')}]", font=get_f(38, 35), fill=(255, 248, 220))
    
    stars = float(info.get('difficultyrating', 0))
    stars_txt = "✦" * int(stars) + ("✦" if stars % 1 >= 0.5 else "")
    draw.text((50, 190), f"{stars_txt}  {stars:.2f}", font=get_f(48, 45), fill=(255, 215, 50))

    bio = BytesIO()
    img.convert("RGB").save(bio, "JPEG", quality=90)
    bio.seek(0)
    bio.name = "map.jpg"
    return bio

def generate_profile_card(user_data, region_text=None, user_id=None, avatar_bytes=None):
    width, height = 900, 520
    
    if user_id and user_id in USER_BACKGROUNDS:
        try:
            img = Image.open(BytesIO(USER_BACKGROUNDS[user_id])).convert("RGB")
            ratio = max(width/img.width, height/img.height)
            img = img.resize((int(img.width*ratio), int(img.height*ratio)), Image.LANCZOS)
            img = img.crop(((img.width-width)//2, (img.height-height)//2, (img.width+width)//2, (img.height+height)//2))
        except:
            img = Image.new("RGB", (width, height), (15, 15, 20))
    else:
        img = Image.new("RGB", (width, height), (15, 15, 20))
    
    draw = ImageDraw.Draw(img, "RGBA")

    try:
        font_title = ImageFont.truetype("font.ttf", 52)
        font_stat_label = ImageFont.truetype("font.ttf", 18)
        font_stat_value = ImageFont.truetype("font.ttf", 26)
        font_small = ImageFont.truetype("font.ttf", 14)
        font_top1 = ImageFont.truetype("font.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_stat_label = ImageFont.load_default()
        font_stat_value = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_top1 = ImageFont.load_default()

    username = user_data.get("Username", "Unknown")
    global_rank = user_data.get("GlobalRank", "N/A")
    country_rank = user_data.get("CountryRank", "N/A")
    pp = user_data.get("OverallPP", 0)
    playcount = user_data.get("OverallPlaycount", 0)
    accuracy = user_data.get("OverallAccuracy", 0)
    region = region_text or user_data.get("Region", "N/A")

    if user_id and user_id in GRADIENT_CACHE:
        accent_color = GRADIENT_CACHE[user_id]
    else:
        accent_color = (138, 43, 226)
    
    text_primary = (255, 255, 255)
    text_secondary = (200, 200, 200)
    bar_bg = (40, 40, 50)

    try:
        avatar_size = 140
        if avatar_bytes:
            avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
            avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
            mask = Image.new("L", (avatar_size, avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, avatar_size, avatar_size], fill=255)
            avatar.putalpha(mask)

            if user_id and user_id in USER_FRAMES:
                frame_color = USER_FRAMES[user_id]
                border_width = 3
            else:
                frame_color = accent_color
                border_width = 2

            avatar_with_frame = Image.new("RGBA", (avatar_size + border_width*2, avatar_size + border_width*2), (0, 0, 0, 0))
            avatar_with_frame_draw = ImageDraw.Draw(avatar_with_frame)
            avatar_with_frame_draw.ellipse([0, 0, avatar_size + border_width*2, avatar_size + border_width*2], fill=frame_color)
            avatar_with_frame.paste(avatar, (border_width, border_width), avatar)
            img.paste(avatar_with_frame, (30, 25), avatar_with_frame)
        else:
            if user_id and user_id in USER_FRAMES:
                frame_color = USER_FRAMES[user_id]
            else:
                frame_color = accent_color
            draw.ellipse([30, 25, 170, 165], outline=frame_color, width=3)
    except Exception as e:
        log.warning(f"Avatar load failed: {e}")
        if user_id and user_id in USER_FRAMES:
            frame_color = USER_FRAMES[user_id]
        else:
            frame_color = accent_color
        draw.ellipse([30, 25, 170, 165], outline=frame_color, width=3)
        
    draw.text((190, 20), username, font=font_title, fill=accent_color)
    draw.text((190, 75), f"#{global_rank} • #{country_rank} {region}", 
              font=font_small, fill=text_secondary)

    acc_percentage = round(accuracy * 100, 2)
    acc_bar_x, acc_bar_y = 190, 125
    acc_bar_width, acc_bar_height = 250, 6
    
    draw.rectangle([acc_bar_x, acc_bar_y, acc_bar_x + acc_bar_width, acc_bar_y + acc_bar_height],
                   fill=bar_bg)
    draw.rectangle([acc_bar_x, acc_bar_y, 
                   acc_bar_x + int(acc_bar_width * accuracy), acc_bar_y + acc_bar_height],
                   fill=accent_color)
    draw.text((acc_bar_x, acc_bar_y - 22), "Accuracy", font=font_stat_label, fill=text_secondary)
    draw.text((acc_bar_x + acc_bar_width + 15, acc_bar_y - 8), f"{acc_percentage}%", 
              font=font_stat_value, fill=accent_color)

    stat_positions = [
        (190, 160, "PP", str(pp)),
        (470, 160, "Playcount", f"{playcount:,}"),
    ]

    for x, y, label, value in stat_positions:
        draw.text((x, y), label, font=font_stat_label, fill=text_secondary)
        draw.text((x, y + 25), value, font=font_stat_value, fill=accent_color)

    draw.line([(190, 210), (850, 210)], fill=bar_bg, width=1)

    top_plays = user_data.get("Top50Plays", [])
    if len(top_plays) >= 3:
        y_offset = 220
        for i in range(3):
            top_play = top_plays[i]
            if i > 0:
                draw.line([(30, y_offset), (870, y_offset)], fill=bar_bg, width=1)
            
            draw.text((30, y_offset + 10), f"TOP {i+1} PLAY", font=font_stat_label, fill=accent_color)
            
            map_name = top_play.get("Filename", "Unknown Map")[:70]
            draw.text((30, y_offset + 40), map_name, font=font_top1, fill=text_primary)
            
            top_pp = top_play.get("MapPP", 0)
            top_acc = round(top_play.get("MapAccuracy", 0) * 100, 2)
            mods = "".join(m.get("acronym", "") for m in top_play.get("Mods", [])) or "NM"
            
            draw.text((30, y_offset + 65), f"{top_pp:.2f}pp • {top_acc}% • {mods}", 
                      font=font_top1, fill=text_secondary)
            
            y_offset += 90
    elif top_plays:
        top1 = top_plays[0]
        draw.line([(30, 220), (870, 220)], fill=bar_bg, width=1)
        
        draw.text((30, 230), "TOP 1 PLAY", font=font_stat_label, fill=accent_color)
        
        map_name = top1.get("Filename", "Unknown Map")[:70]
        draw.text((30, 260), map_name, font=font_top1, fill=text_primary)
        
        top1_pp = top1.get("MapPP", 0)
        top1_acc = round(top1.get("MapAccuracy", 0) * 100, 2)
        mods = "".join(m.get("acronym", "") for m in top1.get("Mods", [])) or "NM"
        
        draw.text((30, 285), f"{top1_pp:.2f}pp • {top1_acc}% • {mods}", 
                  font=font_top1, fill=text_secondary)

    img_rgba = img.convert("RGBA")
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    for i in range(50):
        alpha = int(80 * (1 - i/50))
        gradient_draw.line([(0, i), (width, i)], fill=(*accent_color, alpha))
    
    img = Image.alpha_composite(img_rgba, gradient).convert("RGB")
        
    buffer = BytesIO()
    img.save(buffer, format="PNG", quality=95)
    buffer.seek(0)
    buffer.name = "profile.png"
    return buffer

# ============ INITIALIZE BOT ============
# minimal env checks for safe startup
REQUIRED_ENV = ["BOT_TOKEN", "API_BASE"]
missing_env = [v for v in REQUIRED_ENV if not globals().get(v)]
if missing_env:
    log.warning(f"Missing recommended env vars: {missing_env}. Bot may not function until configured.")

app = Client("osu_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ============ COMMANDS ============
@app.on_message(filters.command("lang"))
async def cmd_lang(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "lang_help"))
    
    lang = message.command[1].lower()
    if lang not in ["ru", "en"]:
        return await message.reply_text(t(uid, "lang_invalid"))
    
    USER_LANGUAGES[uid] = lang
    await message.reply_text(t(uid, "lang_set", lang=lang.upper()))

@app.on_message(filters.document)
async def replay_handler(_, message):
    uid = message.from_user.id
    if not message.document.file_name.endswith(".osr"):
        return
    path = await message.download()
    osu_path = None
    try:
        r = parse_replay(path)
        bid = await beatmap_id_from_hash(r["hash"])
        if not bid:
            return await message.reply_text(t(uid, "map_not_found"))
        osu_path = await download_osu_file(bid)
        s1, p1 = calc_pp_from_osu(osu_path, r["mods"], r["acc"], r["combo"], r["misses"])
        s2, p2 = calc_pp_from_osu(osu_path, r["mods"], 100.0, misses=0)
        await message.reply_text(t(uid, "replay", user=r["username"], p1=p1, s1=s1, p2=p2, s2=s2, diff=p2-p1))
    except Exception as e:
        log.exception("Replay failed")
        await message.reply_text(t(uid, "replay_error"))
    finally:
        if os.path.exists(path):
            os.remove(path)
        if osu_path and os.path.exists(osu_path):
            os.remove(osu_path)

@app.on_message(filters.command("pp"))
async def cmd_pp(_, message):
    uid = message.from_user.id
    text = " ".join(message.command[1:])
    m_bid = RE_BID.search(text)
    if not m_bid:
        return await message.reply_text(t(uid, "pp_help"))
    osu = None
    try:
        bid = m_bid.group(1)
        acc = RE_ACC.search(text)
        mods = RE_MODS.search(text)
        
        osu = await download_osu_file(bid)
        if not osu or not os.path.exists(osu):
            return await message.reply_text(t(uid, "map_not_found"))
        
        stars, pp = calc_pp_from_osu(osu, f"+{mods.group(1)}" if mods else "", float(acc.group(1)) if acc else 100.0)
        await message.reply_text(t(uid, "pp", stars=stars, pp=pp))
    except Exception as e:
        log.exception("PP failed")
        log.error(f"Details: {str(e)}")
        await message.reply_text(t(uid, "api_error"))
    finally:
        if osu and os.path.exists(osu):
            try:
                os.remove(osu)
            except:
                pass

@app.on_message(filters.command("stars"))
async def cmd_stars(_, message):
    uid = message.from_user.id
    m = RE_BID.search(message.text)
    if not m:
        return await message.reply_text(t(uid, "stars_help"))
    osu = None
    try:
        bid = m.group(1)
        osu = await download_osu_file(bid)
        if not osu or not os.path.exists(osu):
            return await message.reply_text(t(uid, "map_not_found"))
        
        bm = load_beatmap(osu)
        stars = pyttanko.diff_calc().calc(bm, 0).total
        await message.reply_text(f"{stars:.2f}★")
    except Exception as e:
        log.exception("Stars failed")
        log.error(f"Details: {str(e)}")
        await message.reply_text(t(uid, "api_error"))
    finally:
        if osu and os.path.exists(osu):
            try:
                os.remove(osu)
            except:
                pass

@app.on_message(filters.command("fc"))
async def cmd_fc(_, message):
    uid = message.from_user.id
    m = RE_BID.search(message.text)
    if not m:
        return await message.reply_text(t(uid, "fc_help"))
    osu = None
    try:
        mods = message.command[2] if len(message.command) > 2 else ""
        osu = await download_osu_file(m.group(1))
        s, p = calc_pp_from_osu(osu, mods, 100.0, misses=0)
        await message.reply_text(f"{s:.2f}★ | {p:.2f}pp")
    except Exception:
        log.exception("FC failed")
        await message.reply_text(t(uid, "api_error"))
    finally:
        if osu and os.path.exists(osu):
            os.remove(osu)

@app.on_message(filters.command("map"))
async def cmd_map(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "map_help"))
    
    text = message.command[1]
    beatmap_id = (RE_URL_BID.search(text) or type('m',(),{'group':lambda x:None})).group(1)
    beatmapset_id = (RE_MAPSET.search(text) or type('m',(),{'group':lambda x:None})).group(1)

    if not beatmap_id and not beatmapset_id:
        return await message.reply_text(t(uid, "invalid_link"))

    msg = await message.reply_text(". . .")
    try:
        info = None
        
        if beatmap_id:
            r, data = await fetch("https://osu.ppy.sh/api/get_beatmaps", {
                "k": OSU_API_KEY, "b": beatmap_id
            })
            if r and data:
                try:
                    js = json.loads(data)
                    info = js[0] if js else None
                except:
                    pass
        
        if not info and beatmapset_id:
            r, data = await fetch("https://osu.ppy.sh/api/get_beatmaps", {
                "k": OSU_API_KEY, "s": beatmapset_id
            })
            if r and data:
                try:
                    js = json.loads(data)
                    info = js[-1] if js else None
                except:
                    pass

        if not info:
            return await msg.edit_text(t(uid, "map_not_found"))

        cover_url = f"https://assets.ppy.sh/beatmaps/{info.get('beatmapset_id', '0')}/covers/cover.jpg"
        r, bg_data = await fetch(cover_url)
        
        if not bg_data:
            bg_data = b""
        
        loop = asyncio.get_event_loop()
        photo = await loop.run_in_executor(None, create_beatmap_card, bg_data, info)
        
        caption = f"[{info.get('artist', 'Unknown')} - {info.get('title', 'Unknown')}](https://osu.ppy.sh/b/{info.get('beatmap_id', '0')})\nDifficulty: {info.get('version', 'Unknown')}"
        await message.reply_photo(photo, caption=caption, reply_markup=pp_keyboard(info.get('beatmap_id', '0')))
        await msg.delete()
    except Exception as e:
        log.exception("Map command failed")
        log.error(f"Details: {str(e)}")
        await msg.edit_text(f"Error: {str(e)}")

def pp_keyboard(bid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Stars", callback_data=f"stars:{bid}"), InlineKeyboardButton("PP", callback_data=f"pp:{bid}")],
        [InlineKeyboardButton("FC", callback_data=f"fc:{bid}"), InlineKeyboardButton("98%", callback_data=f"whatif:{bid}:98")]
    ])

@app.on_message(filters.command("sr"))
async def cmd_search(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "search_help"))
    
    query = " ".join(message.command[1:])
    m = await search_beatmaps_v2(query)
    if not m:
        return await message.reply_text(t(uid, "not_found"))

    SEARCH_CACHE[message.chat.id] = {"maps": m, "index": 0}
    bm = m[0]
    text = f"-1 – {bm['artist']} {bm['title']}\nhttps://osu.ppy.sh/beatmapsets/{bm['id']}#osu/{bm.get('beatmap_id', bm['id'])}"
    await message.reply_text(text, reply_markup=beatmap_keyboard(0, len(m)), disable_web_page_preview=True)


@app.on_callback_query(filters.regex(r"idx_(next|prev)"))
async def cb_idx(_, cq):
    state = SEARCH_CACHE.get(cq.message.chat.id)
    if not state:
        return

    idx = state["index"]
    if cq.data == "idx_next":
        state["index"] = min(idx + 1, len(state["maps"]) - 1)
    else:
        state["index"] = max(idx - 1, 0)

    bm = state["maps"][state["index"]]
    text = f"-{state['index']+1} – {bm['artist']} {bm['title']}\nhttps://osu.ppy.sh/beatmapsets/{bm['id']}#osu/{bm.get('beatmap_id', bm['id'])}"

    # редактируем только если текст изменился
    if cq.message.text != text:
        await cq.message.edit_text(text, reply_markup=beatmap_keyboard(state["index"], len(state["maps"])), disable_web_page_preview=True)

    await cq.answer()


def beatmap_keyboard(idx, total):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀", callback_data="idx_prev"),
            InlineKeyboardButton(f"{idx+1}/{total}", callback_data="noop"),
            InlineKeyboardButton("▶", callback_data="idx_next")
        ]
    ])

@app.on_message(filters.command("top"))
async def cmd_top(_, message):
    m = await search_beatmaps_v2("", sort="ranked")
    if not m:
        return
    TOP_CACHE[message.chat.id] = {"maps": m, "index": 0}
    bm = m[0]
    text = f"{bm['artist']} – {bm['title']}\n\nhttps://osu.ppy.sh/beatmapsets/{bm['id']}#osu/{bm.get('beatmap_id','0')}"
    await message.reply_text(text, reply_markup=top_keyboard_inline(0, len(m)))

@app.on_callback_query(filters.regex(r"top_(next|prev)"))
async def cb_top_logic(_, cq):
    state = TOP_CACHE.get(cq.message.chat.id)
    if not state:
        return
    idx = state["index"]
    if "next" in cq.data:
        state["index"] = min(idx + 1, len(state["maps"]) - 1)
    elif "prev" in cq.data:
        state["index"] = max(idx - 1, 0)

    bm = state["maps"][state["index"]]
    text = f"{bm['artist']} – {bm['title']}\n\nhttps://osu.ppy.sh/beatmapsets/{bm['id']}#osu/{bm.get('beatmap_id','0')}"
    await cq.message.edit_text(text, reply_markup=top_keyboard_inline(state["index"], len(state["maps"])))
    await cq.answer()

def top_keyboard_inline(idx, total):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀", callback_data="top_prev"),
            InlineKeyboardButton(f"{idx+1}/{total}", callback_data="noop"),
            InlineKeyboardButton("▶", callback_data="top_next")
        ]
    ])

@app.on_callback_query(filters.regex(r"^(stars|pp|fc|whatif):(\d+)(?::(\d+))?$"))
async def cb_map_buttons(_, cq):
    action, bid, val = cq.matches[0].groups()
    osu = None
    try:
        osu = await download_osu_file(bid)
        if action == "stars":
            bm = load_beatmap(osu)
            res = f"{pyttanko.diff_calc().calc(bm, 0).total:.2f}★"
        elif action == "pp":
            s, p = calc_pp_from_osu(osu)
            res = f"{s:.2f}★ | {p:.2f}pp"
        elif action == "fc":
            s, p = calc_pp_from_osu(osu, misses=0)
            res = f"FC: {s:.2f}★ | {p:.2f}pp"
        elif action == "whatif":
            s, p = calc_pp_from_osu(osu, acc=float(val))
            res = f"{val}%: {s:.2f}★ | {p:.2f}pp"
        await cq.message.reply_text(res)
    except Exception as e:
        await cq.answer("Error", show_alert=True)
    finally:
        if osu and os.path.exists(osu):
            os.remove(osu)
        await cq.answer()

@app.on_message(filters.command("bind"))
async def cmd_bind(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "bind_help"))

    username = message.command[1]
    url = f"{API_BASE}/profile-username/{username}"

    try:
        r, data = await fetch(url)
        if r is None or data is None or r.status != 200:
            return await message.reply_text(t(uid, "bind_error"))

        profile = json.loads(data)
        BIND_CACHE[uid] = {
            "uid": profile["UserId"],
            "username": profile["Username"]
        }
        await message.reply_text(t(uid, "bind_success", username=profile['Username'], uid=profile['UserId']))
    except Exception as e:
        log.exception("Bind failed")
        log.error(f"Details: {str(e)}")
        await message.reply_text(t(uid, "bind_fail"))

@app.on_message(filters.command(["topplays", "pr"]))
async def cmd_topplays(_, message):
    uid = message.from_user.id
    if len(message.command) > 1:
        username = message.command[1]
    else:
        bound = BIND_CACHE.get(uid)
        if not bound:
            return await message.reply_text(t(uid, "not_bound"))
        username = bound["username"]

    url = f"{API_BASE}/profile-username/{username}"
    try:
        r, data = await fetch(url)
        if r.status != 200:
            return await message.reply_text(t(uid, "profile_not_found"))

        profile = json.loads(data)
        plays = profile.get("Top50Plays", [])
        if not plays:
            return await message.reply_text(t(uid, "no_topplays"))

        TOPPLAYS_CACHE[message.chat.id] = {
            "plays": sort_topplays(plays, "pp"),
            "index": 0,
            "profile": profile,
            "sort": "pp"
        }
        
        play = TOPPLAYS_CACHE[message.chat.id]["plays"][0]
        mods = "".join(m.get("acronym", "") for m in play.get("Mods", [])) or "NM"
        acc = round(play["MapAccuracy"] * 100, 2)
        text = f"Player: {profile.get('Username')}\nTop play 1/{len(plays)}\n{play['Filename']}\nPP: {play['MapPP']:.2f} | Acc: {acc}% | {mods}"
        await message.reply_text(text, reply_markup=topplays_keyboard(0, len(plays)))
    except Exception:
        log.exception("Topplays failed")
        await message.reply_text(t(uid, "api_error"))

@app.on_callback_query(filters.regex(r"tp_(prev|next|sort_pp|sort_date)"))
async def cb_topplays(_, cq):
    state = TOPPLAYS_CACHE.get(cq.message.chat.id)
    if not state:
        return await cq.answer()

    idx = state["index"]
    total = len(state["plays"])

    if cq.data == "tp_next":
        idx = min(idx + 1, total - 1)
    elif cq.data == "tp_prev":
        idx = max(idx - 1, 0)
    elif cq.data == "tp_sort_pp":
        state["plays"] = sort_topplays(state["profile"].get("Top50Plays", []), "pp")
        state["sort"] = "pp"
        idx = 0
    elif cq.data == "tp_sort_date":
        state["plays"] = sort_topplays(state["profile"].get("Top50Plays", []), "date")
        state["sort"] = "date"
        idx = 0

    state["index"] = idx
    play = state["plays"][idx]
    mods = "".join(m.get("acronym", "") for m in play.get("Mods", [])) or "NM"
    acc = round(play["MapAccuracy"] * 100, 2)
    text = f"Top play {idx+1}/{total}\n{play['Filename']}\nPP: {play['MapPP']:.2f} | Acc: {acc}% | {mods}"
    await cq.message.edit_text(text, reply_markup=topplays_keyboard(idx, total))
    await cq.answer()

def topplays_keyboard(idx, total):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀", callback_data="tp_prev"), InlineKeyboardButton(f"{idx+1}/{total}", callback_data="noop"), InlineKeyboardButton("▶", callback_data="tp_next")],
        [InlineKeyboardButton("Sort PP", callback_data="tp_sort_pp"), InlineKeyboardButton("Sort Date", callback_data="tp_sort_date")]
    ])

def sort_topplays(plays, method="pp"):
    if method == "pp":
        return sorted(plays, key=lambda x: x.get("MapPP", 0), reverse=True)
    elif method == "date":
        return sorted(plays, key=lambda x: x.get("PlayedDate", ""), reverse=True)
    return plays

@app.on_message(filters.command("prpic"))
async def cmd_prpic(_, message):
    uid = message.from_user.id
    if len(message.command) > 1:
        username = message.command[1]
    else:
        bound = BIND_CACHE.get(uid)
        if not bound:
            return await message.reply_text(t(uid, "not_bound"))
        username = bound["username"]

    mode = message.command[2].lower() if len(message.command) > 2 else "photo"
    url = f"{API_BASE}/profile-username/{username}"

    try:
        r, data = await fetch(url)
        if r is None or data is None or r.status != 200:
            return await message.reply_text(t(uid, "api_error"))
        data = json.loads(data)
    except Exception as e:
        log.error(f"prpic request failed: {e}")
        return await message.reply_text(t(uid, "api_error"))

    country_code = data.get('Region', '').upper()
    country_name = None
    if country_code:
        try:
            country = pycountry.countries.get(alpha_2=country_code)
            if country:
                country_name = country.name
        except:
            pass
    region_text = f"{country_code} ({country_name})" if country_name else country_code

    text = t(uid, "player_info", username=data.get('Username'), uid=data.get('UserId'), 
             global_rank=data.get('GlobalRank'), country_rank=data.get('CountryRank'),
             pp=data.get('OverallPP'), playcount=data.get('OverallPlaycount'),
             acc=round(data.get('OverallAccuracy', 0) * 100, 2))

    if mode == "text":
        await message.reply_text(text)
        return

    # fetch avatar bytes asynchronously and generate card in executor to avoid blocking
    avatar_bytes = None
    try:
        avatar_url = f"{API_BASE}/avatar/userid/{data['UserId']}?size=256"
        r2, a_bytes = await fetch(avatar_url)
        if r2 and a_bytes:
            avatar_bytes = a_bytes
    except Exception:
        avatar_bytes = None

    loop = asyncio.get_event_loop()
    gen = partial(generate_profile_card, data, region_text, uid, avatar_bytes)
    card = await loop.run_in_executor(None, gen)
    await message.reply_photo(photo=card)

@app.on_message(filters.command("setgr"))
async def cmd_setgr(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "gradient_help"))
    
    color_hex = message.command[1].lstrip("#")
    
    if len(color_hex) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color_hex):
        return await message.reply_text(t(uid, "gradient_invalid"))
    
    try:
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        GRADIENT_CACHE[uid] = (r, g, b)
        await message.reply_text(t(uid, "gradient_set", color=color_hex.upper()))
    except Exception as e:
        await message.reply_text(t(uid, "gradient_error", e=str(e)))

@app.on_message(filters.command("setfr"))
async def cmd_setfr(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "frame_help"))
    
    color_hex = message.command[1].lstrip("#")
    if len(color_hex) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color_hex):
        return await message.reply_text(t(uid, "frame_invalid"))
    
    try:
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        USER_FRAMES[uid] = (r, g, b)
        await message.reply_text(t(uid, "frame_set", color=color_hex.upper()))
    except Exception as e:
        await message.reply_text(t(uid, "frame_error", e=str(e)))

@app.on_message(filters.command("resetfr"))
async def cmd_resetfr(_, message):
    uid = message.from_user.id
    if uid in USER_FRAMES:
        del USER_FRAMES[uid]
        await message.reply_text(t(uid, "frame_reset"))
    else:
        await message.reply_text(t(uid, "frame_not_set"))

@app.on_message(filters.command("compare"))
async def cmd_compare(_, message):
    uid = message.from_user.id
    if len(message.command) < 3:
        return await message.reply_text(t(uid, "compare_help"))
    
    user1, user2 = message.command[1], message.command[2]
    
    async def fetch_profile(username):
        url = f"{API_BASE}/profile-username/{username}"
        r, data = await fetch(url)
        return json.loads(data) if r.status == 200 else None
    
    p1, p2 = await fetch_profile(user1), await fetch_profile(user2)
    if not p1 or not p2:
        return await message.reply_text(t(uid, "compare_not_found"))
    
    text = f"{t(uid, 'compare_header')}\n\n{p1['Username']} vs {p2['Username']}\nPP: {p1['OverallPP']} | {p2['OverallPP']}\nGlobal Rank: #{p1['GlobalRank']} | #{p2['GlobalRank']}\nCountry Rank: #{p1['CountryRank']} | #{p2['CountryRank']}\nAccuracy: {round(p1.get('OverallAccuracy',0)*100,2)}% | {round(p2.get('OverallAccuracy',0)*100,2)}%\nPlaycount: {p1['OverallPlaycount']} | {p2['OverallPlaycount']}"
    await message.reply_text(text)

@app.on_message(filters.command("modstats"))
async def cmd_modstats(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "modstats_help"))
    
    username = message.command[1]
    url = f"{API_BASE}/profile-username/{username}"
    r, data = await fetch(url)
    profile = json.loads(data) if r.status == 200 else None
    if not profile:
        return await message.reply_text(t(uid, "profile_not_found"))
    
    plays = profile.get("Top50Plays", [])
    if not plays:
        return await message.reply_text(t(uid, "no_topplays"))
    
    mods_count = {}
    for play in plays:
        mods = "".join(m.get("acronym", "") for m in play.get("Mods", [])) or "NM"
        mods_count[mods] = mods_count.get(mods, 0) + 1
    
    sorted_mods = sorted(mods_count.items(), key=lambda x: x[1], reverse=True)
    text = t(uid, "modstats_header", username=username) + "\n"
    for mod, count in sorted_mods:
        text += f"{mod}: {count}\n"
    await message.reply_text(text)

@app.on_message(filters.command("toplist"))
async def cmd_toplist(_, message):
    uid = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text(t(uid, "toplist_help"))
    
    type_ = message.command[1].lower()
    if type_ not in ["score", "pp"]:
        return await message.reply_text(t(uid, "toplist_invalid"))
    
    await send_leaderboard(_, message.chat.id, type_, 1, uid)

async def send_leaderboard(client, chat_id, type_, page, user_id, message_id=None):
    url = f"{API_BASE}/leaderboard/type={type_}/region=all/page={page}/limit={LIMIT}"
    headers = {"accept": "application/json", "authorization": f"Bearer {DROID_TOKEN}"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                if r.status != 200:
                    text = t(user_id, "toplist_error", status=r.status)
                    if message_id:
                        return await client.edit_message_text(chat_id, message_id, text)
                    else:
                        return await client.send_message(chat_id, text)
                data = await r.json()
    except Exception as e:
        if message_id:
            return await client.edit_message_text(chat_id, message_id, str(e))
        return await client.send_message(chat_id, str(e))

    leaderboard = data.get("Results", [])
    if not leaderboard:
        text = t(user_id, "toplist_empty")
        if message_id:
            return await client.edit_message_text(chat_id, message_id, text)
        return await client.send_message(chat_id, text)

    text = t(user_id, "toplist_header", type=type_, page=page) + "\n\n"
    for idx, player in enumerate(leaderboard, 1):
        val = f"Score: {player.get('OverallScore', 'N/A')}" if type_ == "score" else f"PP: {player.get('OverallPP', 'N/A')}"
        text += f"{idx + (page-1)*LIMIT}. {player['Username']} - {val}\n"

    keyboard = [
        [
            InlineKeyboardButton(
                t(user_id, "back") if page > 1 else "◀",
                callback_data=f"tl:{type_}:{page-1}" if page > 1 else "noop"
            ),
            InlineKeyboardButton(t(user_id, "next"), callback_data=f"tl:{type_}:{page+1}")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if message_id:
        await client.edit_message_text(chat_id, message_id, text, reply_markup=markup)
    else:
        await client.send_message(chat_id, text, reply_markup=markup)

@app.on_callback_query(filters.regex(r"^tl:"))
async def cb_toplist(client, cq):
    now = time.time()
    uid = cq.from_user.id
    last = COOLDOWN.get(cq.message.chat.id, 0)
    if now - last < CD_SECONDS:
        await cq.answer(t(uid, "wait"), show_alert=True)
        return
    COOLDOWN[cq.message.chat.id] = now

    _, type_, page = cq.data.split(":")
    page = int(page)
    await cq.answer()
    await send_leaderboard(client, cq.message.chat.id, type_, page, uid, message_id=cq.message.id)

@app.on_message(filters.command("dpp"))
async def dpp_cmd(_, msg):
    uid = msg.from_user.id
    args = msg.command
    if len(args) < 2:
        return await msg.reply_text("/dpp <beatmap_id_or_url> [mods] [acc]")

    link = args[1]
    m = re.search(r"beatmaps/(\d+)", link)
    if m:
        beatmap_id = m.group(1)
    else:
        m = re.search(r"#osu/(\d+)", link)
        if m:
            beatmap_id = m.group(1)
        else:
            m = re.search(r"beatmapsets/(\d+)", link)
            if m:
                beatmap_id = m.group(1)
            else:
                return await msg.reply_text("Invalid beatmap link")

    mods = args[2] if len(args) > 2 else ""
    acc = str(float(args[3])) if len(args) > 3 else ""

    form = aiohttp.FormData()
    form.add_field("beatmapfile", "", content_type="application/octet-stream")
    form.add_field("beatmaplink", beatmap_id)
    form.add_field("mods", mods)
    form.add_field("accuracy", acc)
    form.add_field("combo", "")
    form.add_field("misses", "")
    form.add_field("speedmultiplier", "")
    form.add_field("forcecs", "")
    form.add_field("forcear", "")
    form.add_field("forceod", "")
    form.add_field("generatestrainchart", "1")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(DPP_API_URL, data=form, timeout=30) as resp:
                if resp.status != 200:
                    return await msg.reply_text(f"API error: HTTP {resp.status}")
                response = await resp.json()
        except Exception as e:
            return await msg.reply_text(f"Ошибка расчёта DPP: {e}")

    if not response.get("performance"):
        return await msg.reply_text(f"Ошибка расчёта DPP, ответ: {response}")

    beatmap = response.get("beatmap", {})
    perf = response.get("performance", {}).get("droid", {})

    text = (
        f"{beatmap.get('artist', 'Unknown')} - {beatmap.get('title', 'Unknown')} "
        f"[{beatmap.get('version', 'Unknown')}]\n"
        f"Total DPP: {perf.get('total', 0.0):.2f}\n"
        f"Aim: {perf.get('aim', 0.0):.2f}, "
        f"Speed: {perf.get('speed', 0.0):.2f}, "
        f"Accuracy: {perf.get('accuracy', 0.0):.2f}\n"
        f"Mods: {mods or 'NM'}"
    )

    await msg.reply_text(text)
    
@app.on_message(filters.command("yn"))
async def yn_cmd(_, msg):
    await msg.reply_text(random.choice(["yep", "nope"]))

@app.on_message(filters.command("roll"))
async def roll_cmd(_, msg):
    args = msg.command
    if len(args) == 1:
        num = random.randint(1, 100)
        await msg.reply_text(f"rolled: {num}")
    elif len(args) == 2:
        try:
            max_val = int(args[1])
            if max_val < 1:
                return await msg.reply_text("Max must be >= 1")
            num = random.randint(1, max_val)
            await msg.reply_text(f"rolled: {num}")
        except ValueError:
            await msg.reply_text("Only numbers")
    elif len(args) == 3:
        try:
            min_val = int(args[1])
            max_val = int(args[2])
            if min_val > max_val:
                return await msg.reply_text("Min must be <= max")
            num = random.randint(min_val, max_val)
            await msg.reply_text(f"rolled: {num}")
        except ValueError:
            await msg.reply_text("Only numbers")
            
def generate_compare_card(user_data1, user_data2):
    width, height = 900, 520
    img = Image.new("RGB", (width, height), (15, 15, 20))
    draw = ImageDraw.Draw(img, "RGBA")

    try:
        font_title = ImageFont.truetype("font.ttf", 42)
        font_header = ImageFont.truetype("font.ttf", 28)
        font_vs = ImageFont.truetype("font.ttf", 20)
        font_winner = ImageFont.truetype("font.ttf", 16)
        font_stat_value = ImageFont.truetype("font.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_vs = ImageFont.load_default()
        font_winner = ImageFont.load_default()
        font_stat_value = ImageFont.load_default()

    accent_color = (138, 43, 226)
    gold_color = (255, 215, 0)
    text_primary = (255, 255, 255)
    text_secondary = (200, 200, 200)
    bar_bg = (40, 40, 50)
    
    draw.text((30, 15), "Player comparison:", font=font_title, fill=accent_color)
    draw.line([(30, 60), (870, 60)], fill=bar_bg, width=2)

    user1_name = user_data1.get("Username", "Unknown")
    user2_name = user_data2.get("Username", "Unknown")
    
    user1_pp = user_data1.get("OverallPP", 0)
    user2_pp = user_data2.get("OverallPP", 0)
    
    winner_pp = max(user1_pp, user2_pp)
    
    draw.text((50, 85), user1_name, font=font_header, fill=text_primary)
    if user1_pp == winner_pp and user1_pp > 0:
        draw.text((50, 120), "WINNER", font=font_winner, fill=gold_color)
    
    draw.text((390, 95), "vs", font=font_vs, fill=text_secondary)
    
    draw.text((570, 85), user2_name, font=font_header, fill=text_primary)
    if user2_pp == winner_pp and user2_pp > 0:
        draw.text((570, 120), "WINNER", font=font_winner, fill=gold_color)

    draw.line([(30, 165), (870, 165)], fill=bar_bg, width=1)

    y_pos = 195
    
    user1_grank = user_data1.get("GlobalRank", "N/A")
    user2_grank = user_data2.get("GlobalRank", "N/A")
    draw.text((50, y_pos), f"PP: {user1_pp:.2f}", font=font_stat_value, fill=accent_color)
    draw.text((550, y_pos), f"PP: {user2_pp:.2f}", font=font_stat_value, fill=accent_color)
    
    y_pos += 50
    draw.text((50, y_pos), f"Global Rank: #{user1_grank}", font=font_stat_value, fill=text_primary)
    draw.text((550, y_pos), f"Global Rank: #{user2_grank}", font=font_stat_value, fill=text_primary)
    
    y_pos += 50
    user1_crank = user_data1.get("CountryRank", "N/A")
    user2_crank = user_data2.get("CountryRank", "N/A")
    draw.text((50, y_pos), f"Country Rank: #{user1_crank}", font=font_stat_value, fill=text_primary)
    draw.text((550, y_pos), f"Country Rank: #{user2_crank}", font=font_stat_value, fill=text_primary)
    
    y_pos += 50
    user1_acc = round(user_data1.get("OverallAccuracy", 0) * 100, 2)
    user2_acc = round(user_data2.get("OverallAccuracy", 0) * 100, 2)
    draw.text((50, y_pos), f"Accuracy: {user1_acc}%", font=font_stat_value, fill=text_primary)
    draw.text((550, y_pos), f"Accuracy: {user2_acc}%", font=font_stat_value, fill=text_primary)
    
    y_pos += 50
    user1_playcount = user_data1.get("OverallPlaycount", 0)
    user2_playcount = user_data2.get("OverallPlaycount", 0)
    draw.text((50, y_pos), f"Playcount: {user1_playcount}", font=font_stat_value, fill=text_primary)
    draw.text((550, y_pos), f"Playcount: {user2_playcount}", font=font_stat_value, fill=text_primary)

    img_rgba = img.convert("RGBA")
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    for i in range(50):
        alpha = int(80 * (1 - i/50))
        gradient_draw.line([(0, i), (width, i)], fill=(*accent_color, alpha))
    
    img = Image.alpha_composite(img_rgba, gradient).convert("RGB")

    buffer = BytesIO()
    img.save(buffer, format="PNG", quality=95)
    buffer.seek(0)
    buffer.name = "compare.png"
    return buffer

@app.on_message(filters.command("comparepic"))
async def cmd_comparepic(_, message):
    uid = message.from_user.id
    if len(message.command) < 3:
        return await message.reply_text("Usage: /comparepic <username1> <username2>")
    
    user1, user2 = message.command[1], message.command[2]
    
    async def fetch_profile(username):
        url = f"{API_BASE}/profile-username/{username}"
        r, data = await fetch(url)
        if r and data and r.status == 200:
            try:
                return json.loads(data)
            except:
                return None
        return None
    
    try:
        p1 = await fetch_profile(user1)
        p2 = await fetch_profile(user2)
        
        if not p1 or not p2:
            return await message.reply_text(t(uid, "compare_not_found"))
        
        loop = asyncio.get_event_loop()
        card = await loop.run_in_executor(None, generate_compare_card, p1, p2)
        await message.reply_photo(photo=card)
    except Exception as e:
        log.exception("Comparepic failed")
        await message.reply_text(t(uid, "api_error"))

async def fetch_pp_history(username):
    url = f"{API_BASE}/profile-username/{username}"
    r, data = await fetch(url)
    if r and data and r.status == 200:
        try:
            profile = json.loads(data)
            top_plays = profile.get("Top50Plays", [])
            
            dates_pp = {}
            for play in top_plays:
                date_str = play.get("PlayedDate", "")
                if date_str:
                    try:
                        play_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        date_key = play_date.date()
                        current_pp = float(play.get("MapPP", 0))
                        
                        if date_key not in dates_pp:
                            dates_pp[date_key] = current_pp
                        else:
                            dates_pp[date_key] = max(dates_pp[date_key], current_pp)
                    except:
                        pass
            
            return dates_pp
        except:
            return None
    return None

def generate_pp_graph(username, pp_data):
    if not pp_data or len(pp_data) < 2:
        return None
    
    dates = sorted(pp_data.keys())
    last_30_days = datetime.now().date() - timedelta(days=30)
    dates = [d for d in dates if d >= last_30_days]
    
    if len(dates) < 2:
        return None
    
    pp_values = [pp_data[d] for d in dates]
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f0f14')
    ax.set_facecolor('#0f0f14')
    
    ax.plot(dates, pp_values, color='#8A2BE2', linewidth=3, marker='o', markersize=6, label='PP')
    ax.fill_between(dates, pp_values, alpha=0.2, color='#8A2BE2')
    
    ax.grid(True, alpha=0.2, color='#ffffff')
    ax.set_xlabel('Date', color='#ffffff', fontsize=11)
    ax.set_ylabel('PP', color='#ffffff', fontsize=11)
    ax.set_title(f'{username} - PP Progress (Last 30 Days)', color='#ffffff', fontsize=14, pad=20)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=45, color='#ffffff')
    plt.yticks(color='#ffffff')
    
    for spine in ax.spines.values():
        spine.set_color('#404050')
        spine.set_linewidth(2)
    
    ax.tick_params(colors='#ffffff')
    
    min_pp = min(pp_values)
    max_pp = max(pp_values)
    pp_diff = max_pp - min_pp
    
    text_str = f'Min: {min_pp:.0f}pp\nMax: {max_pp:.0f}pp\nGain: +{pp_diff:.0f}pp'
    ax.text(0.02, 0.98, text_str, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#1a1a1f', alpha=0.8),
            color='#8A2BE2', family='monospace')
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='#0f0f14', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    buffer.name = "ppgraph.png"
    return buffer

@app.on_message(filters.command("ppgraph"))
async def cmd_ppgraph(_, message):
    uid = message.from_user.id
    
    if len(message.command) > 1:
        username = message.command[1]
    else:
        bound = BIND_CACHE.get(uid)
        if not bound:
            return await message.reply_text(t(uid, "not_bound"))
        username = bound["username"]
    
    msg = await message.reply_text("Загружаю данные...")
    
    try:
        pp_data = await fetch_pp_history(username)
        
        if not pp_data:
            return await msg.edit_text("Не удалось получить историю PP")
        
        if len(pp_data) < 2:
            return await msg.edit_text("Недостаточно данных для графика (нужно минимум 2 плея)")
        
        graph = generate_pp_graph(username, pp_data)
        
        if not graph:
            return await msg.edit_text("Недостаточно данных за последние 30 дней")
        
        await message.reply_photo(photo=graph)
        await msg.delete()
    except Exception as e:
        log.exception("PPGraph failed")
        await msg.edit_text(f"Ошибка: {str(e)}")

async def fetch_server_stats():
    url = "https://new.osudroid.moe/api2/frontend/online-stats"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    return await r.json()
    except Exception as e:
        log.error(f"Server stats fetch failed: {e}")
    return None

def generate_server_stats_card(stats):
    width, height = 900, 500
    img = Image.new("RGB", (width, height), (15, 15, 20))
    draw = ImageDraw.Draw(img, "RGBA")
    
    try:
        font_title = ImageFont.truetype("font.ttf", 52)
        font_label = ImageFont.truetype("font.ttf", 24)
        font_value = ImageFont.truetype("font.ttf", 48)
        font_small = ImageFont.truetype("font.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_value = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    accent_color = (138, 43, 226)
    gold_color = (255, 215, 0)
    text_primary = (255, 255, 255)
    text_secondary = (200, 200, 200)
    bar_bg = (40, 40, 50)
    
    draw.text((30, 20), "OSU!Droid Server Stats", font=font_title, fill=accent_color)
    draw.line([(30, 75), (870, 75)], fill=bar_bg, width=2)
    
    registered = stats.get("RegisteredUsers", 0)
    active_hour = stats.get("ActiveUsersLastHour", 0)
    active_day = stats.get("ActiveUsersLastDay", 0)
    
    x_positions = [50, 350, 650]
    labels = ["Registered Users", "Online Last Hour", "Active Last Day"]
    values = [registered, active_hour, active_day]
    colors = [gold_color, accent_color, accent_color]
    
    for i, (x, label, value, color) in enumerate(zip(x_positions, labels, values, colors)):
        draw.text((x, 120), label, font=font_label, fill=text_secondary)
        draw.text((x, 170), f"{value:,}", font=font_value, fill=color)
        
        if i < 2:
            draw.line([(310 + i*300, 100), (310 + i*300, 320)], fill=bar_bg, width=1)
    
    draw.line([(30, 350), (870, 350)], fill=bar_bg, width=2)
    
    activity_percent = round((active_day / registered * 100), 2) if registered > 0 else 0
    
    draw.text((30, 380), "Activity Rate (Last 24h)", font=font_label, fill=text_secondary)
    
    bar_width = 800
    bar_x = 50
    bar_y = 430
    
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + 30], fill=bar_bg)
    draw.rectangle([bar_x, bar_y, bar_x + int(bar_width * (active_day / registered)) if registered > 0 else 0, bar_y + 30], fill=accent_color)
    
    draw.text((bar_x + bar_width + 20, bar_y), f"{activity_percent}%", font=font_value, fill=accent_color)
    
    img_rgba = img.convert("RGBA")
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    for i in range(50):
        alpha = int(80 * (1 - i/50))
        gradient_draw.line([(0, i), (width, i)], fill=(*accent_color, alpha))
    
    img = Image.alpha_composite(img_rgba, gradient).convert("RGB")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG", quality=95)
    buffer.seek(0)
    buffer.name = "server_stats.png"
    return buffer

SERVER_STATS_HISTORY = []

def generate_server_stats_graph(history):
    if len(history) < 2:
        return None
    
    dates = [h['timestamp'].date() for h in history]
    active_hour = [h['ActiveUsersLastHour'] for h in history]
    active_day = [h['ActiveUsersLastDay'] for h in history]
    registered = [h['RegisteredUsers'] for h in history]
    
    fig = plt.figure(figsize=(14, 9), facecolor='#0f0f14')
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
    ax_main = fig.add_subplot(gs[0, :])
    ax_hour = fig.add_subplot(gs[1, 0])
    ax_day = fig.add_subplot(gs[1, 1])
    
    for ax in [ax_main, ax_hour, ax_day]:
        ax.set_facecolor('#0f0f14')
    
    ax_main.plot(dates, active_hour, color='#8A2BE2', linewidth=3.5, marker='o', markersize=8, label='Online (Last Hour)', zorder=3)
    ax_main.plot(dates, active_day, color='#FFD700', linewidth=3.5, marker='s', markersize=8, label='Active (Last 24h)', zorder=3)
    ax_main.fill_between(dates, active_hour, alpha=0.15, color='#8A2BE2')
    ax_main.fill_between(dates, active_day, alpha=0.15, color='#FFD700')
    
    ax_main.grid(True, alpha=0.25, color='#ffffff', linestyle='--', linewidth=0.8, zorder=1)
    ax_main.set_ylabel('Active Users', color='#ffffff', fontsize=12, fontweight='bold')
    ax_main.set_title('Server Activity Trend', color='#ffffff', fontsize=13, pad=15, fontweight='bold')
    ax_main.legend(loc='upper left', framealpha=0.95, facecolor='#1a1a1f', edgecolor='#8A2BE2', labelcolor='#ffffff', fontsize=10)
    
    for spine in ax_main.spines.values():
        spine.set_color('#404050')
        spine.set_linewidth(2)
    ax_main.tick_params(colors='#ffffff')
    
    ax_hour.fill_between(dates, active_hour, alpha=0.3, color='#8A2BE2')
    ax_hour.plot(dates, active_hour, color='#8A2BE2', linewidth=2.5, marker='o', markersize=6)
    ax_hour.grid(True, alpha=0.2, color='#ffffff', linestyle='--')
    ax_hour.set_title('Hourly Active', color='#8A2BE2', fontsize=11, fontweight='bold')
    ax_hour.set_ylabel('Users', color='#ffffff', fontsize=10)
    
    for spine in ax_hour.spines.values():
        spine.set_color('#404050')
        spine.set_linewidth(1.5)
    ax_hour.tick_params(colors='#ffffff', labelsize=9)
    
    ax_day.fill_between(dates, active_day, alpha=0.3, color='#FFD700')
    ax_day.plot(dates, active_day, color='#FFD700', linewidth=2.5, marker='s', markersize=6)
    ax_day.grid(True, alpha=0.2, color='#ffffff', linestyle='--')
    ax_day.set_title('Daily Active', color='#FFD700', fontsize=11, fontweight='bold')
    ax_day.set_ylabel('Users', color='#ffffff', fontsize=10)
    
    for spine in ax_day.spines.values():
        spine.set_color('#404050')
        spine.set_linewidth(1.5)
    ax_day.tick_params(colors='#ffffff', labelsize=9)
    
    current_hour = active_hour[-1]
    current_day = active_day[-1]
    current_reg = registered[-1]
    
    prev_hour = active_hour[-2] if len(active_hour) > 1 else current_hour
    prev_day = active_day[-2] if len(active_day) > 1 else current_day
    prev_reg = registered[-2] if len(registered) > 1 else current_reg
    
    hour_change = current_hour - prev_hour
    day_change = current_day - prev_day
    reg_change = current_reg - prev_reg
    
    hour_arrow = "↑" if hour_change > 0 else "↓" if hour_change < 0 else "→"
    day_arrow = "↑" if day_change > 0 else "↓" if day_change < 0 else "→"
    reg_arrow = "↑" if reg_change > 0 else "↓" if reg_change < 0 else "→"
    
    hour_color = "#00FF00" if hour_change >= 0 else "#FF0000"
    day_color = "#00FF00" if day_change >= 0 else "#FF0000"
    
    info_box_text = f" CURRENT STATS\n\n Online (1h): {current_hour}\n   {hour_arrow} {abs(hour_change):+d}\n\n Active (24h): {current_day}\n   {day_arrow} {abs(day_change):+d}\n\n Total Registered: {current_reg:,}\n   {reg_arrow} {abs(reg_change):+d}"
    
    fig.text(0.98, 0.5, info_box_text, transform=fig.transFigure, fontsize=10.5,
            verticalalignment='center', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=1', facecolor='#1a1a1f', alpha=0.95, edgecolor='#8A2BE2', linewidth=2.5),
            color='#ffffff', family='monospace', fontweight='bold')
    
    fig.text(0.5, 0.02, 'OSU!Droid Server Statistics', ha='center', color='#8A2BE2', fontsize=14, fontweight='bold')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='#0f0f14', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    buffer.name = "server_graph.png"
    return buffer

@app.on_message(filters.command("server"))
async def cmd_server(_, message):
    msg = await message.reply_text("Получаю статистику сервера...")
    
    try:
        stats = await fetch_server_stats()
        
        if not stats:
            return await msg.edit_text("Ошибка получения статистики сервера")
        
        stats['timestamp'] = datetime.now()
        SERVER_STATS_HISTORY.append(stats)
        
        if len(SERVER_STATS_HISTORY) > 7:
            SERVER_STATS_HISTORY.pop(0)
        
        if len(SERVER_STATS_HISTORY) >= 2:
            loop = asyncio.get_event_loop()
            graph = await loop.run_in_executor(None, generate_server_stats_graph, SERVER_STATS_HISTORY)
            if graph:
                await message.reply_photo(photo=graph)
                await msg.delete()
                return
        
        await msg.edit_text("Нужно минимум 2 вызова для графика. Попробуй снова через секунду!")
    except Exception as e:
        log.exception("Server stats failed")
        await msg.edit_text(f"Ошибка: {str(e)}")
        
        
def get_difficulty_range(top_plays, margin=1.0):
    if not top_plays:
        return 3.0, 7.0
    
    difficulties = []
    for play in top_plays:
        filename = play.get("Filename", "")
        if "[" in filename and "]" in filename:
            try:
                diff_str = filename.split("[")[1].split("]")[0]
                for char in diff_str:
                    if char.replace(".", "").isdigit():
                        continue
                    diff_str = diff_str.replace(char, "")
                diff = float(diff_str)
                difficulties.append(diff)
            except:
                pass
    
    if difficulties:
        avg_diff = sum(difficulties) / len(difficulties)
        return max(0.5, avg_diff - margin), min(10.0, avg_diff + margin)
    return 3.0, 7.0

async def get_recommendations(username, limit=5):
    url = f"{API_BASE}/profile-username/{username}"
    r, data = await fetch(url)
    if not r or not data or r.status != 200:
        return None
    
    try:
        profile = json.loads(data)
        top_plays = profile.get("Top50Plays", [])
        
        if not top_plays:
            return None
        
        min_diff, max_diff = get_difficulty_range(top_plays)
        
        searched = await search_beatmaps_v2("", limit=50, sort="ranked")
        if not searched:
            return None
        
        recommendations = []
        played_ids = set()
        for play in top_plays:
            filename = play.get("Filename", "")
            if " " in filename:
                try:
                    bid = int(filename.split()[-1].strip("()"))
                    played_ids.add(bid)
                except:
                    pass
        
        for map_data in searched:
            try:
                stars = float(map_data.get("stars", 0))
                if min_diff <= stars <= max_diff:
                    if map_data["id"] not in played_ids:
                        recommendations.append(map_data)
                        if len(recommendations) >= limit:
                            break
            except:
                pass
        
        return recommendations
    except:
        return None

@app.on_message(filters.command("recommend"))
async def cmd_recommend(_, message):
    uid = message.from_user.id
    
    if len(message.command) > 1:
        username = message.command[1]
    else:
        bound = BIND_CACHE.get(uid)
        if not bound:
            return await message.reply_text(t(uid, "not_bound"))
        username = bound["username"]
    
    msg = await message.reply_text("Analyzing top plays...")
    
    try:
        recommendations = await get_recommendations(username, limit=5)
        
        if not recommendations:
            return await msg.edit_text("Could not find recommendations")
        
        text = f"Recommendations for {username}:\n\n"
        for i, rec in enumerate(recommendations, 1):
            text += f"{i}. {rec['artist']} - {rec['title']}\n"
            text += f"   Difficulty: {rec['stars']}*\n"
            text += f"   https://osu.ppy.sh/beatmapsets/{rec['id']}\n\n"
        
        await msg.edit_text(text, disable_web_page_preview=True)
    except Exception as e:
        log.exception("Recommend failed")
        await msg.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("milestone"))
async def cmd_milestone(_, message):
    uid = message.from_user.id
    
    if len(message.command) > 1:
        username = message.command[1]
    else:
        bound = BIND_CACHE.get(uid)
        if not bound:
            return await message.reply_text(t(uid, "not_bound"))
        username = bound["username"]
    
    msg = await message.reply_text("Analyzing milestones...")
    
    try:
        url = f"{API_BASE}/profile-username/{username}"
        r, data = await fetch(url)
        
        if not r or not data or r.status != 200:
            return await msg.edit_text("Profile not found")
        
        profile = json.loads(data)
        pp = profile.get("OverallPP", 0)
        playcount = profile.get("OverallPlaycount", 0)
        accuracy = profile.get("OverallAccuracy", 0) * 100
        
        milestones = []
        
        pp_milestones = [100, 500, 1000, 2000, 3000, 5000, 10000, 15000, 20000, 30000]
        for m in pp_milestones:
            if pp >= m:
                milestones.append((f"{m}pp", "DONE"))
            else:
                remaining = m - pp
                milestones.append((f"{m}pp", f"NEED {remaining:.0f}pp"))
        
        playcount_milestones = [100, 500, 1000, 5000, 10000, 50000, 100000]
        for m in playcount_milestones:
            if playcount >= m:
                milestones.append((f"{m} plays", "DONE"))
            else:
                remaining = m - playcount
                milestones.append((f"{m} plays", f"NEED {remaining:.0f}"))
        
        accuracy_milestones = [90.0, 92.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0]
        for m in accuracy_milestones:
            if accuracy >= m:
                milestones.append((f"{m}% accuracy", "DONE"))
            else:
                remaining = m - accuracy
                milestones.append((f"{m}% accuracy", f"NEED {remaining:.2f}%"))
        
        loop = asyncio.get_event_loop()
        card = await loop.run_in_executor(None, generate_milestone_card, username, pp, playcount, accuracy, milestones)
        
        await message.reply_photo(photo=card)
        await msg.delete()
    except Exception as e:
        log.exception("Milestone failed")
        await msg.edit_text(f"Error: {str(e)}")
        
def generate_milestone_card(username, pp, playcount, accuracy, milestones):
    width, height = 900, 1200
    img = Image.new("RGB", (width, height), (15, 15, 20))
    draw = ImageDraw.Draw(img, "RGBA")
    
    try:
        font_title = ImageFont.truetype("font.ttf", 48)
        font_stat_label = ImageFont.truetype("font.ttf", 20)
        font_stat_value = ImageFont.truetype("font.ttf", 24)
        font_milestone = ImageFont.truetype("font.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_stat_label = ImageFont.load_default()
        font_stat_value = ImageFont.load_default()
        font_milestone = ImageFont.load_default()
    
    accent_color = (138, 43, 226)
    gold_color = (255, 215, 0)
    green_color = (0, 255, 0)
    red_color = (255, 50, 50)
    text_primary = (255, 255, 255)
    text_secondary = (200, 200, 200)
    bar_bg = (40, 40, 50)
    
    draw.text((30, 20), "Milestones", font=font_title, fill=accent_color)
    draw.line([(30, 75), (870, 75)], fill=bar_bg, width=2)
    
    draw.text((30, 100), f"Player: {username}", font=font_stat_label, fill=text_secondary)
    
    y_pos = 150
    draw.text((30, y_pos), f"Current PP: {pp:.2f}", font=font_stat_value, fill=accent_color)
    y_pos += 40
    draw.text((30, y_pos), f"Current Playcount: {playcount}", font=font_stat_value, fill=accent_color)
    y_pos += 40
    draw.text((30, y_pos), f"Current Accuracy: {accuracy:.2f}%", font=font_stat_value, fill=accent_color)
    
    y_pos += 60
    draw.line([(30, y_pos), (870, y_pos)], fill=bar_bg, width=2)
    
    y_pos += 20
    draw.text((30, y_pos), "MILESTONES", font=font_stat_label, fill=accent_color)
    y_pos += 40
    
    for milestone, status in milestones:
        if status == "DONE":
            color = green_color
            symbol = "[OK]"
        else:
            color = red_color
            symbol = "[WIP]"
        
        draw.text((30, y_pos), milestone, font=font_milestone, fill=text_primary)
        draw.text((500, y_pos), symbol, font=font_milestone, fill=color)
        draw.text((600, y_pos), status, font=font_milestone, fill=color)
        y_pos += 35
    
    img_rgba = img.convert("RGBA")
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    for i in range(50):
        alpha = int(80 * (1 - i/50))
        gradient_draw.line([(0, i), (width, i)], fill=(*accent_color, alpha))
    
    img = Image.alpha_composite(img_rgba, gradient).convert("RGB")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG", quality=95)
    buffer.seek(0)
    buffer.name = "milestones.png"
    return buffer

def generate_accuracy_graph(username, pp_data):
    if not pp_data or len(pp_data) < 2:
        return None
    
    dates = sorted(pp_data.keys())
    accuracies = [pp_data[d].get('acc', 0) for d in dates]
    
    last_30_days = datetime.now().date() - timedelta(days=30)
    filtered_data = [(d, a) for d, a in zip(dates, accuracies) if d >= last_30_days]
    
    if len(filtered_data) < 2:
        return None
    
    dates, accuracies = zip(*filtered_data)
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f0f14')
    ax.set_facecolor('#0f0f14')
    
    ax.plot(dates, accuracies, color='#00FF00', linewidth=3, marker='o', markersize=6, label='Accuracy')
    ax.fill_between(dates, accuracies, alpha=0.2, color='#00FF00')
    
    ax.axhline(y=95, color='#FFD700', linestyle='--', linewidth=2, alpha=0.5, label='95% target')
    ax.axhline(y=98, color='#8A2BE2', linestyle='--', linewidth=2, alpha=0.5, label='98% target')
    
    ax.grid(True, alpha=0.2, color='#ffffff')
    ax.set_xlabel('Date', color='#ffffff', fontsize=11)
    ax.set_ylabel('Accuracy %', color='#ffffff', fontsize=11)
    ax.set_ylim([80, 100.5])
    ax.set_title(f'{username} - Accuracy Progress (Last 30 Days)', color='#ffffff', fontsize=14, pad=20)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=45, color='#ffffff')
    plt.yticks(color='#ffffff')
    
    for spine in ax.spines.values():
        spine.set_color('#404050')
        spine.set_linewidth(2)
    
    ax.tick_params(colors='#ffffff')
    ax.legend(loc='lower left', framealpha=0.9, facecolor='#1a1a1f', edgecolor='#00FF00', labelcolor='#ffffff')
    
    min_acc = min(accuracies)
    max_acc = max(accuracies)
    avg_acc = sum(accuracies) / len(accuracies)
    
    text_str = f'Min: {min_acc:.2f}%\nMax: {max_acc:.2f}%\nAvg: {avg_acc:.2f}%'
    ax.text(0.98, 0.02, text_str, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='#1a1a1f', alpha=0.8),
            color='#00FF00', family='monospace')
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='#0f0f14', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    buffer.name = "accuracygraph.png"
    return buffer

async def fetch_accuracy_history(username):
    url = f"{API_BASE}/profile-username/{username}"
    r, data = await fetch(url)
    if r and data and r.status == 200:
        try:
            profile = json.loads(data)
            top_plays = profile.get("Top50Plays", [])
            
            dates_acc = {}
            for play in top_plays:
                date_str = play.get("PlayedDate", "")
                if date_str:
                    try:
                        play_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        date_key = play_date.date()
                        acc = float(play.get("MapAccuracy", 0)) * 100
                        
                        if date_key not in dates_acc:
                            dates_acc[date_key] = {'acc': acc, 'count': 1}
                        else:
                            dates_acc[date_key]['acc'] = (dates_acc[date_key]['acc'] + acc) / 2
                            dates_acc[date_key]['count'] += 1
                    except:
                        pass
            
            return dates_acc
        except:
            return None
    return None

@app.on_message(filters.command("accuracygraph"))
async def cmd_accuracygraph(_, message):
    uid = message.from_user.id
    
    if len(message.command) > 1:
        username = message.command[1]
    else:
        bound = BIND_CACHE.get(uid)
        if not bound:
            return await message.reply_text(t(uid, "not_bound"))
        username = bound["username"]
    
    msg = await message.reply_text("Loading data...")
    
    try:
        acc_data = await fetch_accuracy_history(username)
        
        if not acc_data:
            return await msg.edit_text("Could not get accuracy history")
        
        if len(acc_data) < 2:
            return await msg.edit_text("Not enough data for graph")
        
        loop = asyncio.get_event_loop()
        graph = await loop.run_in_executor(None, generate_accuracy_graph, username, acc_data)
        
        if not graph:
            return await msg.edit_text("Not enough data for last 30 days")
        
        await message.reply_photo(photo=graph)
        await msg.delete()
    except Exception as e:
        log.exception("AccuracyGraph failed")
        await msg.edit_text(f"Error: {str(e)}")
        
async def download_from_mirrors(beatmapset_id: str, no_video: bool = True):
    suffix = "?noVideo=1" if no_video else ""
    mirrors = [
        f"https://api.nerinyan.moe/d/{beatmapset_id}{suffix}",
        f"https://osu.direct/api/d/{beatmapset_id}{suffix}"
    ]
    data = None
    for url in mirrors:
        try:
            log.info(f"Trying mirror: {url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as r:
                    if r.status == 200:
                        data = await r.read()
                        log.info(f"Downloaded {len(data)} bytes from {url}")
                        break
                    else:
                        log.warning(f"Mirror returned HTTP {r.status}: {url}")
        except Exception as e:
            log.error(f"Error downloading from {url}: {e}")
            continue
    return data

@app.on_message(filters.command("dwm"))
async def cmd_dwm(_, message):
    m = RE_MAPSET.search(" ".join(message.command[1:]))
    if not m:
        return await message.reply_text("Invalid link!")

    beatmapset_id = m.group(1)
    buttons = [
        [types.InlineKeyboardButton("With Video", callback_data=f"{beatmapset_id}|0")],
        [types.InlineKeyboardButton("No Video", callback_data=f"{beatmapset_id}|1")]
    ]
    keyboard = types.InlineKeyboardMarkup(buttons)
    await message.reply_text("Choose download type:", reply_markup=keyboard)

@app.on_callback_query()
async def callback_dwm(_, callback_query):
    beatmapset_id, no_video_flag = callback_query.data.split("|")
    no_video = no_video_flag == "1"
    path = os.path.join(DOWNLOAD_DIR, f"{beatmapset_id}.osz")

    await callback_query.message.edit_text(f"Downloading beatmapset {beatmapset_id}...")

    try:
        data = await download_from_mirrors(beatmapset_id, no_video=no_video)
        if not data:
            await callback_query.message.edit_text("All mirrors failed")
            return

        with open(path, "wb") as f:
            f.write(data)
        log.info(f"Saved file to {path}")

        await callback_query.message.edit_text("Uploading file...")
        await callback_query.message.reply_document(path, caption=f"Beatmapset {beatmapset_id}")

    except Exception as e:
        log.error(f"Download error for {beatmapset_id}: {e}")
        await callback_query.message.edit_text(f"Download error: {e}")

    finally:
        if os.path.exists(path):
            os.remove(path)
            log.info(f"Deleted local file {path}")

if __name__ == "__main__":
    log.info("Bot starting")
    app.run()
