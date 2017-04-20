#!/usr/bin/python
import os
import cPickle
import tools._init_paths
from datasets.factory import get_imdb
import numpy as np
import sys



def fishValSubmit(image_set):
    cache_file =  \
        'output/pvanet_full7_ohem/fish_val/zf_faster_rcnn_iter_100000/detections.pkl'

    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as fid:
            boxes = cPickle.load(fid)
    else:
        print(cache_file + ' not found')

    imdb = get_imdb(image_set)
    num_images = len(imdb.image_index)

    gt_roidb = imdb.gt_roidb()
    boxes = np.array(boxes)

    valSubmit = open('./data/fish/valSubmit.csv', 'w')

    valSubmit.write('image,ALB,BET,DOL,LAG,NoF,OTHER,SHARK,YFT\n')

    for i in range(num_images):

        prob = np.zeros(8) #+ 0.03
        
        for j in range(1, 8):
            box = boxes[j][i] 
            for b in box:
                prob[j] = max(prob[j], b[-1])
        
        '''
        if np.sum(prob) <= 0.24:
            prob[0] = 1.0

        totProb = np.sum(prob)
        prob /= totProb

        '''

        imageName = imdb.image_path_at(i)
        imageName = imageName[imageName.find('img') : ]

        
        fishClass = [1, 2, 3, 4, 0, 5, 6, 7]

        valSubmit.write(imageName)
        for j in range(8):
            valSubmit.write(','+str(prob[fishClass[j]]))               
        valSubmit.write('\n')
        

if __name__ == '__main__':
    fishValSubmit('fish_2016_val')
