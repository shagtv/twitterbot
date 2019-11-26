from selenium import webdriver
from selenium.webdriver.common import keys
import time
from getpass import getpass


class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def __del__(self):
        self.bot.close()

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        time.sleep(3)
        email = bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        time.sleep(3)

    def like_tweet(self, hashtag):
        bot = self.bot
        bot.get('https://twitter.com/search?q=' + hashtag + '&src=typed')
        time.sleep(3)
        for i in range(1, 3):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
        tweets = bot.find_elements_by_tag_name('article')

        links = []
        for tweet in tweets:
            sub_links = tweet.find_elements_by_tag_name('a')
            links += [sub_link.get_attribute('href') for sub_link in sub_links if 'status' in sub_link.get_attribute('href')]

        print('Started to like {} tweets'.format(len(links)))

        for link in links:
            bot.get(link)
            time.sleep(3)
            likes = bot.find_elements_by_css_selector('div[data-testid="like"')
            for like in likes:
                try:
                    like.click()
                except:
                    pass
                time.sleep(3)


if __name__ == '__main__':
    print('Welcome to Twitter bot')
    username = input('Enter your twitter username or email: ')
    password = getpass('Enter your password: ')
    hashtag = input('hashtag: ')

    if username and password and hashtag:
        bot = TwitterBot(username, password)
        bot.login()
        bot.like_tweet(hashtag)
