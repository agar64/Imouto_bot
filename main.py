import os
import random
import time
import datetime
import re
import sys
import requests
from telebot.apihelper import ApiTelegramException

import numpy as np

import telebot

from tag_manager import add_user, get_users, remove_user

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# === Fix Disconnections BS ===
def safe_send_message(chat_id, text, retries=3, delay=2, parse_mode=None, disable_web_page_preview=False):
    for attempt in range(retries):
        try:
            return bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        except (requests.exceptions.RequestException, ApiTelegramException) as e:
            print(f"[safe_send_message] Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    print("[safe_send_message] All retries failed.")
    return None

def safe_reply(chat_id, text, retries=3, delay=2, parse_mode=None, disable_web_page_preview=False):
    for attempt in range(retries):
        try:
            return bot.reply_to(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        except (requests.exceptions.RequestException, ApiTelegramException) as e:
            print(f"[safe_send_message] Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    print("[safe_send_message] All retries failed.")
    return None

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    if(message.chat.type == "private"):
        safe_reply(message, f"Hello, {message.from_user.first_name} {message.from_user.last_name}!")
        print("I think this is a private chat!")
    else:
        safe_reply(message, f"Hello, {message.chat.title}!")
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


def slap_msg(adversary, sender):
    msg_repo = [f"{adversary} got his butt slapped by {sender}!", f"{adversary} got sent to the Shadow Realm!",
                f"{adversary} is sleeping with the fishies!", f"{adversary} clawed their throat out!",
                f"{adversary} got cursed by Oyashiro-sama!", f"{adversary} was demoned-away!",
                f"{adversary} was decapitated by {sender}!", f"{adversary}'s ancestors aren't smiling at him!",
                f"{adversary} drowned!", f"{adversary} fell into lava!", f"{adversary} got fired!", f"{adversary} died!",
                f"{adversary} got mauled by a bear!", f"{adversary} died of ligma!", f"{adversary} died of sugma!",
                f"{adversary}'s mom was ground-pounded by {sender}!", f"{adversary} fell out of the world!",
                f"{adversary} got his neck snapped by a Bracken!", f"{adversary} was blown into bits by {sender}!",
                f"{adversary} was shot by {sender}!", f"{adversary} got eaten by {sender}!",
                f"Poor, poor {adversary}! Nipah~~", f"{adversary} met the ground at 200km/h!",
                f"{adversary} got stabbed by {sender} in a dark alley!", f"{adversary} met Jesus!", f"{adversary} is alive and well",
                f"{adversary} was lit on fire by {sender}!", f"No one watched {adversary}'s stream!", f"{adversary} got demonetized!",
                f"{adversary}'s existence was replaced by {sender}!", f"Who's {adversary}?", f"{adversary} got arrested!",
                f"{adversary} received the Sonichu Medallion!", f"{adversary} became an AI-generated image!",
                f"{adversary} got rejected from art school!", f"{adversary} was the Impostor!",
                f"{adversary} is being gaslit by {sender}!", f"{adversary} was shat on by a bird!",
                f"{adversary} stepped on a landmine!", f"{adversary} experienced domestic violence in the hands of {sender}!",
                f"{adversary} was charred to ashes!", f"{adversary} reincarnated into a barnacle!",
                f"{adversary}'s pizza arrived cold!", f"{adversary} ate small bombs!",
                f"{adversary} thought he could outrun {sender}!", f"{adversary} got ran over by an ambulance!",
                f"{adversary} forgot to breathe!", f"{adversary} went cave-diving!", f"{adversary} got stuck in Nutty Putty Cave!",
                f"{adversary} got killed by a butterfly!", f"{adversary} ate {sender}'s fists!", f"{adversary} fell into a sinkhole!",
                f"{adversary} choked on saliva!", f"Everyone forgot {adversary}'s birthday!", f"{adversary} was set up by {sender}!"]
    reply_text = msg_repo[random.randint(0, len(msg_repo)-1)]
    #print(len(msg_repo)-1)
    return reply_text

# Note: Not in use
def slap_msg_mistake(sender):
    msg_repo = [f"{sender} is too stupid to use a command correctly!", f"{sender} can't read!",
                f"{sender} should go back to kindergarten!", f"{sender} can't type!"]
    reply_text = msg_repo[random.randint(0, len(msg_repo) - 1)]
    return reply_text

@bot.message_handler(func=lambda message: message.text.startswith('/s/'))
def sub_handler(message):
    if message.reply_to_message and message.reply_to_message.text:
        try:
            answ = apply_sub(message.reply_to_message.text, message.text)
            safe_reply(message.reply_to_message, f"<b>Did you mean:</b>\n\"{answ}\"", parse_mode="HTML")
        except Exception as e:
            safe_reply(message, "Something went wrong while replying.")
            print(f"Reply error: {e}")
    elif message.reply_to_message and message.reply_to_message.caption:
        try:
            answ = apply_sub(message.reply_to_message.caption, message.text)
            safe_reply(message.reply_to_message, f"<b>Did you mean:</b>\n\"{answ}\"", parse_mode="HTML")
        except Exception as e:
            safe_reply(message, "Something went wrong while replying.")
            print(f"Reply error: {e}")
    else:
        safe_reply(message, "You need to be replying to a text message!")


# ==== Roll command ====

@bot.message_handler(commands=['roll'])
def roll_handler(message):
    parsed = message.text.replace("/roll ", "")

    match = re.fullmatch(r'(\d+)?d(\d+)', parsed) or re.fullmatch(r'd?(\d+)', parsed)

    if not match:
        safe_reply(message, "Badly-Formated Message!")
        return

    if len(match.groups()) == 2:
        count = int(match.group(1)) if match.group(1) else 1
        dice_range = int(match.group(2))
        # safe_reply(message, f"count = {count}, range = {dice_range}")
    else:
        count = 1
        if (match.group(0) == match.group(1)):
            safe_reply(message, "You forgot the d!")
            return
        dice_range = int(match.group(2))
        # safe_reply(message, f"count = {count}, range = {dice_range}")

    if dice_range < 2:
        safe_reply(message, "The range of consent is 2.")
        return

    if count > 1000 or dice_range > 1000:
        safe_reply(message, "The maximum range and count are 1000.")
        return

    rolls = [str(random.randint(1, dice_range)) for _ in range(count)]
    rolls_sum = sum([int(x) for x in rolls])
    result_text = f"<b>{count}d{dice_range}</b>\n" + " ".join(rolls) + f"\n<b>SUM =</b> {rolls_sum}"

    safe_reply(message, result_text, parse_mode="HTML")

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
        safe_reply(message, "Meep, you need a public @username to be added")
        return

    added = add_user(message.chat.id, username)
    if added:
        safe_reply(message, f"@{username} was added to the list! Nipah~~")
    else:
        safe_reply(message, f"@{username} is already on the list or couldn't be added. Meep")


@bot.message_handler(commands=['remove'])
def remove_handler(message):
    username = message.from_user.username
    chat_id = message.chat.id

    if remove_user(chat_id, username):
        safe_reply(message, f"Removed @{username} from the tag list")
    else:
        safe_reply(message, f"@{username} was not in the tag list")


@bot.message_handler(commands=['listEveryone'])
def list_handler(message):
    chat_id = message.chat.id
    usernames = get_users(chat_id)
    reply_text = ' '.join(f"{u}" for u in usernames)
    safe_reply(message, reply_text)

@bot.message_handler(commands=['everyone', 'e1'])
def everyone_handler(message):
    reply_text = everyone_func(message)
    safe_reply(message, reply_text)

@bot.message_handler(func=lambda message: message.text and re.search(r"(!)e1", message.text))
def e1_handler(message):
    print("Hello!")
    reply_text = everyone_func(message)
    safe_reply(message, reply_text)

@bot.message_handler(func=lambda message: message.text and message.text.endswith(("crazy", "crazy.", "crazy!", "crazy...", \
                                                                                  "crazy?", "doido", "louco", "doido.", \
                                                                                  "doido!", "louco.", "louco!")))
def crazy_handler(message):
    #print("Hello!")
    if message.text.endswith(("crazy", "crazy.", "crazy!", "crazy...", "crazy?")):
        reply_text = "frog"
    elif message.text.endswith(("doido", "louco", "doido.", "doido!", "louco.", "louco!")):
        reply_text = "sapo"
    safe_send_message(message, reply_text)


def shout_func(parsed):
    reply_temp = ' '.join(f"{c.upper()}" for c in parsed) + "\n"
    msg_size = len(parsed)
    '''for char in parsed:
        reply_text = reply_text + char.upper().join(" " for c in parsed) + "\n"
        '''
    reply_text = reply_temp
    for char in range(msg_size):
        if char != 0:
            reply_text = reply_text + parsed[char].upper() #+ ''.join(" " for c in parsed) + "\n"
            for c in range(len(parsed)):
                if c == char:
                    reply_text = reply_text + parsed[char].upper()
                elif c == 0:
                    reply_text = reply_text + " "
                else:
                    reply_text = reply_text + "  "
            reply_text = reply_text + "\n"
    return f"<pre><b>{reply_text}</b></pre>"

@bot.message_handler(commands=['shout'])
def shout_handler(message):
    parsed = message.text.replace("/shout ", "")
    parsed = parsed.replace("/shout", "")
    msg_size = len(parsed)

    if msg_size > 25:
        reply_text = "Meep. That's too much for me"
    elif msg_size <= 0:
        if message.reply_to_message and message.reply_to_message.text:
            parsed = message.reply_to_message.text
            reply_text = f"{shout_func(parsed)}"
            print("<= 0")
        else:
            reply_text = "Meep. You need to type something or reply to someone"
    else:
        reply_text = f"{shout_func(parsed)}"
        print(f"msg_size = {msg_size}; msg = {parsed}")
    safe_send_message(message.chat.id, f"{reply_text}", parse_mode="HTML")


@bot.message_handler(commands=['slap'])
def slap_handler(message):
    parsed = message.text.replace("/slap ", "")
    parsed = parsed.replace("/slap", "")
    sender = message.from_user.first_name
    if ((len(parsed) <=0) and (message.reply_to_message is not None) and (message.reply_to_message.from_user.first_name is not None)):
        adversary = message.reply_to_message.from_user.first_name
    elif(len(parsed) <=0):
        adversary = sender
        sender = "himself"
    else:
        adversary = parsed

    reply_text = slap_msg(adversary, sender)

    safe_send_message(message.chat.id, reply_text)


@bot.message_handler(commands=['help'])
def help_handler(message):
    reply_text = "/start - Starts the bot\n[/s/](https://youtu.be/cErgMJSgpv0)<from>/<to> - Substitutes any <from> string to <to> in a message you're replying to" + \
        "\n/roll *n*d*m* - Rolls n amount of m-sided dice. N can be omitted to roll just 1 die" + \
        "\n/add - Adds your [@tag](https://youtu.be/cErgMJSgpv0) to the Everyone command list\n/everyone or /e1 - Tags everyone added to the list with /add" + \
        "\n/remove - Removes your [@tag](https://youtu.be/cErgMJSgpv0) from the Everyone command list\n/github - Links the github for this project" + \
        "\n/shout - Echoes a typed or replied to message in a certain pattern\n/slap *n* or /slap *while replying to someone*" + \
        " - Gives a kill message about *n* or whoever you're replying to (unless it's another bot since bots can't see eachother)"
    safe_reply(message, reply_text, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['github'])
def github_handler(message):
    reply_text = "https://github.com/agar64/Imouto_bot"
    safe_reply(message, reply_text)

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Polling Error: {e}")
        time.sleep(10)  # Wait a bit before retrying