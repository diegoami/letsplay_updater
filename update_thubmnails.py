from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

def update_thumbnails(youtube, playlist_id, directory, skipped, max):
    index = 0
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            title = item['snippet']['title']
            thumbnail_file = f"{directory}/thumbnail{index+1}.png"
            if index+1 < skipped:
                print(f"Skipping youtube.upload_thumbnail({video_id}, {thumbnail_file})")
            elif index+1 >= max:
                print(f"Reached max {max}")
                return
            else:
                if 'Deleted' in title:
                    continue
                print(f"Executing youtube.upload_thumbnail({video_id}, {thumbnail_file})")
                youtube.upload_thumbnail(video_id, thumbnail_file)
                time.sleep(1)
            index += 1

if __name__ == "__main__":
    argparser.add_argument('--config')
    args = argparser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:
        youtube = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))

        with open(args.config, 'r') as confhandle:
            conf_info = yaml.safe_load(confhandle)
            print(conf_info)
            if conf_info.get("playlist",None) and conf_info.get("thumbnail_directory", None):
                update_thumbnails(youtube,
                                  conf_info["playlist"],
                                  conf_info["thumbnail_directory"],
                                  conf_info.get("skipped",0),
                                  conf_info.get("max",1000)
                                  )
        #videoInfo = youtube.get_video(args.videoId)
        #youtube.upload_thumbnail(args.videoId, args.thumbnail)

