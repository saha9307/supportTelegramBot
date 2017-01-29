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
print(type(s))

# -*- coding: utf-8 -*-

# import _mysql
# try:
#     db = _mysql.connect(host="localhost",user="root",
#                   passwd="q100689",db="ModernExpo")
# except BaseException as e:
#     print(str(e))
#     exit()
#     # print(str(e))
#
# db.set_character_set("utf8")
# inn = 2949105119
# db.query("SELECT * FROM UserInfo")
# r=db.use_result()
# # print(db.Error)
# listR = r.fetch_row(0)
# for s in listR:
#     print(s)
#     # print(s[1].decode('utf-8'))\


# def userRegistered(userID):
#     db = _mysql.connect(host="localhost", user="root", passwd="q100689", db="ModernExpo")
#     db.set_character_set("utf8")
#     db.query("SELECT * FROM UserInfo WHERE telegram_user_id = " + str(userID))
#     resultQuery = db.use_result()
#     userInfo = resultQuery.fetch_row(0)
#     db.close()
#     if len(userInfo) > 0:
#         return True
#     else:
#         return False
#
# s = userRegistered('123456')
# print(s)



