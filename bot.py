'''
#############################################################################################################################
# [!!!]Private Tokens & Keys Removed[!!!]     #
# [!!!]PUBLIC TESTING PRODUCTION[!!!]                                                                                       #
#                                                                                                                           #
# Date Started: 3/21/20                                                                                                     #   
#                                                                                                                           #
#                                                                                                                           #
#                                                                                                                           #
# Bot Purpose: Moderaton Comment Streaming, r/Coronavirus title filtering for Massachusetts related posts                   #
#                                                                                                                           #
# To Do:      - Adding Commands so bot can be called from a comment (commands: TBD)                                         #
#             - Stability needs to be improved slightly                                                                     #
#             - Adding moderation options to discord webhook streamlining instead of only linking submission for moderation #
#############################################################################################################################
'''


# //-Packages

import praw
from profanity_check import predict,predict_prob 
import sys
import os
import random
import time
import requests

# //-Reddit API 

reddit = praw.Reddit(
                     client_id = '',
                     client_secret = '',  
                     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',   
                     username = '',
                     password = ''
                     )


reddit.read_only = False

getsub = reddit.subreddit("coronavirus+coronavirusma")

TitleFilter = ['massachusetts','boston','charlie baker']

crosspost_subreddit = ''

delay = 1



# //-Discord Webhook Piplining & Other Functions

Hook = ''

def sendwebhook(comment,text,isCivil):
     webhook = requests.post(Hook,data={
            'content':'`User: '+str(comment.author)+' `'+' ``` '+ str(text)+' ``` \n'+' Submission [Link](https://www.reddit.com/r/CoronavirusMa/comments/'+str(comment.submission)+'/?context=3)'+' \n \n `'+str(isCivil)+'`'+'\n ___________________________________________________________',
            })

# //-LocalHost Checking.

global modlist
modlist = []

def boot():
    internet_chk = requests.get('https://google.com' and 'https://bing.com')
    os.system('cls')
    print('Returned: '+str(internet_chk))
    requests.post(Hook,data={'content':'¯\_(ツ)_/¯    [Automated Response]: Connected! (Ignore this message if you are not a developer)    ¯\_(ツ)_/¯'})

    for mods in reddit.subreddit('coronavirusma').moderator():
        modlist.insert(0,str(mods))
        print('\n Authed mod: '+str(mods))

boot()

# //-Reddit Comment/Reply | Submission/Post Streaming [ Variables ]

comment_stream = getsub.stream.comments(pause_after=-1, skip_existing=True)

submission_stream = getsub.stream.submissions(pause_after=-1, skip_existing=True)

# //-Reddit Comment/Reply | Submission/Post Streaming [ Main ]
while True:
    time.sleep(delay) 
    for comment in comment_stream:
        if comment is None:
            break
        if comment.subreddit == 'coronavirus':
            pass
        else:   
            text = comment.body
            submission_parent = comment.submission
            comment_parent = comment.parent()
            author = comment.author
            score = predict([text])
            for admin in modlist:
                if author == admin:

                    if (text.find('!removepost') != -1):
                        note = text.replace('!removepost ','')
                        if note == '':
                            comment.mod.distinguish(how='yes', sticky=True)
                            
                            post = reddit.submission(id=str(submission_parent))
                            post.mod.remove(spam=False, mod_note=None, reason_id=None)

                            action_completed = reddit.comment(id=str(comment))
                            action_completed.reply('Submission was removed!')
                        else:
                            comment.mod.distinguish(how='yes', sticky=True)

                            post = reddit.submission(id=str(submission_parent))
                            post.mod.remove(spam=False, mod_note=str(note), reason_id=None)

                            action_completed = reddit.comment(id=str(comment))
                            action_completed.reply('Submission was removed! Moderator note: ***'+str(note)+'***')
                    
                    if (text.find('!removecomment') != -1):
                        note = text.replace('!removecomment ', '')
                        if note == '':
                            comment.mod.distinguish(how='yes', sticky=True)
                    
                            remove_comment = reddit.comment(str(comment_parent))
                            remove_comment.mod.remove(spam=False, mod_note=None, reason_id=None)
    
                            action_completed.reply('Comment was removed!')
                        else:
                            comment.mod.distinguish(how='yes', sticky=True)

                            remove_comment = reddit.comment(str(comment_parent))
                            remove_comment.mod.remove(spam=False, mod_note=str(note), reason_id=None)

                            action_completed = reddit.comment(id=str(comment))
                            action_completed.reply('Comment was removed! Moderator note: ***'+str(note)+'***')

                else:
                    
                    pass

            if score == 1:
                isCivil = '[NOT CIVIL]'
                sendwebhook(comment, text, isCivil)
            else:
                isCivil = '[CIVIL]'
                sendwebhook(comment, text, isCivil)

    for submission in submission_stream:
        if submission is None:
            break 
        if submission.subreddit == 'coronavirus':
            submission_title = submission.title
            for v in TitleFilter:
                titleformat = submission_title.lower()
                if (titleformat.find(v) != -1):
                    print('found')
                    postid = submission.id
                    postauthor = submission.author
                    cross_post_to = submission.crosspost(subreddit=crosspost_subreddit, title=str(submission_title),flair_id='5e3ebd28-6e14-11ea-a50f-0e5b76972e6d')
                    crossposted_post = reddit.submission(id=cross_post_to.id)
                    crossposted_post.mod.approve()
                else:
                    pass
        else:
            if submission.subreddit == 'coronavirusma':
                submission_title = submission.title
                submission_author = submission.author
                webhook = requests.post(Hook,data={
                'content':'`User: '+str(submission_author)+' `'+' ``` '+ str(submission_title)+' ``` \n'+' Submission [Link](https://www.reddit.com/r/CoronavirusMa/comments/'+str(submission)+'/?context=3)'+' \n \n ___________________________________________________________',
                })
            pass

            
