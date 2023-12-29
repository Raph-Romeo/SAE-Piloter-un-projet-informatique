import configparser
import os

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), 'Documents', 'task_master_pro_config.ini')

def create_or_read_config() -> dict:
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE_PATH):
        # Create the configuration file with default values
        config['Settings'] = {
            'server_address': 'task_master_pro_domain.com',
            'server_port': '5240',
            'theme': '0'
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)
        print(f"Configuration file created: {CONFIG_FILE_PATH}")
        return {"server_address": "task_master_pro_domain.com", 'server_port': 5240, "theme": 0}
    else:
        # Read the configuration file
        config.read(CONFIG_FILE_PATH)
        # Access values from sections
        server_address = config['Settings']['server_address']
        try:
            server_port = int(config['Settings']['server_port'])
        except:
            server_port = 5240
        try:
            theme = int(config['Settings']['theme'])
        except:
            theme = 0
        return {"server_address": server_address, 'server_port': server_port, "theme": theme}


def edit_config(parameter, new_value):
    # Edit or update a specific value in the configuration
    create_or_read_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    try:
        section, key = parameter.split('.')
        config[section][key] = new_value

        # Save the updated configuration to the file
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

        print(f"Configuration file updated: {CONFIG_FILE_PATH}")
    except ValueError:
        print("Invalid parameter format. Please use 'section.key'.")