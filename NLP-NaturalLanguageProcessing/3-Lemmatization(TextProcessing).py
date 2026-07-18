"""
WordNet Lemmatization is an NLP technique that converts a word to its dictionary (base) form, called a lemma, 
by considering the word's meaning and part of speech. 

Unlike stemming, it produces valid English words (e.g., "studying" → "study", 
**"better" → "good"` with the correct part of speech).

#import nltk
#nltk.download('wordnet')
"""

from nltk.stem import WordNetLemmatizer

def _WordNetLemmatizer():
    words = ["playing", "played", "plays",
    "studies", "studying", "studied",
    "running", "runs",
    "connected", "connecting", "connection",
    "Programming","Programe",
    "History","Historically",
    "Congratulations","Congrats"]

    lemmatizer = WordNetLemmatizer()
    print(lemmatizer.lemmatize("Gambling",pos="v"))

    for word in words:
        print(f"{word} ---> {lemmatizer.lemmatize(word,pos='v')}")




if __name__=="__main__":
    _WordNetLemmatizer()
