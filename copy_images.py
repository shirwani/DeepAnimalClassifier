import os
import glob
import shutil
import random
import string
from utils import *

cfg = get_configs()
classes = cfg['classes']


def copy_image_files(src_dir, dst_dir, num_examples):
    num_px = cfg['image']['num_px']

    image_files = glob.glob(os.path.join(src_dir, '*.j*g'), recursive=False)
    print(src_dir, len(image_files), dst_dir, num_examples)

    if len(image_files) > num_examples:
        image_files = random.sample(image_files, num_examples)

    i = 0
    for f in image_files:
        i += 1
        if i > num_examples:
            break

        src_file = os.path.basename(f)
        file_extension = '.jpeg'
        dst_file = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + file_extension

        src = os.path.join(src_dir, src_file)
        dst = os.path.join(dst_dir, dst_file)

        image = Image.open(src)
        image = image.resize((num_px, num_px))
        image.save(dst)


def cleanup_images_folder():

    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets', 'images', 'train'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets', 'images', 'cv'))
        shutil.rmtree(os.path.join(os.getcwd(), 'datasets', 'images', 'test'))
    except:
        pass

    for cls in classes:
        os.makedirs(os.path.join(os.getcwd(), 'datasets', 'images', 'train', cls))
        os.makedirs(os.path.join(os.getcwd(), 'datasets', 'images', 'cv',    cls))
        os.makedirs(os.path.join(os.getcwd(), 'datasets', 'images', 'test',  cls))


def copy_examples(mode, num_examples):
    for cls in classes:
        srcdir = os.path.join('/Users', 'macmini', 'Downloads', 'animals', cls)
        dstdir = os.path.join(os.getcwd(), 'datasets', 'images', mode, cls)
        os.makedirs(dstdir, exist_ok=True)
        copy_image_files(srcdir, dstdir, num_examples)


def create_examples_for_app(num_examples):
    for cls in classes:
        srcdir = os.path.join('/Users', 'macmini', 'Downloads', 'animals', cls)
        dstdir = os.path.join(os.getcwd(), 'static', 'images', 'examples')
        os.makedirs(dstdir, exist_ok=True)
        copy_image_files(srcdir, dstdir, num_examples)


if __name__ == '__main__':
    cleanup_images_folder()
    copy_examples('train',  num_examples=2000)
    copy_examples('cv',     num_examples=20)
    copy_examples('test',   num_examples=20)

    create_examples_for_app(num_examples=50)
