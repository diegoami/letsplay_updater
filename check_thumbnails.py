from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import os
import yaml
import argparse


def check_thumbnails(youtube, playlist_id, thumbnail_dir):
    index = 0
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            title = item['snippet']['title']
            if 'Deleted' in title:
                continue
            content_details = item['contentDetails']

            video_id = content_details['videoId']
            print(f"Processing {item} at {index}")
            content_details_thm = youtube.get_video_content_details(video_id)
            if content_details_thm and content_details_thm["hasCustomThumbnail"]:
                index += 1
                continue
            else:
                thumbnail_file = f"{thumbnail_dir}/thumbnail{index+1}.png"
                print(f"Executing youtube.upload_thumbnail({video_id}, {thumbnail_file})")
                youtube.upload_thumbnail(video_id, thumbnail_file)
                time.sleep(1)
                index += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # option that takes a value
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:

        with open(args.config, 'r') as confhandle:

            conf_info = yaml.safe_load(confhandle)

            youtube = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
            thumbnail_dir = conf_info["thumbnail_dir"]
            monitored_playlists = conf_info["monitored_playlists"]
            for monitored_playlists in monitored_playlists:
                pl_id = monitored_playlists["pl"]
                th_id = monitored_playlists["th"]
                if pl_id and th_id:
                    print(pl_id, th_id)
                    thumbnail_play_dir = os.path.join(thumbnail_dir, th_id)
                    check_thumbnails(youtube, pl_id, thumbnail_play_dir)