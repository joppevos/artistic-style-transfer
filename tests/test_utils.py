import os
from tools import Exporter
import shutil

root = os.path.dirname(os.path.dirname(__file__))


def test_export_images():
    # test ffmpeg export images in right folder
    video_file = 'test_video.mp4'

    E = Exporter(file_directory='tests/', file_name=video_file)
    E.export_video_to_images()
    assert os.path.isfile(root + '/tests/test_video/frame_0001.ppm')

    # remove folder afterwards
    shutil.rmtree('tests/test_video')

def test_torch_install():

