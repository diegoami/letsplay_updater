from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import yaml
import os
from PIL import Image
import datetime
import difflib
from  collections import defaultdict
import pytesseract

ALL_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def get_all_chars():
    """
    This function iterates through a list of months and appends each character in the month to a list if it is not already present in that list. Finally, it combines the list of characters with a comma and a set of numbers as a single string and returns the result.
    """
    numbs ='1234567890,'
    cmonts = []
    for month in ALL_MONTHS:
        for char in month:
            if char not in cmonts:
                cmonts.append(char)
    result = numbs + ''.join(cmonts)
    return result


def separate_string(input_string):
    for i, char in enumerate(input_string):
        if char.isdigit():
            return input_string[:i], input_string[i:]
    return input_string, ""
def get_closest_month(month_orig):
    closest = difflib.get_close_matches(month_orig, ALL_MONTHS, n=1, cutoff=0.6)
    if closest:
        return closest[0]
    return None

def convert_date_format(orig_str, pattern):
    orig_lines = orig_str.split()
    if len(orig_lines) == 2:
        month_and_day, orig_year = orig_lines[0], orig_lines[1]
        orig_month_name, orig_day = separate_string(month_and_day)
    elif len(orig_lines) == 3:
        orig_month_name, orig_day, orig_year = orig_lines
    else:
        return None
    orig_year = orig_year[:4]
    closest_month = get_closest_month(orig_month_name)
    if closest_month:
        to_conv_date = closest_month+" "+orig_day+" "+orig_year
        try:
            date = datetime.datetime.strptime(to_conv_date, pattern)
            return date.strftime('%d.%m.%Y')
        except:
            return None
    else:
        return None

def generate_date_list_from_map(date_map, output_file):
    with open(output_file, 'w') as f:
        for index, dates in date_map.items():
            first, last = dates[0], dates[-1]
            f.write(f'{index} {first} {last}\n')


def create_dates_map_from_images(dates_dir, pattern):
    dates_map = defaultdict(list)
    for file_name in os.listdir(dates_dir):
        nparts = file_name.split('_')
        img_index = int(nparts[0])
        full_file_name = os.path.join(dates_dir, file_name)
        img = Image.open(full_file_name)
        img = img.resize((img.width * 2, img.height * 2))
        found = False
        tried = set()

        for dpi in [150, 200, 250]:
            for oem in [1, 2, 3]:
                if not found:
                    tessact_config = f'--dpi {dpi} --oem {oem}'
                    if True:
                        date_str = pytesseract.image_to_string(img, config=tessact_config + tewcconfig).strip()
                        tried.add(date_str)
                        conv_date = convert_date_format(date_str, pattern)
                        if conv_date:
                            print(f'{file_name}, {dpi}, {oem} --> {conv_date}')
                            dates_map[img_index].append(conv_date)
                            found = True
        if not found:
            print(f"No valid date found in {tried}")
    return dates_map


if __name__ == "__main__":
    # os.environ["TESSDATA_PREFIX"] = "/home/diego/tesseract/"
    argparser.add_argument('--config')
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
            dates_dir = conf_info["dates_dir"]
            dates_map = create_dates_map_from_images(dates_dir, pattern)
            print(dates_map)
            generate_date_list_from_map(dates_map, output)