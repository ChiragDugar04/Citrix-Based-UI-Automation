import pyautogui
import pytesseract
from PIL import Image
import time
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\chiragd\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


LEFT = 418
TOP = 222
WIDTH = 1084
HEIGHT = 494

TABLE_REGION = (LEFT, TOP, WIDTH, HEIGHT)
SCROLL_BUTTON = (1909, 994)

def capture_and_read():
    print("Capturing table area...")
    screenshot = pyautogui.screenshot(region=TABLE_REGION)
    
    screenshot.save("debug_capture.png")
    print(f"Screenshot saved to {os.getcwd()}\\debug_capture.png")
    
    custom_config = r'--oem 3 --psm 6'
    
    screenshot_gray = screenshot.convert('L') 
    
    text = pytesseract.image_to_string(screenshot_gray, config=custom_config)
    
    print("\n--- Extracted Data ---")
    print(text)
    return text

if __name__ == "__main__":
    print("Script starting in 5 seconds...")
    print("MAKE SURE THE TABLE IS VISIBLE ON SCREEN!")
    time.sleep(5)
    
    captured_text = capture_and_read()
    
    if captured_text.strip():
        print("\n✅ Phase 1 Success! The OCR read the data.")
    else:
        print("\n❌ Phase 1 Failed: The OCR output is empty. Check debug_capture.png.")
