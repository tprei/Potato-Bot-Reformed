# TODO

## Easy
**DONE** - Gold Class Cog
**DONE** - "gold emoji" will change the default emoji
**DONE** golds do not affect gold channel

## Medium
**DONE** - config.py as a JSON loader so that global variables can be configured
**DONE** - Admin Class (clear, clearcm)
**DONE** - Cog that supports live configuration changing by the owner, plus pretty printing each global variable

## Hard
- "gold stats" will get stats for the users with the most golded messages
    - This needs a database for users, gold count (received and sent)
    - This database must support both periodic "dump" (update each minute using some kind of cache) and also when stats command is called.

- "gold" will get a random message from the gold channel
    - Must have database implemented so I can randomly fetch some embed message id, that's because working with histories can be quite slow.

- Logging system (study discord.py)
    - Maybe different log for messages, commands, errors?

- HelpCommand Class (study discord.py)
    - Pagination is probably overkill.

- Some kind of tourney for the infamous mitadas e lagadas
    - Mostly hard because haven't thought much how to do it.
