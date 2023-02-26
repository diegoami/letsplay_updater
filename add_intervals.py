from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import re
def add_intervals(youtube, playlist_id, interval_dir):
    playlist_dir = os.path.join(interval_dir, playlist_id)
    for video_dir in os.listdir(playlist_dir):
        intervals_file = os.path.join(playlist_dir, video_dir, 'intervals.txt')
        with open(intervals_file, 'r') as f:
            intervals_lines = f.readlines()
            if '_' in video_dir:
                video_id = '_'.join(video_dir.split('_')[1:])
                print(f"Processing {video_id}")
                video_snippet = youtube.get_video_snippet(video_id)
                video_desc = video_snippet["description"]
                video_desc_lines = video_desc.split('\n')

                if len(video_desc_lines) < 2:
                    video_desc += '\n ------------------ \n'
                    video_desc += '\n'.join(intervals_lines)
                    video_snippet["description"] = video_desc
                    youtube.update_snippet(video_id, video_snippet)
                    print(f"updating snippet for {video_id}")
                    time.sleep(1)


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
            playlist_id = conf_info["playlist_id"]
            intervals_dir = conf_info["intervals_dir"]
            add_intervals(youtube, playlist_id, intervals_dir)

