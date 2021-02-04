from PIL import Image
from tflite_runtime.interpreter import Interpreter
from datasets import imagenet
import numpy as np

from helpers.timer import Timer
from helpers.mock_input_generator import MockInputGenerator
from abstract.abstract_workload import AbstractWorkload
from helpers.util import echo


# Performs model execution
class Workload(AbstractWorkload):

    def __init__(self):
        super().__init__()

    def getModel(self):
        return "ApexNet"

    def getFramework(self):
        return "TensorFlow"

    def getApplication(self):
        return "ImageNet"

    def getModelToUse(self):
        return "mobilenet_v1_1.0_224_quant.tflite"
   
    def _run_model(self, input_data, model_file):
        """ Run the model on the given input data ; Return the accuracy"""

        f = input_data["data_file"]

        interpreter = Interpreter(model_file)
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']

        image = Image.open(f).convert('RGB').resize((width, height),
                                                            Image.ANTIALIAS)
        results = self.classify_image(interpreter, image)

        label_id, prob = results[0]

        label_map = imagenet.create_readable_names_for_imagenet_labels()

        echo("Top 1 Prediction: {} {}".format(label_map[label_id], prob))

        echo (results[0:10])

        return prob * 100   #percentage


    def set_input_tensor(self, interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def classify_image(self, interpreter, image, top_k=1):
        """Returns a sorted array of classification results."""
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))

        # If the model is quantized (uint8 data), then dequantize the results
        if output_details['dtype'] == np.uint8:
            scale, zero_point = output_details['quantization']
            output = scale * (output - zero_point)

        ordered = np.argpartition(-output, top_k)
        return [(i, output[i]) for i in ordered[:top_k]]