import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from many_stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import sys
	
def find_topics(comments, quantity):
    tokenizer = RegexpTokenizer(r'\w+')

    #Load stop words list
    stop_words = list(stopwords.words('arabic'))
    stop_words.extend(set(get_stop_words('ar')))
    #Stemmer definition
    p_stemmer = PorterStemmer()
    #Add comment to local list
    raw_data = []
    raw_data.extend(comments)
    #List for tokenized texts
    texts = []
    #Loop through raw texts
    for text in raw_data:
        #Clean and tokenize
        raw = text.lower()
        tokens = tokenizer.tokenize(raw)
        #Remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in stop_words and len(i)>4]
        #Stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        #Add tokens to final list
        texts.append(stemmed_tokens)
    #Turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
    #Convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    #Generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=int(quantity), id2word = dictionary, passes=20)
    
    return(ldamodel.print_topics(num_topics=int(quantity), num_words=5))