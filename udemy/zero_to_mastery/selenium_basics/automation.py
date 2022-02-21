from email.policy import default
from selenium import webdriver

chrome_browser = webdriver.Chrome('./chromedriver')
chrome_browser.maximize_window()
# http://allselenium.info/python-selenium-commands-cheat-sheet-frequently-used/ - cheetsheet
chrome_browser.get("https://demo.seleniumeasy.com/basic-first-form-demo.html")
assert 'Selenium Easy Demo - Simple Form to Automate using Selenium' in chrome_browser.title
button_text = chrome_browser.find_element_by_class_name('btn-default')
print(button_text.get_attribute('innerHTML'))
assert 'Show Message' in chrome_browser.page_source