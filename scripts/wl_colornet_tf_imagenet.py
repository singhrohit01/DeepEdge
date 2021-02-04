from PIL import Image
import tensorflow as tf
import cv2
from datasets import imagenet
import numpy as np

from helpers.timer import Timer
from helpers.mock_input_generator import MockInputGenerator
from abstract.abstract_workload import AbstractWorkload
from helpers.util import echo

from skimage.io import imsave, imread
from skimage.transform import resize
from skimage import img_as_ubyte
from matplotlib import pyplot as plt


# Performs model execution
class Workload(AbstractWorkload):

    def __init__(self, arg):
        super().__init__(arg)

    def getModel(self):
        return "ColorNet"

    def getFramework(self):
        return "TensorFlow"

    def getApplication(self):
        return "Colorization of Images"

    def getModelToUse(self):
        return "colorize.tfmodel"

    def plot(self,img1, img2):
	    fig = plt.figure()
	    gs = plt.GridSpec(2,1)
	    ax1 = fig.add_subplot(gs[0,0])
	    ax2 = fig.add_subplot(gs[1,0])
	
	    ax1.imshow(img1, cmap='gray')
	
	    ax2.imshow(img2, cmap='gray')

	    fig.show()
	    
   
    def _run_model(self, input_data, model_file):
        """ Run the model on an input grayscale image and convert it into colored onde"""

        tf.compat.v1.disable_eager_execution()


        f = input_data["data_file"]

        inp_img = np.array(Image.open(f).resize((224,224))).astype(np.float) / 128 - 1

        gd = tf.compat.v1.GraphDef.FromString(open(model_file),mode='rb'.read())
        grayscale = tf.compat.v1.placeholder(tf.float32, [1, 224, 224, 1])
        inferred_rgb, = tf.compat.v1.import_graph_def(gd,input_map={"grayscale": grayscale},return_elements=["inferred_rgb:0"])

       
        with tf.compat.v1.Session() as sess:

            result_file = sess.run(inferred_rgb, feed_dict={grayscale: inp_img})
            
            out_img = result_file[0]

            plot(inp_img, out_img)
			
			

        

        
