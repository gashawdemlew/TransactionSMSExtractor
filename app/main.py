import sys
import pandas as pd
import numpy as np
import os
import time
import google.generativeai as genai

from datetime import datetime

cur_dir = os.getcwd()
parent_dir = os.path.realpath(os.path.join(os.path.dirname(cur_dir)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    sys.path.append(cur_dir)
sys.path.insert(1, ".")

import uvicorn

from app.datamodels.datamodel import *

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from app.sms_extractors.bank_transaction_sms_extractor import BankTransactionSMSExtractor
from app.sms_extractors.financial_credit_sms_extractor import FinancialCreditExtractor
from app.sms_extractors.ride_transport_sms_extractor import TransportRideExtractor
from app.sms_extractors.telecom_package_extractor import PackageExtractor
from app.sms_extractors.telecom_subscription_extractor import SubscriptionExtractor

from app.config.config_static_resources import ConfigStaticFiles

app = FastAPI(
    title="Financial sms extractor API",
    description="The primary purpose of this API is to extract important information from financial related short messaging service (SMS)\
        like bank transaction, telecom package and subscription, transport sms, and credit sms",
    version="1.0.0",
)

@app.get("/", tags = ['ROOT'])
async def start_root():
    msg = {"Message": "Decision Engine Micro-service"}
    return msg

@app.post("/sms_extractor", tags=["Financial SMS extraction"])
async def extract(
    input_data: SMSExtractedText,
):
    start_time = time.perf_counter()
    
    response = {}
    
    bankTransactionsms = BankTransactionSMSExtractor(ConfigStaticFiles.patterns, input_data.sms_json)
    extracted_TXN_info = bankTransactionsms.sms_extraction_process()
    
    package_sms = PackageExtractor(input_data.sms_json)
    extracted_package_info = package_sms.telecom_package_extraction()
    
    subscription_sms = SubscriptionExtractor(input_data.sms_json)
    extracted_subscription_info = subscription_sms.telecom_subscription_extraction()
    
    financialCredit = FinancialCreditExtractor(input_data.sms_json)
    extracted_financial_credit = financialCredit.financial_credit_sms_extraction()
    
    transportRide_sms = TransportRideExtractor(input_data.sms_json)
    extracted_transport_expense = transportRide_sms.transport_sms_extraction()
    
    response["bank_transaction_sms"] = extracted_TXN_info
    response["telecom_package_sms"] = extracted_package_info
    response["telecom_subscription_sms"] = extracted_subscription_info
    response["credit_service_sms"] = extracted_financial_credit
    response["transport_expense_sms"] = extracted_transport_expense
    
    end_time = time.perf_counter()
    comp_time = end_time - start_time
    print(f"Done with sms extraction! Time taken: {comp_time}")
    
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)