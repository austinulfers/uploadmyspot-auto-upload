import os
import logging
import cv2
import json
import pandas as pd

ALLOWABLE_VIDEO_FORMATS = ["mp4", "mov", "avi", "wmv"]
ALLOWABLE_VIDEO_LENGTHS = [10, 15, 20, 30, 60]
ENDING_TOLERANCE = 2

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

    if not os.path.isfile("tmp/Upload.csv"):
        logging.fatal("tmp/Upload.csv not found.")
        raise Exception("'tmp/Upload.csv' file not found.")

def check_videos(folder: str = None):
    if folder is None:
        folder = os.path.dirname(os.getcwd())
    logging.debug(f"Checking videos at {folder}.")
    print(f"Checking videos in {folder}.")
    videos = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.split(".")[-1].lower() in ALLOWABLE_VIDEO_FORMATS]:
            path = os.path.join(dirpath, filename)
            logging.debug(f"Found video at {path}.")
            videos.append(path)
    info_agg = []
    for video_path in videos:
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        dimensions = (width, height)
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = length / fps
        remainder = length % fps
        if remainder > (fps / 2):
            remainder = remainder - fps
        within_tolerance = -ENDING_TOLERANCE < remainder < ENDING_TOLERANCE
        video_path = video_path.replace(folder, "")
        passed = False
        if round(duration, 0) in ALLOWABLE_VIDEO_LENGTHS and within_tolerance:
            if round(fps, 2) == 29.97 or round(fps, 3) == 23.976:
                if width == 1920 and height == 1080:
                    passed = True
            elif round(fps, 2) == 59.94:
                if width == 1280 and height == 720:
                    passed = True
        info = {
            "Path": video_path,
            "Dimensions": dimensions,
            "Frame Count": length,
            "FPS": round(fps, 3),
            "Duration": round(duration, 2),
            "Remainding or Missing Frames": round(remainder, 2),
            "Passed": passed
        }
        info_agg.append(info)
    logging.info(json.dumps(info_agg, indent=4))
    df = pd.DataFrame(info_agg)
    failed = df[df["Passed"] == False]
    if not failed.empty:
        with pd.option_context('display.max_colwidth', -1):
            df_str = failed.to_string().split("\n")
            raise Exception(f"The Following Videos Failed the Checks:\n{chr(10).join(df_str)}")
            

if __name__ == "__main__":
    setup()
    check_videos(r"C:\Users\Austin Ulfers\Desktop\Uploads\Uploads")
