#https://bulkdata.uspto.gov/data/patent/officialgazette/2023/
#https://bulkdata.uspto.gov/data/patent/officialgazette/2023/e-OG20230103_1506-1.zip


import os
import requests 
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def download_zip_file(url, save_path):
    chunk_size = 1024  # Adjust the chunk size as needed
    with requests.get(url, stream=True) as response:
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {os.path.basename(save_path)}", position=0, leave=True)

        with open(save_path, 'wb') as file, ThreadPoolExecutor(max_workers=4) as executor:
            futures = []

            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    # Write the chunk to the file
                    futures.append(executor.submit(file.write, chunk))
                    # Update the progress bar
                    progress_bar.update(len(chunk))

            # Wait for all threads to finish
            for future in futures:
                future.result()

    # Close the progress bar
    progress_bar.close()



def get_patent_data(year):

	baseurl = "https://bulkdata.uspto.gov/data/patent/officialgazette/"
	url1 = urljoin(baseurl, str(year))
	print(url1)

	r = requests.get(url1)
	datas = r.content

	# Check if the request was successful (status code 200)
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
		print(filename)
		save_path = os.path.join(save_dir, filename)
		download_zip_file(links, save_path)

save_dir = "downloaded_files"
os.makedirs(save_dir, exist_ok=True)

get_patent_data(2023)
