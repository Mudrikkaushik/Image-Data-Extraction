import numpy as np
import cv2
import math
from skimage.filters import threshold_local
from PIL import Image

input_file_path = '/teamspace/studios/this_studio/help_comp/upload.png'
output_file_path = '/teamspace/studios/this_studio/Result/preprocessed_image.png'
img = Image.open(input_file_path)
img.thumbnail((800, 800), Image.ANTIALIAS)

def resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def rgb_conv(image):
    """Convert BGR to RGB."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def grey_conv(image):
    """Convert image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.imread(input_file_path)
resize_ratio = 1000 / image.shape[0]
original = image.copy()
image = resize(image, resize_ratio)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 1)
blur = cv2.medianBlur(blur, 7)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
erosion = cv2.erode(blur, kernel, iterations=1)
