import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import threading
import requests
import re
import time
import webbrowser
import json

class BiomeFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sols RNG Biome Finder")
        self.root.geometry("600x400")

        self.config = self.load_config()
        self.LOG_LIMIT = 100
        self.stop_event = threading.Event()
        self.PREDETERMINED_LINK = "https://www.roblox.com/games/15532962292/Sols-RNG-Eon1-1?privateServerLinkCode="
        self.CHANNEL_ID = "1282542323590496277"
        self.AUTHORIZATION_CODE = self.config["AUTHORIZATION_CODE"]

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        with open('config.json') as config_file:
            return json.load(config_file)

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10, padx=10, fill=tk.X)

        keyword_label = tk.Label(frame, text="Keyword:", font=("Helvetica", 12), bg="white")
        keyword_label.pack(side=tk.LEFT, padx=5)

        self.keyword_entry = tk.Entry(frame, font=("Helvetica", 12), bg="lightgrey", bd=0)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(frame, text="Start", command=self.start_retrieving, font=("Helvetica", 12), bg="green", fg="white", bd=0, disabledforeground="white")
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(frame, text="Stop", command=self.stop_retrieving, font=("Helvetica", 12), bg="red", fg="white", bd=0)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20, font=("Helvetica", 10), bg="white", bd=0)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

    def log_message(self, message):
        timestamp = datetime.now().strftime("[%H:%M]")
        formatted_message = f"{timestamp} {message}"
        print(formatted_message)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, formatted_message + '\n')
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.unload_old_logs()

    def unload_old_logs(self):
        self.text_area.config(state=tk.NORMAL)
        lines = int(self.text_area.index('end-1c').split('.')[0])
        if lines > self.LOG_LIMIT:
            self.text_area.delete('1.0', f'{lines - self.LOG_LIMIT}.0')
        self.text_area.config(state=tk.DISABLED)

    def is_valid_link(self, url):
        return url.startswith(self.PREDETERMINED_LINK)

    def retrieve_messages(self, channelid, keyword):
        limit = 1
        headers = {
            'authorization': self.AUTHORIZATION_CODE
        }
        url_pattern = re.compile(r'https?://\S+')
        backoff = 1

        while not self.stop_event.is_set():
            last_message_id = None
            self.log_message('Searching for servers...')

            while not self.stop_event.is_set():
                query_parameters = f'limit={limit}'
                if last_message_id:
                    query_parameters += f'&after={last_message_id}'

                r = requests.get(
                    f'https://discord.com/api/v9/channels/{channelid}/messages?{query_parameters}', headers=headers
                )
                if r.status_code == 404:
                    self.log_message('Error: Unknown Channel. Please check the channel ID.')
                    return
                elif r.status_code == 429:
                    retry_after = int(r.headers.get('Retry-After', backoff))
                    self.log_message(f'Rate limited. Retrying after {retry_after} seconds.')
                    time.sleep(retry_after)
                    backoff = min(backoff * 2, 60)
                    continue
                elif r.status_code != 200:
                    self.log_message(f'Error: Received status code {r.status_code}')
                    return

                messages = r.json()
                if messages:
                    for message in messages:
                        if isinstance(message, dict):
                            content = message.get('content', '').lower()
                            if content and keyword.lower() in content:
                                urls = url_pattern.findall(message['content'])
                                if urls:
                                    self.log_message(f'Logged one new message containing "{keyword}" and a link: {message["content"]}')
                                    last_message_id = message['id']
                                    for url in urls:
                                        if self.is_valid_link(url):
                                            self.log_message(f'Opening link: {url}')
                                            webbrowser.open(url)
                                    self.log_message('Match found. Waiting for 3 minutes before restarting the search...')
                                    for _ in range(180):
                                        if self.stop_event.is_set():
                                            self.log_message('Stopping message retrieval.')
                                            return
                                        time.sleep(1)
                                    self.log_message('Resuming search...')
                                    break
                else:
                    last_message_id = messages[-1]['id']
                
                if self.config.get("ultra_fast_join"):
                    time.sleep(0.5)
                elif self.config.get("faster_join"):
                    time.sleep(1)
                else:
                    time.sleep(5)

    def start_retrieving(self):
        self.stop_event.clear()
        keyword = self.keyword_entry.get()
        if keyword:
            self.keyword_entry.config(state=tk.DISABLED)
            threading.Thread(target=self.retrieve_messages, args=(self.CHANNEL_ID, keyword)).start()
            self.start_button.config(text="Running", state=tk.DISABLED, disabledforeground="white")
        else:
            messagebox.showerror("Error", "Please enter a keyword")

    def stop_retrieving(self):
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.log_message('Stopping message retrieval.')
            self.start_button.config(text="Start", state=tk.NORMAL)
            self.keyword_entry.config(state=tk.NORMAL)

    def on_closing(self):
        self.stop_retrieving()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BiomeFinderApp(root)
    root.mainloop()