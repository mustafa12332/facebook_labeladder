import requests
import json
import hashlib
import hmac

BASE_URL = "https://graph.facebook.com/v3.3/"


class FacebookRequest:

    def __init__(self, method, relative_url, body):
        self.method = method
        self.url = relative_url
        self.body = body


class Facebook:
    @staticmethod
    def batch_requests_builder(all_requests, access_token):
        batch_request_list = []
        for i in range(0,len(all_requests),50):
            if i+50 < len(all_requests):
                list_of_requests = all_requests[i:i+50]
            else:
                list_of_requests = all_requests[i:len(all_requests)]
            batch_request_string = "["
            for request in list_of_requests:
                batch_request_string += f'{{"method":"{request.method}", "relative_url":"{request.url}", "body":"{request.body}"}},'
            batch_request_string += "]"
            files = {'access_token': (None, access_token),
                     'batch': (None, batch_request_string)}
            batch_request_list.append(files)
        return batch_request_list

    @staticmethod
    def get_label_add_url(label_id, page_access_token,user_id):
        request = FacebookRequest("POST", f"{label_id}/label?access_token={page_access_token}", f"user:{user_id}")
        return request
    @staticmethod
    def build_label_url_for_all_users(label_id,page_access_token,users):
        list_of_requests = []
        for user in users:
            request_object = Facebook.get_label_add_url(label_id,page_access_token,user)
            list_of_requests.append(request_object)
        return list_of_requests
    @staticmethod
    def get_list_of_labels(page_auth_token):
        result = requests.get(BASE_URL + "me/custom_labels", {"fields": "name", "access_token": page_auth_token})
        data = json.loads(result.text)
        data_list = []
        for label in data['data']:
            data_list.append((label['name'], label['id']))
        return data_list

    @staticmethod
    def batch_to_list_of_request_results(result):

        result = json.loads(result)
        data = []
        for item in result:
            data.append(item["body"])
        return data
