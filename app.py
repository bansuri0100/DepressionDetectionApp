from flask import Flask, redirect, render_template, request, url_for, session
import time
import re

import pandas as pd
import numpy as np
import spacy
nlp=spacy.load('en_core_web_sm')
import nltk
from sklearn.model_selection import train_test_split

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=['GET', 'POST'])
def index():
	try:
		inp = session["inp"]
		count = session["count"]
	except KeyError:
		count = session["count"] = 0
		inp = session["inp"] = ""
		if request.method == "GET":
			return render_template("index.html")

		if request.method == 'POST':
			inp = request.form['data']
			if inp == '':
				msg='sorry..could u please repeat!!!!'
				return render_template("index.html",msg=msg)
        
			else:
				inp = request.form['data']
				

				df4=pd.read_csv('cleaned_data.csv')
			
				X = df4['cleaned_sentence']
				y = df4['emotion']

				X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)


# In[4]:


				from sklearn.pipeline import Pipeline
				from sklearn.feature_extraction.text import TfidfVectorizer
				from sklearn.svm import LinearSVC

				text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', LinearSVC()),
				])

# Feed the training data through the pipeline
				text_clf.fit(X_train.values.astype('U'), y_train) 


# In[5]:


				def process(str):
					corpus=[]
					sentence=re.sub('[^a-zA-Z]', ' ',str)
					sentence=sentence.lower()
					sentence=sentence.split()
   
					sentence=[s for s in sentence if not nlp.vocab[s].is_stop]
					sentence=' '.join(sentence)
					sent=nlp(sentence)   
					sent2=[s.lemma_ for s in sent ]
					sentence2=' '.join(sent2)
					return(sentence2)


# In[20]:



    
				inp=process(inp)   
				z=pd.Series(inp)
				predictions = text_clf.predict(z)
				predictions
				inp=predictions[0]
				
				session["inp"]=inp
				session["count"]=session["count"]+1
				return render_template("index.html",msg=inp)

	return render_template("index.html")








if __name__ == '__main__':
    app.run(debug=True)
