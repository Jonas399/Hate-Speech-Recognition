import random
import json
import requests as req
import numpy as np

from tensorflow.keras import Model
from utils.models import Message


BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACpVXQEAAAAAwuCJEsBCl1q6N%2FpcKyFY2ipBHXA%3DOIg3kjVDPKZx8GGoOAiM9xd5IWxmHruFYKZgs24Ju01G8o5gKL'


GREETINGS = [
    "Hi there.",
    "Hello friend. How can I help you.",
    "Hello traveler.",
    "Hello fellow human."
]

GREETINGS_PATTERNS = [
    'hi',
    'hello'
]



class Bot:

    def __init__(self, hate_speech_classifier: Model):
        self.model = None
        self.hate_speech_classifier = hate_speech_classifier
        self.examine_tweet = False
        self.examine_user = False
        self.examine_message = False


    def answer(self, content):
        intent = self._classify_intent(content)
        msg_list = []
        ## action
        if intent == 'greeting':
            msg_1 = Message('Welcome my friend.', 'bot')
            msg_2 = Message('You can search for tweets and users or classify your own message.', 'bot')
            msg_3 = Message('Just type a message containing the words \"tweet\", \"user\" or \"message\".', 'bot')
            msg_4 = Message('Have fun.', 'bot')
            msg_list = [msg_1, msg_2, msg_3, msg_4]
        ## offensive language or hate speech 
        elif intent == 'offense':
            msg_1 = Message('Be careful my friend.', 'bot')
            msg_2 = Message('This is a hate speech detection bot.', 'bot')
            msg_3 = Message('Be friendly.', 'bot')
            msg_list = [msg_1, msg_2, msg_3]
        ## action
        elif intent == 'action':
            msg_1 = Message('Alright. You can perform the following actions.', 'bot')
            msg_2 = Message('You can search for tweets and users or classify your own message.', 'bot')
            msg_3 = Message('Type a message containing the words \"tweet\", \"user\" or \"message\".', 'bot')
            msg_list = [msg_1, msg_2, msg_3]
            self._reset_examinations()
        ## user
        elif intent == 'user':
            msg_1 = Message('Okay, now give me the profile link.', 'bot')
            msg_list = [msg_1]
            self._reset_examinations()
            self.examine_user = True
        ## user url
        elif intent == 'user_url':
            if self.examine_user or True: # refactor
                msg_list = []
                pass
            else: # TODO:
                msg_list = []
                pass
        ## tweet
        elif intent == 'tweet':
            msg_1 = Message('Okay, now give me the URL of the tweet.', 'bot')
            msg_list = [msg_1]
            self._reset_examinations()
            self.examine_tweet = True
        ## tweet url
        elif intent == 'tweet_url': # refactor
            if self.examine_tweet or True:
                msg_list = self._examine_tweet(content)  
            else: # TODO:
                msg_1 = Message('You can search for tweets and users or classify your own message.', 'bot')
                msg_2 = Message('Type a message containing the words \"tweet\", \"user\" or \"message\".', 'bot')
                msg_list = [msg_1, msg_2]
        ##
        elif intent == 'message':
            msg_1 = Message('Okay, just type in the text box.', 'bot')
            msg_list = [msg_1]
            self._reset_examinations()
            self.examine_message = True
        elif intent == 'message_text':
            msg_list = self._examine_message(content)
            self._reset_examinations()
        else:
            msg_1 = Message('Sorry, I could not understand what you want.', 'bot')
            msg_2 = Message('You can search for tweets and users or classify your own message.', 'bot')
            msg_3 = Message('Tell me what you want to search for.', 'bot')
            msg_list = [msg_1, msg_2, msg_3]
        return msg_list


    def greet(self):
        msg_list = []
        msg_1 = Message(GREETINGS[random.randrange(0, len(GREETINGS) - 1)], 'bot')
        msg_2 = Message('You can search for tweets and users.', 'bot')
        msg_3 = Message('Type a message containing the words \"tweet\", \"user\" or \"message\".', 'bot')

        msg_list = [msg_1, msg_2, msg_3]
        return msg_list


    def _examine_tweet(self, content: str):
        # parse tweet_id
        messages = []
        splitted_content = content.split('/')
        tweet_id = splitted_content[-1].split('?')[0]
        tweet_fields = "tweet.fields=attachments,author_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source,text,withheld"
        url = f"https://api.twitter.com/2/tweets/{tweet_id}?{tweet_fields}"


        tweet_deleted = False
        try: 
            response = req.request("GET", url, auth=self._bearer_oauth)
        except:
            tweet_deleted = True       

        print('GET tweet Repsonce code: ', response.status_code)
        if response.status_code == 400:
            msg_1 = Message('Something went wrong.', 'bot')
            msg_2 = Message('Try again.', 'bot')
            messages = [msg_1, msg_2]
        elif tweet_deleted:
            msg_1 = Message('Unfortunately the tweet got deleted.', 'bot')
            msg_2 = Message('Try another tweet.', 'bot')
            messages = [msg_1, msg_2]
        else:
            print(response.status_code)
            json_response = response.json()
            text = json_response['data']['text']

            # classify tweet
            max_cls, max_val = self._classify_tweet(text)

            msg_1 = Message(f'The tweet {tweet_id} of {splitted_content[3]}', 'bot')
            msg_2 = Message(f'{text}', 'bot')

            max_val_percent = round((max_val * 100), 2)
            msg_3 = None
            if max_cls == 'hate speech': 
                msg_3 = Message(f'The tweet contains hate speech with a confidence of {max_val_percent}%.', 'bot')
            elif max_cls == 'offensive language': 
                msg_3 = Message(f'The tweet contains offensive language with a confidence of {max_val_percent}%.', 'bot')
            elif max_cls == 'neither': 
                msg_3 = Message(f'The tweet contains no hate speech and no offensive language with a confidence of {max_val_percent}%.', 'bot')
            
            messages = [msg_1, msg_2, msg_3]
        return messages 

    def _examine_user(self):
        pass

    def _examine_message(self, content):
        messages = []
        
        max_cls, max_val = self._classify_tweet(content)

        max_val_percent = round((max_val * 100), 2)
        msg_1 = None
        if max_cls == 'hate speech': 
            msg_1 = Message(f'The tweet contains hate speech with a confidence of {max_val_percent}%.', 'bot')
        elif max_cls == 'offensive language': 
            msg_1 = Message(f'The tweet contains offensive language with a confidence of {max_val_percent}%.', 'bot')
        elif max_cls == 'neither': 
            msg_1 = Message(f'The tweet contains no hate speech and no offensive language with a confidence of {max_val_percent}%.', 'bot')

        msg_2 = Message(f'Keep in mind that the message you just typed is not an actual tweet.', 'bot')
        msg_3 = Message(f'The classification might therefore be inaccurate.', 'bot')

        messages = [msg_1, msg_2, msg_3]
        
        return messages

    def _get_user(self, user_id):
        pass


    def _bearer_oauth(e, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r


    def _classify_intent(self, content: str):
        intent = ''
        casted_content = content.lower()

        offensive_message = False
        predicition = self.hate_speech_classifier.predict(content)
        print('normal message predicition ', predicition[0])
        if (predicition[0] > .55 or predicition[1] > .55) and not self.examine_message:
            offensive_message = True

        if self.examine_message:
            return 'message_text'

        if any(pattern in casted_content for pattern in GREETINGS_PATTERNS) and not 'https' in casted_content:
            intent = 'greeting'
        elif 'action' in casted_content:
            intent = 'action'
        elif 'user' in casted_content:
            intent = 'user'
        elif ('https' in casted_content and 'status' in casted_content) or self.examine_tweet:
            intent = 'tweet_url'
        elif 'https' in casted_content or self.examine_user:
            intent = 'user_url'
        elif 'tweet' in casted_content:
            intent = 'tweet'
        elif 'message' in casted_content:
            intent = 'message'
        elif offensive_message:
            intent = 'offense'

        return intent

    def _classify_tweet(self, tweet):
        predict = self.hate_speech_classifier.predict(tweet)
        # print('Prection of tweet: ', predict)

        hate = round(predict[0]*100, 2)
        offensive = round(predict[1]*100, 2)
        none = round(predict[2]*100, 2)

        print(f'PREDICTIONS: hate {hate}, offensive {offensive}, none {none}')

        max_val = np.max(predict)
        max_idx = np.argmax(predict)

        max_cls = ''
        if max_idx == 0: max_cls = 'hate speech'
        elif max_idx == 1: max_cls = 'offensive language'
        elif max_idx == 2: max_cls = 'neither'

        return max_cls, max_val

    
    def _reset_examinations(self):
        self.examine_tweet = False
        self.examine_user = False
        self.examine_message = False

