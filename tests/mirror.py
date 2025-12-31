import os
import aiohttp
from pyrogram import Client, filters, types
import re
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("mirror-bot")

BOT_TOKEN = "your_bot_token_here"
API_ID= "1234567"
API_HASH= "your_api_hash_here"

app = Client(
    name="mirror_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

RE_MAPSET = re.compile(r"beatmapsets/(\d+)")
DOWNLOAD_DIR = r"C:\Users\user\Desktop\testingodn\downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

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

@app.on_message(filters.command("dw"))
async def cmd_dw(_, message):
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
async def callback_download(_, callback_query):
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
    log.info("Bot starting...")
    app.run()
