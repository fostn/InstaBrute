from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel
from configuration_frame import ConfigurationFrame
from settings_frame import SettingsFrame
from right_frame import RightFrame
from checker import Checker
import os
import atexit
class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Instagram guess by f09l")
         
        self.geometry("600x320")
        self.resizable(False, False)
        self._set_appearance_mode("dark")
      
        self.right_frame = RightFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.id = self.right_frame.id_entry.get()
        self.bot_token = self.right_frame.token_entry.get()
     
        self.configuration_frame = ConfigurationFrame(self, self.right_frame, width=210, height=105)
        self.configuration_frame.pack(side="top", anchor="nw", padx=10, pady=(10, 5))

        
        self.settings_frame = SettingsFrame(self, self.configuration_frame.use_proxy_var, width=210, height=150)
        self.settings_frame.pack(side="top", anchor="nw", padx=10, pady=(5, 10))

        
        self.accounts_file = None
        self.proxies_file = None

        
        self.configuration_frame.use_proxy_var.trace_add("write", self.toggle_load_proxies_button)

        self.checker = Checker(self, self.configuration_frame.use_proxy_var,self.configuration_frame.send_to_telegram_var,self.id, self.bot_token)
        


        self.start_button = CTkButton(self, text="Start", command=self.toggle_checking, width=10,border_color='#D9D3CC',border_width=1,fg_color='#242424',hover_color='#333333')
        self.start_button.pack(padx=5, pady=5, anchor="w", fill="x", expand=True)

        
        self.toggle_load_proxies_button()
    
    def set_accounts_file(self, filename):
        self.accounts_file = filename
        self.right_frame.accounts_file_label.configure(text=f"Accounts File Name: {os.path.basename(filename)}")

    def toggle_checking(self):
        if self.start_button.cget("text") == "Start":
            self.checker.start_checking(self.update_button_text)
        else:
            self.checker.stop_checking(self.update_button_text)

    def update_button_text(self, text):
        self.start_button.configure(text=text)


    def set_proxies_file(self, filename):
        self.proxies_file = filename
        self.right_frame.proxies_file_label.configure(text=f"Proxies File Name: {os.path.basename(filename)}")
        
    def toggle_load_proxies_button(self, *args):
        
        if self.configuration_frame.use_proxy_var.get():
            self.settings_frame.load_proxies_button.configure(state="normal")
        else:
            self.settings_frame.load_proxies_button.configure(state="disabled")

app = App()
app.mainloop()
