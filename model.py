import pandas as pd
import nltk
import seaborn as sns
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn import metrics

# Load dataset
data = pd.read_csv('input/dataset.csv')

# Select only Suicidal and Sentence columns
data = data[['Sentence', 'Suicidal']]

# Remove null rows
data = data.dropna()

# Preprocess the text data
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

data['Sentence'] = data['Sentence'].apply(preprocess)

# Save suicidal keyword list to file
with open('input/suicidal_keywords.txt', 'w') as f:
    f.write('suicide\nsuicidal\nkill myself\ntake my own life\nend my life\n')

# Split the data into training and testing sets (80/20 split)
split = int(0.8 * len(data))
X_train, X_test, y_train, y_test = data['Sentence'][:split], data['Sentence'][split:], data['Suicidal'][:split], data['Suicidal'][split:]

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train and test models
classifiers = {'Naive Bayes': MultinomialNB(),
               'Gradient Boosting': GradientBoostingClassifier(),
               'logistic regression': LogisticRegression(C=4, max_iter=1000, penalty='l2'),
               'Random Forest': RandomForestClassifier()
               }

for name, clf in classifiers.items():
    clf.fit(X_train_vectorized, y_train)
    y_pred = clf.predict(X_test_vectorized)
    print(f'{name} classifier:\n{classification_report(y_test, y_pred)}\nAccuracy: {accuracy_score(y_test, y_pred)}\n')
    # Visualise model prediction vs truth
    sns.heatmap(metrics.confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='YlGnBu')
    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    plt.show()
