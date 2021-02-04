#!/usr/bin/python
import subprocess
import threading

import os
import sys
import MySQLdb

import PIL
from PIL import Image
from IPython import display
import tensorflow as tf
from datasets import imagenet
import numpy as np

global c
global db

def sar_log():
    print("starting sysstat utility to capture runtime logs")
    subprocess.call(["sar", "-o", "logfile", "1"])
    print("sysstat utility running......")

def sadf_log():
    print("Creating memory logs in database readable form")
    with open('memory_logs', "w") as outfile:
        subprocess.call(["sadf", "-d", "logfile", "--", "-r"], stdout=outfile)
    print("Creating cpu logs in database readable form")
    with open('cpu_logs', "w") as outfile:
        subprocess.call(["sadf", "-d", "logfile", "--", "-u"], stdout=outfile)
    print("Database readable output files ready!")


def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def read_from_db():
    try:
        c.execute("SELECT * FROM EdgeTeam_DataSets")
        result = c.fetchall()
        if result is not None:
           return result[0][1]

    except:
        e = sys.exc_info()
        print(e)
        print("read error")

def runModel():
    image_res = read_from_db()
    write_file(image_res,'result_file')
    img = np.array(PIL.Image.open('result_file').resize((224,224))).astype(np.float) / 128 - 1
    gd = tf.GraphDef.FromString(open('/home/atomicpi/mobilenet_v1_1.0_224_frozen.pb','rb').read())
    inp,predictions = tf.import_graph_def(gd, return_elements = ['input:0', 'MobilenetV1/Predictions/Reshape_1:0'])
    with tf.Session(graph = inp.graph):
        x = predictions.eval(feed_dict={inp: img.reshape(1, 224,224, 3)})
    label_map = imagenet.create_readable_names_for_imagenet_labels()
    print("Top 1 Prediction: ", x.argmax(),label_map[x.argmax()], x.max())
    return True

if  __name__ == '__main__':

    try:
    
        print("Trying to connect")
        
        db = MySQLdb.connect(host="172.22.85.19",port=3306, user="EdgeTeam",passwd="EdgeTeam12#$%",db="EdgeTeam")
        
        print("After connect command")
        
        c = db.cursor()
        
        print("Accessed DB")
      
    except:
        e = sys.exc_info()
        print(e)

    try:
        print("starting the script")
        x = threading.Thread(target=sar_log)
        x.start()

        if (runModel() == True):
            print("Press Ctrl-C to end the system logs")


        x.join()

    except KeyboardInterrupt:
        print("ending sysstat utility")
        print("startting new thread")
        y = threading.Thread(target=sadf_log)
        y.start()
        y.join()

    finally:
        print("ending script")

