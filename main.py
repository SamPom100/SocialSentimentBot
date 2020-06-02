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

print("Accessing: " + subreddit.display_name)

print(spacer)

print("Getting hot comments from " + subreddit.display_name)
print(spacer)
masterSET = set()

for submission in subreddit.hot(limit=10):
    masterSET.add(submission.title.lower())
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        masterSET.add(comment.body.lower())

print("Done")
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
print("Function Time: " + end - start)
