import numpy as np 
import tensorflow as tf
import random
import pickle
import os
import sys
import urllib
import tarfile
TRAIN_RANDOM_LABEL = False # Want to use random label for train data?
VALI_RANDOM_LABEL = False # Want to use random label for validation?
IMAGE_HEIGHT = 32
IMAGE_WIDTH = 32
NUM_CHANNEL = 3
full_data_dir = 'cifar10_data/cifar-10-batches-py/data_batch_'
vali_dir = 'cifar10_data/cifar-10-batches-py/test_batch'
DEFAULT_IMAGE_BYTES = IMAGE_HEIGHT*IMAGE_WIDTH*NUM_CHANNEL
# The record is the image plus a one-byte label
RECORD_BYTES = DEFAULT_IMAGE_BYTES+1
NUM_CLASS = 10
NUM_DATA_FILES = 5
NUM_IMAGES = {
    'train': 50000,
    'validation': 10000,
}
DATA_URL = 'https://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz'
def compute_mean_var(image):
    # image.shape: [image_num, w, h, c]
    mean = []
    var  = []
    for c in range(image.shape[-1]):
        mean.append(np.mean(image[:, :, :, c]))
        var.append(np.std(image[:, :, :, c]))
    return mean, var

def _read_one_batch(path, is_random_label):
    '''
    The training data contains five data batches in total. The validation data has only one
    batch. This function takes the directory of one batch of data and returns the images and
    corresponding labels as numpy arrays

    :param path: the directory of one batch of data
    :param is_random_label: do you want to use random labels?
    :return: image numpy arrays and label numpy arrays
    '''
    fo = open(path, 'rb')
    dicts = pickle.load(fo,encoding='bytes')
    fo.close()

    data = dicts[b'data']
    if is_random_label is False:
        label = np.array(dicts[b'labels'])
    else:
        labels = np.random.randint(low=0, high=10, size=10000)
        label = np.array(labels)
    return data, label


def read_in_all_images(address_list, shuffle=True, is_random_label = False):
    """
    This function reads all training or validation data, shuffles them if needed, and returns the
    images and the corresponding labels as numpy arrays

    :param address_list: a list of paths of cPickle files
    :return: concatenated numpy array of data and labels. Data are in 4D arrays: [num_images,
    image_height, image_width, image_depth] and labels are in 1D arrays: [num_images]
    """
    data = np.array([]).reshape([0, IMAGE_WIDTH * IMAGE_HEIGHT * NUM_CHANNEL])
    label = np.array([])

    for address in address_list:
        print ('Reading images from ' + address)
        batch_data, batch_label = _read_one_batch(address, is_random_label)
        # Concatenate along axis 0 by default
        data = np.concatenate((data, batch_data))
        label = np.concatenate((label, batch_label))

    num_data = len(label)

    # This reshape order is really important. Don't change
    # Reshape is correct. Double checked
    data = data.reshape((num_data, IMAGE_WIDTH * IMAGE_HEIGHT, NUM_CHANNEL), order='F')
    data = data.reshape((num_data, IMAGE_HEIGHT, IMAGE_WIDTH, NUM_CHANNEL))


    if shuffle is True:
        print ('Shuffling')
        order = np.random.permutation(num_data)
        data = data[order, ...]
        label = label[order]

    data = data.astype(np.float32)
    return data, label

def read_train():
    path_list = []
    for i in range(1, NUM_DATA_FILES+1):
        path_list.append(full_data_dir + str(i))
    data, label = read_in_all_images(path_list, is_random_label=TRAIN_RANDOM_LABEL)
    return data,label

def read_validation_data():
    '''
    Read in validation data. Whitening at the same time
    :return: Validation image data as 4D numpy array. Validation labels as 1D numpy array
    '''
    validation_array, validation_labels = read_in_all_images([vali_dir],
                                                       is_random_label=VALI_RANDOM_LABEL)
    # validation_array = whitening_image(validation_array)

    return validation_array, validation_labels

