# import telebot
#
# s = dir(telebot.TeleBot)
# print(s)

# x = [1, 2, 3]
# y = x
# y.append(4)
#
# s = "123"
# t = s
# t = t + "4"
#
# print(str(x) + " " + s)

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome  # Get local session of firefox
browser.get("http://go.mail.ru/?chrome=1")  # Load page
# assert "Яндекс".decode("utf-8") in browser.title
# elem = browser.find_element_by_name("text")  # Find the query box
# elem.send_keys("http://программисту.рф/".decode("utf-8") + Keys.RETURN)
# time.sleep(0.2)  # Let the page load, will be added to the API