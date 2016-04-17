import re

def create_vocab(file):
    vocabulary_unigram=[]
    vocabulary_bigram=[]
    f1=open(file,'w')
    for f in open('data_without_stopwords.txt'):
        f=re.sub('\n', '', f)
        f=f.strip()
        words = f.split(' ')[1:]
        for i in range(len(words)-1):
             vocabulary_unigram.append(words[i])
             vocabulary_bigram.append(words[i]+' '+words[i+1])
        vocabulary_unigram.append(words[-1])
    sorted_set_unigram=sorted(set(vocabulary_unigram))
    sorted_set_bigram=sorted(set(vocabulary_bigram))
    for i in sorted_set_unigram:
        if vocabulary_unigram.count(i)>=2 and len(i)>1:
            f1.write(i + '\n')
    for i in sorted_set_bigram:
        if vocabulary_bigram.count(i)>=3 and len(str(i).split())!=1 and len(i)>1:
            f1.write(i + '\n')


create_vocab('vocabulary_bigram.txt')
