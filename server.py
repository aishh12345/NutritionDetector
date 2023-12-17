import tensorflow as tf
import pandas as pd
import numpy as np
from PIL import Image

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


# Load model
reg_model_protein = tf.keras.models.load_model("BestRegressionWeights/proteinBestInceptionRegv3FF.h5")
reg_model_carb = tf.keras.models.load_model("BestRegressionWeights/carbBestInceptionRegv3FF.h5")
reg_model_fats = tf.keras.models.load_model("BestRegressionWeights/fatsBestInceptionRegv3FF.h5")
class_model = tf.keras.models.load_model("72_perc_val_acc_val_loss_model/anotherCopyOfModel29_300Epoch_BestLoss/anotherCopyOfModel29_300Epoch_BestLoss")

# Load Nutrition
df = pd.read_csv("datasets/nutrition101 cut.csv")

def preprocess_regression(img):
    return np.expand_dims(np.asarray(img.resize((199,199))), axis=0)

def preprocess_classification(img):
    return np.array([np.asarray(img.resize((150,150))) / 255.0])

# test_img = Image.open(r"FastFood\ice_cream\120472.jpg")




# predicton = (class_model.predict(preprocess_classification(test_img)))

# print((df.iloc[np.argmax(predicton), 2] + reg_model.predict(preprocess_regression(test_img))[0][0])/2)


# app = FastAPI()


# Endpoint takes in image, returns prediction
@app.post("/regression_cnn")
async def regressionCNN(file: UploadFile = File(...)) -> dict:
    print(file.file)
    contents = await file.read()
    print(len(contents), '\n\n\n\n\n')
    im = Image.fromarray(np.fromstring(contents, np.uint8))
    
    return {
        "prediction_protein": reg_model_protein.predict(preprocess_regression(im))[0][0],
        "prediction_carbohydrates": reg_model_carb.predict(preprocess_regression(im))[0][0],
        "prediction_fats": reg_model_fats.predict(preprocess_regression(im))[0][0]
    }

# Endpoint takes in image, returns prediction
@app.post("/classification_cnn")
async def classificationCNN(file: UploadFile = File(...)) -> dict:
    contents = await file.read()
    im = Image.fromarray(np.fromstring(contents, np.uint8))
    im = im.convert('RGB')

    print(preprocess_classification(im).shape)

    prediction = np.argmax(class_model.predict(preprocess_classification(im)))

    print(df.iloc[prediction, 1])
    return {
        "prediction_protein": df.iloc[prediction, 2],
        "prediction_carbohydrates": df.iloc[prediction, 3],
        "prediction_fats": df.iloc[prediction, 4],
    }


