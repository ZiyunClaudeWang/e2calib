import numpy as np
import cv2 as cv
import glob
import pdb
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((10*7,3), np.float32)
objp[:,:2] = np.mgrid[0:10,0:7].T.reshape(-1,2) * 36
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
#images = glob.glob('/home/claude/git/e2calib/python/gen3_no_trigger/e2calib/*.png')

images = glob.glob('/home/claude/Documents/data/calib/run3/e2calib/*.png')

for i, fname in enumerate(images):

    '''
    if i%5 != 0 or i < 50:
        continue
    '''
    
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (10,7), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        print(i)
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        '''
        cv.drawChessboardCorners(img, (10,7), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
        '''

print("Num of images is ", len(objpoints))
print("Start optimization")
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

pdb.set_trace()

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )

cv.destroyAllWindows()
