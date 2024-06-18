import cv2 as cv

IMAGE_FILE = 'origianlImages/PreWarpedCourse.jpg'
img = cv.imread(IMAGE_FILE)
cv.imshow('edge', img)
