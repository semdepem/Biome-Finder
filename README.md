# Sols RNG Biome Finder

## Overview

This program retrieves messages from a specified Discord channel and searches for messages containing a specific keyword. If a message with the keyword is found and contains a valid link, the link is opened in the default web browser. The program uses a graphical user interface (GUI) built with Tkinter to allow the user to input the keyword and control the message retrieval process.

## Requirements

- Python 3.x
- `requests` library
- `tkinter` library (usually included with Python)

## Installation

1. **Clone the repository or download the source code:**
    ```sh
    git clone https://github.com/yourusername/Biome-Finder.git
    cd Biome-Finder
    ```

2. **Install the required Python libraries:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Build the executable using `pyinstaller`:**
    ```sh
    pyinstaller --onefile --windowed --name "Sols RNG Biome Finder" main.py
    ```

## Usage

1. **Navigate to the `dist` directory:**
    ```sh
    cd dist
    ```

2. **Run the `Sols RNG Biome Finder.exe` file to start the program.**

3. **In the GUI, enter the keyword you want to search for in the Discord messages.**

4. **Enter your Discord authorization code in the provided field.**

5. **Click the "Start" button to begin retrieving messages.**

6. **If a message containing the keyword and a valid link is found, the link will be opened in the default web browser.**

7. **Click the "Stop" button to stop retrieving messages.**

## Notes

- Ensure that your Discord authorization code is kept secure and not shared publicly.
- The program uses fixed channel IDs. Update the `CHANNEL_IDS` variable in `main.py` if you need to change the channels.
- The program logs messages to a Tkinter `ScrolledText` widget and the console for easy monitoring.
- **Disclaimer:** Using the "Ultra Fast Join" or "Faster Join" options may cause you to be rate limited or banned from Discord. The program includes checks to handle rate limiting, but use these options at your own risk.

## Author

- This program was created by Sem_De_Pem.
