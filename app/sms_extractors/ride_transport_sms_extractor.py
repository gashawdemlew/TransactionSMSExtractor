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

class TransportRideExtractor:
    def __init__(self, sms_data):
        self.sms_data = sms_data
    
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
    
    def transport_sms_extraction(self):
        try:
            # create empty dictionary
            sms_info_dict = {}
            extracted_information = {}

            # Iterate over the items
            for item in self.sms_data:
                body = item['body']
                channel = item['channel']
                date = item['date']
            
                if channel in ['Little', 'Adika 7000', '8202']:
                
                    financial_keywords = ["cost", "fare", "ዋጋ፡", "ዋጋ"]

                    found = any(keyword in body for keyword in financial_keywords)
                    
                    if found:
                        try:
                            print("Text body:",body)
                            genai.configure(api_key=ConfigStaticFiles.GOOGLE_API_KEY)

                            model = genai.GenerativeModel('gemini-pro')
                            
                            response = model.generate_content(f"In this given transaction SMS text, {body}, please extract important informations like trip cost and trip date, in json format of key:value")
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
                                "trip_cost": sms_cleaned_json.get("trip_cost"),
                                "trip_date": sms_cleaned_json.get("trip_date"),
                                "date": date
                            }
                            
                            numeric_date = int(self.convert_date_to_number(date))
                            extracted_information[sms_info_dict['sms_channel']+ str(numeric_date)] = sms_info_dict
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
    
    extract_sms = TransportRideExtractor(sms_data)
    extracted_transport_expense = extract_sms.transport_sms_extraction()
    
    print(extracted_transport_expense)