# r/ television Weekly Thread Comment Analyzer

## Simple tool to fetch all comments from this week's r/television recommendation thread.

showfetch.py uses the free tvmaze API to collect all TV shows and save in a JSON. In the future I only need to fetch the newest shows and append to this JSON.

index.py collects all comments from the thread using Reddit PRAW. All shows are then checked to see if they are in these comments. If you want to run this you need to put in your own Reddit dev tool secrets. 

A couple problems right now: 
1. impossible to count common word TV shows- See, You, Dark, etc. 
2. I have to add custom search for those shows that are talked about a lot but not formatted properly (ex: officially the show is The Sandman, but most people on Reddit refer to it as Sandman, causing there to be no match unless clarified in a new check).