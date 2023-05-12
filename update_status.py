from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import re
def update_status(youtube, playlist_id, skipped, max, status):

    index = 0
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            if index+1 < skipped:
                print(f"Skipping youtube.update_snippet({index})")
            elif index+1 > max:
                print(f"Max reached: {max}")
                return
            else:
                if len(item['snippet']) > 0:
                    videoId = item['snippet']["resourceId"]["videoId"]
                    youtube.update_status(videoId, status)
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
            playlist = conf_info["playlist"]
            skipped = conf_info.get("skipped", 0)
            max = conf_info.get("max", 1000)
            status = conf_info.get("status", "public")
            update_status(youtube, playlist,  skipped, max, status)

