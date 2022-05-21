import ffmpeg
import glob
import os
import datetime
from datetime import date

remove_dir = False
frame_rate = 5
width = "1920"
height = "1440"
log_level = "quiet"
overwrite_output = True

input_dir = "/home/ubuntu/timelapse_cameras/5lNfZ3VRud/"


def is_today(input_date: datetime):
    today = date.today()
    converted_date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
    if today == converted_date:
        print(f"Ignoring Images for folder {input_date} as its Today")
        return True


def remove_empty(dir: str):
    dirs = [root for root, dirs, files in os.walk(dir) if not files and not dirs]
    for d in dirs:
        os.rmdir(d)


def get_cameras_and_timelapse_folders(input_dir: str):
    camera_data = []
    directories = glob.glob(input_dir + "*")
    for dir in directories:
        if "_timelapse" in dir:
            folder = dir
            dir = dir.replace(input_dir, "")
            dir = dir.replace("_timelapse", "")
            camera = {"name": dir, "folder": folder + "/"}
            camera_data.append(camera)
    return camera_data


def make_camera_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


for cameras in get_cameras_and_timelapse_folders(input_dir):
    print(f"Converting Images for camera "+ cameras["name"])
    remove_empty(cameras["folder"])
    directories = glob.glob(cameras["folder"] + "*")
    for dir in directories:
        if is_today(dir.replace(cameras["folder"], "")):
            continue
        else:
            file_name = dir.replace(cameras["folder"], "")
            folder_name = cameras["name"]
            print(f"Converting Images from {file_name}")
            make_camera_folder(folder_name)
            stream = ffmpeg.input(
                f"{dir}/*.jpg", pattern_type="glob", framerate=frame_rate
            )
            stream = ffmpeg.filter(
                filter_name="scale", stream_spec=stream, width=width, height=height
            )

            stream = ffmpeg.output(
                stream, f"{folder_name}/{file_name}.mp4", loglevel=log_level
            )
            ffmpeg.run(stream, overwrite_output=overwrite_output)
            if remove_dir:
                os.system(f"rm -rf {dir}")
    print(f"Converting Images for camera {folder_name} Complete")
print("Process Complete")
