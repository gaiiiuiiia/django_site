from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://d-webserver')

assert 'successful' in browser.title


