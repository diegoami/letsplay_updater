from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time
import os
from PIL import Image

import pytesseract

ALL_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def get_all_chars():
    numbs ='1234567890,'
    cmonts = []
    for month in ALL_MONTHS:
        for char in month:
            if char not in cmonts:
                cmonts.append(char)
    result = numbs + ''.join(cmonts)
    return result
if __name__ == "__main__":
    # os.environ["TESSDATA_PREFIX"] = "/home/diego/tesseract/"
    argparser.add_argument('--config')
    tessact_config = r'--dpi 300'
    tess_train_data = ' --tessdata-dir /home/diego/tesseract/eng.traineddata'
    tessedit_char_whitelist = get_all_chars()
    tewcconfig = f'-c tessedit_char_whitelist={tessedit_char_whitelist}'
    args = argparser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:

        with open(args.config, 'r') as confhandle:
            conf_info = yaml.safe_load(confhandle)
            print(conf_info)
            pattern = conf_info["pattern"]

            output = conf_info["output"]
            until = conf_info["until"]
            dates_dir = conf_info["dates_dir"]
            dates_map = {}
            for file_name in os.listdir(dates_dir):
                nparts = file_name.split('_')
                img_index = int(nparts[0])
                full_file_name = os.path.join(dates_dir, file_name)
                img = Image.open(full_file_name)
                img = img.resize((img.width * 2, img.height * 2) )
                #for dpi in [30, 50, 70, 100, 150, 200]:
                for dpi in [150, 200, 250 ]:
                    for oem in [1, 2, 3]:
                        tessact_config = f'--dpi {dpi} --oem {oem}'
                        if True:
                        #if oem == 2 or oem == 3:
                            date_str = pytesseract.image_to_string(img, config=tessact_config + tewcconfig)
                            print(f'{file_name}, {dpi}, {oem} --> {date_str.strip()}')
                       # date_str = pytesseract.image_to_string(img, config=tessact_config + tewcconfig + tess_train_data )
                       # print(f'{file_name}, {dpi}, {oem}, TD --> {date_str.strip()}')
