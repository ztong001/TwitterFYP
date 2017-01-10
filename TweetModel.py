#!/usr/bin/env python


class TweetModel:
    """Data Format for tweet to be analysed
    """

    def __init__(self, uid, text, user, created_at):
        self.uid = uid
        self.text = text
        self.user = user
        self.created_at = created_at
