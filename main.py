import praw
import secret
from praw.models import MoreComments
import time

spacer = "\n\n************************************\n\n"

reddit = praw.Reddit(client_id=secret.client_id,
                     client_secret=secret.client_secret, user_agent=secret.user_agent)

start = time.time()

print(spacer)
subreddit = reddit.subreddit("wallstreetbets")

print("Accessing: " + subreddit.display_name.upper())

print(spacer)

print("Getting current hot posts / comments from " +
      subreddit.display_name.upper())
print(spacer)
masterSET = []

for submission in subreddit.hot(limit=10):
    for sub in submission.title.lower().split(" "):
        masterSET.append(sub)
    submission.comments.replace_more(limit=10)
    for comment in submission.comments.list():
        for sub2 in comment.body.lower().split(" "):
            masterSET.append(sub2)

print("Analyzing")
print(spacer)

autistCount = sum('autist' in s for s in masterSET)
callCount = sum('call' in s for s in masterSET)
putCount = sum('put' in s for s in masterSET)

print("Autist Count: " + str(autistCount))
print("Call Count: " + str(callCount))
print("Put Count: " + str(putCount))

print(spacer)
if(callCount > putCount):
    print("BULLISH by " + str(round(100*(callCount/(callCount + putCount)), 3)))
else:
    print("BEARISH by " + str(round(100*(putCount/(callCount + putCount)), 3)))

print(spacer)
end = time.time()
print("Run time: " + str(round(end - start, 2))+" seconds")
