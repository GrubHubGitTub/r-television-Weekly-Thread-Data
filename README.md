# r/ television Weekly Thread Comment Analyzer

## Tool to fetch all comments from this week's r/television recommendation thread.

showfetch.py uses the free tvmaze API to collect all TV shows and save in a JSON.

commentcheck.py collects all comments from the previous week's discussion thread using Reddit PRAW. All shows are then checked to see if they are in these comments. If you want to run this you need to put in your own Reddit dev tool secrets. 

A couple things to note: 
1. It's hard to accurately count common word TV shows- See, You, Dark, etc. I am currently ignoring all shows with 3 or less characters as it is too hard to tell if they are actually being mentioned or just part of another sentence/word. I have added some regex to help with this, but the regex doesn't work properly for comments that are a list. 
2. I have to add custom search for those shows that are talked about a lot but not formatted properly (ex: Andor, Lord of the Rings, etc.). New checks are added every week if I notice something in the previous weeks thread, or if someone brings it to my attention that the data may be off.

## Run Locally

### get show list:
- run showfetch.py to create a json file with the latest tv show information- this file is named "dd-mm-yyyy-allShows.json"

### get comments:

- install praw

- install pandas  

- create a free reddit dev app here: https://www.reddit.com/prefs/apps/

#### in commentcheck.py:

- on lines 17-19 enter the client id, secret, and name of your reddit dev app to configure the PRAW comment scraper.

- enter the reddit thread 7 character string (found in every reddit URL) on line 22

#### previous week comparison

- lines 187- 199 looks for last weeks file for comparison, you will have to change the dates if looking for a file with a date that is not 6-8 days before. 

- if there is no appropriate file to compare to, you can comment out all lines from 187- 241, and the  allShows json will be saved with the current thread's data.

- lines 248-end uses pandas to spit out a filtered CSV sorted by comments and upvotes. 
