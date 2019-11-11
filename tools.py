import subprocess
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)


class Exporter:

    def __init__(self, file_name, file_directory, resolution='original', iterations='100:100'):
        self.file_directory = file_directory
        self.basename = self.remove_trailing_from_filename(file_name)
        self.filepath = os.path.join(file_directory, file_name)
        self.resolution = resolution
        self.iterations = iterations
        self.export_folder = 'files/' # location where the videos are located
        self.image_path = os.path.join(self.export_folder, self.basename) # path to folder where images are extracted

    def make_dir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    def export_video_to_images(self):
        self.make_dir(self.image_path)
        # see if file already exist
        if os.path.isfile(f'{self.image_path}/frame_0001.ppm'):
            logging.info('Frames already exported, skipping ffmpeg')
            return
        if self.resolution is 'original':
            subprocess.run(['ffmpeg', '-i', f'{self.filepath}', f'{self.image_path}/frame_%04d.ppm'])
        else:
            subprocess.run(['ffmpeg', '-i', f'{self.filepath}', '-vf', f'scale={self.resolution}',
                            f'{self.image_path}/frame_%04d.ppm'])

    @staticmethod
    def remove_trailing_from_filename(file_name):
        file_name = os.path.basename(file_name)
        file_name, _ = os.path.splitext(file_name)
        return file_name

    def make_optical_flow(self):
        self.make_dir(f'inProgress/{self.basename}/{self.basename}_[{self.iterations}]_{self.resolution}')
        subprocess.call(['./makeOptFlow.sh', f'./{self.image_path}/frame_%04d.ppm',
                         f'./{self.image_path}/flow_{self.resolution}'])
        logging.info('Calculating optical flow')

    def start_style_transfer(self):
        # todo make sure the right torch location is used
        cwd = os.getcwd()

        home = str(Path.home())
        os.chdir(f'{home}/Desktop/')
        # todo danger stuff here
        password = 'weesjezelf12'
        cmd1 = subprocess.Popen(['echo', password], stdout=subprocess.PIPE)
        cmd2 = subprocess.Popen(['sudo', '-S', 'bash', './test.sh'], stdin=cmd1.stdout, stdout=subprocess.PIPE)

        # restore path
        os.chdir(cwd)
        subprocess.run([f'{home}/torch/install/bin/th', 'artistic_video.lua',
                        f'-content_pattern', '{self.image_path}/frame_%04d.ppm',
                        f'-flow_pattern', f'{self.image_path}/flow_{self.resolution}/backward_[%d]_'+'{%d}.flo'])

    def run(self):
        self.export_video_to_images()
        self.make_optical_flow()
        self.make_optical_flow()


if __name__ == "__main__":
    video_file = 'test_video.mp4'
    E = Exporter(file_directory='files/', file_name=video_file)
    E.start_style_transfer()
# run artistic video with arguments

# extras
# pil display to show input and output
