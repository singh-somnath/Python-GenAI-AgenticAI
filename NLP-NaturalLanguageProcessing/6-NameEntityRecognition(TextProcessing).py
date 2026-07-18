from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk
nltk.download('words')
nltk.download('maxent_ne_chunker_tab')

def _NameEntityRecognition():

    paragraph = """
     Dr. A. P. J. Abdul Kalam addressed the European Parliament on 25 April 2007 in Strasbourg, France, becoming the 
     rst Indian President to do so. In his speech, he emphasized that lasting peace and prosperity can be achieved 
     through knowledge, innovation, ethical leadership, and international cooperation. 
     He proposed stronger collaboration between India and the European Union in areas such as science, technology, 
     energy security, healthcare, education, and sustainable development through a World Knowledge Platform. Dr. Kalam 
     also inspired the audience by reciting his famous lines, "Where there is righteousness in the heart, there is 
     beauty in the character...", highlighting that peace in the world begins with righteousness in individuals and 
     harmony in society. His address remains one of his most celebrated international speeches because it combined 
     scientific vision, moral values, and a message of global unity.
        """
    words = word_tokenize(paragraph)
    
    stremmer = SnowballStemmer("english")
    
    words = [stremmer.stem(word) for word in words]

    words = [ word for word in words if word not in set(stopwords.words("english"))]

    words = nltk.pos_tag(words)

    words = nltk.ne_chunk(words)
    nltk.ne_chunk(words).draw()
    #print(words)

if __name__ == "__main__":
    _NameEntityRecognition()