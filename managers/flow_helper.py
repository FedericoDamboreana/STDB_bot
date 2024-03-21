import requests

class FlowHelper:

    def __init__(self) -> None:
        self.base_url = "http://192.168.0.200:8020"
        pass

    def is_related(self, question):
        url = f'{self.base_url}/related'
        headers = {'Content-Type': 'application/json'}
        data = {'question': question}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Error: {response.status_code}'
    
    def is_chained(self, question):
        url = f'{self.base_url}/chained'
        headers = {'Content-Type': 'application/json'}
        data = {'question': question}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Error: {response.status_code}'