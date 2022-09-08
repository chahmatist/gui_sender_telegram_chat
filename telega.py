import json

from requests import Session


class Telega:
    def __init__(self, token):
        self.session = Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        self.baseurl = 'https://api.telegram.org/'
        self.token = token

    def get_chat_id(self):
        url = self.baseurl + 'bot' + str(self.token) + '/getUpdates'
        r = self.session.get(url)
        return r.json()

    def send_message(self, token, chat_id, text):
        url = self.baseurl + 'bot' + str(token) + '/sendMessage?chat_id=' + str(chat_id) + '&text=' + str(text)
        r = self.session.get(url)
        data = r.json()
        print(data)
        return data
