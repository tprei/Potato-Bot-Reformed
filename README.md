# 🥔 Potato_Bot 🥔

This is a small discord bot made in Python using the `discord.py` wrapper for the Discord API.

**This project was made for a private server** so it's not a public bot that you can just add to your server, although the source code is provided here so you could host it on your own using your own bot token.

## Some cool features

### Gold channel:

If someone finds something funny/cool in a channel, they can react with a specific emoji (like) and when it reaches a minimum number of likes, that gets forwarded to another channel (highlights channel). These likes get updated in real time!

![Gold message](https://i.imgur.com/bVCUkOJ.jpg)

Original message:

![original messsage](https://i.imgur.com/JW2WBo5.jpg)

### Twitter feed:

I also managed to get the bot to have a twitter feed: a channel that communicates with the Twitter API to fetch tweets in real time from a list of followers that is managed by the server's members!

![twitter feed](https://i.imgur.com/1QQwyLb.jpg)

### ~~Not so~~ motivational images from InspiroBot

Using the InspiroBot website: inspirobot.me, the bot can generate ~~not so much~~ motivational images! This is only for a gag of course.

![motivar](https://i.imgur.com/EEwhXcW.jpg)

## Others!

- Admin commands
- Funny commands
- etc.

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

and more!

## What will I have to configure?

As I've said, this bot was made for a private server so many things might not work in other servers.

Right now, the only feature that won't work due to custom configurations is the `gold` command. To make that work, you must simply configure the `DEFAULT_GOLD_CHANNEL` variable in the *config.json* file: set its value to one of the channels' id's in your own server.
