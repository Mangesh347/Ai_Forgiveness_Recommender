import subprocess
import time

# Function to run main.py in the background
def run_in_background():
    subprocess.Popen(['python', 'main.py'])

if __name__ == "__main__":
    run_in_background()
    print("Your Flask app is now running in the background!")

    # Keep the main script alive while the background script runs
    while True:
        time.sleep(10)  # Keeps the script alive to prevent exit
