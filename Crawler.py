import src.YTSpider as Spider
import src.JSON as JSON
import os
import tqdm

YOUTUBE_API_KEY = "AIzaSyAx_LGql8R3j9edTsXFJJ0VAtbw1nIbIi8"

def main():
    channel_list = JSON.read_JSON('channel')
    yts = Spider.YoutubeSpider(YOUTUBE_API_KEY)
    if not os.path.isdir("data"):
        os.mkdir("data")
    for channel in channel_list:
        print(f"start getting playist of {channel['title']}")
        if not os.path.isdir(f"data/{channel['id']}"):
            os.mkdir(f"data/{channel['id']}")
        videos = yts.get_playlist(channel['uploads'], max_results = 100)
        JSON.save_JSON(videos, name = f"data/{channel['id']}/playlist")
        if not os.path.isdir(f"data/{channel['id']}/video"):
            os.mkdir(f"data/{channel['id']}/video")
        pbar = tqdm.tqdm(videos)
        for video in pbar:
            pbar.set_description(f"Fetching {video['id']}")
            video_info = yts.get_video(video['id'])
            comments = yts.get_comments(video['id'], max_results = 100)
            JSON.save_JSON({"video_info": video_info, "comments": comments}, name = f"data/{channel['id']}/video/{video_info['id']}_info")

if __name__ == "__main__":
    main()