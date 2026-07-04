from nltk.tokenize import sent_tokenize #For convert paragraph to sentence
from nltk.tokenize import word_tokenize #For convert paragraph or sentence to  word
from nltk.tokenize import wordpunct_tokenize

def tokenization():

    corpus="""
    Supervised machine learning uses labeled data to train a model so it can predict 
    the correct output for new inputs.\n
    Unsupervised machine learning works with unlabeled data to 
    discover hidden patterns, relationships, or groups without predefined answers. \n
    Supervised learning is commonly used for tasks such as spam detection, sentiment analysis, 
    and house price prediction. Unsupervised learning is widely applied to customer segmentation, anomaly detection, 
    and data clustering.\n 
    Both approaches are fundamental to artificial intelligence, 
    but they differ primarily in whether the training data includes known labels.
    """
    documents = sent_tokenize(corpus)

    words = word_tokenize(corpus)

    #for sentence in documents:
        #print(word_tokenize(sentence))

    print(wordpunct_tokenize(corpus)) #for punctuation



if __name__=="__main__":
    tokenization()