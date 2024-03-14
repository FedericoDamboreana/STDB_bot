import requests

class FlowHelper:

    def __init__(self) -> None:
        pass

    def is_related(self, question):
        url = 'http://192.168.0.253:5001/related'
        headers = {'Content-Type': 'application/json'}
        data = {'question': question}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Error: {response.status_code}'
    
    def is_chained(self, question):
        url = 'http://192.168.0.253:5001/chained'
        headers = {'Content-Type': 'application/json'}
        data = {'question': question}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Error: {response.status_code}'