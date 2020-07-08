from selenium import webdriver
from time import sleep
from envexample import username, password


class AutoSwipeTinder():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="/home/hoanglm/PycharmProjects/automate-swipe-tinder/chromedriver")

    def login(self):
        self.driver.get("https://tinder.com")

        sleep(2)

        # update new template in Tinder
        select_options = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/span/button")
        select_options.click()

        # login option using facebook
        fb_login = \
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[3]/span/div[2]/button/span[2]')
        fb_login.click()

        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_button = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_button.click()

        self.driver.switch_to_window(base_window)

        popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        popup_1.click()

        popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        popup_2.click()

    def like(self):
        like_btn = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            sleep(1.0)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()


auto_click = AutoSwipeTinder()
auto_click.login()
