import yaml


conf_file = open('cosmos.conf')
config = yaml.safe_load(conf_file)
conf_file.close()
