import requests
from bs4 import BeautifulSoup
import re
import os
import json

HEADERS = {
		"Referer": "https://www.pixiv.net/",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
	}

def download_img_from_url(url, dst):
	"""
    Downloads an image from a given URL and saves it to the specified path.

    Parameters:
	    url : string
	    	The direct URL of the image.
	    dst : string
	    	The file path where the image will be saved.

    Returns:
    	bool
    		True if the download is successful, False otherwise.
    """

	response = requests.get(url, headers=HEADERS)

	# if the request fails
	if response.status_code != 200:
		return False

	with open(dst, 'wb') as handler:
		handler.write(response.content)
	
	return True

def download_imgs_from_artwork_id(artwork_id, folder_path, max_retry=10, verbose=False):
	""" 
    Downloads all images from a given Pixiv artwork/illust.

    Fetches the image metadata for a given Pixiv artwork ID,
    constructs the URLs for each page/image in the artwork, 
    and attempts to download them into the specified folder. 

    If any images fail to download, they are recorded and returned.

    Doesn't have exception handler.

    Parameters:
	    artwork_id : int
	    	The ID of the artwork,
	    folder_path : string
	    	The folder where all images will be saved.
	    max_retry : int, default=10
	    	The maximum number of retries to fetch artwork metadata.
	    verbose : bool
	    	If True, prints additional information during the download process.

	Returns:
		failed : list of string
			A list of artworks' artwork_ids that failed to download
    """

	os.makedirs(folder_path, exist_ok=True)

	artwork_id = str(artwork_id)

	n_retry = 1

	# fetch the artwork's HTML
	url = f"https://www.pixiv.net/en/artworks/{artwork_id}"

	# recently some artworks don't have metadata about
	# images within it due to unknown reasons.
	# retry fetching the artwork page in case this happens.
	while n_retry <= max_retry:
		if verbose:
			print(f"attempt no.{n_retry}")

		html_doc = requests.get(url, headers=HEADERS).text

		soup = BeautifulSoup(html_doc, 'lxml')

		meta = soup.find_all("meta")[-1]

		meta_content = meta.get("content", "")

		if not meta_content.startswith("sentry"):
			# found artwork's info about images within it
			break

		n_retry += 1

	content = meta.get("content")
	# this will throw an exception if the metadata isn't fetched
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