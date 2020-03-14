from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
from tensorflow import keras, losses
import pandas as pd
import numpy as np

def trainModel():
    df = pd.read_csv("./data.csv")
    df.loc[(df.target == -1),'target'] = 0
    y = to_categorical(df.target)
    df.pop("target")
    X = df.to_numpy()

    model = keras.Sequential([
        keras.layers.Dense(units=100, input_dim=21, activation='relu'),
        keras.layers.Dense(units=100, activation='relu'),
        keras.layers.Dense(units=2, activation='softmax')
    ])

    model.compile(
              optimizer='adam',
              loss=losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy']
    )
    model.fit(
            X,
            y,
            epochs=100,
    )
    model.save("model.h5")

def addRow(encodedData):
    df = pd.read_csv("./data.csv")
    columnList = df.columns
    row = pd.DataFrame(encodedData,columns=columnList)
    df = df.append(row, ignore_index=True)
    df.to_csv("./data.csv", index=False)
    return df.tail(1).index.item()

def editRow(feedback,pos):
    df = pd.read_csv("data.csv")
    df["target"].iloc[pos] = feedback
    df.to_csv("./data.csv", index=False)

def predict(val):
    model = load_model("model.h5")
    prediction = model.predict(val)
    return np.argmax(prediction[0])

