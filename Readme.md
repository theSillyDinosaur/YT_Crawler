# Youtube Crawler

Source: https://blog.jiatool.com/posts/youtube_spider_api/

This is the crawler for DLHLP HW5. For those who want a simpler youtube crawler, I suggest that they find another source.  

### AddChannel.py
This file is for adding the channel it'll crawl. With entering the below command:  
```
python3 AddChannel.py
```
You'll enter a basic interface. This python support [inserting/deleting (by title)/listing the title of] channel information in channel.json.

### Crawler.py
This file is the main crawling file. With entering the below command:
```
python3 Crawler.py
```
The program will crawl the latest 100 videos with top 20 comments by default, and store them in data/ folder.
> Before start running the program, you should go to config.json and insert your api key.
