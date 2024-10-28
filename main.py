import os
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_TOKEN: Final = os.getenv('TELEGRAM_API_TOKEN')
USERNAME: Final = '@snipher_bot'

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Snipher, your friendly bot. How can I assist you today?')

# HELP COMMAND
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are some commands to get you started:\n"
        "/start - Greet the bot\n"
        "/help - Get help on how to use the bot\n"
        "/custom - Run a custom command\n"
        "/about - Learn more about the bot\n"
        "/feedback - Provide feedback\n"
        "/stop - Stop the bot interaction\n"
    )
    await update.message.reply_text(help_text)

# ABOUT COMMAND
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Snipher, a bot created to assist you with various tasks!")

# FEEDBACK COMMAND
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We value your feedback! Please type your feedback and I'll record it.")

# STOP COMMAND
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thank you for using Snipher! Goodbye!")
    # Optionally stop the bot interaction or remove the user session here

# CUSTOM COMMAND
async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command! Feel free to add more commands to suit your needs.")

# Response handling
def handle_response(text: str) -> str:
    processed_text: str = text.lower()
    if 'hello' in processed_text:
        return 'Hello! Welcome to Snipher. How can I assist you?'
    elif 'thank you' in processed_text or 'thanks' in processed_text:
        return "You're very welcome!"
    elif 'how are you' in processed_text:
        return "I'm just a bot, but I'm here to help!"
    else:
        return "I'm not sure how to respond to that. Try asking for help with /help."

# MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {msg_type}: "{text}"')

    if msg_type == 'group':
        if USERNAME in text:
            new_text: str = text.replace(USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# ERROR HANDLING
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused an error {context.error}')
    await update.message.reply_text("An error occurred. Please try again later.")

# MAIN FUNCTION TO START BOT
if __name__ == '__main__':
    print('Bot is starting...')
    app = Application.builder().token(API_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about))
    app.add_handler(CommandHandler('feedback', feedback))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('custom', custom))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error Handler
    app.add_error_handler(error)

    # Polling
    print('Polling...')
    app.run_polling(poll_interval=3)
