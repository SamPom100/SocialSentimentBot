from collections import Counter
import praw
import secret
from praw.models import MoreComments
from get_all_tickers import get_tickers as gt
import time
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb

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

commentCounter = 0

for submission in subreddit.hot(limit=30):
    for sub in submission.title.upper().split(" "):
        masterSET.append(sub)
        commentCounter += 1
    submission.comments.replace_more(limit=30)
    for comment in submission.comments.list():
        for sub2 in comment.body.upper().split(" "):
            masterSET.append(sub2)
            commentCounter += 1


print("Analyzing")
print(spacer)

autistCount = sum('AUTIST' in s for s in masterSET)
callCount = sum('CALL' in s for s in masterSET)
putCount = sum('PUT' in s for s in masterSET)

print("Autist Count: " + str(autistCount))
print("Call Count: " + str(callCount))
print("Put Count: " + str(putCount))
print("Total Comments Analyzed: "+str(commentCounter))

sentiment = "WSB is "
print(spacer)
if(callCount > putCount):
    sentiment += "BULLISH by " + \
        str(round(100*(callCount/(callCount + putCount)), 1)) + "%"
else:
    sentiment += "BEARISH by " + \
        str(round(100*(putCount/(callCount + putCount)), 1)) + "%"

print(sentiment)


slices = [callCount, putCount]
names = ['Calls', 'Puts']
colors = ['springgreen', 'lightcoral']
plt.figure(0)
plt.pie(slices, labels=names, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontsize': 17, 'weight': 'bold'})
plt.title('Calls or Puts')


print(spacer)

list_of_tickers = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)

tickerList = []

r_item = ['A', 'ON', 'IT', 'FOR', 'AT', 'ARE', 'BE', 'ALL', 'SO',
          'GO', 'OR', 'CAN', 'HE', 'NOW', 'OUT', 'AN', 'HAS', 'BY', 'ONE',
          'SEE', 'GOOD', 'BIG', 'ANY', 'NEW', 'AM', 'NEXT', 'WELL', 'PUMP', 'EVER',
          'RUN', 'VERY', 'PLAY', 'DD', 'POST', 'ELSE', 'LOVE', 'TELL', 'BEST', 'LIFE',
          'HOPE', 'TWO', 'NICE', 'BIT', 'MAN', 'TRUE', 'FUN', 'LOW', 'TECH', 'CAR', 'STAY',
          'EOD', 'JOB', 'FLAT', 'OLD', 'RTX', 'HOME', 'OW', 'JOE', 'BEAT', 'WOW', 'X', 'ATH',
          'SAVE', 'EAT', 'HUGE', 'PER', 'LIVE', 'CARE', 'RIOT', 'PEAK', 'TURN', 'PLUS', 'HEAR']


main_list = [
    item for item in masterSET if item in list_of_tickers if item not in r_item]

Counter = Counter(main_list)
most_occur = Counter.most_common(12)
mainFrame = pd.DataFrame(most_occur)
mainFrame.columns = ['Ticker', 'Frequency']

#temp = mainFrame.plot(kind='bar', x='Ticker', y='Frequency')

plt.figure(1)
ax = sb.barplot(x='Ticker', y='Frequency', data=mainFrame)
plt.title("What's on WallStreetBet's mind today")
plt.annotate('--------- Summary ---------\n'+sentiment + '\nCalls: '+str(callCount)+'\nPuts: '+str(putCount)+'\nAutist Count: ' +
             str(autistCount)+'\nAnalyzed '+str(commentCounter)+' comments', xy=(9, 60))

print(spacer)


end = time.time()
print("Run time: " + str(round(end - start, 2))+" seconds")

plt.show()
