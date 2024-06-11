from customtkinter import CTkFrame, CTkLabel, CTkEntry
import os
import json
import webbrowser
class RightFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = CTkLabel(self, text="Checker")
        self.label.pack(padx=5, pady=(5, 0), anchor="n")

        top_frame = CTkFrame(self)
        top_frame.pack(side="top", fill="x", pady=5)

        self.good_label = CTkLabel(top_frame, text="Authorized: 0",text_color='#65B741')
        self.good_label.pack(side="left", padx=(5, 20))
        self.bad_label = CTkLabel(top_frame, text="Invalid credentials: 0",text_color='#E72929')
        self.bad_label.pack(side="right", padx=(20, 5))

       
        center_frame = CTkFrame(self)
        center_frame.pack(side="top", fill="x", pady=5)

        self.checked_label = CTkLabel(center_frame, text="Checked: 0",text_color='#D9D3CC')
        self.checked_label.pack(side="right", padx=(20, 5))

  
        self.secure_label_center = CTkLabel(center_frame, text="Secure Accounts: 0",text_color='#FF5739')
        self.secure_label_center.pack(side="left", padx=(5, 20), anchor="center")

        error_frame = CTkFrame(self)
        error_frame.pack(side="top", fill="x", pady=5)

       
        self.error_label = CTkLabel(error_frame, text="Errors: 0")
        self.error_label.pack(side="left", padx=(5, 20), anchor="center")

        self.proxy_error_label = CTkLabel(error_frame, text="Proxy Errors: 0")
        self.proxy_error_label.pack(side="right", padx=(20, 5), anchor="center")
    
        bottom_line_frame = CTkFrame(self)
        bottom_line_frame.pack(side="top", fill="x", pady=5)

      
        self.total_accounts_label = CTkLabel(bottom_line_frame, text="Total Accounts: 0")
        self.total_accounts_label.pack(side="left", padx=(5, 20), anchor="center")

 
        self.total_proxies_label = CTkLabel(bottom_line_frame, text="Total Proxies: 0")
        self.total_proxies_label.pack(side="right", padx=(20, 5), anchor="center")

        bottom_frame = CTkFrame(self)
        bottom_frame.pack(side="top", fill="x", pady=5)

        self.accounts_file_label = CTkLabel(bottom_frame, text="Accounts File Name: ")
        self.accounts_file_label.pack(side="left", padx=(10, 15))

        self.proxies_file_label = CTkLabel(bottom_frame, text="Proxies File Name: ")
        self.proxies_file_label.pack(side="right", padx=(20, 10))
        
        self.bottom_center_label = CTkLabel(self, text="developed by @f09l", cursor="hand2")
        self.bottom_center_label.pack(side="bottom", pady=(0, 5), anchor="center")
        self.bottom_center_label.bind("<Button-1>", self.open_url) 

     
        self.entry_frame = CTkFrame(self)
        self.entry_frame.pack(side="top", fill="x", pady=5)

        self.token_label = CTkLabel(self.entry_frame, text="Token:")
        self.token_label.pack(side="left", padx=(5, 10))

        self.token_entry = CTkEntry(self.entry_frame, placeholder_text="enter your token",show='*')
        self.token_entry.pack(side="left", padx=5)

        self.id_label = CTkLabel(self.entry_frame, text="ID:")
        self.id_label.pack(side="left", padx=(10, 0))

        self.id_entry = CTkEntry(self.entry_frame, placeholder_text="enter your id",)
        self.id_entry.pack(side="left", padx=5)
        self.pack_propagate(False)  

        self.entry_frame.pack_forget() 

    def open_url(self, event):
        url = "https://www.instagram.com/f09l/" 
        webbrowser.open_new(url) 
    def toggle_entry_frame(self, use_proxies=None):
        if self.master.configuration_frame.send_to_telegram_var.get():
            self.entry_frame.pack(side="top", fill="x", pady=5)
            self.entry_frame.pack_propagate(True)
            # Enable all entry widgets
            for child in self.entry_frame.winfo_children():
                if isinstance(child, CTkEntry):
                    child.configure(state="normal")
            self.load_credentials()
        else:
            self.entry_frame.pack_forget()
    def load_credentials(self):
        if os.path.exists("bot_credentials.json"):
            with open("bot_credentials.json", "r") as file:
                data = json.load(file)
                if "id" in data:
                    self.id_entry.insert(0, data["id"])
                if "token" in data:
                    self.token_entry.insert(0, data["token"])