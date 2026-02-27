#launcher.py
import pyautogui
import time
import webbrowser

# Configuration
TARGET_URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
ANCHOR_IMAGE = 'anchor_header.png'

def launch_and_prepare():
    print(" Starting Launcher...")

    print(f"Opening {TARGET_URL}...")
    webbrowser.open(TARGET_URL)
    time.sleep(5) 

    print("Maximizing window to ensure coordinate consistency...")
    pyautogui.hotkey('win', 'up') 
    time.sleep(2)

    max_scroll_attempts = 20
    found = False

    print(f"Scanning for table header '{ANCHOR_IMAGE}'...")

    for attempt in range(max_scroll_attempts):
        try:
            
            header_location = pyautogui.locateOnScreen(ANCHOR_IMAGE, confidence=0.7)
            
            if header_location:
                print(f" Table found on scroll attempt {attempt}!")
                
                pyautogui.scroll(-300) 
                found = True
                break
        except Exception:
            pass
        
        print(f"   [Attempt {attempt+1}] Table not visible yet. Scrolling down...")
        pyautogui.scroll(-500) 
        time.sleep(1) 

    if found:
        print(" Environment is perfectly aligned for scraping.")
        return True
    else:
        print(" ERROR: Could not find the table after 20 scrolls.")
        print("Check if anchor_header.png matches your screen resolution.")
        return False

if __name__ == "__main__":
    launch_and_prepare()