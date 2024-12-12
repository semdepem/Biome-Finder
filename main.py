import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import threading
import requests
import re
import time
import webbrowser

class BiomeFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sols RNG Biome Finder")
        self.root.geometry("800x600")

        self.LOG_LIMIT = 100
        self.stop_event = threading.Event()
        self.PREDETERMINED_LINK = "https://www.roblox.com/games/15532962292/Sols-RNG-Eon1-1?privateServerLinkCode="

        self.ultra_fast_join = False
        self.faster_join = False

        self.CHANNEL_IDS = {
            "Biomes": "1282542323590496277",
            "Merchants": "1282543762425516083"
        }

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10, padx=10, fill=tk.X)

        keyword_label = tk.Label(frame, text="Keyword:", font=("Helvetica", 12), bg="white")
        keyword_label.pack(side=tk.LEFT, padx=5)

        self.keyword_entry = tk.Entry(frame, font=("Helvetica", 12), bg="lightgrey", bd=0)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        auth_label = tk.Label(frame, text="Authorization Code:", font=("Helvetica", 12), bg="white")
        auth_label.pack(side=tk.LEFT, padx=5)

        self.auth_entry = tk.Entry(frame, font=("Helvetica", 12), bg="lightgrey", bd=0, show="*")
        self.auth_entry.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(frame, text="Start", command=self.start_retrieving, font=("Helvetica", 12), bg="green", fg="white", bd=0, disabledforeground="white")
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(frame, text="Stop", command=self.stop_retrieving, font=("Helvetica", 12), bg="red", fg="white", bd=0)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        toggle_frame = tk.Frame(self.root, bg="white")
        toggle_frame.pack(pady=10, padx=10, fill=tk.X)

        self.ultra_fast_join_button = tk.Button(toggle_frame, text="Ultra Fast Join: OFF", command=self.toggle_ultra_fast_join, font=("Helvetica", 12), bg="blue", fg="white", bd=0)
        self.ultra_fast_join_button.pack(side=tk.LEFT, padx=5)

        self.faster_join_button = tk.Button(toggle_frame, text="Faster Join: OFF", command=self.toggle_faster_join, font=("Helvetica", 12), bg="orange", fg="white", bd=0)
        self.faster_join_button.pack(side=tk.LEFT, padx=5)

        search_label = tk.Label(toggle_frame, text="Searching for:", font=("Helvetica", 12), bg="white")
        search_label.pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar(value="Biomes")
        self.search_dropdown = tk.OptionMenu(toggle_frame, self.search_var, "Biomes", "Merchants")
        self.search_dropdown.config(font=("Helvetica", 12), bg="lightgrey", bd=0)
        self.search_dropdown.pack(side=tk.LEFT, padx=5)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=25, font=("Helvetica", 10), bg="white", bd=0)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

    def toggle_ultra_fast_join(self):
        self.ultra_fast_join = not self.ultra_fast_join
        state = "ON" if self.ultra_fast_join else "OFF"
        self.ultra_fast_join_button.config(text=f"Ultra Fast Join: {state}")
        self.log_message(f"Ultra Fast Join {state}")

    def toggle_faster_join(self):
        self.faster_join = not self.faster_join
        state = "ON" if self.faster_join else "OFF"
        self.faster_join_button.config(text=f"Faster Join: {state}")
        self.log_message(f"Faster Join {state}")

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

    def start_retrieving(self):
        keyword = self.keyword_entry.get().strip()
        self.AUTHORIZATION_CODE = self.auth_entry.get().strip()
        if not keyword:
            self.log_message('Error: Please enter a keyword.')
            return
        if not self.AUTHORIZATION_CODE:
            self.log_message('Error: Please enter the authorization code.')
            return
        self.stop_event.clear()
        threading.Thread(target=self.retrieve_messages, args=(keyword,)).start()

    def retrieve_messages(self, keyword):
        headers = {
            'Authorization': self.AUTHORIZATION_CODE,
            'User-Agent': 'Mozilla/5.0'
        }
        url_pattern = re.compile(r'https?://\S+')
        backoff = 1
        limit = 2
        channelid = self.CHANNEL_IDS[self.search_var.get()]

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
                    self.log_message(f'Enter a valid Authorization code in the config file.')
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
                                            
                                            self.log_message('Pausing for 3 minutes')
                                            for _ in range(180):
                                                if self.stop_event.is_set():
                                                    return
                                                time.sleep(1)

                if self.ultra_fast_join:
                    for _ in range(5):
                        if self.stop_event.is_set():
                            return
                        self.log_message('Looking for servers with 0.5 second delay...')
                        time.sleep(0.1)
                elif self.faster_join:
                    for _ in range(10):
                        if self.stop_event.is_set():
                            return
                        self.log_message('Looking for servers with 1 second delay...')
                        time.sleep(0.1)
                else:
                    for _ in range(50):
                        if self.stop_event.is_set():
                            return
                        self.log_message('Looking for servers with 5 second delay...')
                        time.sleep(0.1)

    def stop_retrieving(self):
        self.stop_event.set()
        self.log_message('Stop button pressed, stopping program')

    def on_closing(self):
        self.stop_event.set()
        self.log_message('Window closed, stopping program')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BiomeFinderApp(root)
    root.mainloop()