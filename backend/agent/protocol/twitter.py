import tweepy
import os
from dotenv import load_dotenv

class TwitterClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # Initialize the client
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
    
    def post_tweet(self, text: str) -> dict:
        """
        Post a tweet with the given text.
        
        Args:
            text (str): The text content of the tweet
            
        Returns:
            dict: Response from Twitter API containing tweet details
        """
        try:
            response = self.client.create_tweet(text=text)
            return {
                'success': True,
                'tweet_id': response.data['id'],
                'text': response.data['text']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 