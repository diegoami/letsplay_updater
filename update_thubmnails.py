from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

def update_thumbnails(youtube, playlist_id, directory):
    index = 0
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            thumbnail_file = f"{directory}/thumbnail{index+1}.png"
            print(f"Executing youtube.upload_thumbnail({video_id}, {thumbnail_file})")
            youtube.upload_thumbnail(video_id, thumbnail_file)
            time.sleep(1)
            index += 1
            if index >= 5:
                return

if __name__ == "__main__":
    argparser.add_argument('--config')
    args = argparser.parse_args()
    if args.config == None:
        print("required argument --config <videoId>")
    else:
        youtube = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))

        with open(args.config, 'r') as confhandle:
            conf_info = yaml.safe_load(confhandle)
            print(conf_info)
            if conf_info.get("playlist",None) and conf_info.get("thumbnail_directory", None):
                update_thumbnails(youtube, conf_info["playlist"], conf_info["thumbnail_directory"])
        #videoInfo = youtube.get_video(args.videoId)
        #youtube.upload_thumbnail(args.videoId, args.thumbnail)

