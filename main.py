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

def buildtree(con_id,dcheader,l1,l2,gi1,gi2,dad):
    if len(l1)<=2 or len(l2)<=2:return
    Name_son1 = (f'{dcheader[con_id[0]]} <={con_id[1]}')
    Name_son2 = (f'{dcheader[con_id[0]]} > {con_id[1]}')
    son1 = Node(Name_son1,len(l1),dad,gi1)
    son2 = Node(Name_son2,len(l2),dad,gi2)
    dad.children[Name_son1] = son1
    dad.children[Name_son2] = son2
    if gi1 < gi2:
        son2 = dad
        a,b,c,d,e = splitdata(preprocess1(l2), l2)
        buildtree(a,dcheader,b,c,d,e,dad)

    else:
        son1 = dad
        a, b, c, d, e = splitdata(preprocess1(l1), l1)
        buildtree(a, dcheader, b, c, d, e, dad)








def splitdata (possible_value,data):
    bestgini=shuji(data)
    li1 = []
    li2 = []
    exit_ = False
    for i, n in enumerate(possible_value):
        o = 0
        for q in n:
            o += 1
            for row in data:
                if row[i]<=q:
                    li1.append(row)
                else:li2.append(row)
                gini1 = shuji(li1)
                gini2 = shuji(li2)

            xiao=min(gini1,gini2)
            if gini1 == 0 or gini2 == 0:
                condition_id = [i,q] #i=coloum number, q=specific value under i coloum
                exit_ = True
                break
            if xiao<bestgini:
                bestgini = gini1
                condition_id = [i,q]
                if i != len(possible_value)-1 and o != len(n):
                    li1 = []
                    li2 = []
        if exit_:
            break
    return condition_id,li1,li2,gini1,gini2

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
    Path = ('fishiris.csv')
    Data,dchead = load(Path)
    a, b, c, d, e = splitdata(preprocess1(Data), Data)
    dad = Node(None, None, None, None)
    buildtree(a, dchead, b, c, d, e, dad)
ascd=1