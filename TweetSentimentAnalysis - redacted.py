import argparse
import re
import nltk
import twitter
from tkinter import *
from tkinter import scrolledtext
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
nltk.download('punkt')

# initialize api instance
twitter_api = twitter.Api(consumer_key='consumer_key',
                        consumer_secret='consumer_secret',
                        access_token_key='access_token_key',
                        access_token_secret='access_token_secret',
                        tweet_mode='extended')

def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    
    result = ""
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
    #    print('Sentence {} has a sentiment score of {}'.format(
    #        index, sentence_sentiment))
        result = result + 'Sentence ' + str(index + 1) + ' has a sentiment score of '+ str(round(sentence_sentiment,2)) + '\n'

    #print('Overall Sentiment: score of {} with magnitude of {}'.format(
    #    score, magnitude))
    result = result + '\nOverall Sentiment: score of ' + str(round(score,2)) + ' with magnitude of ' + str(round(magnitude,2)) + '\n'
    return result


def analyze(text_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    #really just setting the text so analyze thinks it's a document
    content = text_filename

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    # Print the results
    #print_result(annotations)
    return print_result(annotations)


#original main that prints to console
#tweet does not grab anything if it is a video, funnily enough it does have a sentiment rating of 0.3    
def original_main():
    last_tweet = twitter_api.GetUserTimeline(screen_name="realDonaldTrump", count=5)
    print("Last 5 tweets")

    print("Most recent tweet:")
    print(last_tweet[0].full_text)
    analyze(last_tweet[0].full_text)

    print("\nSecond nost recent tweet:")
    print(last_tweet[1].full_text)
    analyze(last_tweet[1].full_text)

    print("\nThird most recent tweet:")
    print(last_tweet[2].full_text)
    analyze(last_tweet[2].full_text)

    print("\nFourth most recent tweet:")
    print(last_tweet[3].full_text)
    analyze(last_tweet[3].full_text)

    print("\nFifth most recent tweet:")
    print(last_tweet[4].full_text)
    analyze(last_tweet[4].full_text)

def pickText(tweet):
    picked = ''
    sentences = nltk.sent_tokenize(tweet)
    for sentence in sentences:
      text = re.sub('[^\w\s]','',sentence)
      tokens = text.split()
      picked += (' '.join(tokens))
      picked+='. '
    return picked
    
def clicked(label1, label2, label3, label4, text1, text2, text3):
    last_tweet = twitter_api.GetUserTimeline(screen_name="realDonaldTrump", count=3)
    label1.configure(text="President Trump's latest 3 Tweets\n\nMost recent tweet:")
    text1.insert(INSERT,last_tweet[0].full_text)
    
    label2.configure(text=analyze(pickText(last_tweet[0].full_text))+"\nSecond most recent tweet:")
    #label2.configure(text=(pickText(last_tweet[0].full_text))+"\nSecond most recent tweet:")
    text2.insert(INSERT,last_tweet[1].full_text)
    label3.configure(text=analyze(pickText(last_tweet[1].full_text))+"\nThird most recent tweet:")
    #label3.configure(text=(pickText(last_tweet[1].full_text))+"\nThird most recent tweet:")
    text3.insert(INSERT,last_tweet[2].full_text)
    label4.configure(text=analyze(pickText(last_tweet[2].full_text)))
    #label4.configure(text=(pickText(last_tweet[2].full_text)))

#simple GUI that analyzes 3 Tweets
def main():
    window = Tk()

    window.title("President Trump's Tweet Sentiment Analysis")
    window.geometry('450x800')
    label1 = Label(window, text="", font=("Arial", 12))
    label1.grid(column=0, row=1)
    label2 = Label(window, text="", font=("Arial", 12))
    label2.grid(column=0, row=3)
    label3 = Label(window, text="", font=("Arial", 12))
    label3.grid(column=0, row=5)
    label4 = Label(window, text="", font=("Arial", 12))
    label4.grid(column=0, row=7)
    text1 = scrolledtext.ScrolledText(window,width=60,height=3)
    text1.grid(column=0,row=2)
    text2 = scrolledtext.ScrolledText(window,width=60,height=3)
    text2.grid(column=0,row=4)
    text3 = scrolledtext.ScrolledText(window,width=60,height=3)
    text3.grid(column=0,row=6)
    
    button = Button(window, text="Refresh", font=("Arial", 10), command=lambda:clicked(label1, label2, label3, label4, text1, text2, text3))
    button.grid(column=0, row=0)

    window.mainloop()

main()