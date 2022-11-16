import csv
from sklearn.model_selection import train_test_split
class Node():
    def __init__(self,name,count,parent,impurity=0):
        self.name=name
        self.count=count
        self.impurity=impurity
        self.children={}
        self.parent =parent
        self.label = {}



def preprocess1(data):
    l_feature=len(data[0])-1
    possible_value=[set() for _ in range(l_feature)]
    for i in range(l_feature):
        for row in data:
            possible_value[i].add(row[i])
    return possible_value #p=[{'feature0':'不重复出现数字‘}，{}...]

def findcommon (li):
    names = []
    for lis in li:
        names.append(lis[-1])
    return max(set(names), key=names.count)



def buildtree(con_id,dcheader,l1,l2,gi1,gi2,dad=Node(None, None, None, None),prunegini=0.000):
    #if len(l1)<=2 or len(l2)<=2:return
    Name_son1 = {con_id[0] : con_id[1]}
    Name_son2 = {con_id[0] : con_id[1]}
    son1 = Node(Name_son1,len(l1),dad,gi1)
    son2 = Node(Name_son2,len(l2),dad,gi2)
    dad.children[f'{dcheader[con_id[0]]} >={float(con_id[1])}'] = son1
    dad.children[f'{dcheader[con_id[0]]} < {float(con_id[1])}'] = son2
    if gi2 >=prunegini:
        dad2 = son2
        cond_id, lis1, lis2, gin1, gin2, best_gain2 = splitdata(preprocess1(l2), l2)
        if best_gain2 >0:
            buildtree(cond_id, dcheader, lis1, lis2, gin1, gin2, dad2,prunegini)
    else: son2.label = findcommon(l2)
    if gi1 >=prunegini:
        dad1 = son1
        cond_id_, lis1_, lis2_, gin1_, gin2_, best_gain1 = splitdata(preprocess1(l1), l1)
        if best_gain1 >0:
            buildtree(cond_id_, dcheader, lis1_, lis2_, gin1_, gin2_, dad1,prunegini)
    else: son1.label = findcommon(l1)
    return








def splitdata (possible_value,data):
    global condition_id, ls1, ls2, ginitai1, ginitai2
    bestgini=calc_gini(data)
    bestgain=0.0
    li1 = []
    li2 = []
    for i, n in enumerate(possible_value):
        for q in n:
            for row in data:
                if row[i]>=q:
                    li1.append(row)
                else:li2.append(row)
            gini1 = calc_gini(li1)
            gini2 = calc_gini(li2)
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

def calc_gini(ww):
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

def predict (data,dchead,dad):
    if dad.label:
        return print(dad.label)

    for i in dad.children:
        idx = set(dad.children[i].name.keys()).pop()
        value = float(set(dad.children[i].name.values()).pop())
        break
    if data[idx] >=value:
        dad_ = dad.children[i]
        predict(data, dchead, dad_)
    else:
        dad_ = dad.children[f'{dchead[idx]} < {value}']
        predict(data, dchead, dad_)






if __name__ == '__main__':
    Path = 'fishiris.csv'
    gdad=Node(None, None, None, None)
    Data, dchead = load(Path)
    X_train, X_test = train_test_split(Data, test_size=0.2, random_state=42)
    condition_id, list_1, list_2, gini1, gini2, bestgain = splitdata(preprocess1(X_train), X_train)
    buildtree(condition_id, dchead, list_1, list_2, gini1, gini2, gdad, prunegini=0.05)
    for i in X_test:
        i.pop()
        dt_test = [float(x) for x in i]
        predict(dt_test, dchead, gdad)
    testvalue = [5, 3.6, 1.4, 0.2]
    predict(testvalue, dchead, gdad)
    # below for debug
ascd=1