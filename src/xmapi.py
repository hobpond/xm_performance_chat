import os
import requests

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

API_PATH = "/api/xm/1"
GROUPS_PATH = "/groups"
GROUP_PERFORMANCE_PATH = "/performance/groups"
OAUTH_PATH = "/oauth2/token"

load_dotenv()
XM_BASE_URL = os.getenv("xmatters.base_url")
XM_KEY = os.getenv("xmatters.user")
XM_SECRET = os.getenv("xmatters.secret")
XM_CLIENT_ID = os.getenv("xmatters.client_id")
XM_CLIENT_SECRET = os.getenv("xmatters.client_secret")
XM_PATH = os.getenv("xmatters.path")

class RequestException(Exception):
    pass

class XMApi(BaseModel):
    base_url: str = Field(XM_BASE_URL, description="The base api url for your xMatters instance. For example https://acme.xmatters.com")
    key: str = Field(XM_KEY, description="The access key for xMatters.")
    secret: str = Field(XM_SECRET, description="The secret pair for the acceses key to xMatters.")

    class Config:
        title = "xmapi"
        description = "xMatters base class to ineract with xMatters' api"

        @staticmethod
        def schema_extra(schema, model):
            schema['examples'] = [
                {
                    'base_url': 'https://acme.xmatters.com',
                    'key': 'my_key',
                    'secret': 'my_secret'
                }
            ]

    def standard_headers(self):
        access_token = self.get_access_token().get("access_token")
        return {"Authorization": f"Bearer {access_token}"}
    
    def standard_auth(self):
        return HTTPBasicAuth(self.key, self.secret)

    def get_group(self, target_name):
        url = self.base_url + API_PATH + GROUPS_PATH + f"/{quote(target_name)}"
        params = {
            "embed": "supervisors,services"
        }
        return self.validate_response(requests.get(url, params=params, auth=self.standard_auth()))

    def get_group_performance(self, start_time_utc, end_time_utc):
        params = {
            "limit": 10,
            "offset": 0,
            "sortBy": "alerts.total",
            "sortOrder": "DESCENDING",
            "from": start_time_utc,
            "to": end_time_utc
        }
        return self.validate_response(requests.get(XM_BASE_URL + XM_PATH + GROUP_PERFORMANCE_PATH, params=params, headers=self.standard_headers()))

    def get_one_group_performance(self, target_name, start_time_utc, end_time_utc):
        group_uuid = self.get_group(target_name).get("id")
        params = {
            "limit": 10,
            "offset": 0,
            "parentGroup": group_uuid,
            "sortBy": "alerts.total",
            "sortOrder": "DESCENDING",
            "from": start_time_utc,
            "to": end_time_utc
        }
        return self.validate_response(requests.get(XM_BASE_URL + XM_PATH + GROUP_PERFORMANCE_PATH, params=params, headers=self.standard_headers()))

    def get_access_token(self):
        params = {
            "grant_type": "password",
            "client_id": XM_CLIENT_ID,
            "client_secret": XM_CLIENT_SECRET,
            "username": self.key,
            "password": self.secret,
            "scope": "ui-proxy"
        }
        return self.validate_response(requests.post(self.base_url + API_PATH + OAUTH_PATH, params=params))
      
    def validate_response(self, response):
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            raise RequestException("Request failed with status code: " + str(response.status_code))
