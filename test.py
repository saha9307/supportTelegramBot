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
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
# import time

# browser = webdriver.Chrome  # Get local session of firefox
# browser.get("http://go.mail.ru/?chrome=1")  # Load page
# assert "Яндекс".decode("utf-8") in browser.title
# elem = browser.find_element_by_name("text")  # Find the query box
# elem.send_keys("http://программисту.рф/".decode("utf-8") + Keys.RETURN)
# time.sleep(0.2)  # Let the page load, will be added to the API

# import json
# import pycurl
# from _io import BytesIO
# from urllib.parse import urlencode
#
# struct = {'INN': '3405601611'}
#
# jenc = json.dumps(struct)
#
# # print(jenc)
#
# postfields = urlencode(struct)
#
# buffer = BytesIO()
# c = pycurl.Curl()
# c.setopt(c.URL, 'http://212.1.103.131/BaseCRM/hs/WebModern/GetUserInfo?session=87a95fsfc-063d-482c-8687-6c95733eec9d')
# c.setopt(c.WRITEDATA, buffer)
# c.setopt(c.POSTFIELDS, postfields)
# c.setopt(c.USERNAME, 'Администратор'.encode('utf-8'))
# c.setopt(c.USERPWD, '')
# c.perform()
# c.close()
#
# body = buffer.getvalue()
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
# print(body.decode('iso-8859-1'))

# $curlObject->setData(json_encode($data));
# $curlObject->setTypeRequest("POST");
# $curlObject->setUserName("Администратор");
# $curlObject->setPassword('');
# $curlObject->setURL('http://212.1.103.131/BaseCRM/hs/WebModern/GetUserInfo?session=87a95fsfc-063d-482c-8687-6c95733eec9d');
# $resultRequest = $curlObject->StartCurlRequest();


import json
import requests
from requests.auth import HTTPDigestAuth

url = 'http://212.1.103.131/BaseCRM/hs/WebModern/GetUserInfo?session=87a95fsfc-063d-482c-8687-6c95733eec9d'
headers = {'Content-Type': "application/json"}
data = {"INN": "2949105119"}
jdata = json.dumps(data).encode('utf8')
# res = requests.post(url, json=jdata, headers=headers)
res = requests.post(url, auth=('Администратор'.encode('utf-8'), ''), data=jdata, headers=headers)
# res = requests.post(url, json=jdata, headers=headers, auth=HTTPDigestAuth("Администратор", ""))
print(res.status_code)
# print(type(res))
s = json.loads(res.text)
print(s)
