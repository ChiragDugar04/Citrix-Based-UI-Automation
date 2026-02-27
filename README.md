# Citrix Vision: Intelligent UI Scraper & MySQL Data Pipeline

![Automation Flow](https://img.shields.io/badge/Status-Enterprise--Ready-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![RPA](https://img.shields.io/badge/Focus-Citrix%20Automation-orange)

## 🚀 Overview
This project is an advanced, vision-based Robotic Process Automation (RPA) suite designed specifically for **Citrix-based environments**. In Citrix sessions, traditional DOM-based scrapers fail because the application is served as a live video stream. 

This suite overcomes the "Citrix Wall" by using **Computer Vision (OCR)** to act as the robot's eyes and **Real-time MySQL Synchronization** to ensure data persistence during the scraping process.

---

## 🛠️ Tech Stack
* **Python**: Core orchestration and logic.
* **PyAutoGUI**: Human-like UI interaction (scrolling, window management).
* **PyTesseract (OCR)**: Image-to-text conversion using the Tesseract engine.
* **MySQL**: Enterprise-grade relational database for persistent storage.
* **Pandas**: Data structuring, deduplication, and CSV export.
* **Regex**: Intelligent noise filtering for OCR text cleaning.

---

## 📐 System Architecture
The project follows a modular **Single Responsibility Principle** architecture:

1. **Phase 1: Launcher (`launcher.py`)** — Automatically navigates to the target URL, maximizes the window, and uses a **Visual Search Loop** to find anchor images (`anchor_header.png`) to ensure the environment is ready.

2. **Phase 2: Intelligent Scraper (`smart_scraper.py`)** — Uses **Dynamic Region Detection** to establish a capture zone. It employs "Smart Scrolling" logic that tracks the state of the report to prevent duplicate data entry.

3. **Phase 3: Database Handler (`database_handler.py`)** — A dedicated module that manages the MySQL lifecycle. It uses atomic transactions to sync batches in real-time as they are scraped.

4. **Phase 4: Orchestrator (`main.py`)** — The central entry point that manages the end-to-end execution flow.

---

## 🌟 Key Features
* **Resilience to Latency**: The bot re-anchors its vision every scroll to handle shifting UI elements or network lag.
* **Real-time Persistence**: Data is committed to MySQL per batch. If the script is interrupted, no data is lost.
* **Resolution Independence**: Uses image-matching rather than hardcoded coordinates to locate table regions.
* **Anti-Duplicate Logic**: Compares current batch headers with historical data to ensure the page actually turned.

---

## 📋 Prerequisites & Setup

### 1. Tesseract OCR
Install the Tesseract OCR engine on your machine and note the path to `tesseract.exe`.

### 2. Database Schema
Create the database in your MySQL environment:
```sql
CREATE DATABASE world_stats;
USE world_stats;
CREATE TABLE country_population (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255) UNIQUE,
    population VARCHAR(100),
    percentage VARCHAR(50),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Installation
```bash
pip install pyautogui pytesseract pandas mysql-connector-python
```

---

## 🚦 How to Run

1. Ensure your MySQL server is running.
2. Update `DB_CONFIG` in `database_handler.py` with your credentials.
3. Run the master controller:

```bash
python main.py
```

---

## 📈 Future Roadmap
* **Discrepancy Auditor**: Post-processing script to mathematically validate OCR totals.
* **Deep Learning**: Integration of YOLO models for more complex object detection in legacy UIs.
