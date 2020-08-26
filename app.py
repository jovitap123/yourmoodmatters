from keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import sequence
import re
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
from flask import Flask, request, render_template
import numpy as np
app = Flask(__name__)

@app.route('/')
def hello_world():
        return render_template('index.html')

#@app.route('/handle_data', methods=['POST'])
#def handle_data():
    #feeling = request.form['feeling']
    #print(feeling)

    # insert model
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        feeling = request.form['feeling']
        data=[feeling]

        #Text Cleaning
        def remove_url(text):
            return re.sub(r'https?://\S+|www\.\S+', '', text)
        def remove_html(text):
            return BeautifulSoup(text).get_text()
        def words(text):
            return re.sub('[^a-zA-Z]', ' ', text)
        def lower_words(text):  
            return text.lower()
        def stemming(text):
            p_stemmer = PorterStemmer()
            stemmed = [p_stemmer.stem(i) for i in text]  
            return ' '.join(stemmed)

        def clean_text(text):
            url_removed = remove_url(text)
            html_removed = remove_html(url_removed)
            words_only = words(html_removed)
            lowered = lower_words(words_only)
            stemmed = stemming(lowered)
            return stemmed

        data=data.apply(lambda x: clean_text(x))
        
        #Tokenize Cleaned text
        num_words = 2000
        oov_token = '<UNK>'
        pad_type = 'post'
        trunc_type = 'post'

        tokenizer = Tokenizer(num_words=num_words, oov_token=oov_token)
        tokenizer.fit_on_texts(data)
        # Get our training data word index
        word_index = tokenizer.word_index
        # Encode training data sentences into sequences
        test_sequences = tokenizer.texts_to_sequences(data)
        # Pad the training sequences
        test_seq = pad_sequences(test_sequences, padding=pad_type, truncating=trunc_type, maxlen=65)
       
        #Load best model and weights
        json_file=open('bestmodel.json','r')
        loaded_model_json=json_file.read()
        json_file.close()
        best_model=model_from_json(loaded_model_json)
        best_model.load_weights('weights.best.hdf5')
       
        #Predictions
        model_output= np.round(best_model.predict(test_seq),0).astype(int)
   
        if model_output == 1:
            output_feeling = "distressed"
        else:
            output_feeling= "fine"

    return render_template('index.html', output=f"It looks like you are {output_feeling}.")

    #----------------------------------------------

if __name__ =="__main__":
    app.run(debug=True)