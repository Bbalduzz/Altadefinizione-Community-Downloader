import requests
from random import choice
from bs4 import BeautifulSoup
import webbrowser
import os, sys
from datetime import datetime, timedelta
from colorama import Fore

class WebRequests():
    def __init__(self, token):
        self.token = token
        self.headers: dict = {
            'Authorization': f'Bearer {self.token}',
        }

class AltadefinizioneExploit:
    def __init__(self):
        self.updated_domain = self.new_domain()
        self.session = requests.Session()
        new_user = self.register()
        self.new_token = new_user['token']
        self.new_ver_code = new_user['ver_code']
        self.new_userid = new_user['id']
        self.session.headers.update(WebRequests(self.new_token).headers)
        self.verify_email(new_user['id'], new_user['ver_code'])

    def progress_bar(self, progress, total, film_name):
        percent = 100 * (progress / float(total))
        bar = '█' * int(percent) + '-' * (100 - int(percent))
        print(f'\r[+] Downloading {film_name}... |{bar}| {percent:.2f}%', end='\r')

    def new_domain(self):
        r = requests.get('https://altadefinizione-nuovo.click/').content
        soup = BeautifulSoup(r, 'html.parser')
        domain = soup.select('h2 > a')[0].text.split('.')[-1]
        return domain

    def email_ud(self):
        email = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%') for _ in range(10)])
        return f"{email}@{''.join([choice('abcdefghijklmnopqrstuvwxyz') for _ in range(4)])}.{''.join([choice('abcdefghijklmnopqrstuvwxyz') for _ in range(2)])}"
    def verify_email(self, user_id, verification):
        self.session.get(f'https://altadefinizionecommunity.{self.updated_domain}/api/verify/email/{user_id}/{verification}')

    def register(self):
        rand_pass = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_=+)') for _ in range(10)])
        rand_email = self.email_ud()
        req = requests.post(f'https://altadefinizionecommunity.{self.updated_domain}/api/register', 
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

    def search_content(self, query):
        slugs = []
        types = []
        results = self.session.get(f'https://altadefinizionecommunity.online/api/autocomplete?search={query}').json()
        for i,r in enumerate(results['results']):
            print(f"    {i}. [{Fore.WHITE}{r['type']}{Fore.RESET}] {r['text']} {Fore.CYAN}({Fore.RESET}{r['final_quality']}{Fore.CYAN}){Fore.RESET}")
            slugs.append(r['slug'])
            types.append(r['type'])
        c = int(input(f'{Fore.YELLOW}●{Fore.RESET} Enter ID: '))
        return slugs[c],types[c]

    def check_media(self, url):
        r = self.session.get(f'https://altadefinizione-originale.{self.updated_domain}/api/posts/slug/{url.split("/")[-1]}').json()
        return r['post']['type']
            
    def get_serie(self, serie_url):
        serie_name = serie_url.split('?')[0].removeprefix(f'https://altadefinizionecommunity.{self.updated_domain}/p/')
        serie = self.session.get(
            f'https://altadefinizionecommunity.{self.updated_domain}/api/posts/seasons/{serie_name}',
        ).json()
        seasons = [(season['season_label'], len(season['episodes'])) for season in serie['seasons']]
        all_urls = []
        for n,season in enumerate(seasons):
            print(season[0])
            urls = []
            for episode in range(season[1]):
                print(f'    ⇢ {Fore.WHITE}Episode{Fore.RESET} {episode+1}')
                ep = []
                r = self.session.get(f'https://altadefinizionecommunity.online/api/post/urls/stream/{serie_url.split("/")[-1]}/{n}/{episode}').json()
                for stream in r['streams']:
                    ep.append(stream['url'])
                    print(f"        {Fore.WHITE}Quality{Fore.RESET}: {stream['resolution']['name']}, {stream['download_size']}")
                urls.append(ep)
            all_urls.append(urls)
        to_download = input(f'{Fore.YELLOW}●{Fore.RESET} Enter the season, episode and quality u want to download {Fore.WHITE}(format: 1-1-1){Fore.RESET}: ').split('-')
        wod = input(f'{Fore.YELLOW}●{Fore.RESET} Watch online or Download? [{Fore.GREEN}W{Fore.RESET} / {Fore.GREEN}D{Fore.RESET} / {Fore.MAGENTA}d-all{Fore.RESET} {Fore.WHITE}to download all episodes of all series{Fore.RESET}]: ').lower()
        match wod:
            case 'w':
                webbrowser.open(all_urls[int(to_download[0])-1][int(to_download[1])-1][int(to_download[2])-1])
            case 'd':
                self.download_serie([all_urls[int(to_download[0])-1][int(to_download[1])-1][int(to_download[2])-1]], token, serie_name)
            case 'd-all':
                print(f'{Fore.RED}►{Fore.RESET} Make sure you have enough disk space!')
                self.download_serie(all_urls, token, serie_name)
            case other:
                print('not a valid option')

    def download_serie(self, urls, serie_name):
        try: os.mkdir('SERIES')
        except: pass
        for n,url in enumerate(urls):
            r = self.session.get(url, stream=True)
            total_length = int(r.headers.get('content-length'))
            dl = 0
            self.progress_bar(dl, total_length, serie_name)
            with open(f'SERIES/{serie_name}-{n}.mp4', 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)
                        dl += len(chunk)
                        self.progress_bar(dl, total_length, serie_name)
        print(f'\n {serie_name} downloaded')

    def get_film(self, film_url):
        film_name = film_url.split('/')[-1]
        film = self.session.get(
            f'https://altadefinizionecommunity.{self.updated_domain}/api/post/urls/stream/{film_name}',
        ).json()

        print(f'== {Fore.GREEN}Options{Fore.RESET} ==\n')
        urls = []
        for n, stream in enumerate(film['streams']):
            urls.append(stream['url'])
            size = stream['download_size']
            res = stream['resolution']['name']
            print(f'{Fore.GREEN}[{Fore.RESET}{n+1}{Fore.GREEN}]{Fore.RESET} Quality: {res}, {size}')
        wod = input(f'\nWatch online or Download? [{Fore.GREEN}W{Fore.RESET} / {Fore.GREEN}D{Fore.RESET}]: ').lower()
        match wod:
            case 'd':
                choice = input(f'{Fore.YELLOW}●{Fore.RESET} Chose the resolution u want to download (enter the nuber in square brackets): ')
                match choice:
                    case '1':
                        self.download_film(urls[0], film_name)
                    case '2':
                        self.download_film(urls[1], film_name)
                    case '3':
                        self.download_film(urls[2], film_name)
                    case '4':
                        self.download_film(urls[3], film_name)
                    case other:
                        print('enter a valid choice!')
            case 'w':
                choice = input(f'{Fore.YELLOW}●{Fore.RESET} Chose the resolution you prefer to watch  (enter the nuber in square brackets): ')
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

    def download_film(self, url, film_name):
        try: os.mkdir('FILMS')
        except: pass
        r = self.session.get(url, stream=True)
        total_length = int(r.headers.get('content-length'))
        dl = 0
        self.progress_bar(0, total_length, film_name)
        with open(f'FILMS/{film_name}.mp4', 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
                    dl += len(chunk)
                    self.progress_bar(dl, total_length, film_name)
        print(f'\n {film_name} downloaded')

    def generate_account(self):
        try: os.mkdir('ACCOUNTS')
        except: pass
        def gen():
            new_user = self.register()
            self.verify_email(new_user['id'], new_user['ver_code'], new_user['token'])
            with open('ACCOUNTS/acounts.txt','a') as f:
                f.write(f'\n{str(datetime.now())}\n')
                f.write(f'[+] expires: {str(datetime.now() + timedelta(hours=24))}\n')
                f.write(f"[+] email: {new_user['email']}\n")
                f.write(f"[+] password: {new_user['password']}\n")
                f.write('='*50)
            print(f"[{Fore.GREEN}+{Fore.RESET}] {Fore.WHITE}Account generated{Fore.RESET}: {new_user['email']} | {new_user['password']}")
        if len(sys.argv) > 1:
             while 1: gen()
        else: gen()
        
    def download(self, url):
        if self.check_media(url) == 'movie':
            self.get_film(url)
        else:
            self.get_serie(url)

if __name__ == '__main__':
    dl = AltadefinizioneExploit()
    use = input(f'{Fore.YELLOW}●{Fore.RESET} What do u wanna do? [({Fore.YELLOW}G{Fore.RESET})enerate/({Fore.YELLOW}D{Fore.RESET})ownload]: ').lower()
    match use:
        case 'g':
            dl.generate_account()
        case 'd':
            if url := input(f'{Fore.YELLOW}●{Fore.RESET} Enter url: '):
                dl.download(url)
