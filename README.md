#programming_stat_bot

This is a simple bot used to parse through submissions to the subreddit /r/programming using python and the praw package. programming_stat_bot parses through the title text of each submission and checks whether a particular language is mentioned. The bot then sorts the submissions for each language and lists the top ten submissions based on number of upvotes for the top five most mentioned languages.

To see the listing of submissions, check out the comment section for programming_stat_bot submissions.

Feel free to make any suggestions or additions for programming_stat_bot either on github or personal message the bot on reddit.

## Features:

* **supports 250+ languages**:

    check out the language.txt file to see supported languages

* **replies to comments**:

    language you are curious about didn't make the list? Ask programming stat bot to retrieve the language for you. All you need to do is make a comment to programming_stat_bot's original submission in the following format:

`programming_stat_bot:language`

for example:

`programming_stat_bot:python`
will reply with the top ten submissions for python.
