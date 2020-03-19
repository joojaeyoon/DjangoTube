import random
import string
import cv2

ALPHANUMERIC_CHARS = string.ascii_lowercase+string.digits
STRING_LENGTH = 6


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


def get_video_data(filepath, slug):
    video = cv2.VideoCapture(filepath)

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)

    video.set(cv2.CAP_PROP_POS_FRAMES, int(frame_count/2))

    _, frame = video.read()

    filepath = filepath.split("/")[:-1]
    filepath = "/".join(filepath).replace("videos", "thumbnails", 1)
    filepath += f"/{slug}.png"

    cv2.imwrite(filepath, frame)

    video.release()

    duration = frame_count/fps

    minutes = str(int(duration/60))
    seconds = str(int(duration % 60))

    if len(minutes) == 1:
        minutes = "0"+minutes
    if len(seconds) == 1:
        seconds = "0"+seconds

    time = f'{minutes}:{seconds}'

    return [time, filepath]
