from bs4 import BeautifulSoup
import os, json

start_dir = "/"

def get_all_dirs(start_dir: str = "/"):
    pages = []
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            page_path = os.path.join(root, filename)
            try: int(filename)
            except: continue
            pages.append(page_path)
    return pages
  
pages = get_all_dirs(start_dir)
dump_full = []
for page in pages:
    dump = {}
    dump["id"] = f"{page.split("/")[-2]}_{page.split("/")[-1]}"
    with open(page, "r") as open_file: contents = open_file.read()
    soup = BeautifulSoup(contents, 'html.parser')
    current_div = soup.find('div', class_='grid-item')
    while current_div:
        h4_text = current_div.find('h4').text.strip()
        span_text = current_div.find('span').text.strip()
        dump[h4_text]  = span_text
        current_div = current_div.find_next_sibling('div', class_='grid-item')
    img_tags = soup.find_all('img')
    img_sources = [img['src'] for img in img_tags]
    dump["images"] = img_sources
    dump_full.append(dump)
#for dump in dump_full: print(dump)

#json_data = json.dumps(dump_full, indent=4)
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(dump_full, json_file, ensure_ascii=False, indent=4)
