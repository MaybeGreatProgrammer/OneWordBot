# OneWordBot

OneWordBot is a Discord bot that allows you to ban words. Banned words are placed into BannedWords.txt. A user who says the word is given the "Ghost" role. It bans ghosts that leave the server. It's programmed to only ban people on one specific server, but if you're hosting it yourself, you can remove the full_functionality check.

# Commands

### Wordmaster only

*!bw [word] :* Bans a word or phrase
*!ubw [word] :* Unbans a word or phrase
*!takeout :* Sends the BannedWords.txt file

### Anyone

*!ping :* Replies "Pong!"
*!pong :* Replies "Ping!"

# Roles

All roles should be configured on any Discord server the bot has joined

*Ghost:* Forbidden from sending messages in any channel (this has to be configured in channel or group permissions)

*Wordmaster:*  Is allowed by the bot to run "Wordmaster only" commands. Doesn't need any special permissions.

*Exempt:* Makes the bot react with a black cross mark if the user uses a banned word instead of giving the Ghost role. Doesn't need any special permissions.
