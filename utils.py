import subprocess
import os

class Exporter:

    def __init__(self, filename, resolution='original', iterations='100:100'):
        self.filepath = filename
        self.basename = self.get_file_name(filename)
        self.resolution = resolution
        self.iterations = iterations

    def make_dir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def export_video_to_images(self):
        export_path = f'files/{self.basename}'
        self.make_dir(export_path)
        if self.resolution is 'original':
            subprocess.run(['ffmpeg','-i', f'{self.filepath}', f'{export_path}/frame_%04d.ppm'])
        else:
            subprocess.run(['FFMPEG','-i', f'{self.filepath}', '-vf', f'scale={self.resolution}', f'{export_path}/frame_%04d.ppm'])

    def get_file_name(self, video_file):
        base = os.path.basename(video_file)
        filename, _ = os.path.splitext(base)
        return filename

    def make_optical_flow(self):
        self.make_dir(f'inProgress/{self.basename}/{self.basename}_[{self.iterations}]_{self.resolution}')
        subprocess.run(['./makeOptFlow.sh', './${self.basename}/frame_%04d.ppm',
                        './${self.basename}/flow_{self.resolution}'])
        print('calculating optical flow')

    # make optical flow
    # check if optical flow files already exist
    # if they exist, check how frames left until max frames




video_file = 'drone.mp4'
E = Exporter(video_file)
E.export_video_to_images()

# FFMPEG -i $1 -vf scale=$resolution ${filename}/frame_%04d.ppm
# convert video to frames with ffmpeg png if they dont exist yet



# run artistic video with arguments

# extras
# pil display to show input and output

