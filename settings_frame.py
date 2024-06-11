from customtkinter import CTkFrame, CTkLabel, CTkSlider, CTkButton, filedialog
import random

class SettingsFrame(CTkFrame):
    def __init__(self, master, use_proxy_var, width=200, height=140):
        super().__init__(master, width=width, height=height)

        self.label = CTkLabel(self, text="Settings")
        self.label.pack(padx=5, pady=(5, 0), anchor="w")
        
        self.threads_slider = CTkSlider(self, from_=0, to=25, command=self.slider_event)
        self.threads_slider.set(1)  
        self.threads_slider.pack(padx=5, pady=5, anchor="w")
        
        self.value_label = CTkLabel(self, text="Threads: 1")
        self.value_label.pack(padx=5, pady=5, anchor="center")
        
        
        self.load_proxies_button = CTkButton(self, text="Load Proxies", command=self.load_proxies, width=10,border_color='#D9D3CC',border_width=1,fg_color='#242424',hover_color='#333333')
        self.load_proxies_button.pack(padx=5, pady=5, anchor="w", side="left", fill="x", expand=True)
        
        self.load_accounts_button = CTkButton(self, text="Load Accounts", command=self.load_accounts, width=12,border_color='#D9D3CC',border_width=1,fg_color='#242424',hover_color='#333333') 
        self.load_accounts_button.pack(padx=5, pady=5, anchor="e", side="right", fill="x", expand=True)
        
        self.pack_propagate(False) 

        self.use_proxy_var = use_proxy_var

        if not use_proxy_var.get():
            self.load_proxies_button.configure(state="disabled")

        use_proxy_var.trace_add("write", self.toggle_load_proxies_button)

    def slider_event(self, value):
        self.value_label.configure(text=f"Threads: {int(value)}")

    def load_proxies(self):
        filename = filedialog.askopenfilename(title="Select Proxies File",filetypes=[("Text files", "*.txt")])
        
        if filename:
            print("Proxies file selected:", filename)
            with open(filename, "r") as file:
                proxies = [line.strip() for line in file.readlines()]
                print("Proxies:", proxies)
            total_proxies = len(proxies)
            self.master.right_frame.total_proxies_label.configure(text=f"Total Proxies: {total_proxies}")
            self.master.set_proxies_file(filename)  


    def load_accounts(self):
        filename = filedialog.askopenfilename(title="Select Accounts File",filetypes=[("Text files", "*.txt")])
        if filename:
            print("Accounts file selected:", filename)
            total_accounts = sum(1 for line in open(filename))
            self.master.set_accounts_file(filename)
            self.master.right_frame.total_accounts_label.configure(text=f"Total Accounts: {total_accounts}")


    def toggle_load_proxies_button(self, *args):
        if self.use_proxy_var.get():
            self.load_proxies_button.configure(state="normal")
        else:
            self.load_proxies_button.configure(state="disabled")
