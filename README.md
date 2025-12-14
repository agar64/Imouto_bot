# Imouto Bot

Imouto Bot is a playful Telegram bot built with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). It mixes useful utilities with fun chat interactions, including dice rolls, substitution replies, group tagging, ASCII shouts, and meme responses.

## Getting started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Provide your bot token**
   Set the `BOT_TOKEN` environment variable before running the bot.
   ```bash
   export BOT_TOKEN="<your-telegram-bot-token>"
   ```
3. **Run the bot**
   ```bash
   python main.py
   ```

## Reliability helpers

Network hiccups can drop Telegram connections. Both `safe_send_message` and `safe_reply` wrap message sending in retry loops, logging failures and backing off briefly before retrying. This keeps commands responsive even when Telegram temporarily throttles or disconnects.【F:main.py†L20-L39】

## Commands and behaviors

### Greetings
- `/start`, `/hello`: Send a greeting tailored to the chat type (private vs group).【F:main.py†L41-L49】

### Substitution `/s/`
- Usage: reply to a message with `/s/<from>/<to>/` to replace `<from>` with `<to>` in the replied text or caption. Invalid formats are rejected with a helpful error.【F:main.py†L54-L136】

### Dice rolls `/roll`
- Usage: `/roll NdM` (e.g., `/roll 2d6`) or `/roll d20`.
- Validates format, enforces limits (max 1000 dice and faces), and sums the random rolls in a bold HTML response.【F:main.py†L138-L175】

### Everyone tagging
- Commands: `/add`, `/remove`, `/listEveryone`, `/everyone` (alias `/e1`).
- Users with public `@username`s can opt in via `/add`; `/remove` unregisters them. `/listEveryone` shows the stored handles, and `/everyone` mentions every stored user in the chat. A fallback `/e1` trigger also responds to messages containing `!e1`. Usernames are persisted per-chat in `everyone_tags.json` through the helper functions in `tag_manager.py`.【F:main.py†L176-L228】【F:tag_manager.py†L4-L42】

### Shout formatting `/shout`
- Transforms input text into an ASCII block layout. Accepts inline text (`/shout hello`) or replies to another message; rejects empty input and overly long text (>25 characters). Renders with HTML `<pre><b>` to preserve spacing.【F:main.py†L230-L268】

### Slap responses `/slap`
- Produces a random playful “slap” or “death” message, targeting either provided text, the replied user, or the sender themself when no target is given.【F:main.py†L270-L287】

### Help and metadata
- `/help`: Summarizes commands with Markdown formatting and disables link previews.【F:main.py†L289-L297】
- `/github`: Shares the project repository link.【F:main.py†L299-L302】

### Keyword easter eggs
- Any text ending with “crazy” (or Portuguese equivalents) receives “frog”/“sapo” replies via the fallback text handler.【F:main.py†L304-L312】

## Data storage

- The per-chat user list for the `/everyone` feature lives in `everyone_tags.json`. If the file does not exist, it is created automatically when the first user is added.【F:tag_manager.py†L4-L42】

## Running considerations

- The bot uses long polling (`infinity_polling`) inside a retry loop to recover from polling errors after a short delay.【F:main.py†L314-L319】
- Because Telegram bots cannot see messages from other bots, some reply-based commands may not work when replying to another bot user (notably `/slap`).【F:main.py†L289-L297】

Enjoy experimenting with Imouto Bot’s utility commands and playful interactions!
