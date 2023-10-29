#https://bulkdata.uspto.gov/data/patent/officialgazette/2023/
#https://bulkdata.uspto.gov/data/patent/officialgazette/2023/e-OG20230103_1506-1.zip


import os
import requests 
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def download_zip_file(url, save_path):
    chunk_size = 5000

    if os.path.exists(save_path):
        local_size = os.path.getsize(save_path)
        headers = {'Range': f'bytes={local_size}-'}
        mode = 'ab'
    else:
        local_size = 0
        headers = None
        mode = 'wb'

    with requests.get(url, stream=True, headers=headers) as response:
        if response.status_code == 206:
            print(f"Resuming download of {os.path.basename(save_path)}")
        else:
            print(f"Downloading {os.path.basename(save_path)}")

        total_size = int(response.headers.get('content-length', 0)) + local_size
        progress_bar = tqdm(total=total_size, initial=local_size, unit='B', unit_scale=True, desc=f"Downloading {os.path.basename(save_path)}", position=0, leave=True)

        with open(save_path, mode) as file, ThreadPoolExecutor(max_workers=4) as executor:
            futures = []

            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    futures.append(executor.submit(file.write, chunk))
                    progress_bar.update(len(chunk))

            for future in futures:
                future.result()

        progress_bar.close()




def get_patent_data(year):

	baseurl = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/"
	url1 = urljoin(baseurl, str(year))
	print(url1)

	r = requests.get(url1)
	datas = r.content

	if r.status_code == 200:
		print("accessing data")

	soup = BeautifulSoup(datas, 'html.parser')
	#print(soup)
	
	links = soup.find_all('a')
	
	ziplinks = []
	for link in links:
		if link['href'].endswith('.zip'):
			temp = url1 + "/" + link['href']
			ziplinks.append(temp)
	print(ziplinks)

	for links in ziplinks:
		link_parts = links.split('/')
		filename = link_parts[-1]
		filename = os.path.basename(filename)
		#print(filename)
		save_path = os.path.join(save_dir, filename)
		download_zip_file(links, save_path)

save_dir = "downloaded_files"
os.makedirs(save_dir, exist_ok=True)

get_patent_data(2023)
