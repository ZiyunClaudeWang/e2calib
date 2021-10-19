#!/usr/bin/env python
import rosbag
import rospy
import pdb
import os
import cv2
from tqdm import tqdm
from sensor_msgs.msg import Image


def getImageFilesFromDir(dir):
    '''Generates a list of files from the directory'''
    image_files = list()
    timestamps = list()
    if os.path.exists(dir):
        for path, names, files in os.walk(dir):
            for f in files:
                if os.path.splitext(f)[1] in ['.bmp', '.png', '.jpg']:
                    image_files.append( os.path.join( path, f ) )
                    timestamps.append(os.path.splitext(f)[0]) 
    #sort by timestamp
    sort_list = sorted(zip(timestamps, image_files))
    image_files = [file[1] for file in sort_list]
    return image_files


def loadImageToRosMsg(filename, offset_s=0, offset_ns=0):
    image_np = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
    timestamp_nsecs = os.path.splitext(os.path.basename(filename))[0]
    timestamp = rospy.Time( secs=int(timestamp_nsecs[0:-9]), nsecs=int(timestamp_nsecs[-9:]) )

    offset_ts = rospy.Duration( secs=offset_s, nsecs=offset_ns)

    timestamp = timestamp + offset_ts

    rosimage = Image()
    rosimage.header.stamp = timestamp
    rosimage.height = image_np.shape[0]
    rosimage.width = image_np.shape[1]
    rosimage.step = rosimage.width  #only with mono8! (step = width * byteperpixel * numChannels)
    rosimage.encoding = "mono8"
    rosimage.data = image_np.tostring()
    
    return rosimage, timestamp

#create the bag
folder = "/home/claude/Documents/data/calib/april/e2calib/"
realsense_bag_name = "/home/claude/Documents/data/calib/april/realsense_april.bag"
bag_name = os.path.join(folder, "recons.bag")

#!!!!!!!! offset
offset_s = 1633544422
offset_ns = 571176000

skip = 180 
rs_frame_count = 0

try:
    bag = rosbag.Bag(bag_name, 'w')
    '''
    # write realsense bag into file
    rs_bag = rosbag.Bag(realsense_bag_name, 'r')
    for topic, msg, t in tqdm(rs_bag.read_messages(topics=["/camera/color/image_raw"])):
        ts = msg.header.stamp
        if rs_frame_count > skip:
            bag.write(topic, msg, ts)
        rs_frame_count += 1
    '''

    #write images
    image_files = getImageFilesFromDir(folder)
    for image_filename in image_files:
        image_msg, timestamp = loadImageToRosMsg(image_filename, offset_s=offset_s, offset_ns=offset_ns )
        bag.write("/ev_recons", image_msg, timestamp)

finally:
    bag.close()

