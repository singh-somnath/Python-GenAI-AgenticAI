from nltk.stem import PorterStemmer
from nltk.stem import RegexpStemmer
from nltk.stem import SnowballStemmer

def _PorterStemmer():
    words = ["playing", "played", "plays",
        "studies", "studying", "studied",
        "running", "runs",
        "connected", "connecting", "connection",
        "Programming","Programe",
        "History","Historically",
        "Congratulations","Congrats"]

    _stemming = PorterStemmer()

    for word in words:
        print(f"{word} --> {_stemming.stem(word)}")


def _RegexpStemmer():

    regStemmer = RegexpStemmer('ing$|s$|ed$|able$',min=4)
    print(regStemmer.stem("capable"))

def _SnowBallSytammer():
    _snowballStemmer = SnowballStemmer(language="english")

    words = ["playing", "played", "plays",
        "studies", "studying", "studied",
        "running", "runs",
        "connected", "connecting", "connection",
        "Programming","Programe",
        "History","Historically",
        "Congratulations","Congrats"]

    for word in words:
        print(f"{word}<--->{_snowballStemmer.stem(word)}")

if __name__=="__main__":
    _SnowBallSytammer()

###################################################################################33



