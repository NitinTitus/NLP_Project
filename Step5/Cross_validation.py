import Multinomial_nb_model
import re
import math
import pickle

def prior_probability(training_set):
    positive=negative=0
    for f in training_set:
        if f.split(' ')[0]=='+':
            positive+=1
        else:
            negative+=1
    return positive,negative

def file_size():
    count=0
    for f in open('data_without_stopwords.txt'):
        count+=1
    return count

def test(training_set,test_set):
    vocab=[]
    positive_dict = pickle.load(open('positive.pickle'))
    negative_dict = pickle.load(open('negative.pickle'))
    correct=tp=tn=fp=fn=0
    positive_prior,negative_prior=prior_probability(training_set)
    for f in open('vocabulary.txt'):
        f=re.sub('\n', '', f)
        vocab.append(f)
    for f in test_set:
        words=f.split(' ')
        sentiment = f.split(' ')[0]
        positive_probability=0
        negative_probability=0
        for i in words:
            if i in vocab:
                positive_probability+=math.log(positive_dict[i])
                negative_probability+=math.log(negative_dict[i])
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
        Multinomial_nb_model.train(training_set)
        correct,tp,tn,fp,fn=test(training_set,test_set)
        accuracy = float(tp+tn)/float(tp+tn+fp+fn)
        print (accuracy*100)
        tot_accuracy+=accuracy
    print ((tot_accuracy/10)*100)

cross_validation()