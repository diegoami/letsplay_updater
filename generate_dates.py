from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
import yaml
import time

import re


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
            pattern = conf_info["pattern"]

            output = conf_info["output"]
            until = conf_info["until"]

            with open(output, 'w') as f:
                for index in range(until):
                    f.write(f'{index+1} {pattern} {pattern}\n')