def norm_images(image):
    # image.shape: [image_num, w, h, c]
    image = image.astype('float32')
    mean, var = compute_mean_var(image)
    image[:, :, :, 0] = (image[:, :, :, 0] - mean[0]) / var[0]
    image[:, :, :, 1] = (image[:, :, :, 1] - mean[1]) / var[1]
    image[:, :, :, 2] = (image[:, :, :, 2] - mean[2]) / var[2]
    return image

def norm_images_using_mean_var(image, mean, var):
    image = image.astype('float32')
    image[:, :, :, 0] = (image[:, :, :, 0] - mean[0]) / var[0]
    image[:, :, :, 1] = (image[:, :, :, 1] - mean[1]) / var[1]
    image[:, :, :, 2] = (image[:, :, :, 2] - mean[2]) / var[2]
    return image

def download_and_extract(data_path):
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(data_path, filename)

    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                filename, 100.0 * count * block_size / total_size))
            sys.stdout.flush()

        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')

    tarfile.open(filepath, 'r:gz').extractall(data_path)

def get_filenames(is_training,data_path):
    """Returns a list of filenames."""
    data_dir = os.path.join(data_path,'cifar-10-batches-bin')
    if not os.path.exists(data_dir):
        download_and_extract(data_path=data_path)
    if is_training:
        return [
            os.path.join(data_dir, 'data_batch_%d.bin' % i)
            for i in range(1, NUM_DATA_FILES + 1)
        ]
    else:
        return [os.path.join(data_dir, 'test_batch.bin')]
# 从二进制文件中读取固定长度纪录， 可以使用tf.FixedLengthRecordReader的tf.decode_raw操作。
# decode_raw操作可以讲一个字符串转换为一个uint8的张量。
# 举例来说，the CIFAR-10 dataset的文件格式定义是：每条记录的长度都是固定的，一个字节的标签，后面是3072（32*32*3）字节的图像数据。
# 也就是说我们每次固定获取3073个字节的数据。uint8的张量的标准操作就可以从中获取图像片并且根据需要进行重组。
def parse_record(is_training,raw_record):
    record_vector = tf.decode_raw(raw_record,tf.uint8)
    label = tf.cast(record_vector[0],tf.int32)
    depth_major = tf.reshape(record_vector[1:RECORD_BYTES],[NUM_CHANNEL,IMAGE_HEIGHT,IMAGE_WIDTH])

    image = tf.cast(tf.transpose(depth_major,[1,2,0]),tf.float32)
    return image,label

def preprocess_image(image,is_training):
    if is_training:
        image = tf.image.resize_image_with_crop_or_pad(image,IMAGE_HEIGHT+8,IMAGE_WIDTH+8)
        image = tf.image.random_crop(image,[IMAGE_HEIGHT,IMAGE_WIDTH,NUM_CHANNEL])
        image = tf.image.random_flip_left_right(image)

    image = tf.image.per_image_standardization(image)
    return image

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def generate_tfrecord(train, labels, output_path, output_name):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    writer = tf.python_io.TFRecordWriter(os.path.join(output_path, output_name))
    for ind, (file, label) in enumerate(zip(train, labels)):
        img_raw = file.tobytes()

        example = tf.train.Example(features=tf.train.Features(feature={
            'image_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
        }))
        writer.write(example.SerializeToString())  # Serialize To String
        if ind != 0 and ind % 1000 == 0:
            print("%d num imgs processed" % ind)
    writer.close()



def lr_schedule_200ep(epoch):
    if epoch < 60:
        return 0.1
    elif epoch < 120:
        return 0.02
    elif epoch < 160:
        return 0.004
    elif epoch<300:
        return 0.0008
    else:
        return 0.0001

def lr_schedule_300ep(epoch):
    if epoch < 150:
        return 0.1
    if epoch < 225:
        return 0.01
    elif epoch < 320:
        return 0.001
    else:
        return 0.0001