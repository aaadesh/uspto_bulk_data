#https://bulkdata.uspto.gov/data/patent/officialgazette/2023/
#https://bulkdata.uspto.gov/data/patent/officialgazette/2023/e-OG20230103_1506-1.zip


import os
import requests 
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def download_zip_file(url, save_path):
	response = requests.get(url)
	# Check if the request was successful (status code 200)
	if response.status_code == 200:
	# Save the content to a local file
		with open(save_path, 'wb') as file:
			file.write(response.content)
		print(f"Downloaded: {url} to {save_path}")
	else:
		print(f"Failed to download file. Status code: {response.status_code}")


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
