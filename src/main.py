from datetime import datetime
from datetime import date
from collections import Counter
import praw
import secret
from praw.models import MoreComments
import time
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from stocklist import NasdaqController
import os
from tqdm import tqdm
import time
import sys


def main():
    spacer = "\n\n************************************\n\n"

    reddit = praw.Reddit(client_id=secret.client_id,
                         client_secret=secret.client_secret, user_agent=secret.user_agent)

    start = time.time()

    print(spacer)
    subreddit = reddit.subreddit("wallstreetbets")

    print("Accessing: " + subreddit.display_name.upper())
    print("Getting posts / comments from " +
          subreddit.display_name.upper())
    print(spacer)
    masterSET = []

    commentCounter = 0
    toolbar_width = 30
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    # return to start of line, after '['
    sys.stdout.write("\b" * (toolbar_width+1))

    for submission in subreddit.hot(limit=25):  # .hot, .new
        for sub in submission.title.upper().split(" "):
            masterSET.append(sub)
            commentCounter += 1
        submission.comments.replace_more(limit=25)
        for comment in submission.comments.list():
            for sub2 in comment.body.upper().split(" "):
                masterSET.append(sub2)
                commentCounter += 1
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")  # this ends the progress bar
    print("Analyzing")
    print(spacer)

    callCount = sum('CALL' in s for s in masterSET)
    putCount = sum('PUT' in s for s in masterSET)

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

    """
    slices = [callCount, putCount]
    names = ['Calls', 'Puts']
    colors = ['springgreen', 'lightcoral']
    plt.figure(0)
    plt.pie(slices, labels=names, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 17, 'weight': 'bold'})
    plt.title('Calls vs. Puts')
    """

    print(spacer)

    # get all stock tickers
    # from get_all_tickers import get_tickers as gt
    # list_of_tickers = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)

    StocksController = NasdaqController(True)
    list_of_tickers = StocksController.getList()

    tickerList = []

    r_item = ['A', 'ON', 'IT', 'FOR', 'AT', 'ARE', 'BE', 'ALL', 'SO',
              'GO', 'OR', 'CAN', 'HE', 'NOW', 'OUT', 'AN', 'HAS', 'BY', 'ONE',
              'SEE', 'GOOD', 'BIG', 'ANY', 'NEW', 'AM', 'NEXT', 'WELL', 'PUMP', 'EVER',
              'RUN', 'VERY', 'PLAY', 'DD', 'POST', 'ELSE', 'LOVE', 'TELL', 'BEST', 'LIFE',
              'HOPE', 'TWO', 'NICE', 'BIT', 'MAN', 'TRUE', 'FUN', 'LOW', 'TECH', 'CAR', 'STAY',
              'EOD', 'JOB', 'FLAT', 'OLD', 'RTX', 'HOME', 'OW', 'JOE', 'BEAT', 'WOW', 'X', 'ATH',
              'SAVE', 'EAT', 'HUGE', 'PER', 'LIVE', 'CARE', 'PEAK', 'TURN', 'PLUS', 'HEAR', 'GAIN', 'BRO', 'RH', 'JUST', 'NEED', 'KNOW']

    main_list = [
        item for item in masterSET if item in list_of_tickers if item not in r_item]

    most_occur = Counter(main_list).most_common(12)
    mainFrame = pd.DataFrame(most_occur)
    mainFrame.columns = ['Ticker', 'Frequency']

    # temp = mainFrame.plot(kind='bar', x='Ticker', y='Frequency')
    plt.figure(figsize=(15, 7))
    dateformat = date.today().strftime("%B %d, %Y")
    # dateformat = "July 24, 2020"
    ax = sb.barplot(x='Ticker', y='Frequency', data=mainFrame)
    plt.title("WSB DAILY: THE MOST POPULAR TICKERS ON R/WSB TODAY", fontsize=20)
    annotation = ('--------- Summary ---------\n'+sentiment + '\nCalls: '+str(callCount)+'\nPuts: '+str(putCount) +
                  '\nAnalyzed '+str(commentCounter)+' comments'+'\nToday is: '+dateformat+'\n---------------------------')

    plt.text(0.9, 0.5, annotation,
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)

    plt.subplots_adjust(left=0.06, bottom=0.07, right=0.97,
                        top=0.94, wspace=None, hspace=None)

    print(spacer)
    end = time.time()
    print("Run time: " + str(round(end - start, 2))+" seconds")
    fileTitle = datetime.today().strftime('"%m-%d-%Y"')
    fileTitle = fileTitle[1:-1]
    plt.savefig('history/'+fileTitle+'.png')
    # plt.show()


print("Starting Sentiment Bot")
os.system('git fetch')
main()
os.system('git add .')
os.system('git commit -m "new image"')
os.system('git push origin master')
