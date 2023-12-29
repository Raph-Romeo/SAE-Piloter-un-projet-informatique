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
            'theme': '0',
            'auto_resize_columns': '0'
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)
        print(f"Configuration file created: {CONFIG_FILE_PATH}")
        return {"server_address": "task_master_pro_domain.com", 'server_port': 5240, "theme": 0, "auto_resize_columns": 0}
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
        if theme != 1 and theme != 0:
            theme = 0
        try:
            auto_resize_columns = int(config['Settings']['auto_resize_columns'])
        except:
            auto_resize_columns = 0
        if auto_resize_columns != 1 and auto_resize_columns != 0:
            auto_resize_columns = 0
        return {"server_address": server_address, 'server_port': server_port, "theme": theme, "auto_resize_columns": auto_resize_columns}


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