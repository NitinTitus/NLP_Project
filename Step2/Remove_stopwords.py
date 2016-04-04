import re

def func():
    f1=open('data_without_stopwords.txt','w')
    stopwords=[]
    vocabulary=[]
    for i in open('stopwords.txt'):
        i=re.sub('\n', '', i)
        stopwords.append(i.lower())
    for f in open('data.txt'):
        f=re.sub('[^A-Za-z\s\+\-\']+',' ',f)
        f=re.sub('\'','',f)
        f=re.sub('\s+', ' ', f)
        words=f.split(' ')
        for i in words:
            i=i.lower()
            if i not in stopwords:
                f1.write(i + ' ')
        f1.write('\n')

func()



