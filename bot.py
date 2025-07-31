# bot.py
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.youtube import youtube_handler, format_choice, handle_plain_link

# Replace this with your real Telegram bot token
BOT_TOKEN = "7768190495:AAFU_wJ5gRVYG5bRTHCJVN7BWJHB4h8T4pI"

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update, context):
    await update.message.reply_text(
        "👋 Welcome to BijanoBot!\n\nSend me a YouTube link or use /youtube <link> to get MP3 or MP4 download options."
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("youtube", youtube_handler))
    app.add_handler(MessageHandler(filters.Regex("^(🎧 MP3.*|🎬 MP4.*)$"), format_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_plain_link))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
