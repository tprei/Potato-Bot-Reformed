```
▄▄▄·     ▄▄▄▄▄ ▄▄▄·▄▄▄▄▄          ▄▄▄▄·      ▄▄▄▄▄
█ ▄█▪    •██  ▐█ ▀█•██  ▪         ▐█ ▀█▪▪    •██
██▀· ▄█▀▄ ▐█.▪▄█▀▀█ ▐█.▪ ▄█▀▄     ▐█▀▀█▄ ▄█▀▄ ▐█.
█▪·•▐█▌.▐▌▐█▌·▐█ ▪▐▌▐█▌·▐█▌.▐▌    ██▄▪▐█▐█▌.▐▌▐█▌·
▀    ▀█▄▀▪▀▀▀  ▀  ▀ ▀▀▀  ▀█▄▀▪    ·▀▀▀▀  ▀█▄▀▪▀▀▀
```

This is a small discord bot made in Python using the `discord.py` wrapper for the Discord API.

This project was made for a private server so it's not a public bot that you can just add to your server, although the source code is provided here so you could host it on your own using your own bot token.

## How to run it?

First of all, many things that were developed here were developed solely for a few people's use, this means some things were configured to run in a specific environment and you will have to re-configure them in order for things to work.

That being said, here's what you must do.

First you must have all dependencies (**it's heavily recommended that you do this inside a virtual enviroment**).

You can install them with pip:

`pip install -r requirements.txt`

Now you have to setup the enviroment variable for the bot auth token.

In Linux and MacOS that will be (if you use .bashrc for your shell configs):

`echo export DISCORD_TOKEN=<your_token_here> >> .bashrc`

Now to run the bot, you just have to do:

`python run.py`

## Some features

- gold: Forwards messages that have a minimum number of reactions to a "gold" channel.
- boralol: DM's your friends to get their attention
- clear: Clears chat
- clearcm: Clears chat's commands
- motivar: Sends a funny motivational picture

## What will I have to configure?

As I've said, this bot was made for a private server so some things might not work in other servers.

Right now, the only feature that won't work due to custom configurations is the `gold` command. To make that work, you must simply configure the `DEFAULT_GOLD_CHANNEL` variable in the *config.json* file: set its value to one of the channels' id's in your own server.
