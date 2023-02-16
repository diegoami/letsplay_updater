from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time
from PIL import Image, ImageFont, ImageDraw
def update_thumbnails(youtube, playlist_id, directory, skipped, max, thumbnail_name, search_text, text_conf):
    index = 0
    font1 = ImageFont.truetype(text_conf["font"]["name"], text_conf["font"]["size"])
    color = (text_conf["font"]["color"]["r"], text_conf["font"]["color"]["g"], text_conf["font"]["color"]["b"])
    for video_items in youtube.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            title = item['snippet']['title']
            thumbnail_file_input = f"{directory}/{thumbnail_name}"
            thumbnail_file_output = f"{directory}/thumbnail{index+1}.png"
            if index+1 < skipped:
                print(f"Skipping youtube.upload_thumbnail({video_id})")
            elif index+1 >= max:
                print(f"Reached max {max}")
                return
            else:
                if 'Deleted' in title:
                    continue
                extracted_title = title.replace(search_text, '')
                baseImg = Image.open(thumbnail_file_input)
                img = baseImg.copy()
                imgDraw = ImageDraw.Draw(img)
                imgDraw.text((text_conf["coords"]["x2"], text_conf["coords"]["y"]), extracted_title, color, font1)
                #youtube.upload_thumbnail(video_id, thumbnail_file)
                img = img.resize((1280, 720))
                img.save(thumbnail_file_output)
                #time.sleep(1)
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
                                  conf_info.get("max",1000),
                                  conf_info.get("thumbnail_name", "thumbnail"),
                                  conf_info.get("search_text", ""),
                                  conf_info.get("text_conf", None),



                )

