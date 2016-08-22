# @String img_dir
# @String colors 

from ij import IJ, ImagePlus, ImageStack, 
import os
import sys

def mk_fname_ref(img_list, wlength_string, delimiter = '_'):
    '''Create a reference dict for matching stage position images from
    different channels.
    
    Keyword arguments:
    img_list: the list of image files being worked on. contains all
    wavelengths.
    wlength_string: string containing identifying information for the channel
    of interest, e.g. '488' for images with filenames containing
    'w3.488.laser.25'.
    delimiter (optional): the delimiter used to break up the filename for
    removing the wavelength information.

    Returns: a dictionary whose key:value pairs are:
        key: the filename with the wavelength identifying fragment removed
        value: the full filename of the image
        for all images in the wavelength defined.
        Example of a key:value pair:
            a_stage_pos_fname.tf:a_stage_pos_wavelengthinfo_fname.tif
    '''

    wlength_imlist = [i for i in img_list if wlength_string in i]
    wlength_rm = []
    for fname in wlength_imlist:
        split_fname = fname.split(delimiter)
        fname_no_wlength = '_'.join([x for x in split_fname if wlength_string
                                     not in x])
        wlength_rm.append(fname_no_wlength)
    return dict(zip(wlength_rm, wlength_imlist))

# parse command line arguments
if len(sys.argv) != 2:
    sys.exit('Two command line arguments expected, ' + str(len(sys.argv)) +
             'provided.')
    img_dir = sys.argv[1]
    colors = sys.argv[2]
output_dir = img_dir + '/merges'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
# retrieve the list of images
dir_contents = os.listdir(img_dir)
im_list = [i for i in dir_contents if i.lower().endswith('.tif')]
blue = False
cyan = False
green = False
yellow = False
red = False
brightfield = False
# determine which colors are present. the colors input string provided at
# script call should be the first letter of each color to be included in the
# merged image. 
if 'b' in colors:
    blue = True
if 'c' in colors:
    cyan = True
if 'g' in colors:
    green = True
if 'y' in colors:
    yellow = True
if 'r' in colors:
    red = True
if 'w' in colors:
    brightfield = True
if yellow and green:
    print 'This script does not support overlay of green and yellow wavelengths.'
    sys.exit()
if blue and cyan:
    print 'This script does not support overlay of blue and cyan wavelengths.'
    sys.exit()
# assign wavelength strings for colors
blue_wavelength = '405'
cyan_wavelength = '447'
green_wavelength = '488'
yellow_wavelength = '515'
red_wavelength = '594'
bf_delimiter = 'Brightfield'
# create a dict of dicts. each sub-dictionary will contain key:value pairs
# whose keys are a shortened version of an image's filename with the wavelength
# information removed, and the value is the full filename. the top dictionary
# will contain one of these sub-dictionaries for each wavelength as the values,
# with the keys being the channel. see mk_fname_ref docstring for more
# clarification.  also define which color to use to search for matched images 
# of other channels (first_wavelength)
color_sublists = {}
first_wavelength = ''
if blue:
    if first_wavelength == '':
        first_wavelength = 'bfp'
    color_sublists['bfp'] = mk_fname_ref(im_list,blue_wavelength)
if cyan:
    if first_wavelength == '':
        first_wavelength = 'cfp'
    color_sublists['cfp'] = mk_fname_ref(im_list,cyan_wavelength)
if green:
    if first_wavelength == '':
        first_wavelength = 'gfp'
    color_sublists['gfp'] = mk_fname_ref(im_list,green_wavelength)
if yellow:
    if first_wavelength == '':
        first_wavelength = 'yfp'
    color_sublists['yfp'] = mk_fname_ref(im_list,yellow_wavelength)
if red:
    if first_wavelength == '':
        first_wavelength = 'rfp'
    color_sublists['rfp'] = mk_fname_ref(im_list,red_wavelength)
if brightfield:
    if first_wavelength == '':
        first_wavelength = 'bf'
    color_sublists['bf'] = mk_fname_ref(im_list, bf_delimiter)
if first_wavelength == '':
    raise ValueError('No wavelengths selected.')
# get the series of images identifier strings to be processed. see mk_fname_ref
# to see how these are made identical amongst images from different
# wavelengths.
im_series = color_sublists[first_wavelength].keys()
for stage_pos in im_series:
    cyan_id = '*None*'
    green_id = '*None*'
    red_id = '*None*'
    bf_id = '*None*'
    if blue:
        cyan_id = color_sublists['bfp'][stage_pos]
        c_imp = ImagePlus(cyan_id, img_dir+'/'+cyan_id)
    if cyan:
        cyan_id = color_sublists['cfp'][stage_pos]
        c_imp = ImagePlus(cyan_id, img_dir+'/'+cyan_id)
    if green:
        green_id = color_sublists['gfp'][stage_pos]
        g_imp = ImagePlus(green_id, img_dir+'/'+green_id)
    if yellow:
        green_id = color_sublists['yfp'][stage_pos]
        g_imp = ImagePlus(green_id, img_dir+'/'+green_id)
    if red:
        red_id = color_sublists['rfp'][stage_pos]
        r_imp = ImagePlus(red_id, img_dir+'/'+red_id)
    if brightfield:
        bf_id = color_sublists['bf'][stage_pos]
        bf_imp = ImagePlus(bf_id, img_dir+'/'+bf_id)
    cmd_string = 'c1=*None* c2='+green_id+' c3=*None* c4='+bf_id+' c5='+cyan_id+' c6='+red_id+' c7=*None* create'
    composite = IJ.run('Merge Channels...', cmd_string)
    IJ.saveAsTiff(composite, output_dir + '/' + stage_pos)
    if blue:
        c_imp.close()
    if cyan:
        c_imp.close()
    if green:
        g_imp.close()
    if yellow:
        g_imp.close()
    if red:
        r_imp.close()
    if brightfield:
        bf_imp.close()
    composite.close()

