import requests
from bs4 import BeautifulSoup
import re
import os
import json

def download_img_from_url(url, dst):
	"""
    Downloads an image from a given URL and saves it to the specified path.

    Parameters:
	    url: the direct URL of the image.
	    dst: the file path where the image will be saved.

    Returns:
    	True if the download is successful, False otherwise.
    """

	headers = {
		"Referer": "https://www.pixiv.net/",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
	}

	response = requests.get(url, headers=headers)

	# if the request fails
	if response.status_code != 200:
		return False

	with open(dst, 'wb') as handler:
		handler.write(response.content)
	
	return True

def download_imgs_from_artwork_id(artwork_id, folder_path, verbose=False):
	""" 
    Downloads all images from a given Pixiv artwork/illust.

    Parameters:
	    artwork_id: the ID of the artwork, expected to be string
	    folder_path: the folder where all images will be saved.

	Returns:
		A list of images that failed to download
    """
	os.makedirs(folder_path, exist_ok=True)

	artwork_id = str(artwork_id)

	# fetch the artwork's HTML
	url = f"https://www.pixiv.net/en/artworks/{artwork_id}"
	html_doc = requests.get(url).text

	soup = BeautifulSoup(html_doc, 'lxml')

	meta = soup.find_all("meta")[-1]

	content = meta.get("content")
	content = json.loads(content)  # parse JSON
	# print(json.dumps(content, indent=4)) # prettify

	# get metadata to construct the url to download individual images
	temp_dict = content["illust"][artwork_id]["userIllusts"][artwork_id]
	page_count = temp_dict["pageCount"]
	# create_date = temp_dict["createDate"].split("+")[0].replace("-", "/").replace(":", "/").replace("T", "/")
	create_date = temp_dict["updateDate"].split("+")[0].replace("-", "/").replace(":", "/").replace("T", "/")
	
	# to keep track of the list of images that failed to download
	failed = []

	for i in range(page_count):
		img_and_page = f"{artwork_id}_p{i}"
		img_path = os.path.join(folder_path, f"{img_and_page}.jpg")
		img_url = f"https://i.pximg.net/img-master/img/{create_date}/{img_and_page}_master1200.jpg"

		if verbose:
			print(f"Attempting to download from url: {img_url}")

		if download_img_from_url(img_url, img_path):
			print(f"Downloaded {img_and_page}")
		else:
			print(f"Download {img_and_page} --FAILED--")
			failed.append(img_and_page)

	return failed