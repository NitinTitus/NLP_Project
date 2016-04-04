import re
import pickle

def vocab(list,text,char):
    vocabulary=[]
    count=0
    for f in list:
         if f.split(' ')[0]==char:
             words=f.split(' ')
             for i in words:
                 vocabulary.append(i)
         count+=1
    sorted_set=sorted(set(vocabulary))
    f1=open(text,'w')
    for i in sorted_set:
        if(len(i)>1 and vocabulary.count(i)>=2):
            f1.write(i + ' ' + str(vocabulary.count(i)) + '\n')

def find_total_count(text):
    total_frequency=0
    for f in open(text):
        f=re.sub('\n', '', f)
        word,frequency= f.split(' ')
        total_frequency+=int(frequency)
    return total_frequency

def vocab_size():
    count=0
    for f in open('vocabulary.txt'):
        count+=1
    return count

def create_probability_distribution(text,tot_count,pickle_text):
    dict={}
    total=0
    v = vocab_size()
    for f in open('vocabulary.txt'):
        f=re.sub('\n', '', f)
        dict[f]=1
    for f in open(text):
        f=re.sub('\n', '', f)
        word,frequency=f.split(' ')
        dict[word]+=int(frequency)
    for i in dict:
        dict[i]=float(dict[i])/float(tot_count + v)
        total+=dict[i]
    pickle.dump(dict,pickle_text)

def train(training_set):
    vocab(training_set,'vocabulary_positive.txt','+')
    vocab(training_set,'vocabulary_negative.txt','-')
    total_positive_count = find_total_count('vocabulary_positive.txt')
    total_negative_count = find_total_count('vocabulary_negative.txt')
    create_probability_distribution('vocabulary_positive.txt' ,total_positive_count, open('positive.pickle','w'))
    create_probability_distribution('vocabulary_negative.txt' ,total_negative_count,open('negative.pickle','w'))

training_set=[]
for f in open('data_without_stopwords.txt'):
     f=re.sub('\n', '', f)
     training_set.append(f)
train(training_set)