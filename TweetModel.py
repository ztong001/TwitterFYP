#!/usr/bin/env python


class TweetModel:
    """Data Format for tweet to be analysed
    """

    def __init__(self, uid, text, user, created_at):
        self.uid = uid
        self.text = text
        self.user = user
        self.created_at = created_at

    def to_dict(self):
        """Returns a dictionary representation of the Tweet
        """
        return {
            "id": self.uid, "text": self.text, "user": self.user, "created_at": self.created_at}
