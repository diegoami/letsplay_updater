from oauth2client.tools import argparser
import yaml



if __name__ == "__main__":
    argparser.add_argument('--config')
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

            with open(output, 'w') as f:
                for index in range(until):
                    f.write(f'{index+1} {pattern} {pattern}\n')

