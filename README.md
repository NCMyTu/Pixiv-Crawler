# Pixiv Image Crawler
Crawl all images from Pixiv on a given artist's artworks page.

## ⚠️ Important Notice
Pixiv no longer returns metadata on artwork pages, so I have written a new script.

**Use `crawl_pixiv_new.ipynb` only. The old one will not work correctly.**

This new approach relies heavily on browser automation, which makes it difficult to parallelize.

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
