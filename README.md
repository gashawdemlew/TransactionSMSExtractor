# Financial and Transaction Related SMS Extractor

## Description

This repository provides an **API** to extract important information from financial and transactional SMS messages. The API is specifically designed for SMS received from:

- **Banks**: CBE Bank, Awash Bank, COOP Bank, Amara Bank, and more.
- **Telecom Service Providers**: Ethio-Telecom, Safaricom, and others.
- **Ride Transport Service Providers**: Ride, Feres, and others.
- **Credit Service Providers**: Telebirr, Apollo, and more.

The API is tailored to support services in **Ethiopia** and is built using two approaches:

1. **Regex-based Pattern Matching**: Extracts information by building regex patterns for specific SMS formats.
2. **Prompt Engineering with LLMs**: Utilizes **Gemini API** for advanced natural language processing. Learn more about the Gemini API [here](https://ai.google.dev/gemini-api/docs?_gl=1*m1rf45*_ga*MTIyMzI1NTA1MS4xNzM5NTc2MDIw*_ga_P1DBVKWT6V*MTczOTU3NjAyMC4xLjEuMTczOTU3NjAzMS40OS4wLjExOTQzNDc4NjA.).

---

## Features

The API provides the following features:

- **Data Extraction**:
  - Transaction amount
  - Remaining balance
  - Transaction type (debit/credit)
  - Transaction date and time
  - Sender and recipient details
- **Localization**: Designed for Ethiopian service providers, ensuring high accuracy for local use cases.
- **Deployment Options**:
  - Run locally
  - Deploy on on-premise servers or cloud platforms (e.g., Huggingface, Vercel, etc.).

---

## Prerequisites

Before starting, ensure the following are installed:

- **Python**: Version 3.11.5 or higher.
- **Git**: To clone the repository.
- **Docker**: If you plan to use Docker for deployment.

---

## Installation and Usage

Follow these steps to set up and run the API:

### 1. Clone the Repository

Clone the repository to your local machine and navigate into the project folder:

```bash
git clone https://github.com/gashawdemlew/TransactionSMSExtractor.git
cd TransactionSMSExtractor
```
### 2. Check Python Version
Ensure your Python version is 3.11.5 or higher. Run the following command:
```bash
python --version
```
---

### 3. Set Up a Virtual Environment (Optional but Recommended)
To avoid dependency conflicts, create and activate a virtual environment:
On Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Once activated, your terminal prompt should show the virtual environment name (e.g., (venv)).
