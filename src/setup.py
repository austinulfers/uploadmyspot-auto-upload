import os
import logging

def setup():
    """Sets up the application for first time use.

    Raises:
        Exception: when the template config file is found but no config file.
        Exception: no config file found and no template file found.
    """    
    if not os.path.isdir("tmp"):
        logging.warning("tmp folder not found. Creating now.")
        os.mkdir("tmp")

    if not os.path.isdir("log"):
        logging.warning("log folder not found. Creating now.")
        os.mkdir("log")

    if not os.path.isfile("config.ini"):
        logging.fatal("config.ini not found.")
        if os.path.isfile("config.ini.template"):
            logging.debug("config.ini.template file found")
            raise Exception("Please ensure to add all credentials to config file and rename to 'config.ini'")
        raise Exception("'config.ini' file not found.")

if __name__ == "__main__":
    setup()
