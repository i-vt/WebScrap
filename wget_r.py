import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def recursive_download(base_url, current_url, save_directory, visited):
    if current_url in visited:
        return
    visited.add(current_url)

    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    create_directory(save_directory)

    for link in soup.find_all('a', href=True):
        href = link['href']
        next_url = urljoin(current_url, href)
        next_save_path = os.path.join(save_directory, os.path.basename(next_url))

        if is_valid_url(next_url) and base_url in next_url:
            if next_url.endswith('/'):
                next_save_directory = os.path.join(save_directory, href.strip('/'))
                create_directory(next_save_directory)
                recursive_download(base_url, next_url, next_save_directory, visited)
            else:
                download_file(next_url, next_save_path)

if __name__ == "__main__":
    base_url = "http://example.com"
    save_directory = "downloaded_files"
    visited_urls = set()

    create_directory(save_directory)
    recursive_download(base_url, base_url, save_directory, visited_urls)
