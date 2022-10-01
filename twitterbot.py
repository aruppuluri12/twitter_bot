import tweepy
import urllib.request
import io
import random


class TwitterBot(object):

    def __init__(self, consumer_key, consumer_secret, access_token, token_secret,
                 source_file_name, quotes_file_name):
        self.source_file_name = source_file_name
        self.quotes_file_name = quotes_file_name

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)
        self.twitter = tweepy.API(auth)

    def _get_image_list(self):
        with open(self.source_file_name) as source_fh:
            images = []
            for line in source_fh:
                images.append(source_fh.readline().strip())
            return images

    def _get_media(self, images):
        with open(self.source_file_name) as source_fh:
            media_ids = []
            random_images = random.sample(images, 4)
            for i in random_images:
                res = self.twitter.media_upload("", file=io.BytesIO(
                    urllib.request.urlopen(i).read()))
                media_ids.append(res.media_id)
            return media_ids

    def _get_quotes_list(self):
        with open(self.quotes_file_name) as quotes_fh:
            quotes = []
            for line in quotes_fh:
                quotes.append(quotes_fh.readline().strip())
            return quotes

    def post(self):
        images = self._get_image_list()
        media = self._get_media(images)
        tweets = self._get_quotes_list()
        tweet = random.choice(tweets)
        self.twitter.update_status(tweet, media_ids=media)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--consumer_key', dest='consumer_key',
                      help="twitter consumer key")
    parser.add_option('--consumer_secret', dest='consumer_secret',
                      help="twitter consumer secret")
    parser.add_option('--access_token', dest='access_token',
                      help="twitter token key")
    parser.add_option('--token_secret', dest='token_secret',
                      help="twitter token secret")
    parser.add_option('--source_file', dest='source_file',
                      default="tweet_list.txt",
                      help="source file (one line per tweet)")
    parser.add_option('--quotes_file', dest='quotes_file',
                      default="quotes.txt",
                      help="quotes file (one line per tweet)")
    (options, args) = parser.parse_args()

    bot = TwitterBot(options.consumer_key, options.consumer_secret,
                     options.access_token, options.token_secret, options.source_file, options.quotes_file)

    bot.post()
