
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
        return "ResNet-50v1"

    def getFramework(self):
        return "TensorFlow"

    def getApplication(self):
        return "ImageNet"

    def getModelToUse(self):
        return "saved_model.pb"
   
    def _run_model(self, input_data, model_file):
        """ Run the model on the given input data ; Return the accuracy"""

        f = input_data["data_file"]

        img = np.array(Image.open(f).resize((224,224))).astype(np.float) / 128 - 1

        gd = tf.compat.v1.GraphDef.FromString(open(model_file).read())


        inp= tf.import_graph_def(gd)

        with tf.compat.v1.Session as sess:

            x = sess.graph.get_tensor_by_name('softmax:0')
            predictions = sess.run(x, {'DecodeJpeg:0': img})

        label_map = imagenet.create_readable_names_for_imagenet_labels()

        echo("Top 1 Prediction: {} {} {}".format(predictions.argmax(),label_map[predictions.argmax()], predictions.max()))

        return predictions.max()
