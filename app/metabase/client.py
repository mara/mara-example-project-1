
import requests
import json

from . import config

class MetabaseClient(object):
    def __init__(self):
        """A client for interacting with the Metabase api"""
        self.metabase_url=config.internal_metabase_url()
        self.session_id = None

        response = requests.post(
            self.metabase_url + '/api/session',
            json={'username': config.metabase_admin_email(),
                  'password': config.metabase_admin_password()})

        if response.status_code == 200:
            self.session_id = response.json()['id']
        else:
            raise Exception(f'{response.status_code}: {response.text}')


    def request(self, method, path, data = None):
        print(f'{method.__name__} {self.metabase_url + path} {json.dumps(data) if data else ""}')
        response = method(self.metabase_url + path, headers={'X-Metabase-Session': self.session_id}, json=data)
        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f'{response.status_code}: {response.text}')
        elif response.text:
            return response.json()
        else:
            return None

    def get(self, path) -> dict:
        return self.request(requests.get, path)

    def post(self, path, data=None) -> dict:
        return self.request(requests.post, path, data)

    def put(self, path, data=None) -> dict:
        return self.request(requests.put, path, data)

    def delete(self, path, data=None) -> dict:
        return self.request(requests.delete, path, data)
