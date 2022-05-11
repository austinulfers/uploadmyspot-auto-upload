import os
import logging
import cv2
import json
import pandas as pd
import shutil

ALLOWABLE_VIDEO_FORMATS = ["mp4", "mov", "wmv", "mpg"]
ALLOWABLE_VIDEO_LENGTHS = [10, 15, 20, 30, 60]
FRAME_TOLERANCE = 3

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

def check_videos(folder: str = None, allowed_video_formats: list = ALLOWABLE_VIDEO_FORMATS, allowed_video_lengths: list = ALLOWABLE_VIDEO_LENGTHS, frame_tolerance: int = FRAME_TOLERANCE):
    """Checks the videos in the above directory and if they don't pass, they get
    relocated to the failed videos folder that is created if it doesn't already
    exist.

    Args:
        folder (str, optional): Folder to look for videos. Defaults to directory
            above current working directory.
        allowed_video_formats (list, optional): List of video formats to look 
            for. Defaults to ALLOWABLE_VIDEO_FORMATS.
        allowed_video_lengths (list, optional): List of video lengths to look 
            for. Defaults to ALLOWABLE_VIDEO_LENGTHS.
        frame_tolerance (int, optional): Number of seconds to allow for the 
            video to end. Defaults to FRAME_TOLERANCE.

    Raises:
        Exception: Occurs when any video doesn't pass the specs.
    """    
    if folder is None:
        folder = os.path.dirname(os.getcwd())
    logging.debug(f"Checking videos at {folder}.")
    print(f"Checking videos in {folder}.")
    videos = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.split(".")[-1].lower() in allowed_video_formats]:
            path = os.path.join(dirpath, filename)
            logging.debug(f"Found video at {path}.")
            if not dirpath.split("\\")[-1].startswith("_"):
                logging.debug(f"Adding video {path}.")
                videos.append(path)
    info_agg = []
    for video_path in videos:
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        dimensions = (width, height)
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.release()
        duration = length / fps
        remainder = length % fps
        if remainder > (fps / 2):
            remainder = remainder - fps
        within_tolerance = -frame_tolerance < remainder < frame_tolerance
        # video_path = video_path.replace(folder, "")
        passed = False
        if round(duration, 0) in allowed_video_lengths and within_tolerance:
            if round(fps, 2) == 59.94:
                if width == 1280 and height == 720:
                    passed = True
                else:
                    print(f"{video_path} has unacceptable width/height.")
            elif round(fps, 2) == 29.97 or round(fps, 3) == 23.976:
                if width == 1920 and height == 1080:
                    passed = True
                elif width == 1280 and height == 720:
                    passed = True
                else:
                    print(f"{video_path} has unacceptable width/height.")
            else:
                print(f"{video_path} has unacceptable frame rate.")
        else:
            print(f"{video_path} either not within tolerance or unacceptable video length.")
        if not passed:
            # full_path = folder + video_path
            logging.debug(f"{video_path} failed check.")
            new_folder = os.path.join(os.path.dirname(video_path), "_Failed")
            if not os.path.isdir(new_folder):
                logging.info(f"_Failed folder not found. Creating here {new_folder}.")
                os.mkdir(new_folder)
            new_file_location = os.path.join(new_folder, video_path.split("\\")[-1])
            logging.debug(f"Moving {video_path} to {new_file_location}")
            shutil.move(video_path, new_file_location)
        info = {
            "Path": video_path,
            "Dimensions": dimensions,
            "Frame Count": length,
            "FPS": round(fps, 3),
            "Duration": round(duration, 2),
            "Remaining or Missing Frames": round(remainder, 2),
            "Passed": passed
        }
        info_agg.append(info)
    logging.info(json.dumps(info_agg, indent=4))
    df = pd.DataFrame(info_agg)
    if df.empty:
        raise FileNotFoundError(f"No videos found in {folder}.")
    failed = df.query("~Passed")
    if not failed.empty:
        with pd.option_context('display.max_colwidth', -1):
            df_str = failed.to_string().split("\n")
            error_str = f"The Following Videos Failed the Checks:\n{chr(10).join(df_str)}"
            raise Exception(error_str)
            
if __name__ == "__main__":
    setup()
    check_videos()
