import yaml


conf_file = open('cosmos.yaml')
config = yaml.safe_load(conf_file)
conf_file.close()
