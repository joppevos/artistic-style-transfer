import subprocess
import os
import logging
logging.basicConfig(level=logging.DEBUG)


class Exporter:

    def __init__(self, file_name, file_directory, resolution='original', iterations='100:100'):
        self.file_directory = file_directory
        self.basename = self.get_file_name(file_name)
        self.filepath = os.path.join(file_directory, file_name)
        self.resolution = resolution
        self.iterations = iterations
        self.export_folder = 'files/'
        self.image_path = os.path.join(self.export_folder, self.basename)

    def make_dir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True )

    def file_path(self, file_directory):
        return os.path.join(self.file_directory, self.basename)

    def export_video_to_images(self):
        self.image_path = os.path.join(self.export_folder, self.basename)
        self.make_dir(self.image_path)

        # see if file already exist
        if os.path.isfile(f'{self.image_path}/frame_0001.ppm'):
            logging.info('Frames already exported, skipping ffmpeg')
            return
        if self.resolution is 'original':
            subprocess.run(['ffmpeg','-i', f'{self.filepath}', f'{self.image_path}/frame_%04d.ppm'])
        else:
            subprocess.run(['ffmpeg','-i', f'{self.filepath}', '-vf', f'scale={self.resolution}', f'{self.image_path}/frame_%04d.ppm'])

    def get_file_name(self, file_name):
        file_name = os.path.basename(file_name)
        file_name, _ = os.path.splitext(file_name)
        return file_name

    def make_optical_flow(self):
        self.make_dir(f'inProgress/{self.basename}/{self.basename}_[{self.iterations}]_{self.resolution}')
        subprocess.call(['./makeOptFlow.sh', f'./{self.image_path}/frame_%04d.ppm',
                        f'./{self.image_path}/flow_{self.resolution}'])
        logging.info('Calculating optical flow')


if __name__ == "__main__":
    video_file = 'test_video.mp4'
    E = Exporter(file_directory='files/', file_name=video_file)
    E.export_video_to_images()
    E.make_optical_flow()



# run artistic video with arguments

# extras
# pil display to show input and output

