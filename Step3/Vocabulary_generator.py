import re

def func():
    f1=open('data_without_stopwords.txt','r')
    f2=open('vocabulary.txt','w')
    vocabulary=[]
    for i in f1:
        i=re.sub('\n','',i)
        for j in i.split(' '):
            vocabulary.append(j)
    sorted_set=sorted(set(vocabulary))
    for i in sorted_set:
        if(vocabulary.count(i)>=2 and len(i)>1):
                f2.write(i + '\n')

func()



