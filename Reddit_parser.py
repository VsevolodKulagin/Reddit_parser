import praw
from datetime import datetime
from praw.models import MoreComments
#from itertools import islice
from threading import Thread
import time

Tickers = ('GME','NOK','AMC','NAKD','EXPR')

def obtain_data(commentsTree, root_id = 0):
    for depth, comment in enumerate(commentsTree):
        
            if isinstance(comment, MoreComments):
                continue
            
            #while True:   # the first success will break, discovered after the replacement MoreComments will be ignored
            #    try:
            #        submission.comments.replace_more()
            #        break
            #    except PossibleExceptions:
            #        print("Handling replace_more exception")
            #        sleep(1)
            
            
            
            for ticker in Tickers:
                if ticker in comment.body: 
                    record = dict(ticker = ticker, ups=comment.ups, downs=comment.downs, depth=depth, submission_id=comment.link_id, root_id=root_id, time = comment.created_utc, comment_id = comment.id)
                    #print(record)
                    data.append(record)
                    
            if ((comment.replies) and (root_id)):
                obtain_data(comment.replies, root_id)
                
            if ((comment.replies) and (root_id == 0)):
                obtain_data(comment.replies, comment.id)
                

data = []
threads = []

def ParseReddit():
#Creating read-only instance
    reddit = praw.Reddit(
                         client_id = "iovQ5RnL83_oJw",
                         client_secret = "_SISblQzwOKQ5d7DaCn_xTtcjRcxpw",
                         user_agent = "PC:Test_app:v1.0 (by /u/Vsev_kool)"
                        )



    for submission in reddit.subreddit("wallstreetbets").hot(limit=100):
        th = Thread(target = obtain_data, args = (submission.comments,))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    f = open("wallstreetbets_tickers_"+str(datetime.now().date())+"_"+str(datetime.now().hour)+"_"+str(datetime.now().minute)+".tsv",'w')

    for record in data:
        f.write(str(record['ticker'])+'\t'+str(record['ups'])+'\t'+str(record['downs'])+'\t'+str(record['depth'])+'\t'+str(record['submission_id'])+'\t'+str(record['root_id'])+'\t'+str(record['time'])+'\t'+str(record['comment_id'])+'\n')
    f.close()

    data.clear()
    threads.clear()  


while True:
    ParseReddit()
    time.sleep(400)
    time.sleep(400)    