import csv

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from Tracer import Tracer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report


class Node:
    def __init__(self, name, count, parent, impurity=0):
        self.name = name
        self.count = count
        self.impurity = impurity
        self.children = {}
        self.parent = parent
        self.label = {}


def preprocess1(data):
    l_feature = len(data[0]) - 1
    possible_value = [set() for _ in range(l_feature)]
    classes = set()
    for i in range(l_feature):
        for row in data:
            possible_value[i].add(row[i])
            if i == 0:
                classes.add(row[l_feature])
    return possible_value, classes  # p=[{'feature0':'不重复出现数字‘}，{}...]


def findcommon(li):
    names = []
    for lis in li:
        names.append(lis[-1])
    return max(set(names), key=names.count)


def buildtree(con_id, dcheader, l1, l2, gi1, gi2, dad=Node(None, None, None, None), prunegini=0.000):
    # if len(l1)<=2 or len(l2)<=2:return
    Name_son1 = {con_id[0]: con_id[1]}
    Name_son2 = {con_id[0]: con_id[1]}
    son1 = Node(Name_son1, len(l1), dad, gi1)
    son2 = Node(Name_son2, len(l2), dad, gi2)
    dad.children[f'{dcheader[con_id[0]]} >={float(con_id[1])}'] = son1
    dad.children[f'{dcheader[con_id[0]]} < {float(con_id[1])}'] = son2
    if gi2 >= prunegini:
        dad2 = son2
        cond_id, lis1, lis2, gin1, gin2, best_gain2 = splitdata(preprocess1(l2)[0], l2)
        if best_gain2 > 0:
            buildtree(cond_id, dcheader, lis1, lis2, gin1, gin2, dad2, prunegini)
    else:
        son2.label = findcommon(l2)
    if gi1 >= prunegini:
        dad1 = son1
        cond_id_, lis1_, lis2_, gin1_, gin2_, best_gain1 = splitdata(preprocess1(l1)[0], l1)
        if best_gain1 > 0:
            buildtree(cond_id_, dcheader, lis1_, lis2_, gin1_, gin2_, dad1, prunegini)
    else:
        son1.label = findcommon(l1)
    return


def splitdata(possible_value, data):
    global condition_id, ls1, ls2, ginitai1, ginitai2
    bestgini = calc_gini(data)
    bestgain = 0.0
    li1 = []
    li2 = []
    for i, n in enumerate(possible_value):
        for q in n:
            for row in data:
                if row[i] >= q:
                    li1.append(row)
                else:
                    li2.append(row)
            gini1 = calc_gini(li1)
            gini2 = calc_gini(li2)
            gain = bestgini - (len(li1) / len(data)) * gini1 - (len(li2) / len(data)) * gini2
            if gain > bestgain:
                bestgain = gain
                condition_id = [i, q]
                ls1 = li1
                ls2 = li2
                ginitai1 = gini1
                ginitai2 = gini2
            li1 = []
            li2 = []
    return condition_id, ls1, ls2, ginitai1, ginitai2, bestgain


def calc_gini(ww):
    gini = 0
    chang = len(ww)
    temp = preprocess0(ww)
    for i in temp:
        gini += (temp[i] / chang) ** 2
    return 1 - gini


def preprocess0(data):
    datacount = {}
    for row in data:
        key = row[-1]
        if datacount.get(key) is None:
            datacount[key] = 1
        else:
            datacount[key] += 1
    return datacount  # total={'feature0':'count','feature2':'count'...}


def load(path, mapping=None):
    reader = csv.reader(open(path, 'r'))
    dcheader = {}
    lsHeader = next(reader)
    for i, szY in enumerate(lsHeader):
        colid = i
        dcheader[colid] = szY
    data = []
    for r in reader:
        for i in range(len(r)):
            if mapping is not None:
                r[i] = mapping(r[i])
        data.append(r)
    return data, dcheader


mapping = {}


