# Youtube Thumbnail Updater
This script is used to update the thumbnails for videos in a given Youtube playlist. 

## Requirements
- Python 3.x
- oauth2client
- youtube3
- yaml

## Usage
1. Download the file `update_thumbnails.py`
2. Create a `client_secrets.json` file and place in the same directory as the script.
3. Create a `config.yml` file with the following structure:
    ```
    playlist: <Youtube playlist id>
    thumbnail_directory: <path to directory containing thumbnails>
    skipped: <number of thumbnails to skip>
    max: <maximum number of thumbnails to upload>
    ```
4. Run the script with following command:
    ```
    python update_thumbnails.py --config config.yml
    ```
5. The script will upload the thumbnails to the videos in the given playlist.

## Notes
- The script will automatically skip Deleted videos in the playlist.
- The script will wait 1 second between each thumbnail upload to avoid rate limiting.

# Update YouTube Playlist Snippets

A script to update the snippets of YouTube videos in a playlist. The script uses the `update_snippets` function to make changes to the snippets of the videos in the playlist.

## Prerequisites

- A Google API project with the YouTube API enabled
- A client secrets JSON file for the API project
- Python 3.x
- The `google-auth` and `google-api-python-client` packages installed

## Usage

1.  Clone or download this repository.
2.  Create a Google API project and enable the YouTube API for the project.
3.  Download the client secrets JSON file for your API project and place it in the same directory as the script.
4.  Create a YAML file with the following format:


`playlist: <playlist_id>
search_text: <text_to_search_for_in_snippet>
replace_text: <text_to_replace_search_text_with>
prepend_desc: <text_to_prepend_to_snippet>
tags: <tags_to_add_to_snippet>`

5.  Run the script using the following command, replacing `<config>` with the path to the YAML file you created:


`python update_snippets.py --config <config>`

## Optional Parameters

You can also specify the following optional parameters in the YAML file:

-   `skipped`: the number of videos to skip before making changes (default: 0)
-   `max`: the maximum number of videos to update (default: 1000)

# Process Data Images

## Overview
This script is used to extract dates from images and convert them to a standardized format. The script uses the pytesseract library to perform optical character recognition (OCR) on the images and difflib library to find the closest matching month name in the list ALL_MONTHS.

## Requirements
- python 3.x
- pytesseract
- Image
- datetime
- yaml
- difflib
- argparse

## Usage
The script is executed by running `python process_date_migs --config <config_file_path>`

The script takes one required argument, --config, which specifies the path to a configuration file in YAML format. The configuration file should contain the following information:

`pattern: 
output: 
until: 
dates_dir:`

dates_dir is the path to the directory containing the images to be processed. The script outputs the processed dates in the format dd.mm.yyyy. 


## Configuration

The script can be configured by modifying the tessact_config and tessedit_char_whitelist variables. tessact_config specifies the configuration options for pytesseract and tessedit_char_whitelist specifies the characters that pytesseract should recognize in the images. The list ALL_MONTHS contains the month names to be used for date recognition.

## Limitations
The script is limited by the accuracy of the pytesseract library and the similarity threshold set in the difflib.get_close_matches function. The script may not work correctly if the dates in the images are in a format significantly different from the expected format.