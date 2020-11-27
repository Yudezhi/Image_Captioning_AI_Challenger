# coding: utf-8
"""
Preprocess a raw json dataset into hdf5/json files for use in data_loader.lua

Input: json file that has the form
[{ file_path: 'path/img.jpg', captions: ['a caption', ...] }, ...]
example element in this list would look like
{'captions': [u'A man with a red helmet on a small moped on a dirt road. ', u'Man riding a motor bike on a dirt road on the countryside.', u'A man riding on the back of a motorcycle.', u'A dirt path with a young person on a motor bike rests to the foreground of a verdant area with a bridge and a background of cloud-wreathed mountains. ', u'A man in a red shirt and a red hat is on a motorcycle on a hill side.'], 'file_path': u'val2014/COCO_val2014_000000391895.jpg', 'id': 391895}

This script reads this json, does some basic preprocessing on the captions
(e.g. lowercase, etc.), creates a special UNK token, and encodes everything to arrays

Output: a json file and an hdf5 file
The hdf5 file contains several fields:
/images is (N,3,256,256) uint8 array of raw image data in RGB format
/labels is (M,max_length) uint32 array of encoded labels, zero padded
/label_start_ix and /label_end_ix are (N,) uint32 arrays of pointers to the 
  first and last indices (in range 1..M) of labels for each image
/label_length stores the length of the sequence for each of the M sequences

The json file has a dict that contains:
- an 'ix_to_word' field storing the vocab in form {ix:'word'}, where ix is 1-indexed
- an 'images' field that is a list holding auxiliary information for each image, 
  such as in particular the 'split' it was assigned to.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import argparse
import sys
import hashlib
import jieba
from random import shuffle, seed

def main(params):

  imgs = {filename[filename.rfind('/')+1:filename.rfind('.')].replace('annotations', 'images'):json.load(open(filename, 'r')) for filename in params['input_json']}
  tmp = []
  for k in imgs.keys():
    for img in imgs[k]:
      img['filename'] = img['image_id'] # k+'/'+img['image_id']
      img['image_id'] = int(int(hashlib.sha256(img['image_id'].encode("utf-8")).hexdigest(), 16) % sys.maxsize)
      tmp.append(img)
  imgs = tmp

  
  # create output json file
  out = {  "info": {
    "contributor": "He Zheng",
    "description": "CaptionEval",
    "url": "https://github.com/AIChallenger/AI_Challenger.git",
    "version": "1",
    "year": 2017
  },
  "licenses": [
    {
      "url": "https://challenger.ai"
    }
  ],
  "type": "captions",
  'images':[], 'annotations':[]}

  cnt = 0
  empty_cnt = 0
  for i,img in enumerate(imgs):
    out['images'].append(
      {u'id': img['image_id'],\
       u'url': img['url'],\
       u'file_name': img['filename']})
    for j,s in enumerate(img['caption']):
      if len(s) == 0:
        continue
      w = jieba.cut(s.strip().replace(u'。',''), cut_all=False)
      s = u' '.join(w)
      out['annotations'].append({'image_id': img['image_id'], 'caption': s, 'id': cnt})
      cnt += 1
  
  json.dump(out, open(params['output_json'], 'w'))
  print('wrote ', params['output_json'])

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  # input json
  parser.add_argument('--input_json', nargs='+', required=True, help='input json file to process into hdf5')
  parser.add_argument('--output_json', default='data.json', help='output json file')

  args = parser.parse_args()
  params = vars(args) # convert to ordinary dict
  print('parsed input parameters:')
  print(json.dumps(params, indent = 2))
  main(params)


