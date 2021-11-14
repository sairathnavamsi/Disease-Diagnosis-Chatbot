import nltk
import warnings
warnings.filterwarnings("ignore")
import random
import string # to process standard python strings

f=open('knowledge base.txt','r',errors = 'ignore')

raw=f.read()
raw=raw.lower()# converts to lowercase
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 


lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi","hiii","hii","hiiii","hiiiii", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi,are you suffering from any health issues?(Y/N)", "hey,are you having any health issues?(Y/N)", "hii there,are you having any health issues?(Y/N)", "hi there,are you having any health issues?(Y/N)", "hello,are you having any health issues?(Y/N)", "I am glad! You are talking to me,are you having any health issues?(Y/N)"]
Basic_Q = ("yes","y")
Basic_Ans = "okay,tell me about your symptoms"
Basic_Om = ("no","n")
Basic_AnsM = "thank you visit again"
fev=("iam suffering from fever", "i affected with fever","i have fever","fever")
feve_r=("which type of fever you have? and please mention your symptoms then we try to calculate your disease.")


# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Checking for Basic_Q
def basic(sentence):
    for word in Basic_Q:
        if sentence.lower() == word:
            return Basic_Ans
def fever(sentence):
    for word in fev:
        if sentence.lower() == word:
            return feve_r

# Checking for Basic_QM
def basicM(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in Basic_Om:
        if sentence.lower() == word:
            
           
            return Basic_AnsM

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(user_response):

    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    print(tfidf[-1])
    vals = cosine_similarity(tfidf[-1], tfidf)
    print(vals)
    idx=vals.argsort()[0][-2]
    print(idx)

    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        sent_tokens.remove(user_response)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx] 
        sent_tokens.remove(user_response)
        return robo_response
      
def chat(user_response):
    user_response=user_response.lower()
   
    if(user_response!='bye'):
        
        if(user_response=='thanks' or user_response=='thank you' ):
            return "You are welcome.."
        elif(basicM(user_response)!=None):
            return basicM(user_response)
        else:
            if(greeting(user_response)!=None):
                return greeting(user_response)
            elif(basic(user_response)!=None):
                return basic(user_response)
            elif(fever(user_response)!=None):
                return fever(user_response)
            else:
                return response(user_response)
                sent_tokens.remove(user_response)                
    else:

        return "Bye! take care.."
    
while (True):
    a=str(input())
    print(chat(a))