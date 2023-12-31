import requests
from pprint import pprint
from datetime import datetime
import src.JSON as JSON
import os

video_folder = "videos"


def main():
    print("YTSpider, start testing!")
    config = JSON.read_JSON("Config")
    YOUTUBE_API_KEY = config['api_key']
    youtube_channel_id = "UC7ia-A8gma8qcdC6GDcjwsQ"

    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)
    
    print("start getting playist")
    video_ids = youtube_spider.get_playlist(uploads_id, max_results=5)
    JSON.save_JSON(video_ids, name = "playlist")
    if not os.path.isdir(video_folder):
        os.mkdir(video_folder)
    for video_id in video_ids:
        video_info = youtube_spider.get_video(video_id)
        print(f"Fetching {video_id}")

        comments = youtube_spider.get_comments(video_id)
        JSON.save_JSON({"video_info": video_info, "comments": comments}, name = f"{video_folder}/{video_info['id']}_info")

class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='snippet, contentDetails', max_results=100):
        page_token = ''
        videos = []
        while 1:
            path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}&pageToken={page_token}'
            data = self.get_html_to_json(path)
            if not data:
                break

            page_token = data.get('nextPageToken', '')
            for data_item in data['items']:
                if len(videos) >= max_results:
                    break
                videos.append({
                    "id": data_item['contentDetails']['videoId'],
                    "title": data_item['snippet']['title']
                    })
            if not page_token:
                break
            if len(videos) >= max_results:
                break
        return videos
    
    def get_popular_chart(self, regionCode, videoCategoryId, part='contentDetails'):
        page_token = ''
        video_ids = []
        while 1:
            path = f'search?part={part}&chart=mostPopular&regionCode={regionCode}&videoCategoryId={videoCategoryId}'
            data = self.get_html_to_json(path)
            if not data:
                break

            page_token = data.get('nextPageToken', '')
            for data_item in data['items']:
                video_ids.append(data_item['contentDetails']['videoId'])
            if not page_token:
                break
        return video_ids

    def get_video(self, video_id, part='snippet,statistics'):
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]

        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {'id': data_item['id']}
        key_pairs = [('snippet', 'channelTitle'),
                    ('snippet', 'title'),
                    ('snippet', 'description'),
                    ('statistics', 'likeCount'),
                    ('statistics', 'commentCount'),
                    ('statistics', 'viewCount')
                    ]
        for (key1, key2) in key_pairs:
            if(key1 in data_item.keys() and key2 in data_item[key1].keys()):
                info[key2] = data_item[key1][key2]
            else:
                info[key2] = None
                print(f"{info['id']}: {key2} lost!")
        return info

    def get_comments(self, video_id, page_token='', part='snippet', max_results=100, filter=None):
        page_token = ''
        comments = []
        while 1:
            path = f'commentThreads?part={part}&videoId={video_id}&maxResults=100&pageToken={page_token}'
            data = self.get_html_to_json(path)
            if not data:
                break
            page_token = data.get('nextPageToken', '')

            for data_item in data['items']:
                if len(comments) >= max_results:
                    break
                data_item = data_item['snippet']
                top_comment = data_item['topLevelComment']
                if not (filter == None or filter(top_comment['snippet']['textOriginal'])):
                    continue

                ru_name = top_comment['snippet'].get('authorDisplayName', '')
                if not ru_name:
                    ru_name = None

                comments.append({
                    'reply_id': top_comment['id'],
                    'reply_content': top_comment['snippet']['textOriginal'],
                })
            
            if not page_token:
                break
            if len(comments) >= max_results:
                break
        return comments
    
    def isChannel(self, result):
        return ("id" in result.keys() and "kind" in result["id"].keys() and "youtube#channel" == result["id"]["kind"])
    
    def get_channel_info(self, keyword=None, channel_id=None, part='snippet, contentDetails'):
        if channel_id == None:
            path_id = f'search?part=snippet&q={keyword}'
            data = self.get_html_to_json(path_id)
            if not data or 'items' not in data.keys():
                return {}
            channel_list = list(filter(self.isChannel, data['items']))
            if len(channel_list) == 0:
                return {}
            channel_id = list(filter(self.isChannel, data['items']))[0]['id']['channelId']

        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]

        info = {
            'title': data_item['snippet']['title'],
            'id': data_item['id'],
            'customUrl': data_item['snippet']['customUrl'] if 'customUrl' in data_item['snippet'].keys() else None,
            'uploads': data_item['contentDetails']['relatedPlaylists']['uploads']
        }
        return info

if __name__ == "__main__":
    main()