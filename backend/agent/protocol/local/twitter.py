from ...protocol.twitter import TwitterClient

def post_tweet(text: str) -> dict:
    """
    Post a tweet with the given text.
    
    Args:
        text (str): The text content of the tweet
        
    Returns:
        dict: Response from Twitter API containing tweet details or error information
    """
    client = TwitterClient()
    return client.post_tweet(text) 