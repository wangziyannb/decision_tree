import csv
class Node():
    def __init__(self,name,count,parent,impurity=0):
        self.name=name
        self.count=count
        self.impurity=impurity
        self.children={}
        self.parent =parent



def preprocess1(data):
    l_feature=len(data[0])-1
    possible_value=[set() for _ in range(l_feature)]
    for i in range(l_feature):
        for row in data:
            possible_value[i].add(row[i])
    return possible_value #p=[{'feature0':'不重复出现数字‘}，{}...]

def buildtree(con_id,dcheader,l1,l2,gi1,gi2,dad=Node(None, None, None, None)):
    #if len(l1)<=2 or len(l2)<=2:return
    Name_son1 = (f'{dcheader[con_id[0]]} >={con_id[1]}')
    Name_son2 = (f'{dcheader[con_id[0]]} < {con_id[1]}')
    son1 = Node(Name_son1,len(l1),dad,gi1)
    son2 = Node(Name_son2,len(l2),dad,gi2)
    dad.children[Name_son1] = son1
    dad.children[Name_son2] = son2
    if gi1 < gi2:
        dad = son2
        z, x, c, v, b, best_gain2 = splitdata(preprocess1(l2), l2)
        if best_gain2 >0:
            buildtree(z,dcheader,x,c,v,b,dad)
        else: return
    else:
        dad = son1
        z, x, c, v, b, best_gain1 = splitdata(preprocess1(l1), l1)
        if best_gain1 >0:
            buildtree(z,dcheader,x,c,v,b,dad)
        else: return








def splitdata (possible_value,data):
    global condition_id, ls1, ls2, ginitai1, ginitai2
    bestgini=shuji(data)
    bestgain=0.0
    li1 = []
    li2 = []
    for i, n in enumerate(possible_value):
        for q in n:
            for row in data:
                if row[i]>=q:
                    li1.append(row)
                else:li2.append(row)
            gini1 = shuji(li1)
            gini2 = shuji(li2)
            gain = bestgini-(len(li1)/len(data))*gini1-(len(li2)/len(data))*gini2
            if gain >bestgain:
                bestgain = gain
                condition_id = [i,q]
                ls1 = li1
                ls2 = li2
                ginitai1 = gini1
                ginitai2 = gini2
            li1 = []
            li2 = []
    return condition_id, ls1, ls2, ginitai1, ginitai2, bestgain

def shuji(ww):
    gini=0
    chang = len(ww)
    temp=preprocess0(ww)
    for i in temp:
        gini+=(temp[i]/chang)**2
    return 1-gini


def preprocess0 (data):
    datacount = {}
    for row in data:

        key=row[-1]

        if datacount.get(key)==None:
            datacount[key]=1
        else:datacount[key]+=1
    return datacount #total={'feature0':'count','feature2':'count'...}

def load(path):
    reader = csv.reader(open(path, 'r'))
    dcheader = {}
    lsHeader = next(reader)
    for i, szY in enumerate(lsHeader):
        colid = i
        dcheader[colid] = szY

    data=[row for row in reader]
    return data, dcheader


if __name__ == '__main__':
    Path = 'fishiris.csv'
    gdad=Node(None, None, None, None)
    Data, dchead = load(Path)
    a_, m_, op_, d_, e_, qwe_ = splitdata(preprocess1(Data), Data)
    buildtree(a_, dchead, m_, op_, d_, e_, gdad)
    # not stable use with caution
ascd=1