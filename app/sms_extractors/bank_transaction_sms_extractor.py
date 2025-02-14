import re
import json
import sys
import os
import google.generativeai as genai

from datetime import datetime

cur_dir = os.getcwd()
parent_dir = os.path.realpath(os.path.join(os.path.dirname(cur_dir)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    sys.path.append(cur_dir)
sys.path.insert(1, ".")


from config.config_static_resources import ConfigStaticFiles

class BankTransactionSMSExtractor:
    def __init__(self, pattern, sms_data):
        self.patterns = pattern
        self.sms_data = sms_data
    
    def extract_transaction_info(self, pattern, text):
        try:
            transaction_info = {}

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                transaction_info['account'] = match.group('account')
                transaction_info['type'] = match.group('type')
                transaction_info['amount'] = match.group(
                    'amount').split()[-1] if match.group('amount') else None
                transaction_info['source'] = match.group('source')

                if match.group('source'):
                    words = match.group('source').split()
                    length = len(words)
                    substring = ' '.join(words[:min(length, 4)])
                    transaction_info['source'] = substring
                else:
                    transaction_info['source'] = None
                transaction_info['balance'] = match.group(
                    'balance').split()[-1] if match.group('balance') else None

                return transaction_info
        except Exception as e:
            print(f"Error in SMS extraction: {e}")
            raise
    
    def convert_date_to_number(self, date_str):
        # Define possible date formats
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d','%Y-%m-%dT%H:%M:%S.%f%z']
        
        for fmt in formats:
            try:
                # Try to parse the date
                date = datetime.strptime(date_str, fmt)
                return date.timestamp()  # Return the timestamp as a number
            except ValueError:
                continue  # Try the next format if current one fails
        
        return None  # Return None if no format matches
    
    def sms_extraction_process(self):
        try:
            # create empty dictionary
            sms_info_dict = {}
            extracted_information = {}

            # Iterate over the items
            for item in self.sms_data:
                body = item['body']
                channel = item['channel']
                date = item['date']

                pattern = ""

                # Define the patterns based on the channel
                if channel in ["CBE", "CBO", "DashenBank", "Dashen Bank"]:
                    pattern = self.patterns["Bank_general"]
                elif channel == "wegagenBank":
                    pattern = self.patterns["Bank_wegagen_2"] if "Withdrawal" in body else self.patterns["Bank_wegagen_1"]
                elif channel == "BOA":
                    pattern = self.patterns["Bank_BOA"]
                elif channel == "ZemenBank":
                    pattern = self.patterns["Bank_Zemen"]
                elif channel == "AwashBank" or channel == "Awash Bank":
                    pattern = self.patterns["Bank_Awash"]
                elif channel == "GedaaBank":
                    pattern = self.patterns["Bank_Gedaa"]
                elif channel == "127":
                    if "transferred" in body or "paid" in body:
                        pattern = self.patterns["mMoney-1"]
                    elif "recharged" in body:
                        pattern = self.patterns["mMoney-3"]
                    else:
                        pattern = self.patterns["mMoney-2"]
                elif channel == "M-pesa":
                    pattern = self.patterns["mMoney-2"] if "received" in body else self.patterns["mMoney-3"]
                elif channel == "COOPayEBIRR":
                    pattern = self.patterns["COOPayEBIRR"]
                elif channel == "CBEBirr" or channel == "CBE-Birr" or channel == "CBE Birr":
                    pattern = self.patterns["CBEBIRR"]

                # Check if the pattern is not empty
                if pattern:
                    transaction_info = self.extract_transaction_info(pattern, body)

                    # if extraction is okey
                    if transaction_info:
                        sms_info_dict["sms_channel"] = channel
                        sms_info_dict["bank_account"] = transaction_info["account"]
                        # Identifiy transaction type (credit vs debit)
                        if transaction_info["type"] in ["credited", "transferred to", "received", "Credited", "deposit"]:
                            sms_info_dict["type"] = "credit"
                            source = transaction_info["source"]

                            if transaction_info["type"] in ["deposit"]:
                                sms_info_dict["from"] = channel
                                sms_info_dict["to"] = channel
                                sms_info_dict["reason"] = "Cash deposit"
                            elif channel == "CBEBirr" or channel == "CBE-Birr" or channel == "CBE Birr":
                                sms_info_dict["from"] = "CBE"
                                sms_info_dict["to"] = channel
                                sms_info_dict["reason"] = "Cash deposit"
                            elif source is not None and "deposit" in source.lower():
                                sms_info_dict["from"] = "Telebirr"
                                sms_info_dict["to"] = channel
                                sms_info_dict["reason"] = None
                            elif source is not None and "telebirr" in source.lower():
                                sms_info_dict["from"] = "Telebirr"
                                sms_info_dict["to"] = channel
                                sms_info_dict["reason"] = None
                            else:
                                sms_info_dict["from"] = transaction_info["source"]
                                sms_info_dict["to"] = channel
                                sms_info_dict["reason"] = None
                            # sms_info_dict["from"] = transaction_info["source"]

                        elif transaction_info["type"] in ["bought", "paid", "payment", "recharged", "Credited", "withdrawn", "Withdrawal"]:
                            sms_info_dict["type"] = "debit"
                            sms_info_dict["from"] = channel
                            sms_info_dict["to"] = channel

                            source = transaction_info.get("source")
                            if source is not None:
                                source = source.lower()
                                reasons = {
                                    "airtime": "Airtime payment",
                                    "package": "Package subscription payment",
                                    "atm": "ATM withdrawal",
                                    "bill": "Bill payment",
                                    "tax": "Tax payment",
                                    "electric": "Electric service payment",
                                    "water": "Water service payment",
                                    "airplane": "Airplane ticket payment"
                                }
                                sms_info_dict["reason"] = next((reason for substring, reason in reasons.items(
                                ) if substring in source), "other service payment")
                            else:
                                sms_info_dict["reason"] = "Other service payment"
                        else:
                            sms_info_dict["type"] = "debit"
                            sms_info_dict["from"] = channel

                            source = transaction_info["source"]
                            if source is not None and "atm" in source.lower():
                                sms_info_dict["to"] = channel
                                sms_info_dict["reason"] = "ATM Withdrawal"
                            elif source is not None and "telebirr" in source.lower():
                                sms_info_dict["to"] = "Telebirr"
                                sms_info_dict["reason"] = None
                            else:
                                sms_info_dict["to"] = transaction_info["source"]
                                sms_info_dict["reason"] = None

                        sms_info_dict["amount"] = transaction_info["amount"]
                        sms_info_dict["balance"] = transaction_info["balance"]
                        sms_info_dict["date"] = date
                        
                        numeric_date = int(self.convert_date_to_number(date))
                        extracted_information[sms_info_dict['sms_channel']+ str(numeric_date)] = sms_info_dict 
                elif channel in ['Tsehay Bank', 'Berhan Bank', 'ENAT BANK', 'Tsedey Bank', 'Awash Bank', 'LIB']:
                    
                    financial_keywords = ["credited", "transferred to", "received", "Credited", "deposit", "bought", "paid", "payment", "recharged", "Credited", "withdrawn", "Withdrawal"]

                    found = any(keyword in body for keyword in financial_keywords)
                    
                    if found:
                        try:
                            print("Text body:",body)
                            genai.configure(api_key=ConfigStaticFiles.GOOGLE_API_KEY)

                            model = genai.GenerativeModel('gemini-pro')
                            
                            response = model.generate_content(f"In this transaction SMS text input, {body}, please extract important information like account, check transaction is credit or debit, amount of credit or debit, transaction from, transaction to, current balance, transaction reason, and transaction_date, in json format of key:value")
                            response.resolve()
                            generated_text =response.text.strip()
                            sms_json = response.text.replace('\n', ' ').replace('```', ' ').replace('\\','')

                            sms_json = sms_json.replace("json", "")
                            sms_json = sms_json.replace("JSON", "")
                            sms_json = sms_json.replace('(', '').replace(')', '')

                            sms_cleaned_json = json.loads(sms_json)
                            
                            print("sms_cleaned_json", sms_cleaned_json)
                            
                            sms_info_dict = {
                                "sms_channel":channel,
                                "bank_account": sms_cleaned_json.get("account"),
                                "type": None,
                                "from": sms_cleaned_json.get("transaction_from"),
                                "to": sms_cleaned_json.get("transaction_to"),
                                "reason": sms_cleaned_json.get("transaction_reason"),
                                "amount": None,
                                "balance": sms_cleaned_json.get("current_balance"),
                                "date": date
                            }

                            for key, value in sms_cleaned_json.items():
                                if "check" in key or "type" in key:
                                    sms_info_dict["type"] = value
                                if "amount" in key:
                                    sms_info_dict["amount"] = value
                            
                            numeric_date = int(self.convert_date_to_number(date))
                            extracted_information[sms_info_dict['sms_channel']+ numeric_date] = sms_info_dict
                            
                        except Exception as e:
                            print(e)
                    else:
                        print("No suitable pattern exists for the channel:", channel)
                else:
                    print("No suitable pattern exists for the channel:", channel)
                    
            return extracted_information
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    json_path = os.path.join(os.path.dirname(__file__), "testData/sms_json.json")
        
    with open(json_path, 'r') as file:
        sms_data = json.load(file)
    
    extract_sms = BankTransactionSMSExtractor(ConfigStaticFiles.patterns, sms_data)
    extracted_TXN_info = extract_sms.sms_extraction_process()
    
    print(extracted_TXN_info)
