from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time
from PIL import Image, ImageFont, ImageDraw

def split_string(s):
    words = s.split()
    n = len(words)
    half_n = round(n / 2)
    index = 0
    total = 0
    for i, word in enumerate(words):
        total += len(word)
        if total >= half_n:
            index = i
            break
    return ' '.join(words[:index+1]), ' '.join(words[index+1:])

# Example usage
s = "This is a sample string that we want to split into two halves without breaking any words."
left, right = split_string(s)
print(left)
print(right)


def generate_thumbnails(youtube, playlist_id, directory, skipped, max, thumbnail_name, remove_texts, text_conf, split_conf):
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
                extracted_title = title
                if remove_texts:
                    for remove_text in remove_texts:
                        extracted_title = extracted_title.replace(remove_text, '')
                if split_conf:
                    split_index = split_conf["index"]
                    split_separator = split_conf["separator"]
                    split_expected = split_conf.get("expected", None)

                    extracted_splits = extracted_title.split(split_separator)
                    if split_expected  and len(extracted_splits) != split_expected:
                        print(f"Wrong number of seprators in { extracted_title}")
                        continue
                    else:
                        extracted_title = extracted_splits[split_index]
                extracted_title = extracted_title.replace('-', '').replace('(', '').replace(')', '').replace(',', '').strip()

                baseImg = Image.open(thumbnail_file_input)
                img = baseImg.copy()
                imgDraw = ImageDraw.Draw(img)
                if "y2" in text_conf["coords"]:
                    ext_title1, ext_title2 = split_string(extracted_title)
                    imgDraw.text((text_conf["coords"]["x2"], text_conf["coords"]["y"]), ext_title1, color, font1)
                    imgDraw.text((text_conf["coords"]["x2"], text_conf["coords"]["y2"]), ext_title2, color, font1)
                else:
                    imgDraw.text((text_conf["coords"]["x2"], text_conf["coords"]["y"]), extracted_title, color, font1)
                ext_title1, ext_title2 = split_string(extracted_title)
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
                generate_thumbnails(youtube,
                                    conf_info["playlist"],
                                    conf_info["thumbnail_directory"],
                                    conf_info.get("skipped",0),
                                    conf_info.get("max",1000),
                                    conf_info.get("thumbnail_name", "thumbnail"),
                                    conf_info.get("remove_texts", None),
                                    conf_info.get("text_conf", None),
                                    conf_info.get("split_conf", None)

                                    )

