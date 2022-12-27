from utils import exploit
from colorama import Fore

dl = exploit.AltadefinizioneExploit()
if url := input(f'{Fore.YELLOW}●{Fore.RESET} Enter url: '):
	dl.download(url)