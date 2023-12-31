import src.YTSpider as YTSpider
import src.JSON as JSON
import os

def main():
    c = channelInfo("channel")
    while(1):
        op = input('Operation: (i)nsert, (s)equentially insert, (d)elete, (l)ist, (e)xit:')
        if op == 'i' or op == 'insert':
            keyword = input('Insert Keyword...')
            c.search_and_insert(keyword)
        if op == 's' or op == 'sequentially' or op == 'sequentially insert':
            while 1:
                keyword = input('Sequentially Insert Keyword... ((e)xit)')
                if keyword == 'e' or keyword == 'exit':
                    break
                c.search_and_insert(keyword)
        elif op == 'd' or op == 'delete':
            keyword = input('Delete Title...')
            c.delete_byTitle(keyword)
        elif op == 'l' or op == 'list':
            c.list_byTitle()
        elif op == 'e' or op == 'exit':
            break
        else:
            print("Invalid operation.")

class channelInfo:
    def __init__(self, file_name):
        self.file_name = file_name
        if os.path.isfile(f"{file_name}.json"):
            self.channel = JSON.read_JSON(file_name)
            print("Found the file!")
        else:
            self.channel = []
            print("File not found, will start from scratch")
        self.yts = YTSpider.YoutubeSpider(YTSpider.YOUTUBE_API_KEY)

    def search_and_insert(self, keyword):
        new_info = self.yts.get_channel_info(keyword=keyword)
        if new_info == {}:
            print("channel not found!")
        else:
            for i, info in enumerate(self.channel):
                if info['id'] == new_info['id']:
                    print(f"pop old: {info}")
                    self.channel.pop(i)
                    break
            print(f"insert: {new_info}")
            self.channel.append(new_info)
            JSON.save_JSON(self.channel, name = self.file_name)
        return
    
    def list_byTitle(self):
        print("listed by channel title")
        for i, info in enumerate(self.channel):
            print(f"{i}\t{info['title']}")
        return
    
    def delete_byTitle(self, keyword):
        for i, info in enumerate(self.channel):
            if keyword in info['title']:
                print(f"delete: {info}")
                self.channel.pop(i)
                break
        JSON.save_JSON(self.channel, name = self.file_name)
        return

if __name__ == "__main__":
    main()
        