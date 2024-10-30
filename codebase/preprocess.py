import numpy as np
import cv2
import math
from skimage.filters import threshold_local
from PIL import Image
input_file_path = 'D:/bytexl_project/help_comp/english.png' 
output_file_path = 'D:/bytexl_project/result/preprocess.jpg'  
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
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
rectKernelv2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 20))
dilated = cv2.dilate(erosion, rectKernel)
closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, rectKernelv2)
(thresh, b_w_image) = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(b_w_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
def app_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * peri, True)
def get_contour(bbox):
    for c in bbox:
        approx = app_contour(c)
        if len(approx) == 4:
            return approx
receipt_contour = get_contour(largest_contours)
def rect_contour(contour):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect / resize_ratio
def wrap_perspective(img, rect):
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))
scanned = wrap_perspective(original.copy(), rect_contour(receipt_contour))
def conv_bw(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset=5, method="gaussian")
    return (gray > T).astype("uint8") * 255
result = conv_bw(scanned)
output = Image.fromarray(result)
output.save(output_file_path)
print("Preprocessing complete, saved at:", output_file_path)