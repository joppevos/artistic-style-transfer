import subprocess
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)


class Exporter:

    def __init__(self, file_path, style_image, style_weight=100,
                 temp_weight=1e3, resolution='original', iterations='50,50'):
        self.basename = self.remove_trailing_from_filename(file_path)
        self.filepath = file_path
        self.resolution = resolution
        self.iterations = iterations
        self.export_folder = 'files/'  # location where the videos are located
        self.image_path = os.path.join(self.export_folder, self.basename)  # path to folder where images are extracted
        self.style_weight = style_weight
        self.temp_weight = temp_weight
        self.style_image = style_image
        self.backend = 'cudnn'
        self.original_colors = 0
        self.gpu = 0
        self.last_frame_index = 1

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
        # cmd1 = subprocess.Popen(['echo', password], stdout=subprocess.PIPE)
        # cmd2 = subprocess.Popen(['sudo', '-S', 'bash', './test.sh'], stdin=cmd1.stdout, stdout=subprocess.PIPE)

        # restore path
        os.chdir(cwd)
        subprocess.run([f'{home}/torch/install/bin/th', 'artistic_video.lua',
                        '-content_pattern', f'{self.image_path}/frame_%04d.ppm',
                        '-flow_pattern', f'{self.image_path}/flow_{self.resolution}/backward_[%d]_' + '{%d}.flo',
                        '-style_weight', f'{self.style_weight}',
                        '-temporal_weight', f'{self.temp_weight}',
                        '-output_folder', f'inProgress/{self.basename}/{self.basename}_[{self.iterations}]_{self.resolution}',
                        '-style_image', f'{self.style_image}',
                        '-backend', f'{self.backend}',
                        '-num_iterations', f'{self.iterations}',
                        '-original_colors', f'{self.original_colors}',
                        '-gpu', f'{self.gpu}',
                        '-continue_with', f'{self.last_frame_index}',
                        '-number_format', '%04d'])

    def run(self):
        self.export_video_to_images()
        self.make_optical_flow()
        # self.start_style_transfer()


if __name__ == "__main__":
    E = Exporter(file_path='/home/joppe/projects/style-transfer/input_videos/skater.mp4',
                 style_image='/home/joppe/projects/style-transfer/boats.png',
                 resolution='50:50')
    E.run()
