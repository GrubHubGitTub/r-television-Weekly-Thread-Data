# r/ television Weekly Thread Comment Analyzer

## Tool to fetch all comments from this week's r/television recommendation thread.

showfetch.py uses the free tvmaze API to collect all TV shows and save in a JSON.

commentcheck.py collects all comments from the previous week's discussion thread using Reddit PRAW. All shows are then checked to see if they are in these comments. If you want to run this you need to put in your own Reddit dev tool secrets. 

A couple things to note: 
1. It's hard to accurately count common word TV shows- See, You, Dark, etc. I am currently ignoring all shows with 3 or less characters as it is too hard to tell if they are actually being mentioned or just part of another sentence/word. 
2. I have to add custom search for those shows that are talked about a lot but not formatted properly (ex: officially the show is The Sandman, but most people on Reddit refer to it as Sandman, causing there to be no match unless clarified in a new check). New checks are added every week if I notice something in the previous weeks thread, or if someone brings it to my attention that the data may be off.