import re
import pickle
import math

def find_total_count(text):
    total_frequency=0
    for f in open(text):
        f=re.sub('\n', '', f)
        if f.count(' ')==1:
            word,frequency= f.split(' ')
            total_frequency+=int(frequency)
        else:
            word1,word2,frequency=f.split(' ')
            total_frequency+=int(frequency)
    return total_frequency

def prior_probability(training_set):
    positive=negative=0
    for f in training_set:
        if f.split(' ')[0]=='+':
            positive+=1
        else:
            negative+=1
    return positive,negative

def vocab_size():
    count=0
    for f in open('vocabulary_bigram.txt'):
        count+=1
    return count

def file_size():
    count=0
    for f in open('data_without_stopwords.txt'):
        count+=1
    return count

def create_vocab(training_set,file,char):
    vocabulary_unigram=[]
    vocabulary_bigram=[]
    f1=open(file,'w')
    for f in training_set:
        if(f.split(' ')[0]==char):
            f=f.strip()
            words = f.split(' ')[1:]
            for i in range(len(words)-1):
                vocabulary_unigram.append(words[i])
                vocabulary_bigram.append(words[i]+' '+words[i+1])
            vocabulary_unigram.append(words[-1])
    vocabulary_bigram=[x for x in vocabulary_bigram if vocabulary_bigram.count(x)>=3]
    vocabulary_unigram=[x for x in vocabulary_unigram if vocabulary_unigram.count(x)>=2]
    sorted_set_unigram=sorted(set(vocabulary_unigram))
    sorted_set_bigram=sorted(set(vocabulary_bigram))
    for i in sorted_set_unigram:
        sub=0
        for j in sorted_set_bigram:
                word1,word2=j.split(' ')
                if word1==i or word2==i:
                    sub+=vocabulary_bigram.count(j)
        if (vocabulary_unigram.count(i)-sub)>=2 and len(i)>1:
            f1.write(i + ' ' + str(vocabulary_unigram.count(i)-sub) + '\n')

    for i in sorted_set_bigram:
         if len(str(i).split())!=1 and len(i)>1:
            f1.write(i + ' ' + str(vocabulary_bigram.count(i)) + '\n')

def create_probability_distribution(text,tot_count,pickle_text):
    dict={}
    total=0
    v = vocab_size()
    for f in open('vocabulary_bigram.txt'):
        f=re.sub('\n', '', f)
        dict[f]=1
    for f in open(text):
        f=re.sub('\n', '', f)
        if f.count(' ')==1:
            word,frequency=f.split(' ')
            dict[word]+=int(frequency)
        else:
            word1,word2,frequency=f.split(' ')
            dict[word1+' '+word2]+=int(frequency)
    for i in dict:
        dict[i]=float(dict[i])/float(tot_count + v)
        total+=dict[i]
    pickle.dump(dict,pickle_text)

def train(training_set):
    create_vocab(training_set,'vocabulary_bigram_positive.txt','+')
    create_vocab(training_set,'vocabulary_bigram_negative.txt','-')
    total_positive_count = find_total_count('vocabulary_bigram_positive.txt')
    total_negative_count = find_total_count('vocabulary_bigram_negative.txt')
    create_probability_distribution('vocabulary_bigram_positive.txt' ,total_positive_count, open('positive_bigram.pickle','w'))
    create_probability_distribution('vocabulary_bigram_negative.txt' ,total_negative_count,open('negative_bigram.pickle','w'))

def test(training_set,test_set,positive_count,negative_count):
    vocab=[]
    positive_dict = pickle.load(open('positive_bigram.pickle'))
    negative_dict = pickle.load(open('negative_bigram.pickle'))
    correct=tp=tn=fp=fn=0
    positive_prior,negative_prior=prior_probability(training_set)
    for f in open('vocabulary_bigram.txt'):
        f=re.sub('\n', '', f)
        vocab.append(f)
    for f in test_set:
        f=f.strip()
        words=f.split(' ')[1:]
        positive_probability=0
        negative_probability=0
        for i in range(len(words)-1):
            string=words[i]+ ' ' + words[i+1]
            if string in vocab:
                positive_probability+=math.log(positive_dict[string])
                negative_probability+=math.log(negative_dict[string])
            else:
                size=vocab_size()
                if words[i] in vocab:
                     positive_probability+=math.log(positive_dict[words[i]])
                     negative_probability+=math.log(negative_dict[words[i]])
                else:
                    temp=1.0/(positive_count+size)
                    positive_probability+=math.log(temp)
                    temp=1.0/(negative_count+size)
                    negative_probability+=math.log(temp)
                if words[i+1] in vocab:
                    positive_probability+=math.log(positive_dict[words[i+1]])
                    negative_probability+=math.log(negative_dict[words[i+1]])
                else:
                        temp=1.0/(positive_count+size)
                        positive_probability+=math.log(temp)
                        temp=1.0/(negative_count+size)
                        negative_probability+=math.log(temp)
        positive_probability+=math.log(positive_prior)
        negative_probability+=math.log(negative_prior)
        if(positive_probability>negative_probability):
            if(f.split(' ')[0]=='+'):
                correct+=1
                tp+=1
            else:
                fp+=1
        else:
            if f.split(' ')[0] == '-':
                correct += 1
                tn+=1
            else:
                fn+=1
    return correct,tp,tn,fp,fn


def cross_validation():
    list=[]
    tot_accuracy=0
    fold_size=file_size()/10
    for f in open('data_without_stopwords.txt'):
        f=re.sub('\n', '', f)
        list.append(f)
    for i in range(9,-1,-1):
        test_set=list[i*fold_size:][:fold_size]
        training_set=list[0:i*fold_size] + list[(i+1) * fold_size:]
        train(training_set)
        correct,tp,tn,fp,fn=test(training_set,test_set,find_total_count('vocabulary_bigram_positive.txt'),find_total_count('vocabulary_bigram_negative.txt'))
        accuracy = float(tp+tn)/float(tp+tn+fp+fn)
        print (accuracy*100)
        tot_accuracy+=accuracy
    print ((tot_accuracy/10)*100)

cross_validation()