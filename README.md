# Tickler links

I was frustrated that I never got around to re-reading a bunch of articles or notes that I saved, so I set up this script to send myself an email every morning with something to re-read. 

Examples of these emails include: 
- my quarterly development goals to keep fresh in mind
- notes from a book on programming I read a while ago
- links to good articles I found that I would like to read again

Each of these emails should be saved in the email_text folder as .txt files. This script will iterate through the emails in alphabetical order, sending one each weekday and looping when it's gone through all of them.

### Other setup

I recommend setting up a spam email address to use as the sender account, becuase (at least through Gmail) you have to relax your security settings to easily send emails programmatically. 
- See e.g. here: https://realpython.com/python-send-email/ 

You'll need to set up a cron trigger to run this script once per weekday. 