import tkinter as tk
from tkinter import messagebox

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


class App:
    def __init__(self, master):
        self.master = master
        master.title("Suicidal Content Detector")

        # Create input label and text box
        self.input_label = tk.Label(master, text="Enter text:")
        self.input_label.pack()
        self.input_textbox = tk.Text(master, height=30, width=100)
        self.input_textbox.pack()

        # Create output label and prediction label
        self.output_label = tk.Label(master, text="Prediction:")
        self.output_label.pack()
        self.prediction_label = tk.Label(master, text="")
        self.prediction_label.pack()

        # Create predict button
        self.predict_button = tk.Button(master, text="Predict", command=self.predict)
        self.predict_button.pack()

        # Load the dataset
        self.data = pd.read_csv("input/dataset.csv")

        # Preprocess the text data
        self.vectorizer = CountVectorizer()
        self.data["Sentence"].fillna("", inplace=True)
        self.X = self.vectorizer.fit_transform(self.data["Sentence"])
        self.y = self.data["Suicidal"]

        # Train a logistic regression model
        self.clf = LogisticRegression(max_iter=1000)
        self.clf.fit(self.X, self.y)

    def predict(self):
        # Get the text from the input box
        new_text = self.input_textbox.get("1.0", "end-1c")

        # Make a prediction on the new text
        new_text_vec = self.vectorizer.transform([new_text])
        prediction = self.clf.predict(new_text_vec)[0]

        # Update the prediction label
        if prediction == 0:
            messagebox.showinfo("Warning", "THIS SITE IS SAFE TO USE ENJOY BROWSING ")
        else:
            messagebox.showwarning("Warning", "THIS SITE CONTAINS SUICIDAL CONTENT SO PLEASE AVOID USING IT")


# Create the GUI app and run it
root = tk.Tk()
app = App(root)
root.mainloop()