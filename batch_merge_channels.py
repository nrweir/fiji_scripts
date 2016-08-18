# @String img_dir
 

from ij import IJ, ImagePlus, ImageStack
import os

dir_contents = os.listdir(img_dir)
im_list = [i for i in dir_contents if i.lower().endswith('.tif')]
bfp_list = [i for i in im_list if '405' in i]
cfp_list = [i for i in im_list if '445' in i]
gfp_list = [i for i in im_list if '488' in i]
yfp_list = [i for i in im_list if '515' in i]
rfp_list = [i for i in im_list if '594' in i]
