# Pixiv Image Crawler
Crawl all images from Pixiv on a given artist's artworks page.

## Usage
### 1. Update Account Details  
Modify `account.txt` with your Pixiv credentials:
```
email=your_email  
password=your_password  
username=your_username
```
### 2. Update the URL in `crawl_pixiv.ipynb`
The URL must be in the following format:
```
https://www.pixiv.net/en/users/{artist_id}/artworks?p={page_number}
```
Replace `{artist_id}` with the artist's Pixiv ID and `{page_number}` with the desired page number.
The script will only crawl images from that specified page.
