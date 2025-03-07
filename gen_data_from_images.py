import glob
import os
from utils import *

cfg = get_configs()
num_px = cfg['image']['num_px']
classes = cfg['classes']

def load_img_files(mode, i, x, y):
    cls = classes[i]
    folder_path = os.path.join(os.getcwd(), 'datasets', 'images', mode, cls)
    jpg_files = glob.glob(os.path.join(folder_path, '*.*'), recursive=False)

    for jpg_file in jpg_files:
        try:
            img = img_to_matrix(jpg_file, num_px)
            x.append(img)
            y.append(i)
        except:
            print(jpg_file)

    return x, y


def create_data_file(mode):
    print(f"\nCreating {mode} set...\n")
    x = []
    y = []

    for i in range(len(classes)):
        x, y = load_img_files(mode, i, x, y)

    x = np.array(x)
    y = np.array(y)
    print("x.shape: " + str(x.shape))
    print("y.shape: " + str(y.shape))

    with h5py.File('datasets/'+ mode +'.h5', 'w') as file:
        file.create_dataset('x', data=x)
        file.create_dataset('y', data=y)

    load_back_and_check_data(mode)


def load_back_and_check_data(mode):
    print(f"\nLoading back {mode} set...\n")

    dataset = h5py.File('datasets/' + mode + '.h5', "r")
    x = np.array(dataset["x"][:])
    y = np.array(dataset["y"][:])
    print("x.shape: " + str(x.shape))
    print("y.shape: " + str(y.shape))
    print("y: " + str(y))


if __name__ == '__main__':
    create_data_file('train')
    create_data_file('cv')
    create_data_file('test')
