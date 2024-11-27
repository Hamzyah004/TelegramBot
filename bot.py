#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import re
import time
import asyncio

# Initialize global variable to store the current sum
current_sum = 0

# Define the pattern for matching the message
pattern = re.compile(r"CIJENA:\s*(-?\d*\.\d+|\d+)")  # matches the "CIJENA: x" pattern


# Function to handle the "/start" command
async def start(update: Update, context):
    await update.message.reply_text("Bot je aktivan! Posalji poruku oblika 'CIJENA: x', gdje je x cijeli ili decimalni broj.")


# Function to handle the "/resetuj" command
async def resetuj(update: Update, context):
    global current_sum
    current_sum = 0
    await update.message.reply_text("Suma je resetovana.")


# Function to handle incoming messages with the "CIJENA: x" pattern
async def handle_message(update: Update, context):
    global current_sum

    message_text = update.message.text
    # Try to match the "CIJENA: x" pattern
    match = pattern.search(message_text)

    if match:
        # Extract the double number from the message
        number = float(match.group(1))
        current_sum += number  # Add the number to the sum

        # Check if the sum has reached 40 or more
        if current_sum >= 40:
            await update.message.reply_text(f"Suma je dostignula minimalnu vrijednost, stanje: {current_sum:.2f}.")


# Main function to set up the bot
async def main():
    global current_sum
    # Get your bot's API token from BotFather
    token = 'YOUR_BOT_TOKEN'  # Replace with your token

    # Create the Application and pass in the bot's token
    application = Application.builder().token(token).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("resetuj", resetuj))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot and stop after 1 second
    # Running the bot asynchronously, and then shutting down after 1 second
    try:
        await asyncio.sleep(1)  # Wait for 1 second
        await application.shutdown()  # Shut down the bot after 1 second
    except asyncio.CancelledError:
        pass  # Handle the case where we want to cancel the bot

if __name__ == '__main__':
    asyncio.run(main())
