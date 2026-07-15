#
import numpy as np

def preprocess_input(image):
    image /= 255.0
    return image

def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[2] == 3:
        return image 
    else:
        image = image.convert('RGB')
        return image 