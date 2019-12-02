import time
from getpass import getpass
from random import randint

from selenium import webdriver
from selenium.webdriver.common import keys


class TwitterBot:
    def __init__(self, username, password, web_driver):
        self.username = username
        self.password = password
        self.bot = web_driver

    def __del__(self):
        """
        Close the browser on exit
        :return: None
        """
        self.bot.close()

    def login(self):
        """
        Login on Twitter
        :return: None
        """
        self.bot.get('https://twitter.com/')
        self.__wait(3, 5)
        email = self.bot.find_element_by_name('session[username_or_email]')
        password = self.bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        self.__wait(3, 5)

    def like_tweet(self, tag):
        """
        Like last tweets by hash tag
        :param tag:
        :return: None
        """
        self.bot.get('https://twitter.com/search?q=' + tag + '&src=typed')
        self.__wait(3, 3)
        for i in range(1, 3):
            self.bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            self.__wait(2, 3)
        tweets = self.bot.find_elements_by_tag_name('article')

        links = []
        for tweet in tweets:
            sub_links = tweet.find_elements_by_tag_name('a')
            links += [sub_link.get_attribute('href')
                      for sub_link in sub_links if 'status' in sub_link.get_attribute('href')]

        print('Started to like {} tweets'.format(len(links)))

        for link in links:
            self.bot.get(link)
            self.__wait(3, 5)
            likes = self.bot.find_elements_by_css_selector('div[data-testid="like"')
            for like in likes:
                like.click()
                self.__wait(3, 5)

    @staticmethod
    def __wait(min_sec, max_sec):
        """
        Wait some seconds to load page or avoid blocking the account
        :param min_sec:
        :param max_sec:
        :return: None
        """
        time.sleep(randint(min_sec, max_sec))


if __name__ == '__main__':
    print('Welcome to Twitter bot')
    twitter_username = input('Enter your twitter username or email: ')
    twitter_password = getpass('Enter your password: ')
    hashtag = input('Enter hashtag: ')

    driver_type = int(input('Choose webdriver 1) Chrome 2) Firefox: '))
    if driver_type == 1:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()

    if twitter_username and twitter_password and hashtag:
        bot = TwitterBot(twitter_username, twitter_password, driver)
        bot.login()
        bot.like_tweet(hashtag)
