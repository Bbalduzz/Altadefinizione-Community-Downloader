## Tools
### Account Generator
La funzione `register()` registra un nuovo utente con credenziali random precedentemente generate. Questa funzione ritorna un `dict` con le seguenti informazioni:
    1. `'token'` --> necessario per le richieste al sito
    2. `'email'` 
    3. `'ver_code'` --> codice per verificare il nuovo account
    4. `'id'` --> id utente per verificare l'account
    5. `'password'`
Successivamente la funzione `verify_email()` si occupa di verificare il nuovo account. Questa funzione accetta 2 argomenti: `'id'` e `'ver_code'`.
La funzione `generate_account()` serve per generare solamente un account random. Non viene usata in altre funzioni.
##### Esempio
```python
new_user = self.register()
self.verify_email(new_user['id'], new_user['ver_code'])
```
### Downloader
La sezione si divide in 2 parti: **movie** and **tvshows**
A ogni download, viene generato un account nuovo (guardare sezione prima).
La funzione primcipale è `download()`, accetta 1 argomento: l'url del film/serie che si vuole scaricare. La funzione per prima cosa controlla di che tipo è il contenuto che vuoi scaricare tramite la funzione `check_media()`. Questa accetta 1 argomento (l'url).
Successivamente a seconda che sia un film o una serie chiama le funzioni `get_film()` o `get_serie()`. Entrambe accettano 1 argomento: l'url. Queste funzioni permettono di sciegliere se guardare il contenuto o scaricarlo e la qualità da scaricare. Successivamente chiamano rispettivamente `download_film()` e `download_serie()`. Accettano entrambe 2 argomenti, l'url e il titolo del contenuto.
##### Esempio
```python
dl = exploit.AltadefinizioneExploit()
if url := input(f'Enter url: '):
    dl.download(url)
```

### Seach Content
La funzione `search_content()` accetta 1 argomento: il nome del film. Restituisce i diversi risultati e un `tuple` formato da `slug` (nome unico per quel contentuto) e `type` (movie o tvshow).
##### Esempio
```python
dl = exploit.AltadefinizioneExploit()
slug,media = dl.search_content(movie.name)
dl.download(f'https://altadefinizionecommunity.{dl.updated_domain}/p/{slug}')
```

## Usage examples
- [Nexploix](https://github.com/Bbalduzz/Nexploix): netflix movie downloader by Bbalduzz