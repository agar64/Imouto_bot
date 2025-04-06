import os
import random
import time
import datetime
import re
import sys

import numpy as np

import telebot

from tag_manager import add_user, get_users, remove_user

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    if(message.chat.type == "private"):
        bot.reply_to(message, f"Hello, {message.from_user.first_name} {message.from_user.last_name}!")
        print("I think this is a private chat!")
    else:
        bot.reply_to(message, f"Hello, {message.chat.title}!")
        print("I think this is a group chat!")
    print(f"I detect this as a {message.chat.type} chat")

    #start_conversation(message.chat.id)


# ==== /s/ command ====

def apply_sub(message, substitution):
    """
    Apply a substitution to a message, where the substitution is formatted as:
    /s/‹from›/‹to›/

    Args:
        message (str): The original message to modify
        substitution (str): The substitution pattern

    Returns:
        str: The modified message
    """
    # Parse the substitution string
    pattern = r'^/s/(.+?)/([^/]*)$'
    match = re.match(pattern, substitution)

    if not match:
        raise ValueError("Invalid substitution format. Expected format: /s/‹from›/‹to›/")

    from_text = match.group(1)
    to_text = match.group(2)

    # Apply the substitution
    result = re.sub(from_text, to_text, message)
    return result


@bot.message_handler(func=lambda message: message.text.startswith('/s/'))
def sub_handler(message):
    if message.reply_to_message and message.reply_to_message.text:
        try:
            answ = apply_sub(message.reply_to_message.text, message.text)
            bot.reply_to(message.reply_to_message, f"<b>Did you mean:</b>\n\"{answ}\"", parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, "Something went wrong while replying.")
            print(f"Reply error: {e}")
    else:
        bot.reply_to(message, "Você precisa estar respondendo a uma mensagem com texto!")


# ==== Roll command ====

@bot.message_handler(commands=['roll'])
def roll_handler(message):
    parsed = message.text.replace("/roll ", "")

    match = re.fullmatch(r'(\d+)?d(\d+)', parsed) or re.fullmatch(r'd?(\d+)', parsed)

    if not match:
        bot.reply_to(message, "Mensagem mal formatada!")
        return

    if len(match.groups()) == 2:
        count = int(match.group(1)) if match.group(1) else 1
        dice_range = int(match.group(2))
        # bot.reply_to(message, f"count = {count}, range = {dice_range}")
    else:
        count = 1
        dice_range = int(match.group(2))
        # bot.reply_to(message, f"count = {count}, range = {dice_range}")

    if dice_range < 2:
        bot.reply_to(message, "The range of consent is 2.")
        return

    if count > 1000 or dice_range > 1000:
        bot.reply_to(message, "The maximum range and count are 1000.")
        return

    rolls = [str(random.randint(1, dice_range)) for _ in range(count)]
    result_text = f"<b>{count}d{dice_range}</b>\n" + " ".join(rolls)

    bot.reply_to(message, result_text, parse_mode="HTML")

# === @everyone ===

def everyone_func(message):
    usernames = get_users(message.chat.id)

    if not usernames:
        return "Nobody was added to the list yet. Use /add to join"

    mentions = ' '.join(f"@{u}" for u in usernames)
    return mentions
@bot.message_handler(commands=['add'])
def add_handler(message):
    username = message.from_user.username
    if not username:
        bot.reply_to(message, "Meep, you need a public @username to be added")
        return

    added = add_user(message.chat.id, username)
    if added:
        bot.reply_to(message, f"@{username} was added to the list! Nipah~~")
    else:
        bot.reply_to(message, f"@{username} is already on the list or couldn't be added. Meep")


@bot.message_handler(commands=['remove'])
def remove_handler(message):
    username = message.from_user.username
    chat_id = message.chat.id

    if remove_user(chat_id, username):
        bot.reply_to(message, f"Removed @{username} from the tag list")
    else:
        bot.reply_to(message, f"@{username} was not in the tag list")


@bot.message_handler(commands=['listEveryone'])
def list_handler(message):
    chat_id = message.chat.id
    usernames = get_users(chat_id)
    reply_text = ' '.join(f"{u}" for u in usernames)
    bot.reply_to(message, reply_text)

@bot.message_handler(commands=['everyone', 'e1'])
def everyone_handler(message):
    reply_text = everyone_func(message)
    bot.reply_to(message, reply_text)

@bot.message_handler(func=lambda message: message.text and re.search(r"(!)e1", message.text))
def e1_handler(message):
    print("Hello!")
    reply_text = everyone_func(message)
    bot.reply_to(message, reply_text)

@bot.message_handler(commands=['help'])
def help_handler(message):
    reply_text = "/start - Starts the bot\n/s/<from>/<to> - Substitutes any <from> string to <to> in a message you're replying to" + \
        "\n/roll *n*d*m* - Rolls n amount of m-sided dice. N can be omitted to roll just 1 die" + \
        "\n/add - Adds your @tag to the Everyone command list\n/everyone or /e1 - Tags everyone added to the list with /add" + \
        "\n/remove - Removes your @tag from the Everyone command list\ngithub - Links the github for this project"
    bot.reply_to(message, reply_text, parse_mode="Markdown")

@bot.message_handler(commands=['github'])
def github_handler(message):
    reply_text = "https://github.com/agar64/Imouto_bot"
    bot.reply_to(message, reply_text)

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Polling Error: {e}")
        time.sleep(10)  # Wait a bit before retrying