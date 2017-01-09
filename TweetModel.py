import json


class TweetModel:
    """Data Format for tweet to be analysed
    """

    def __init__(self, id, text, user, created_at):
        self.id = id
        self.text = text
        self.user = user
        self.created_at = created_at


class ModelEncoder(json.JSONEncoder):

    def default(self, tweet):
        if isinstance(tweet, TweetModel):
            return {"id": tweet.id,
                    "text": tweet.text,
                    "user": tweet.user,
                    "created_at": tweet.created_at}
        # Let base class default method raise the TypeError
        return json.JSONEncoder.default(self, tweet)
