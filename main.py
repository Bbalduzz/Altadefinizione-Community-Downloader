import requests
from random import choice
from bs4 import BeautifulSoup
import webbrowser

class WebRequests():
    def __init__(self, token):
        self.token = token
        self.headers: dict = {
            'Authorization': f'Bearer {self.token}',
        }

class AltadefinizioneExploit:
    def __init__(self):
        pass

    def yopmail_gen_ud(self):
        req = requests.get('https://yopmail.com/en/alternate-domains').content
        soup = BeautifulSoup(req, 'html.parser')
        ud_domains = [dom.text for dom in soup.select('div.lstdom > div')]
        email = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%') for i in range(10)])
        return email + choice(ud_domains)

    def verify_email(self, user_id, verification, token):
        requests.get(f'https://altadefinizionecommunity.online/api/verify/email/{user_id}/{verification}', headers=WebRequests(token).headers)

    def register(self):
        rand_pass = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_=+)') for i in range(10)])
        rand_email = self.yopmail_gen_ud()
        req = requests.post('https://altadefinizionecommunity.online/api/register', 
            json={"email":rand_email,"password":rand_pass,"password_confirmation":rand_pass,"fingerprint":1117459144040421,"selected_plan":1}
        ).json()
        try:
            return {
                'token': req['token'],
                'email': rand_email,
                'ver_code': req['user']['verification_code'],
                'id': req['user']['id'],
                'password': rand_pass
            }
        except Exception as e:
            print('Something went wrong. The error thrown is', e)
            print(req)

    def get_film(self, token):
        film_url = input('Enter the Film URL:\n')
        film_name = film_url.split('/')[-1]
        film = requests.get(
            f'https://altadefinizionecommunity.online/api/post/urls/stream/{film_name}',
            headers=WebRequests(token).headers,
        ).json()

        print(f'== Options ==\n')
        urls = []
        for n, stream in enumerate(film['streams']):
            urls.append(stream['url'])
            size = stream['download_size']
            res = stream['resolution']['name']
            print(f'[{n+1}] Quality: {res}, {size}')
        wod = input('\nWatch online or Download? [W / D]: \n').lower()
        match wod:
            case 'd':
                choice = input('Chose the resolution u want to download(enter the nuber in square brackets):\n')
                match choice:
                    case '1':
                        self.download_film(urls[0], token)
                    case '2':
                        self.download_film(urls[1], token)
                    case '3':
                        self.download_film(urls[2], token)
                    case '4':
                        self.download_film(urls[3], token)
                    case other:
                        print('enter a valid choice!')
            case 'w':
                choice = input('Chose the resolution you prefer to watch  (enter the nuber in square brackets):\n')
                match choice:
                    case '1':
                        webbrowser.open(urls[0], new=1, autoraise=True)
                    case '2':
                        webbrowser.open(urls[1], new=1, autoraise=True)
                    case '3':
                        webbrowser.open(urls[2], new=1, autoraise=True)
                    case '4':
                        webbrowser.open(urls[3], new=1, autoraise=True)
                    case other:
                        print('enter a valid choice!')

    def download_film(self, url, token):
        r = requests.get(url, stream=True, headers=WebRequests(token).headers)
        print('Downloading ...')
        with open('film.mp4', 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
        print('Done')

    def run(self):
        new_user = self.register()
        self.verify_email(new_user['id'], new_user['ver_code'], new_user['token'])
        self.get_film(new_user['token'])


dl = AltadefinizioneExploit()
dl.run()