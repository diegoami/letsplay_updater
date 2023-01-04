from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import re
def update_snippets(youtube, playlist_id, search_text, replace_text, prepend_desc, tags, skipped, max):
    index = 0
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            videoId = item['snippet']["resourceId"]["videoId"]

            video_snippet = youtube.get_video_snippet(videoId)
            video_snippet["title"] = re.sub(search_text, replace_text, video_snippet["title"])
            video_snippet["title"] = video_snippet["title"].replace(search_text, replace_text)
            video_snippet["tags"] = tags
            youtube.update_snippet(video_id=videoId, video_snippet=video_snippet)
            if index+1 < skipped:
                print(f"Skipping youtube.update_snippet({videoId}, {video_snippet})")
            elif index+1 >= max:
                print(f"Max reached: {max}")
                return
            else:
                print(f"Executing youtube.update_snippet({videoId}, {video_snippet})")
                if videoId not in video_snippet["description"]:
                    prep_replace = prepend_desc.replace("VIDEO_ID", videoId).replace("INDEX_ID", str(index + 1))
                    video_in = video_snippet["description"].split("\n")
                    video_out = []
                    for index, inv in reversed(list(enumerate(video_in))):
                        if "----" in inv:
                            break
                        video_out = video_out + [inv]
                    video_post = "\n".join(reversed(video_out))
                    video_snippet["description"] = prep_replace + "\n-----------\n" + video_post


                youtube.update_snippet(videoId, video_snippet)
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
            skipped = conf_info.get("skipped",0)
            max = conf_info.get("max", 1000)

            search_text = conf_info["search_text"]
            replace_text = conf_info["replace_text"]
            prepend_desc = conf_info["prepend_desc"]
            tags = conf_info["tags"]
            update_snippets(youtube, playlist, search_text, replace_text, prepend_desc, tags, skipped, max)

