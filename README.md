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

---

### 4. Install Required Python Packages
Install all dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
Ensure the installation is successful and all required packages are installed.

---

### 5. Get a Gemini API Key
The API requires access to the Gemini API for advanced NLP tasks. Follow these steps to obtain your API key:

Visit the Gemini API Key Generator.
Log in with your Google account.
Generate an API key and copy it.

---

### 6. Configure Environment Variables
To securely use the Gemini API key, save it as an environment variable. Create a .env file in the config folder (or at the root of your project) and add the following line:
```bash
GEMINI_API_KEY=<your_gemini_api_key>
```
Replace <your_gemini_api_key> with the API key you copied earlier.

If you don’t have a config folder, create it manually and add the .env file inside.

---

### 7. Run the API

You can run the API in two ways:

a) Run the Script Directly

Start the API by running the main.py script:
```bash
python main.py
```
The server will start, and the API will be available at:
```bash
http://localhost:8002
```

b) Use Docker (Optional)
If you prefer to use Docker for containerized deployment:

Build the Docker image:
```bash
docker build -t sms-extractor .
```
Run the Docker container:
```bash
docker run -p 8000:8000 sms-extractor
```

---

### 8. Test the API
Once the API is running, test it using the following methods:

a) Using cURL
b) Using Postman
c) Using Test Data
Use the sample SMS data provided in the testData folder to validate the API. Replace the SMS content in the test request with any of the examples from the folder.

---

### 9. Deploy the API (Optional)

You can deploy the API to a cloud platform for public access. Deployment options include:

a) Huggingface Spaces
b) Vercel
After deployment, you’ll receive a public URL to access the API.

---

### Full Example Workflow
Here is an example of the complete workflow:

1. Clone the repository.
2. Check Python version and set up a virtual environment.
3. Install dependencies.
4. Obtain a Gemini API key and configure it in a .env file.
5. Run the API locally or with Docker.
6. Test the API using sample SMS messages.
7. Optionally, deploy the API to the cloud for public use.

---

### Tips
- Regularly update the requirements.txt file to ensure compatibility with the latest Gemini API and Python versions.
- Secure your API key by not hardcoding it in the code. Always use environment variables.
- Use the provided testData folder to validate changes before deploying.

---

### Technologies Used
- Python: Programming language.
- FastAPI: Framework for building the API.
- Regular Expressions (Regex): For pattern matching.
- Gemini API: For advanced NLP with prompt engineering.
- Docker: For containerized deployment.
- Cloud Platforms: For hosting the API, such as Huggingface or Vercel.

---

### Test Deployed API
The API is deployed on Hugging Face space, Please [here](https://huggingface.co/spaces/gashudemman/TransactionSMSExtractorAPI).here to test.

---

### Contribution
Contributions are welcome! If you'd like to improve the project or add new features:

- Fork the repository.
- Create a new branch for your changes.
- Submit a pull request.

---

### License
This project is licensed under the MIT License.

---

### Contact
For any questions or support, feel free to reach out:

- Email: gashudemman@gmail.com
- LinkedIn: https://www.linkedin.com/in/gashaw-demlew-b35865150/
