# handlers/youtube.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.ads import show_ad
import yt_dlp

keyboard = [["🎧 MP3 (audio)", "🎬 MP4 (video)"]]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

async def youtube_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📥 Send like this:\n`/youtube https://youtu.be/xyz`",
            parse_mode="Markdown"
        )
        return

    url = context.args[0]
    context.user_data["yt_url"] = url
    await update.message.reply_text("Choose format to get download link:", reply_markup=markup)

async def handle_plain_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "youtube.com" in text or "youtu.be" in text:
        context.user_data["yt_url"] = text
        await update.message.reply_text("Choose format to get download link:", reply_markup=markup)

def get_youtube_direct_url(url: str, audio_only=False) -> str:
    import re

    # Clean up the URL
    if "&" in url:
        url = re.sub(r"&.*", "", url)

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "user_agent": "Mozilla/5.0",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])

        # Sort formats by resolution / quality
        formats = sorted(formats, key=lambda f: f.get("height", 0), reverse=True)

        for f in formats:
            has_video = f.get("vcodec") != "none"
            has_audio = f.get("acodec") != "none"
            if audio_only:
                if not has_video and has_audio and f.get("url"):
                    return f["url"]
            else:
                if has_video and has_audio and f.get("url"):
                    return f["url"]

    raise Exception("No valid stream found")



async def format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    url = context.user_data.get("yt_url")

    if not url:
        await update.message.reply_text("❌ No video URL found. Use /youtube or send the link again.")
        return

    await update.message.reply_text("⏳ Fetching download link...")

    try:
        direct_url = get_youtube_direct_url(url, audio_only=("MP3" in choice))
        await update.message.reply_text(f"Here is your download link:\n{direct_url}")

        # Optional ad message
        await show_ad(update)

    except Exception as e:
        await update.message.reply_text(f"❌ Failed to get download link: {e}")
