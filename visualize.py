import argparse

import numpy as np
import six
from tqdm import tqdm
import time

from model import HumanPartsNet
from data import MiniBatchLoader
import chainer
from os.path import basename

import cv2

resultdir = "./result/"
X_dir = "./data/img/"
y_dir = "./data/mask/"

def standardize(image):
    subtracted_img = image - 126
    return subtracted_img / 255.

parser = argparse.ArgumentParser(description='Human parts network')
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
parser.add_argument('--pretrainedmodel', '-p', default=None,
                    help='Path to pretrained model')
parser.add_argument('--file', '-f', type=str,
                    help='Path to image to predict mask')
args = parser.parse_args()

# model setteing
model = HumanPartsNet(n_class=15)
if args.pretrainedmodel is not None:
    from chainer import serializers
    serializers.load_npz(args.pretrainedmodel, model)

# img = np.transpose(np.expand_dims(cv2.imread(args.file), 0), (0, 3, 1, 2)) / 255.
bname = basename(args.file)
img = np.transpose(np.expand_dims(standardize(cv2.resize(cv2.imread(args.file), (300, 300)).astype(np.uint8)), 0), (0, 3, 1, 2))
x = chainer.Variable(img.astype(np.float32), volatile='on')
y = model.predict(x)
mask = np.argmax(y.data[0], axis=0)

np.save(resultdir + bname + '.npy', mask)