def entry_mapping(attr):
    global mapping
    try:
        return str(float(attr))
    except:
        if mapping is None:
            mapping = {}
        if mapping.get(attr) is not None:
            return mapping[attr]
        else:
            mapping[attr] = len(mapping)
            return mapping[attr]


def predict(data, dchead, dad):
    if dad.label:
        return dad.label
    idx = value = i = None
    for i in dad.children:
        idx = set(dad.children[i].name.keys()).pop()
        value = float(set(dad.children[i].name.values()).pop())
        break
    if idx is None or value is None:
        return 16
    if data[idx] >= value:
        dad_ = dad.children[i]
        return predict(data, dchead, dad_)
    else:
        dad_ = dad.children[f'{dchead[idx]} < {value}']
        return predict(data, dchead, dad_)


class Metrics:
    def __init__(self, cm, class_label):
        self.cm = cm
        self.class_label = class_label
        self.precision = self.calculate_precision()
        self.recall = self.calculate_recall()
        self.f1_score = self.calculate_f1_score()

    def calculate_precision(self):
        precision = {}
        for c in self.class_label:
            index = self.class_label[c]
            for i in range(len(self.class_label)):
                p = self.cm[index][index] / self.cm[len(self.cm) - 1][index]
                precision[c] = p
        return precision

    def calculate_recall(self):
        recall = {}
        for c in self.class_label:
            index = self.class_label[c]
            for i in range(len(self.class_label)):
                p = self.cm[index][index] / self.cm[index][len(self.cm) - 1]
                recall[c] = p
        return recall

    def calculate_f1_score(self):
        f1 = {}
        for c in self.class_label:
            f = ((1 + 1 * 1) * self.precision[c] * self.recall[c]) / ((1 * 1) * self.precision[c] + self.recall[c])
            f1[c] = f
        return f1


if __name__ == '__main__':
    Path = 'Social_Network_Ads.csv'
    t = Tracer(Path)
    gdad = Node(None, None, None, None)
    # mapping = {'Female': "0", 'Male': "1", 'True': 1, 'true': 1, 'False': 0, 'false': 0}

    Data, dchead = load(Path, entry_mapping)
    _, classes = preprocess1(Data)
    confusion_matrix = np.zeros((len(classes) + 1, len(classes) + 1))
    classes_dict = {}
    i = 0
    for c in classes:
        classes_dict[c] = i
        i += 1
    X_train, X_test = train_test_split(Data, test_size=0.2, random_state=42)
    condition_id, list_1, list_2, gini1, gini2, bestgain = splitdata(preprocess1(X_train)[0], X_train)
    buildtree(condition_id, dchead, list_1, list_2, gini1, gini2, gdad, prunegini=0.05)
    validation_result = []

    for i in X_test:
        ground_truth = i.pop()
        dt_test = [float(x) for x in i]
        result = predict(dt_test, dchead, gdad)
        if result != ground_truth:
            print("(miss) label:", i, ", ground_truth:", ground_truth, ", pred:", result)
        confusion_matrix[classes_dict[ground_truth]][classes_dict[result]] += 1
        validation_result.append({"label": i, "gt": ground_truth, "pred": result})

    ls = [x for x in classes]
    ls.append("total")
    confusion_matrix[len(classes_dict)] = np.sum(confusion_matrix, axis=0)
    for i in confusion_matrix:
        i[len(i) - 1] = np.sum(i)
    d = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=ls)
    d.plot()

    m = Metrics(confusion_matrix, classes_dict)
    metrics = {"precision": m.precision, "recall": m.recall, "f1": m.f1_score}
    metrics = dict(metrics, **{"result": validation_result})
    t.output(metrics)
    plt.show()
    # testvalue = [5, 3.6, 1.4, 0.2]
    # a = predict(testvalue, dchead, gdad)
    # print("(virtual)ground_truth:", None, ", pred:", a)
    # below for debug

ascd = 1
