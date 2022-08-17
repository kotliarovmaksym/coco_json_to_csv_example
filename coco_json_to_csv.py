#!/usr/bin/env python3

import wget
import json
from zipfile import ZipFile
import os
import sys
import pandas as pd


###data downloading and extraction-----------------

path_to_save = ""

URL = str(sys.argv[1])

if len(sys.argv)>2:
    path_to_save = str(sys.argv[2])

print("Started download from",URL) 
filename = wget.download(URL)

print("Extracting from archive")

with ZipFile(filename,'r') as zipObj:
   zipObj.extractall()


with open('annotations/person_keypoints_val2017.json') as datafile:
    data = json.load(datafile)

print("Started processing file:",filename) 
###--------------------------------


###dictionary separating for easier data manipulations========
categories_ds = pd.DataFrame(data['categories'])  
images_names_ds = pd.DataFrame(data['images'])
annotations_ds = pd.DataFrame(data['annotations'])
###===========================================================


###forming dataframe------------------------------
#merging three dataframes
proto_ds = pd.merge(images_names_ds[['id', 'file_name','coco_url', 'height', 'width']], annotations_ds[['image_id','bbox','category_id']], how="right", right_on='image_id', left_on='id')
proto_ds = pd.merge(categories_ds[['id','supercategory']], proto_ds, how='right', right_on='category_id', left_on='id')

#deleting needless columns
proto_ds.drop("id_x", inplace=True, axis = 1)
proto_ds.drop("id_y", inplace=True, axis = 1)
proto_ds.drop("category_id", inplace=True, axis = 1)
proto_ds.drop('image_id', inplace=True, axis = 1)
###------------------------------------------------


###calculating bound box ordinates=============
#copying values from bbox column to x_min and y_min cols using cycle
#   (didnt find process methods from pandas that able to work with
#    elements of list in value cell 
proto_ds['x_min']= proto_ds['bbox']
for i,val in enumerate(proto_ds['bbox']):         
    (proto_ds["x_min"])[i] = val[0]
    
    
proto_ds['y_min']= proto_ds['bbox']
for i,val in enumerate(proto_ds['bbox']):
    (proto_ds["y_min"])[i] = val[1]
    
#calculating x_max and y_max from data in bbox column  
proto_ds['x_max']= proto_ds['bbox']
for i,val in enumerate(proto_ds['bbox']):
    (proto_ds["x_max"])[i] = float('{:.2f}'.format(val[0]+val[2]))
    
    
proto_ds['y_max']= proto_ds['bbox']
for i,val in enumerate(proto_ds['bbox']):
    (proto_ds["y_max"])[i] = float('{:.2f}'.format(val[1]+val[3]))
###=============================================


###continue with forming dataframe-------------------------------------

proto_ds.drop('bbox',inplace=True, axis = 1) #deleting obsolete data

#moving columns in right order
proto_ds = proto_ds[['supercategory','file_name','width','height','x_min','y_min','x_max','y_max','coco_url']]

#renaming columns
proto_ds.columns = ['label', 'image_name', 'image_width', 'image_height', 'x_min', 'y_min', 'x_max', 'y_max', 'image_url']

###--------------------------------------------------------------------


###exporting to csv==================

proto_ds.to_csv(path_to_save + "/" + filename[0:filename.find('.')]+".csv")

                    
###==================================




datafile.close()

print("Finished, check ", filename[0:filename.find('.')]+".csv")







