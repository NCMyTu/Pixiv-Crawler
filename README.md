# Pixiv Image Crawler
Crawl all images from Pixiv on a given artist's artworks page.

## ⚠️ Important Notice
**Use `crawl_pixiv_new.ipynb` only. The old one will not work correctly.**

## ⚠️ Performance Note
This crawler is bottlenecked on the step that fetches image URLs from each individual artwork.
Because Pixiv no longer provides metadata directly on the artist or artwork listing pages, the script must visit each artwork page separately to collect image URLs, which slows down the crawling process, especially for artists with many artworks.

If you want to speed things up, feel free to run multiple instances in parallel or exploring Pixiv’s API (it's broken anyway).

## Usage
### 1. Update Account Details  
Modify `account.txt` with your Pixiv credentials:
```
email=your_email  
password=your_password  
username=your_username
```

### 2. Set the Artist ID in `crawl_pixiv_new.ipynb`
Open the `crawl_pixiv_new.ipynb` file and locate the following line:
```python
artist_id =  # Fill this in
```
