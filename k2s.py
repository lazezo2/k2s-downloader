import sys
import time
import requests
import contextlib
from io import BytesIO
from random import choice
from concurrent.futures import as_completed

from PIL import Image
from tqdm import tqdm
from requests_futures.sessions import FuturesSession

from utils import get_working_proxies

DOMAINS = [
    # "keep2share.cc",
    "k2s.cc",
    # "tezfiles.com",
    # "fboom.me",
    # "fast-download.me"
]

def generate_from_key(url: str, key: str, proxy: str) -> str:

    if proxy:
        prox = {'https': f'http://{proxy}'}
    else:
        prox = None
    
    while True:
        with contextlib.suppress(Exception):
            r = requests.post(f"https://{choice(DOMAINS)}/api/v2/getUrl", json={
                "file_id": url,
                "free_download_key": key
            }, proxies=prox).json()
            return r['url']

def generate_download_urls(file_id: str, count: int = 1, skip: int = 0) -> list:
    
    
    if skip > 0:
        proxy_urls = get_working_proxies()[skip:]
    else:
        proxy_urls = get_working_proxies()
    working_link = False
    free_download_key = ""
    urls = []
    captcha = requests.post(f"https://{choice(DOMAINS)}/api/v2/requestCaptcha").json()
    r = requests.get(captcha["captcha_url"])
    
    """
    # in windows
    im = Image.open(BytesIO(r.content))
    im.show()
    
    # Save the image to a file
    #captcha_image_path = 'captcha_image.png'
    #im.save(captcha_image_path)
    """
    
    # in google colab
    
    # Assuming r.content contains the image data
    image_data = r.content

    # Save the image directly from the content to a file
    captcha_image_path = 'captcha_image.png'
    with open(captcha_image_path, "wb") as file:
        file.write(image_data)  
    
    """
    # not work in colab!!
    # Display the image using Colab's tools
    from IPython.display import Image as IPImage, display

    display(IPImage(filename=captcha_image_path))
    # end of " in google colab"
    """
    
    response = input(f"Enter captcha response: ")

    for url in proxy_urls:
        print(f"\033[KTrying {url}", end='\r')
        prox = {'https': f'http://{url}'}
        if not url:
            prox = None
        while not working_link:
            try:
                free_r = requests.post(f"https://{choice(DOMAINS)}/api/v2/getUrl", json={
                    "file_id": file_id,
                    "captcha_challenge": captcha["challenge"],
                    "captcha_response": response
                }, proxies=prox, timeout=5).json()
            except KeyboardInterrupt:
                sys.exit()
            except :
                break

            if free_r['status'] == "error":
                if free_r["message"] == "Invalid captcha code":
                    r = requests.get(captcha["captcha_url"])
                    
                    """
                    # in windows
                    im = Image.open(BytesIO(r.content))
                    im.show()
                    """
                    
                    # in google colab
    
                    # Assuming r.content contains the image data
                    image_data = r.content

                    # Save the image directly from the content to a file
                    captcha_image_path = 'captcha_image.png'
                    with open(captcha_image_path, "wb") as file:
                        file.write(image_data)  
        
                    response = input(f"Enter captcha response (2): ")
                    continue
                elif free_r["message"] == "File not found":
                    sys.exit("File not found")

            if "time_wait" not in free_r:
                working_link = True
                break

            if free_r['time_wait'] > 30:
                break

            for i in range(free_r['time_wait'] - 1):
                print(f"\033[K[{url}] Waiting {free_r['time_wait'] - i} seconds...", end='\r')
                time.sleep(1)
            
            free_download_key = free_r['free_download_key']
            working_link = True

        if working_link:

            session = FuturesSession(max_workers=5)
            futures = []

            # Generate links
            while len(urls) < count:
                futures = []
                to_generate = count - len(urls)
                for _ in range(to_generate):
                    future = session.post(f"https://{choice(DOMAINS)}/api/v2/getUrl", json={
                        "file_id": file_id,
                        "free_download_key": free_download_key
                    }, proxies=prox)
                    futures.append(future)

                for future in tqdm(as_completed(futures), total=len(futures), leave=False):
                    try:
                        result = future.result()
                        urls.append(result.json()['url'])
                    except KeyboardInterrupt:
                        sys.exit()
                    except:
                        continue

    if not working_link:
        raise Exception("No working links found")
    """
    # Save the URLs to a file
    save_file_path = "downloaded_urls.json"
    with open(save_file_path, 'w') as file:
        json.dump(urls, file)
    save_file_path1 = "downloaded_urls1.json"
    with open(save_file_path1, 'w') as file:
        json.dump(urls[:count], file)
    """
    
    """
    # read urls from file
    import json
    urls = []
    file_path = "downloaded_urls.json"
    def load_download_urls(file_path: str = 'downloaded_urls.json') -> list:
      with open(file_path, 'r') as file:
        urls = json.load(file)
      #print(urls)
      return urls
    urls = load_download_urls(file_path)
    """
    return urls[:count]
    

def get_name(file_id: str) -> str:
    r = requests.post(f"https://{choice(DOMAINS)}/api/v2/getFilesInfo", json={
        "ids": [file_id]
    }).json()
    return r['files'][0]['name']
