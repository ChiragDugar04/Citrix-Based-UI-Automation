import pyautogui
import pytesseract
import time
import re
import pandas as pd
import sys

# 1. SETUP
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\chiragd\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def get_current_table_view():
    """Finds the table on the current screen and returns the capture region."""
    try:
        header_pos = pyautogui.locateOnScreen('anchor_header.png', confidence=0.7)
        if header_pos:
            # FIX: We start 50 pixels ABOVE the header to make sure we catch 
            # the first rows like China/India that are right at the top.
            left = int(header_pos.left)
            top = int(header_pos.top - 50) 
            width = int(header_pos.width + 500)
            height = 800 
            return (left, top, width, height)
        return None
    except Exception:
        return None

def clean_text(raw_text):
    cleaned_rows = []
    lines = raw_text.split('\n')
    
    # regex: Handles noise, captures Country, Population, and Percentage
    pattern = r'(?:[a-zA-Z]{1,3}\s+)?([A-Z][a-zA-Z\s\.\(\)]+)\s+([\d,]{5,})\s+([\d.]*%)'
    
    for line in lines:
        if "World" in line: continue 
        match = re.search(pattern, line)
        if match:
            country = match.group(1).strip()
            pop = match.group(2).strip()
            perc = match.group(3).strip()
            cleaned_rows.append((country, pop, perc))
    return cleaned_rows

def run_intelligent_scraper():
    all_data = []
    last_batch_first_item = None
    pages_to_attempt = 12 

    print("🚀 Starting Intelligent Scraper...")
    
    
    print("Resetting to top of page...")
    pyautogui.press('home')
    time.sleep(2)

    for i in range(pages_to_attempt):
        print(f"\n--- Processing Batch {i+1} ---")
        
        dynamic_region = get_current_table_view()
        
        if not dynamic_region:
            print("⚠️ Table not found. Attempting to scroll and find it...")
            pyautogui.press('down', presses=10)
            time.sleep(1)
            continue

        screenshot = pyautogui.screenshot(region=dynamic_region)
        # screenshot.save(f"debug_batch_{i}.png") # Helpful to check if it sees China/India
        
        raw_text = pytesseract.image_to_string(screenshot, config='--psm 6')
        current_batch = clean_text(raw_text)
        
        if not current_batch:
            print("⚠️ No data matched. Scrolling...")
            pyautogui.scroll(-400)
            time.sleep(1)
            continue

        # Anti-Duplicate Check
        if current_batch[0][0] == last_batch_first_item:
            print(f"🔄 Duplicate detected. Forcing scroll...")
            pyautogui.press('pagedown')
            time.sleep(2)
            continue

        all_data.extend(current_batch)
        last_batch_first_item = current_batch[0][0]
        print(f"✅ Added {len(current_batch)} rows. First: {last_batch_first_item}")

        # Standard scroll for next batch
        pyautogui.press('pagedown')
        time.sleep(2) 

    df = pd.DataFrame(all_data, columns=['Country', 'Population', 'Percentage'])
    df = df.drop_duplicates(subset=['Country'])
    df.to_csv('intelligent_scraped_data.csv', index=False)
    print(f"\n🏆 Success! {len(df)} unique records saved.")

if __name__ == "__main__":
    run_intelligent_scraper()
