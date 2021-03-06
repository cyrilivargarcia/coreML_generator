
from coremltools import *
import turicreate as turi
import os

model_name = input("Model name: ")
author = input("Author name: ")
license = input("License: ")
short_description = input("Short Description: ")

folder_name = "images"
label_name = "name"
model = "resnet-50"
sframe = "name"

data = turi.image_analysis.load_images(folder_name)

dir_path = len(os.path.dirname(os.path.realpath(__file__)) + folder_name) + 2
p = os.path.realpath(__file__ + "/" + folder_name + "/").split("/")
f = len(p[len(p) - 1])


def get_label(path):
	p = path[dir_path:].split("/")[0]
	return p

data[label_name] = data["path"].apply(get_label)
data.save(sframe + ".sframe")
data.explore()

dataBuffer = turi.SFrame(sframe + ".sframe")

trainingBuffers, testingBuffers = dataBuffer.random_split(0.9)

model = turi.image_classifier.create(trainingBuffers, target=label_name, model=model)

evaluations = model.evaluate(testingBuffers)

print("Accuracy: " + str(evaluations["accuracy"]))

model.save(model_name + ".model")

model.export_coreml(model_name + ".mlmodel")

mlmodel = models.MLModel(model_name + ".mlmodel")
mlmodel.author = author
mlmodel.license = license
mlmodel.short_description = short_description

mlmodel.save(model_name + ".mlmodel")

