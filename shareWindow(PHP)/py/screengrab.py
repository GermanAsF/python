import pygetwindow as gw
import mss
import mss.tools
import ctypes
import json
import requests
import time

def load_config():
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print("Configuration file 'config.json' not found.")
        exit()

def save_config(config):
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

def capture_window(window_title, cutoffs):
    # Get all windows titles
    windows = gw.getWindowsWithTitle(window_title)
    
    # Find the window whose title starts with the provided input
    for window in windows:
        if window.title.startswith(window_title):
            # Get the monitor scaling factor
            scaling_factor = get_monitor_scaling()

            # Calculate the relative coordinates within the window
            rel_left = int(cutoffs["left"] * scaling_factor)
            rel_top = int(cutoffs["top"] * scaling_factor)
            rel_right = int((window.width - cutoffs["right"]) * scaling_factor)
            rel_bottom = int((window.height - cutoffs["bottom"]) * scaling_factor)

            monitor = {"top": window.top + rel_top, "left": window.left + rel_left, 
                       "width": rel_right - rel_left, "height": rel_bottom - rel_top}

            # Take screenshot of the window's content
            with mss.mss() as sct:
                screenshot = sct.grab(monitor)

            # Save the screenshot as 'screencap.png' and overwrite if it already exists
            screenshot_path = "screencap.png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)

            return screenshot_path

def get_monitor_scaling():
    # Get the monitor scaling factor
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    hdc = user32.GetDC(None)
    horizontal_dpi = gdi32.GetDeviceCaps(hdc, 88)  # 88 is the value for LOGPIXELSX
    scaling_factor = horizontal_dpi / 96.0  # 96 is the default DPI value
    user32.ReleaseDC(None, hdc)
    return scaling_factor

def confirm_window():
    confirmation = input("Is the screenshot of the correct window? (yes/no): ").lower()
    return confirmation == "yes"

def adjust_cutoff(window_title, cutoffs, config):
    while True:
        print("Current cutoffs:")
        for key, value in cutoffs.items():
            print(f"{key.capitalize()}: {value}")

        section = input("Select section to adjust (Top/Bottom/Left/Right), or 'done' to finish: ").lower()
        if section == "done":
            break

        if section in cutoffs:
            adjustment = input(f"Enter adjustment for {section.capitalize()} (e.g., +5, -5, 5): ").strip()
            try:
                if adjustment.startswith("+"):
                    cutoffs[section] += int(adjustment[1:])
                elif adjustment.startswith("-"):
                    cutoffs[section] -= int(adjustment[1:])
                else:
                    cutoffs[section] = int(adjustment)
            except ValueError:
                print("Invalid adjustment. Please enter a number.")

            # Save the configuration file with adjusted cutoffs
            save_config(config)

            # Take a new screenshot to show the changes
            capture_window(window_title, cutoffs)
        else:
            print("Invalid section. Please select from Top, Bottom, Left, or Right.")

def send_to_api(api_url, password, screenshot_path):
    # Prepare the payload for the API request
    payload = {"password": password}

    # Prepare the files to be sent (the screenshot)
    files = {"file": open(screenshot_path, "rb")}

    try:
        # Send the POST request to the API
        response = requests.post(api_url, data=payload, files=files)
        if response.status_code == 200:
            print("Screenshot successfully sent to the API.")
            print("API Response:", response.text)
        else:
            print("Failed to send screenshot to the API.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending screenshot to the API: {e}")



def main():
    # Load configuration from config.json
    config = load_config()
    api_url = config["api"]["url"]
    password = config["api"]["pass"]
    cutoffs = config["cutoffs"]

    print(password)
    print(api_url)

    window_title = input("Enter the starting characters of the window title you want to capture: ")
    screenshot_path = capture_window(window_title, cutoffs)
    print(f"Screenshot saved screencap.png")

    if not confirm_window():
        return

    adjust_cutoff(window_title, cutoffs, config)

    # Update config.json with adjusted cutoffs
    config["cutoffs"] = cutoffs
    save_config(config)

    # Ask for the interval
    interval = int(input("Enter the interval in seconds for sending screenshots to the API: "))
    if interval <= 0:
        print("Interval should be a positive integer. Exiting.")
        return

    # Confirm sending screenshots to the API
    if input("Do you want to send screenshots to the API at specified interval? (yes/no): ").lower() != "yes":
        return

    # Send screenshots to the API at specified interval
    while True:
        screenshot_path = capture_window(window_title, cutoffs)
        send_to_api(api_url, password, screenshot_path)
        time.sleep(interval)

if __name__ == "__main__":
    main()
