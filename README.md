# Heihachi
A discord bot to receive Tekken 8 frame data primary from [wavu.wiki](https://wavu.wiki/t/Wavu:Tekken_8)

## Instruction

Clone this to a linux server that has Python 3.10.0+ and install the dependencies with:
```py
pip install -r requirements.txt
```

You need your own discord bot ([instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)) and have the tokens in the `src/resources/config.json`. You can add a feedback channel there also.


The executable is `src/main.py`.

## Commands
```
Slash Command
/fd <character> <move>       -    get frame data of a move from a character

```