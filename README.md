# Sols RNG Biome Finder

## Overview

This program retrieves messages from a specified Discord channel and searches for messages containing a specific keyword. If a message with the keyword is found and contains a valid link, the link is opened in the default web browser. The program uses a graphical user interface (GUI) built with Tkinter to allow the user to input the keyword and control the message retrieval process.

## Requirements

- Python 3.x
- `requests` library
- `tkinter` library (usually included with Python)

## Installation

1. **Clone the repository or download the source code.**

2. **Install the required Python libraries:**
    ```sh
    pip install requests
    ```

3. **Install `tkinter` if it is not already installed:**
    - On Windows:
        ```sh
        pip install tk
        ```
    - On macOS:
        ```sh
        brew install python-tk
        ```
    - On Linux (Debian-based):
        ```sh
        sudo apt-get install python3-tk
        ```

4. **Create a [config.json](http://_vscodecontentref_/3) file in the same directory as [main.py](http://_vscodecontentref_/4) and add your Discord authorization code:**
    ```json
    {
        "AUTHORIZATION_CODE": "your_discord_authorization_code",
        "faster_join": false,
        "ultra_fast_join": false
    }
    ```

5. **Update the path to the script in the [AUTOJOINSOLS.BAT](http://_vscodecontentref_/5) file:**
    ```bat
    @echo off
    REM Change directory to the location of your Python script
    cd /d "path_to_your_script_directory"

    REM Run the Python script and minimize the command prompt window
    start /min pythonw main.py

    REM Close the command prompt window
    exit
    ```

## Usage

1. **Run the [AUTOJOINSOLS.BAT](http://_vscodecontentref_/6) file to start the program.**

2. **In the GUI, enter the keyword you want to search for in the Discord messages.**

3. **Click the "Start" button to begin retrieving messages. The keyword entry will be disabled to prevent further edits.**

4. **If a message containing the keyword and a valid link is found, the link will be opened in the default web browser.**

5. **Click the "Stop" button to stop retrieving messages and re-enable the keyword entry.**

## Code Explanation

- **`main.py`**: The main script that contains the logic for retrieving messages from Discord, searching for the keyword, and handling the GUI.
- **`retrieve_messages(channelid, keyword)`**: Function that retrieves messages from the specified Discord channel and searches for the keyword.
- **`log_message(message)`**: Function that logs messages to the GUI and the console.
- **`unload_old_logs()`**: Function that removes old log messages from the GUI to keep the log size manageable.
- **[start_retrieving()](http://_vscodecontentref_/7)**: Function that starts the message retrieval process and disables the keyword entry.
- **[stop_retrieving()](http://_vscodecontentref_/8)**: Function that stops the message retrieval process and re-enables the keyword entry.
- **[on_closing()](http://_vscodecontentref_/9)**: Function that handles the closing of the GUI window and stops the message retrieval process.

## Notes

- Ensure that your Discord authorization code is kept secure and not shared publicly.
- The program uses a fixed channel ID. Update the [CHANNEL_ID](http://_vscodecontentref_/10) variable in [main.py](http://_vscodecontentref_/11) if you need to change the channel.
- The program logs messages to a Tkinter [ScrolledText](http://_vscodecontentref_/12) widget and the console for easy monitoring.
- **Disclaimer**: Enabling the `faster_join` or `ultra_fast_join` options in the [config.json](http://_vscodecontentref_/13) file may result in your account being rate-limited or banned by Discord due to the high frequency of API requests. Use these options at your own risk.

## Author

This program was created by Sem_DE_Pem.

## License

This project is licensed under the MIT License.
