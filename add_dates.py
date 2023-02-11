from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import re
def update_dates(youtube, playlist_id, list_map, skipped, max):
    index = 0
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            if index+1 < skipped:
                print(f"Skipping youtube.update_snippet({index})")
            elif index+1 > max:
                print(f"Max reached: {max}")
                return
            elif index+1 not in list_map:
                print(f"{index} not found in list_map")
            else:
                if len(item['snippet']) > 0:
                    to_add = list_map[index+1]
                    videoId = item['snippet']["resourceId"]["videoId"]
                    video_snippet = youtube.get_video_snippet(videoId)
                    if " to " not in video_snippet["title"]:

                        video_snippet["title"] = video_snippet["title"] + ' - ' +to_add
                        print(f"Executing youtube.update_snippet({videoId}, {video_snippet})")
                        youtube.update_snippet(videoId, video_snippet)
                        time.sleep(1)
                    else:
                        print(f"Found {to_add} in video title")

            index += 1

def load_dates_list(date_lst_file):
    dates_map =  {}
    with open(date_lst_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if len(line.split()) == 3:
                index, start_date, end_date = line.split()
                dates_map[int(index)] = f'{start_date} to {end_date}'

    return dates_map

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
            skipped = conf_info.get("skipped",0)
            max = conf_info.get("max", 1000)

            search_text = conf_info["search_text"]
            replace_text = conf_info["replace_text"]
            prepend_desc = conf_info["prepend_desc"]
            tags = conf_info["tags"]
            date_lst_file = conf_info["list"]

            dates_map = load_dates_list(date_lst_file)
            update_dates(youtube, playlist, dates_map, skipped, max)

