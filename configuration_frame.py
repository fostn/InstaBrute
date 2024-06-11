from customtkinter import CTkFrame, CTkLabel, CTkCheckBox,BooleanVar

class ConfigurationFrame(CTkFrame):
    def __init__(self, master, right_frame, width=200, height=140):
        super().__init__(master, width=width, height=height)

        self.right_frame = right_frame

        self.label = CTkLabel(self, text="Configuration")
        self.label.pack(padx=5, pady=(5, 0), anchor="w")
        
        self.send_to_telegram_var = BooleanVar()
        self.use_proxy_var = BooleanVar()

        self.send_to_telegram_checkbox = CTkCheckBox(self, text="Send to Telegram bot", variable=self.send_to_telegram_var, command=self.right_frame.toggle_entry_frame)
        self.send_to_telegram_checkbox.pack(padx=5, pady=5, anchor="w")

        self.use_proxy_checkbox = CTkCheckBox(self, text="Use Proxies", variable=self.use_proxy_var)
        self.use_proxy_checkbox.pack(padx=5, pady=5, anchor="w")
        
        self.pack_propagate(False)

    def get_configuration(self):
        send_to_telegram = self.send_to_telegram_var.get()
        use_proxy = self.use_proxy_var.get()
        return send_to_telegram, use_proxy
