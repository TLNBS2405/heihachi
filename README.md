# Heihachi

A Discord bot to receive Tekken 8 frame data primarily from [Wavu Wiki](https://wavu.wiki/t/Main_Page)

## Instructions

Clone this repository to a Linux server that has Python 3.10.0+ and install the dependencies with:

```bash
git clone git@github.com:TLNBS2405/heihachi.git
cd heihachi
python3 -m pip install -r requirements.txt
```
### Config

The Heihachi bot is configured using the `src/resources/config.json` file. A sample file is provided in `src/resources/config.sample.json`. You should copy this file to `src/resources/config.json` and fill in the required fields.

```json
{
    "DISCORD_TOKEN": "YOUR_DISCORD_TOKEN",
    "FEEDBACK_CHANNEL_ID": [feedback_channel_id],
    "ACTION_CHANNEL_ID": [action_channel_id]
}
```
You can obtain your own Discord token by creating a Discord bot ([instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)).

The `FEEDBACK_CHANNEL_ID` is the channel where the bot will send feedback messages. The bot supports the slash command `/fd feedback <message>` to allow users to provide feedback on the bot's operation or frame data, and have the bot repost it in a dedicated channel for easier tracking.

![Feedback](/assets/feedback_example.png)

The `ACTION_CHANNEL_ID` is the channel where the bot will send "actioned" messages, to indicate whether a particular piece of feedback was actioned by the server owner or not.

![Actioned](/assets/actioned_example.png)

Channel IDs can be obtained by right-clicking on a channel and selecting "Copy Channel ID" at the very bottom.

### Running the bot

The executable is `src/main.py`. Don't forget to put this project into your `PYTHONPATH`!

Execute the below command from the project's root directory -

```bash
PYTHONPATH=. python3 src/main.py
```

## Commands

The bot supports the following slash commands -

| Command | Description |
| --- | --- |
| `/fd <character> <move>` | Get frame data of a move from a character |
| `/<character> <move>` | Same as above |
| `/feedback <message>` | Send feedback to the bot owner |
