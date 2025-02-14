from pydantic import BaseModel,ValidationError
from pydantic import BaseModel, validator, HttpUrl
from typing import Optional, List, Dict,Any
from enum import Enum
from typing import Union
from typing_extensions import Literal
import datetime


class SMSExtractedText(BaseModel):
    sms_json: List[dict] = []