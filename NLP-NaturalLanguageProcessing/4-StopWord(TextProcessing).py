from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
def _stopWord():

    paragraph = """
    Good afternoon, Ladies and Gentlemen.

    I am delighted to be with the honourable Members of the European Parliament on the occasion of the Golden Jubilee year of the European Union. I was wondering what thoughts I could share with you. As you are aware, as a democratic nation India has experience in providing leadership to over one billion people with multi-language, multicultural and multi-religious systems. I wish to share this experience with you, friends.

    European civilisation has a unique place in human history. Its people were valiantly engaged in the adventure of exploring the Planet Earth, resulting in the discovery of many ideas and systems. Europe has seen the birth of pioneers in science, leading to the development of technologies. Europe was the theatre of conflicts among the nations lasting hundreds of years, including the two World Wars. Now, with this backdrop and these dynamics, you have established the European Union with a vision of peace and prosperity for the entire region. The European Union has become an example for connectivity among nations, probably with no possibility of war, leading to lasting regional peace.

    Before I started out on my journey to Europe, I was thinking: why are Europe and India unique and natural partners? Do we share a common history and heritage and, possibly in the future, a common destiny? This was the question. I was astonished by what I found: the depth and vitality of our inter-connectedness, through language, culture, ancient beliefs, ideologies and the movement of people, have stood the test of time. This has matured into a very strong bond through sustained trade and intellectually satisfying collaboration in many areas of science and technology. For example, on 23 April 2007, the Italian scientific satellite Agile was launched by the Indian Polar Satellite Launch Vehicle rocket system into a very precise orbit. Scientists from India and Europe are very excited. Let us congratulate them.

    India is a country that has learnt over the years to evolve and maintain a unique unity amid diversity. Similarly, the European Union’s greatest contribution has been to demonstrate to the world that it is possible to build a strong union of nations without compromising national identities. It has become an inspirational model and an example to emulate for every region in the world. The European Union and India support a social form of economic development and we encourage a model of growth with equity. Both are conscious of the need for growth to respect the environment and to make it sustainable for future generations. With India’s and the European Union’s centuries of valuable experience, we can develop a doctrine of global cooperation based on the foundation of regional collaboration and core competencies of our nations.

    The European Union and India radiate a message to the world that regional cooperation and interregional collaboration will lead to a win-win situation for all, so that we can have a politically and socio-economically emergent civilisation. Our contribution will be successful if, before the 21st century is over, we are able to make all regions transform into happy unions leading to the emergence of a world of unions. In this context, I am reminded of the dream of an Indian poet who said 3000 years ago in the Tamil classic: ,which means, ‘I am a world citizen. Every citizen is my own kith and kin’. He said that 3000 years ago.

    Against this backdrop, I have brought from India a message to launch three important Indo-European tasks that could contribute to global peace and prosperity. I propose these missions on the basis of India’s experience and the European Union’s dynamics.

    The first task is the evolution of an enlightened society, in which citizens have a system of values, leading to a prosperous and peaceful world.

    The second idea is creating energy independence. Normally people talk about energy security. I am talking about energy independence: a three-dimensional approach to energy choice that aims to achieve a clean world.

    The third aim is a World Knowledge Platform to bring together the core skills of the European Union and India in certain areas in order to provide solutions to critical issues like water, healthcare and capacity-building.

    When nations join together to build a cohesive society, it is necessary to ensure that the benefits of development encompass all sections of society. Worldwide poverty, illiteracy, unemployment and deprivation are driving forward the forces of anger and violence. These forces are linked to some earlier real or perceived historical enmities, tyrannies, injustice, inequalities, ethnic issues and religious fundamentalism that are flowing into an outburst of extremism worldwide. Both India and the European Union have witnessed and are witnessing the unsavoury acts of certain misguided sections of society. Together we must address the root causes of such phenomena in order to find lasting ways to promote peace. How do we do that?

    We need a carrier of eternal goodness and wholesomeness in human conduct, which is called ‘righteousness’. As we say in India:

    ‘Where there is righteousness in the heart

    There is beauty in the character.

    When there is beauty in the character,

    There is harmony in the home.

    When there is harmony in the home,

    There is order in the nation.

    When there is order in the nation,

    There is peace in the world.’
        """
    words = word_tokenize(paragraph)
    
    stremmer = SnowballStemmer("english")
    
    words = [stremmer.stem(word) for word in words]

    words = [ word for word in words if word not in set(stopwords.words("english"))]

    print(' '.join(words))

if __name__ == "__main__":
    _stopWord()