from dataclasses import dataclass
import logging
import os
import sys
cur_dir = os.getcwd()
parent_dir = os.path.realpath(os.path.join(os.path.dirname(cur_dir)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    sys.path.append(cur_dir)
sys.path.insert(1, ".")


@dataclass
class ConfigStaticFiles:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    batchApi_username: str = f"fast_name"
    batchApi_password: str = f"fast_password"
    batch_api_sms_endpoint: str = f"http://a8a53a205972f43c5abc664530ff3f8f-766311352.us-east-2.elb.amazonaws.com/sms/"
    extractedSMS_S3_storage: str = "s3://kft-lakehouse-zones/cleansed/qena_digital_lending/extracted_sms_sample_data/sms_df.csv"
    extracted_telecom_packages_S3: str = "s3://kft-lakehouse-zones/cleansed/qena_digital_lending/extracted_sms_sample_data/telecom_sms_df.csv"
    extracted_telecom_subscription_S3: str = "s3://kft-lakehouse-zones/cleansed/qena_digital_lending/extracted_sms_sample_data/subscription_sms_df.csv"
    extracted_ride_sms_df_S3: str = "s3://kft-lakehouse-zones/cleansed/qena_digital_lending/extracted_sms_sample_data/ride_sms_df.csv"
    extracted_financial_sms_df_S3: str = "s3://kft-lakehouse-zones/cleansed/qena_digital_lending/extracted_sms_sample_data/financial_sms_df.csv"

    ######
    ROBOWFLOW_API_KEY = os.getenv('ROBOWFLOW_API_KEY')

    patterns = {
        # ====CBEbirr debit, credit, and airtime charging=====
        'CBEBIRR': r'(?:.*?\s(A/C No)\s)?(?P<account>[0-9*]+)?(?P<type>credited|withdrawn|bought).*?\s(?P<amount>\d+(?:,\d{3})*(?:\.\d{2})?)Br ?(\.)(?:.*?\s(to|from)\s)?(?P<source>[ 0-9A-Za-z:]*)??(on)((?:.*?\s(balance|current balance)).*?\s(?P<balance>\d+(?:,\d{3})*(?:\.\d{2})?)Br)?\.?',
        # ====COOPayEBIRR===
        'COOPayEBIRR': r'(?:.*?\s(A/C No)\s)?(?P<account>[0-9*]+)?(?P<type>transferred)\sETB(?P<amount>\d+(?:,\d{3})*(?:\.\d{2})?)(?:.*?\s(to)\s)?(?P<source>[ 0-9A-Za-z:]*)?((?:.*?\s(balance|current balance)).*?\sETB(?P<balance>\d+(?:,\d{3})*(?:\.\d{2})?))?\.?',
        # Transfer from telebirr to other account/bank and bill payment
        'mMoney-1': r'(?P<type>transferred|paid).*?\s(?P<amount>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(account)\s)?(?P<account>[0-9*]+)?(?:\s(to)\s)?(?P<source>[ 0-9A-Za-z/]*)??(on)((?:.*?\s(account balance|Current Balance is|Avail\. Bal\.|available balance|balance now is|Available Bal\.|Current Bal\.|current balance))(.*?\s(?P<balance>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?',
        # receiving from other other account/bank to telebirr and M-pesa
        'mMoney-2': r'(?:.*?\s(A/C No)\s)?(?P<account>[0-9*]+)?(?P<type>received|payment|bought)(?P<amount>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(to|from)\s)?[ 0-9-]*(?P<source>[ A-Za-z/]*)?((?:.*?\s(balance|current balance))(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)))?\.?',
        # ===Telebirr and M-pasa airtime and package bundle
        'mMoney-3': r'(?:.*?\s(A/C No)\s)?(?P<account>[0-9*]+)?(?P<type>bought|recharged)(?P<amount>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?P<source>[ 0-9A-Za-z/]*)??(on)((?:.*?\s(balance|current balance))(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)))?\.?',
        # Gedaa bank credit and debit
        'Bank_Gedaa': r'Dear Customer, ETB(?P<amount>\d+(?:,\d{3})*(?:\.\d{2})?) has been (?P<type>Credited|Debited|Debit|Credit|Transferred from|Transferred to)(?:.*?\s(Acc:)\s)?(?P<account>[0-9*]+)(?:.*?\s(from|to Beneficiary|)\s)?(?P<source>[ 0-9A-Za-z/-]*)? on (?P<date>\d{2} [A-Z]{3} \d{4}). Your available balance is ETB(?P<balance>\d+(?:,\d{3})*(?:\.\d{1})?)',
        # Wegagen bank transfering/ debit
        'Bank_wegagen_1': r'(?:.*?\s(A/C No)\s)?(?P<account>[0-9*]+)?.*?(?P<type>transfered).*?\s(?P<amount>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(from|by|to|)\s)?(?P<source>[ 0-9A-Za-z/]*)??(on)((?:.*?\s(Current Balance is|Avail\. Bal\.|available balance|balance now is|Available Bal\.|Current Bal\.|current balance))(.*?\s(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?',
        # Wegagen bank withdrawal
        'Bank_wegagen_2': r'(?P<type>Withdrawal).*?\s(?P<amount>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(account)\s)?.*?\s(?P<account>[0-9*]+)?.*?(?:.*?\s(from|by|to|)\s)?(?P<source>[ 0-9A-Za-z/]*)??(on)((?:.*?\s(Current Balance is|Avail\. Bal\.|available balance|balance now is|Available Bal\.|Current Bal\.|current balance))(.*?\s(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?',
        # Boa debit and credit
        'Bank_BOA': r'(?:.*?\s(A/C No)\s)?(?P<account>[0-9*]+).*?(?P<type>credited|debited|debit|credit|credited by|debited by|Transferred from|Transferred to).*?\s(?P<amount>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(Info:))(.*?\s(?P<source>[ 0-9A-Za-z/]*)(?:\sto\s(.+))?)((?:.*?\s(Current Balance is|Avail\. Bal:|available balance|balance now is|Available Bal\.|Current Bal\.|current balance))(.*?\s(?P<balance>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?',
        # AwashBank debit and credit
        'Bank_Awash': r"(?:.*?\s(account)\s)?(?P<account>['0-9*]+)?.*?(?P<type>Credited|Debited).*?\s(?P<amount>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(on)\s)?(?P<date>[ 0-9/]*)?(?:.*?\s(from)\s)?(?P<source>[ A-Za-z/]*)?((?:.*?\s(Current Balance is|Avail\. Bal\.|available balance|balance now is|Available Bal\.|Current Bal\.|current balance))(.*?\s(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?",
        # Zemenbank debit and credit
        'Bank_Zemen': r"(?P<amount>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?P<source>[ A-Za-z/]*)?.*?(?P<type>deposit|withdrawal)(?:.*?\s(A/c No.)\s)?(?P<account>[0-9x]+)?((?:.*?\s(Available Bal\.|Current Bal\.))(.*?\s(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?",
        # CBE/CBO/DashenBank
        'Bank_general': r"(?:.*?\s(account)\s)?(?P<account>['0-9*]+)?.*?(?P<type>Credited|Debited|Debit|Credit|Transferred from|Transferred to|transferred).*?\s(?P<amount>(?:ETB|Birr|birr).*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))(?:.*?\s(on)\s)?(?P<date>[ 0-9/]*)?(?:.*?\s(by|to)\s)?(?P<source>[ A-Za-z/]*)?((?:.*?\s(Current Balance is|Avail\. Bal\.|available balance|balance now is|Available Bal\.|Current Bal\.|current balance))(.*?\s(?P<balance>.*?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?))))?\.?",
    }
    
    
