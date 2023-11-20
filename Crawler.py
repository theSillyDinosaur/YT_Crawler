import src.YTSpider as Spider
import src.JSON as JSON
import os
import tqdm

def main():
    config = JSON.read_JSON("Config")
    YOUTUBE_API_KEY = config['api_key']
    renew = config['renew']
    channel_list = JSON.read_JSON('channel')
    yts = Spider.YoutubeSpider(YOUTUBE_API_KEY)
    if not os.path.isdir("data"):
        os.mkdir("data")
    for channel in channel_list:
        if not os.path.isdir(f"data/{channel['id']}"):
            os.mkdir(f"data/{channel['id']}")
        if renew or not os.path.isfile(f"data/{channel['id']}/playlist.json"):
            print(f"start getting playist of {channel['title']}")
            videos = yts.get_playlist(channel['uploads'], max_results = config['video_num'])
            JSON.save_JSON({'channel': channel, 'videos': videos}, name = f"data/{channel['id']}/playlist")
        else:
            print(f"ignore getting playist of {channel['title']}")
            videos = JSON.read_JSON(name = f"data/{channel['id']}/playlist")['videos']
        if not os.path.isdir(f"data/{channel['id']}/video"):
            os.mkdir(f"data/{channel['id']}/video")
        pbar = tqdm.tqdm(videos)
        for video in pbar:
            if renew or not os.path.isfile(f"data/{channel['id']}/video/{video['id']}.json"):
                pbar.set_description(f"Fetching {video['id']}")
                video_info = yts.get_video(video['id'])
                comments = yts.get_comments(video['id'], max_results = config['comment_num'], filter=is_mostly_zh)
                JSON.save_JSON({"video_info": video_info, "comments": comments}, name = f"data/{channel['id']}/video/{video_info['id']}")
            else:
                pbar.set_description(f"Skipping fetching {video['id']}")

def is_mostly_zh(strs):
    count_zh = 0
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            count_zh = count_zh + 1
    if count_zh >= 0.8 * len(strs):
        return True
    else:
        return False

if __name__ == "__main__":
    main()