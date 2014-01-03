from social.backends import twitter

class TwitterOAuth(twitter.TwitterOAuth):
    def unauthorized_token(self):
        token = super(TwitterOAuth, self).unauthorized_token()
        if type(token) == bytes:
            token = token.decode('utf-8')
        return token

