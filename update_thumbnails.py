from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

def update_thumbnails(youtube, playlist_id, directory, skipped, max):
    """
    This method appears updates the thumbnails of videos in a given YouTube playlist.
    The function takes in the following parameters: a youtube object representing a YouTube API client, the playlist_id of the playlist to update, the directory where the thumbnail files are stored, the skipped number of thumbnails to skip before updating, and the max number of thumbnails to update before stopping.
    The function loops through the videos in the playlist using the iterate_videos_in_playlist method of the youtube object, and for each video, it extracts the video ID, title, and content details.
    The function then generates a file path for the thumbnail file based on the current index of the video item, and checks if the current index is less than the number of thumbnails to skip. If so, it prints a message indicating that the thumbnail update is being skipped.

    If the current index is greater than or equal to the max parameter, the function prints a message indicating that the maximum number of thumbnails has been reached and returns. Otherwise, the function checks if the video title contains the word "Deleted". If it does, the function continues to the next video item without updating the thumbnail. If the title does not contain "Deleted", the function prints a message indicating that the thumbnail update is being executed and calls the youtube.upload_thumbnail method to update the video thumbnail with the file located at the generated thumbnail file path. The function then waits for one second using the time.sleep method before continuing to the next video item.
    """
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

