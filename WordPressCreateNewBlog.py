__author__ = 'anatarajan2'

import random
import sys
import new
import unittest
from selenium import webdriver
from sauceclient import SauceClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

USERNAME = 'samarr'
ACCESS_KEY = '8ce86162-6393-4fa4-bdab-a89810ada58a'
sauce = SauceClient(USERNAME, ACCESS_KEY)
browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": "31"},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"},
            {"platform": "Windows 10",
             "browserName": "firefox",
             "version": "47"},
            {"platform": "Windows 7",
             "browserName": "internet explorer",
             "version": "9"},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"}]
wordpress_username = 'shariqmahmood21'
wordpress_password = 'Chilly9959'
blogTitle = None
blogContent = None
base_url='https://wordpress.com/wp-login.php'


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator

@on_platforms(browsers)
class StepinSummit2016(unittest.TestCase):
    def setUp(self):
        self.desired_capabilities['name'] = self.id()
        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.set_page_load_timeout(60)
        self.driver.implicitly_wait(60)
    def test_createblog(self):
        blogTitle = 'MyNewBlogTitle' + str(random.randint(0, 999999))
        blogContent = 'This is the blog content' + str(random.randint(0, 999999))
        self.driver.get(base_url)
        #self.driver.find_element_by_link_text("Sign In").click()
        self.driver.find_element_by_id("user_login").clear()
        self.driver.find_element_by_id("user_login").send_keys(wordpress_username)
        self.driver.find_element_by_id("user_pass").clear()
        self.driver.find_element_by_id("user_pass").send_keys(wordpress_password)
        self.driver.find_element_by_id("wp-submit").click()
        self.driver.find_element_by_css_selector("span.masterbar__item-content").click()
        self.driver.find_element_by_link_text("Add").click()
        self.driver.find_element_by_css_selector("textarea.textarea-autosize.editor-title__input").clear()
        self.driver.find_element_by_css_selector("textarea.textarea-autosize.editor-title__input").send_keys(blogTitle)
        self.driver.find_element_by_id("tinymce-1").clear()
        self.driver.find_element_by_id("tinymce-1").send_keys(blogContent)
        self.driver.find_element_by_xpath("//div[@id='primary']/div/div[2]/div[2]/div[2]/div/div[3]/div/button").click()
        self.driver.find_element_by_css_selector("a.notice__action > span").click()
        WebDriverWait(self.driver, 20).until(expected_conditions.tittle.contains(blogTitle))
        assert blogTitle in self.driver.title
        #self.driver.close()
        #self.driver.find_element_by_css_selector("img.gravatar").click()
        #self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main()
