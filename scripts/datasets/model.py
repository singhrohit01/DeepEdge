import PIL
from PIL import Image
from IPython import display
import tensorflow as tf
from datasets import imagenet
import numpy as np
img = np.array(PIL.Image.open('/home/atomicpi/image.jpeg').resize((224,224))).astype(np.float) / 128 - 1
gd = tf.GraphDef.FromString(open('home/atomicpi/mobilenet_v1_1.0_224_frozen.pb','rb').read())
inp,predictions = tf.import_graph_def(gd, return_elements = ['input:0', 'MobilenetV1/Predictions/Reshape_1.0'])
with tf.Session(graph = inp.graph):
    x = predictions.eval(feed_dict={inp: img.reshape(1, 224,224, 3)})
label_map = imagenet.create_readable_names_for_imagenet_labels()
display.display(PIL.Image.open('/home/atomicpi/image.jpeg'))
print("Top 1 Prediction: ", x.argmax(),label_map[x.argmax()], x.max())

