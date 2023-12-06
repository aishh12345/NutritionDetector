import tensorflow as tf
import pandas as pd
import numpy as np
from PIL import Image



# Load model
reg_model = tf.keras.models.load_model("BestRegressionWeights\proteinBestInceptionRegv3FF.h5")
class_model = tf.keras.models.load_model("D:/RandomGits/NutritionDetector/72_perc_val_acc_val_loss_model/anotherCopyOfModel29_300Epoch_BestLoss/anotherCopyOfModel29_300Epoch_BestLoss")

# Load Nutrition
df = pd.read_csv("datasets/nutrition101 cut.csv")

test_img = Image.open(r"FastFood\ice_cream\120472.jpg")

dataPath = "FastFood"
valDataset = tf.keras.utils.image_dataset_from_directory(
  dataPath,
  validation_split=0.2,
  subset="validation",
  color_mode = "rgb",
  shuffle = True,
  seed=123,
  image_size=(199, 199),
  batch_size=16)

valDataset2 = tf.keras.utils.image_dataset_from_directory(
  dataPath,
  validation_split=0.2,
  subset="validation",
  color_mode = "rgb",
  shuffle = True,
  seed=123,
  image_size=(150, 150),
  batch_size=16,
  )

protein_labels = list(df['protein'])
name_labels = list(df['name'])

def regression_dataset(data_list):
    def convt_labels(imgs, label):
        def convert_label(label):
            return np.array([data_list[int(y_i)] for y_i in label.numpy()])
        numeric_label = tf.py_function(convert_label, [label], tf.int32)
        return imgs, numeric_label
    return convt_labels


valDataset = valDataset.map(regression_dataset(protein_labels))

normalization_layer = tf.keras.layers.Rescaling(1./255)
valDataset2 = valDataset2.map(lambda x, y: (normalization_layer(x), y))

AUTOTUNE = tf.data.AUTOTUNE
valDataset = valDataset.cache().prefetch(buffer_size=AUTOTUNE)
valDataset2 = valDataset2.cache().prefetch(buffer_size=AUTOTUNE)


def combine_model(cls, reg):
    # return (df.iloc[cls, 2] + reg)/2
    return (reg)

y_pred = np.array(list(map(combine_model, np.argmax(class_model.predict(valDataset2), axis=1), reg_model.predict(valDataset))))
# print()
print(tf.keras.metrics.mean_squared_error(np.concatenate([y for x, y in valDataset], axis=0), np.array([x[0] for x in y_pred])))


