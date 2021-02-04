
from PIL import Image
import tensorflow as tf
from datasets import imagenet
import numpy as np

from helpers.timer import Timer
from helpers.mock_input_generator import MockInputGenerator
from abstract.abstract_workload import AbstractWorkload
from helpers.util import echo


# Performs model execution
class Workload(AbstractWorkload):

    def __init__(self, arg):
        super().__init__(arg)

    def getModel(self):
        return "ApexNet"

    def getFramework(self):
        return "TensorFlow"

    def getApplication(self):
        return "ImageNet"

    def getModelToUse(self):
        return "mobilenet_v1_1.0_224_frozen.pb"
   
    def _run_model(self, input_data, model_file):
        """ Run the model on the given input data ; Return the accuracy"""

        f = input_data["data_file"]

        img = np.array(Image.open(f).resize((224,224))).astype(np.float) / 128 - 1

        gd = tf.compat.v1.GraphDef.FromString(open(model_file).read())

        inp,predictions = tf.import_graph_def(gd, return_elements = ['input:0', 'MobilenetV1/Predictions/Reshape_1:0'])

        with tf.compat.v1.Session(graph = inp.graph):
            x = predictions.eval(feed_dict={inp: img.reshape(1, 224,224, 3)})

        label_map = imagenet.create_readable_names_for_imagenet_labels()

        echo("Top 1 Prediction: {} {} {}".format(x.argmax(),label_map[x.argmax()], x.max()))

        return x.max()
