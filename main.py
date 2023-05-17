import json  # to print list/dict in textbox
import tkinter as tk  # root GUI module
import tkinter.scrolledtext as scrolledtext  # module for scrollable text widget
import tkinter.ttk as ttk  # themed GUI module
from tkinter.filedialog import askopenfile  # module to read file
from tkinter import messagebox
import requests  # module to get all contents of a website
from bs4 import BeautifulSoup  # module to get only text from a website
from PIL import Image, ImageTk  # module to open and load a image
from ttkthemes import ThemedStyle  # module to use in-built GUI themes


import tkinter as tk
from tkinter import messagebox

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression




# class to get all frames together
class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs, ):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)

        ex = tk.Menu(menu, tearoff=0)
        menu.add_cascade(menu=ex, label="Exit")
        ex.add_command(label="Exit",
                       command=self.destroy)

        tk.Tk.config(self, menu=menu)

        for F in (Startpage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Startpage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Home page
class Startpage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Detection of sucidial ideation", font=("Simplifica", 22))  # page heading
        label.pack(pady=5, padx=5)

        ttk.Label(self, text="").pack()

        button1 = ttk.Button(self, text="Detect ",
                             command=lambda: controller.show_frame(PageOne))  # got to detect page
        button1.pack()

        ttk.Label(self, text="").pack()

        button2 = ttk.Button(self, text="About",
                             command=lambda: controller.show_frame(PageTwo))  # got to about page
        button2.pack()

        ttk.Label(self, text="").pack()

        img = ImageTk.PhotoImage(Image.open(r'wallpaper.jpg').resize((1200, 700)))  # set the home page image
        img.image = img
        ttk.Label(self, image=img).pack()


#   *****   PAGES   *****
# Detect page
class PageOne(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Detect Suicidal Thoughts from Webpages", font=("Simplifica", 22))  # page heading
        label.pack(pady=5, padx=5)

        ttk.Label(self, text="\n").pack()

        ttk.Label(self, text="Enter a webpage", font=(18)).pack()
        text = tk.Entry(self, font=(26), width=70, bg="lightgray")  # textbox to enter a website
        text.pack()

        ttk.Label(self, text="").pack()

        # load the file containing fixed keywords
        j = []
        f = open(r'keywords.txt')
        for line in f:
            j.append(line.strip())
        f.close()
        d = dict.fromkeys(j, 0)

        # code to scan the website given in textbox
        def scan():
            count = 0
            url = text.get()
            text.delete(0, "end")
            result = requests.get(url.strip())
            soup = BeautifulSoup(result.content, 'lxml')
            for i in soup.get_text().split():
                if (i.lower() in j):
                    count += 1
                    if i.lower() in d:
                        d[i.lower()] += 1
            l3.config(state=tk.NORMAL)
            l3.delete('1.0', "end")
            di = dict(sorted(d.items(), reverse=True, key=lambda item: item[1]))
            lis = [(k, v) for k, v in di.items() if v >= 1]
            if count == 0:

                l3.insert(tk.END,
                          url.strip() + " = " + str(count) + "\n\nKeywords matched:  \n" + json.dumps(lis) + "\n\n Predicted output:No")
                messagebox.showinfo("Warning", "THIS SITE IS SAFE TO USE ENJOY BROWSING ")
            else:
                l3.insert(tk.END,
                          url.strip() + " = " + str(count) + "\n\nKeywords matched:  \n" + json.dumps(lis) + "\n\n Predicted output:Yes")
                messagebox.showwarning("Warning", "THIS SITE CONTAINS SUICIDAL CONTENT SO PLEASE AVOID USING IT")
            l3.config(state=tk.DISABLED)

        b2 = ttk.Button(self, text="Scan", command=scan)
        b2.pack()

        ttk.Label(self, text="").pack()

        # code to open and scan the list of websites given in a text file
        def open_n_scan():
            files = askopenfile(mode='r', filetypes=[("Text File", "*.txt")])
            l3.config(state=tk.NORMAL)
            l3.delete('1.0', "end")
            for url in files:
                count = 0
                result = requests.get(url.strip())
                soup = BeautifulSoup(result.content, 'lxml')
                for i in soup.get_text().split():
                    if (i.lower() in j):
                        count += 1
                l3.insert(tk.END, url.strip() + " = " + str(count) + "\n")
            l3.config(state=tk.DISABLED)

        ttk.Label(self, text="Select your text file containing urls", font=(18)).pack()

        b1 = ttk.Button(self, text="Open and Scan", command=open_n_scan)
        b1.pack()

        ttk.Label(self, text="").pack()

        l3 = scrolledtext.ScrolledText(self, font=(18), height=10, width=70, bg="lightgray",
                                       state=tk.DISABLED)  # multiline textbox
        l3.pack()

        ttk.Label(self, text="").pack()

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(Startpage))  # go to home page
        button1.pack()

        ttk.Label(self, text="").pack()

        button2 = ttk.Button(self, text="About",
                             command=lambda: controller.show_frame(PageTwo))  # got to about page
        button2.pack()


# About page
class PageTwo(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="About", font=("Simplifica", 22))  # page heading
        label.pack(pady=5, padx=5)

        ttk.Label(self, text="").pack()

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(Startpage))  # got to home page
        button1.pack()

        ttk.Label(self, text="").pack()

        button2 = ttk.Button(self, text="Detect",
                             command=lambda: controller.show_frame(PageOne))  # got to detect page
        button2.pack()

        ttk.Label(self, text="").pack()

        tk.Message(self, relief="sunken", bd=4, font=(20), width=1100,
                   text="Suicide is a serious public health problem that can have long-lasting effects on individuals, families, and communities. The good news is that suicide is preventable. Preventing suicide requires strategies at all levels of society. This includes prevention and protective strategies for individuals, families, and communities. Everyone can help prevent suicide by learning the warning signs, promoting prevention and resilience, and a committing to social change.").pack()
        # Info on suicide
        ttk.Label(self, text="").pack()

        tk.Message(self, relief="sunken", bd=4, font=(20), width=1100,
                   text=" Contact the National Suicide Prevention Lifeline Call 1-800-273-TALK (1-800-273-8255)   You’ll be connected to a skilled, trained counselor in your area. For more information, visit the National Suicide Prevention Lifelineexternal icon").pack()
        # Info on suidide content
        ttk.Label(self, text="").pack()

        tk.Message(self, relief="sunken", bd=4, font=(20), width=1100,
                   text=" Coping and problem-solving skills, Cultural and religious beliefs that discourage suicide, Connections to friends, family, and community support, Supportive relationships with care providers, Availability of physical and mental health care, Limited access to lethal means among people at risk").pack()
        # About
        ttk.Label(self, text="").pack()

        ttk.Label(self, text="", font=(20)).pack()  # copyright


app = MyApp()

# set default app theme
style = ThemedStyle(app)
style.set_theme("plastik")

# set app icon
icon = ImageTk.PhotoImage(Image.open(r'icon.jpg'))
app.iconphoto(True, icon)

app.resizable(0, 0)
app.title("Detect web pages with Suicidal Thoughts")  # app title
app.state('zoomed')  # maximized app by default
app.mainloop()



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
