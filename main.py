#main.py
import launcher
import smart_scrapper
import time
import sys

def run_automation_suite():
    
    print("\n[PHASE 1] Launching Application and Aligning UI...")
    setup_success = launcher.launch_and_prepare()
    
    if not setup_success:
        print("\n CRITICAL ERROR: Could not prepare the environment.")
        print("Automation terminated to prevent coordinate mismatch.")
        sys.exit()
    
    print("\n Environment Ready. Switching to Extraction Mode...")
    time.sleep(2) 

    print("\n[PHASE 2] Starting Smart Scraper...")
    try:
        smart_scrapper.run_intelligent_scraper()
        print("\n Extraction Cycle Completed Successfully.")
    except Exception as e:
        print(f"\n ERROR during scraping: {e}")
        sys.exit()

    print("ALL PHASES COMPLETE")
  

if __name__ == "__main__":
    run_automation_suite()
