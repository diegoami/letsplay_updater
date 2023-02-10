from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import re
def update_snippets(youtube, playlist_id, search_text, replace_text, prepend_desc, tags, skipped, max):
    """
    This function updates the snippets (title, description, and tags) of videos in a given YouTube playlist. The function takes several arguments:
    -   `youtube`: an object representing the YouTube API.
    -   `playlist_id`: the id of the playlist to update the snippets of.
    -   `search_text`: a string that will be searched for in the title of each video in the playlist.
    -   `replace_text`: a string that will replace the `search_text` in the title of each video in the playlist.
    -   `prepend_desc`: a string that will be added to the beginning of the description of each video in the playlist.
    -   `tags`: a list of strings that will be added as tags to each video in the playlist.
    -   `skipped`: an integer representing the number of videos to skip at the beginning of the playlist.
    -   `max`: an integer representing the maximum number of videos to update.
    The function uses the `youtube` object to get the list of videos in the playlist and then iterates over each video to update its snippet. If the index of the current video is less than `skipped`, the function will print a message indicating that the video is being skipped. If the index of the current video is greater than `max`, the function will return and not update any more videos. Otherwise, it will get the snippet of the video and perform the updates as specified by the arguments.
    """
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
                    try:
                        video_snippet = youtube.get_video_snippet(videoId)
                    except Exception as err:
                        print("Ignoring deleted video")
                        continue
                    replace_result = replace_text.replace('_INDEX_', str(index+1).rjust(2, '0'))
                    title = re.sub(search_text, replace_result, video_snippet["title"])
                    #video_snippet["title"] = video_snippet["title"].replace(search_text, replace_text)
                    video_snippet["title"] = title
                    video_snippet["tags"] = tags
                    print(f"Executing youtube.update_snippet({videoId}, {video_snippet})")
                    if videoId not in video_snippet["description"]:
                        prep_replace = prepend_desc.replace("VIDEO_ID", videoId).replace("INDEX_ID", str(index + 1))
                        video_in = video_snippet["description"].split("\n")
                        video_out = []
                        for ind_inv, inv in reversed(list(enumerate(video_in))):
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

