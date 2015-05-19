# -*- coding: utf-8 -*-
"""
Created on Sun May 10 01:14:53 2015

@author: Harsh Hemani

REMEMBER: Google imposes a limit of 25k images per day even if you use api key.

ALL RIGHTS RESERVED.
"""


import os
import Image
import urllib
import ImageChops
import numpy as np
from cStringIO import StringIO
#import matplotlib.pyplot as plt



def exactly_same(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def get_googlemap_as_image(baseurl="http://maps.googleapis.com/maps/api/staticmap", 
                     center=['17.7302099', '83.3204157'], 
                     zoom='20', 
                     image_size='640x640',                     
                     maptype='satellite'):
    url = baseurl + '?' + 'center=' + center[0] + ',' + center[1]
    url = url + '&' + 'zoom=' + zoom
    url = url + '&' + 'size=' + image_size
    url = url + '&' + 'maptype=' + maptype
    # optionally you can add your static maps api key here
    # url = url + '&' + 'key=' + api_key
    buffer = StringIO(urllib.urlopen(url).read())
    image = Image.open(buffer)
    return image
    
def download_googlemap_batch(n_images=1000, 
                   start_location=[17.7302099,83.3204157], 
                   direction='latitude', 
                   shift=0.00085,
                   zoom_lvl = '20',
                   image_dimensions = '640x640',
                   maptype = 'satellite',
                   save_dir='temp'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    info_file_path = os.path.join(save_dir, 'info.txt')
    info_file = open(info_file_path, 'w')
    info_file.write('start_location:' + repr(start_location) + '\n')
    info_file.write('n_images:' + repr(n_images) + '\n')
    info_file.write('advancement direction:' + direction + '\n')
    info_file.write('advancement step-size:' + repr(shift) + '\n')
    info_file.write('zoom level:' + zoom_lvl + '\n')
    info_file.write('image dimensions:' + image_dimensions + '\n')
    info_file.write('map type:' + maptype + '\n')
    info_file.write('images directory:' + save_dir + '\n')
    min_lati = -84.9
    max_lati = 84.9
    min_longi = -179.9
    max_longi = 179.9
    lati, longi = start_location
    lati_longi_list = []
    for i in range(n_images):
        if direction == 'latitude':
            lati = start_location[0] + i*shift
            if lati >= max_lati:
                lati = min_lati
        else:
            longi = start_location[1] + i*shift
            if longi >= max_longi:
                longi = min_longi
        pos = ["%0.7f" % (lati), "%0.7f" % (longi)]
        lati_longi_list.append(pos)
    blank_image = get_googlemap_as_image(center=lati_longi_list[0], zoom='500', image_size=image_dimensions, maptype=maptype)
    width, height = blank_image.size
    cropbox = [width / 5, height / 5, 3 * width / 5, 3 * height / 5]
    print 'Downloading and saving images...'
    for i, center in enumerate(lati_longi_list):
        print '> ', i+1, '/', n_images
        image_path = os.path.join(save_dir, str(center[0])+'LAT'+str(center[1])+'LONG'+'.png')
        print ' + center:', center
        print '   * path:', image_path
        image = get_googlemap_as_image(center=center, zoom=zoom_lvl, image_size=image_dimensions, maptype=maptype)
        if exactly_same(image.crop(cropbox), blank_image.crop(cropbox)):
            print 'Zoom lvl too high! try reducing it a bit.'
            print 'DONT FORGET TO TUNE THE STEP SIZE!!!'
            info_file.write('zoom lvl too high, unable to write:' + image_path + '\n')
            info_file.write('PS: DONT FORGET TO ADJUST STEP SIZE!!\n')
            info_file.close()
            print 'Aborting!!!'
            return
        image.save(image_path)
        print '   * done.'
    info_file.close()
    

if __name__ == '__main__':
    download_googlemap_batch(n_images=4, 
                                direction='longitude', 
                                start_location=[17.7302099,83.3204157], 
                                zoom_lvl='20',
                                save_dir='10052015')
    print 'Done'
