import praw
import secret
from praw.models import MoreComments
import time

spacer = "\n\n************************************\n\n"

reddit = praw.Reddit(client_id=secret.client_id,
                     client_secret=secret.client_secret, user_agent=secret.user_agent)

start = time.time()


# assume you have a Reddit instance bound to variable `reddit`
print(spacer)
subreddit = reddit.subreddit("wallstreetbets")

print("Accessing: " + subreddit.display_name)
# print(subreddit.description)

print(spacer)


print("Getting hot comments from " + subreddit.display_name)
print(spacer)
masterSET = set()

for submission in subreddit.hot(limit=10):
    # Output: the submission's title
    masterSET.add(submission.title.lower())
    submission.comments.replace_more(limit=10)
    for comment in submission.comments.list():
        masterSET.add(comment.body.lower())

print("Done")

print(spacer)

autistCount = sum('autist' in s for s in masterSET)
callCount = sum('call' in s for s in masterSET)
putCount = sum('put' in s for s in masterSET)
print("Autist Count" + str(autistCount))
print("Call Count" + str(callCount))
print("Put Count" + str(putCount))

print(spacer)
if(callCount > putCount):
    print("BULLISH by " + str(callCount / (callCount+putCount))+"%")
else:
    print("BEARISH by " + str(putCount / (callCount+putCount))+"%")
# print(submission.score)  # Output: the submission's score
# print(submission.id)     # Output: the submission's ID
# print(submission.url)    # Output: the URL the submission points to
# or the submission's URL if it's a self post

end = time.time()
print(end - start)
