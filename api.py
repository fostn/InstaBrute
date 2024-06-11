import requests
import urllib
import configparser
from password_mixin import PasswordMixin
import os
import random
import urllib.parse
import uuid
import re
import random

class InstagramAPI:
    def __init__(self):
        pass
    def authenticate(self, username, password,proxies=None):
        encrypt = PasswordMixin()
        encrypted_password = urllib.parse.quote_plus(encrypt.password_encrypt(password))
        url = "https://i.instagram.com/api/v1/accounts/login/"
        headers = {
				'User-Agent': 'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
				}
        data = {
        "phone_id": str(uuid.uuid4()).upper(),
        "reg_login": "0",
        "device_id": str(uuid.uuid4()).upper(),
        "att_permission_status": "0",
        "has_seen_aart_on": "1",
        "username": f"{username}",
        "adid": str(uuid.uuid4()).upper(),
        "login_attempt_count": "0",
        "enc_password": f"{encrypted_password}"
        }

        phone_id = str(uuid.uuid4()).upper()
        device_id = str(uuid.uuid4()).upper()
        adid = str(uuid.uuid4()).upper()

        data = f"signed_body=SIGNATURE.%7B%22phone_id%22%3A%22{phone_id}%22%2C%22reg_login%22%3A%220%22%2C%22device_id%22%3A%22{device_id}%22%2C%22att_permission_status%22%3A%220%22%2C%22has_seen_aart_on%22%3A%221%22%2C%22username%22%3A%22{username}%22%2C%22adid%22%3A%22{adid}%22%2C%22login_attempt_count%22%3A%220%22%2C%22enc_password%22%3A%22{encrypted_password}%22%7D"
        
        try:
            response = requests.post(url, data=data,headers=headers,proxies=proxies,timeout=5)
            if 'ig-set-authorization' in response.headers and response.status_code == 200:
                try:
                    token = response.headers['ig-set-authorization']
                except:
                    token = ''
                return {
                message:"authorized",
                'token':token
                }
            elif "Incorrect password" in response.text:
                return {
                'message':"Incorrect password"
                }
            elif "challenge_required" in response.text:
                return {
                'message':"Secure"
                }
            elif "checkpoint_required" in response.text:
                return {
                'message':"captcha"
                }
            elif "Incorrect Username" in response.text:
                return {
                'message':"Incorrect Username"
                }
            elif "The username you entered doesn't appear to" in response.text:
                return {
                'message':"The username you entered doesn't appear to"
                }
                
            elif "We couldn't find an account with the username" in response.text:
                return {
                'message':"We couldn't find an account with the username"
                }
            else:
                return {
                'message':response.text
                }
        except:
            return {
                'message':"Proxy Error"
            }
