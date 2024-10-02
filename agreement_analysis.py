from lxml import etree
import nltk
from nltk.metrics import agreement
from nltk.metrics.distance import masi_distance

class agreement_analysis:

    def change4array(self,numbers):
        num = []
        string = ""

        if numbers == "":
            return []

        #print(numbers)

        for let in numbers:
            if let == ",":
                num.append(int(string))
                #print(string)
                string = ""
            else:
                string = string + let
        num.append(int(string))

        num.sort()

        return num

    def __init__(self, path_A, path_B, path_C):
        self.path_A = path_A
        self.path_B = path_B
        self.path_C = path_C

        self.max_source = 0

        paths = [path_A, path_B, path_C]

        for path in paths:
            tree = etree.parse(path)

            signals = tree.xpath("//signal")
            for signal in signals:
                if self.max_source < int(signal.attrib["source"]):
                    self.max_source = int(signal.attrib["source"])
    
        path = path_A

        tree = etree.parse(path)

        signals = tree.xpath("//signal")

        self.tokens_A = {}

        for signal in signals:
            if self.max_source < int(signal.attrib["source"]):
                self.max_source = int(signal.attrib["source"])

        for i in range(1, self.max_source + 1):
            self.tokens_A[i] = []

        for signal in signals:
            self.tokens_A[int(signal.attrib["source"])] += self.change4array(signal.attrib["tokens"])
        
        path = path_B

        tree = etree.parse(path)

        signals = tree.xpath("//signal")

        self.tokens_B = {}

        for signal in signals:
            if max_source < int(signal.attrib["source"]):
                max_source = int(signal.attrib["source"])

        for i in range(1, max_source + 1):
            self.tokens_B[i] = []

        for signal in signals:
            self.tokens_B[int(signal.attrib["source"])] += self.change4array(signal.attrib["tokens"])
        
        path = path_C

        tree = etree.parse(path)

        signals = tree.xpath("//signal")

        self.tokens_C = {}

        for signal in signals:
            if self.max_source < int(signal.attrib["source"]):
                self.max_source = int(signal.attrib["source"])

        for i in range(1, self.max_source + 1):
            self.tokens_C[i] = []

        for signal in signals:
            self.tokens_C[int(signal.attrib["source"])] += self.change4array(signal.attrib["tokens"])
    
    def silver_change(self, k, tokens_A, tokens_B):
        v = tokens_A[k]
        p = tokens_B[k]
        #print(v)
        #print(p)
        #print()
        for l in range(len(v)):
            ele = v[l]
            for i in range(1,6):
                if (ele - i) in p:
                    v.append(ele - i)
                if (ele + i) in p:
                    v.append(ele + i)

        for l in range(len(p)):
            ele = p[l]
            for i in range(1,6):
                if (ele - i) in v:
                    p.append(ele - i)
                if (ele + i) in v:
                    p.append(ele + i)

        v = list(set(v))
        p = list(set(p))

        v.sort()
        p.sort()

        return v, p
    
    def silver_change_for3(self,k, tokens_A, tokens_B, tokens_C):
        v = tokens_A[k]
        p = tokens_B[k]
        q = tokens_C[k]

        for l in range(len(v)):
            ele = v[l]
            for i in range(1,6):
                if (ele - i) in p:
                    v.append(ele - i)
                if (ele + i) in p:
                    v.append(ele + i)
                if (ele - i) in q:
                    v.append(ele - i)
                if (ele + i) in q:
                    v.append(ele + i)

        for l in range(len(p)):
            ele = p[l]
            for i in range(1,6):
                if (ele - i) in v:
                    p.append(ele - i)
                if (ele + i) in v:
                    p.append(ele + i)
                if (ele - i) in q:
                    p.append(ele - i)
                if (ele + i) in q:
                    p.append(ele + i)

        for l in range(len(q)):
            ele = q[l]
            for i in range(1,6):
                if (ele - i) in v:
                    q.append(ele - i)
                if (ele + i) in v:
                    q.append(ele + i)
                if (ele - i) in p:
                    q.append(ele - i)
                if (ele + i) in p:
                    q.append(ele + i)

        v = list(set(v))
        p = list(set(p))
        q = list(set(q))

        v.sort()
        p.sort()
        q.sort()

        return v, p, q
    
    #Calcula a concordância gold, e retorna um vetor com todos os valores calculados
    def golden_metrics(self):
        golen_metrics = []

        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_A.items():
            if len(v) == 0:
                data.append(('anotador-a', k, frozenset([-1])))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset([-1])))
            else:
                data.append(('anotador-a', k, frozenset(v)))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset(v)))

            for k, v in self.tokens_B.items():
                if len(v) == 0:
                    data.append(('anotador-b', k, frozenset([-1])))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset([-1])))
                else:
                    data.append(('anotador-b', k, frozenset(v)))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset(v)))
        
        task.load_array(data)
        golen_metrics.append(task.alpha())

        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_A.items():
            if len(v) == 0:
                data.append(('anotador-a', k, frozenset([-1])))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset([-1])))
            else:
                data.append(('anotador-a', k, frozenset(v)))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset(v)))

            for k, v in self.tokens_C.items():
                if len(v) == 0:
                    data.append(('anotador-c', k, frozenset([-1])))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset([-1])))
                else:
                    data.append(('anotador-c', k, frozenset(v)))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset(v)))
            
        task.load_array(data)
        golen_metrics.append(task.alpha())

        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_B.items():
            if len(v) == 0:
                data.append(('anotador-b', k, frozenset([-1])))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset([-1])))
            else:
                data.append(('anotador-b', k, frozenset(v)))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset(v)))

            for k, v in self.tokens_C.items():
                if len(v) == 0:
                    data.append(('anotador-c', k, frozenset([-1])))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset([-1])))
                else:
                    data.append(('anotador-c', k, frozenset(v)))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset(v)))
                
        task.load_array(data)
        golen_metrics.append(task.alpha())

        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_A.items():
            if len(v) == 0:
                data.append(('anotador-a', k, frozenset([-1])))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset([-1])))
            else:
                data.append(('anotador-a', k, frozenset(v)))
                #print('anotador-a' + ' ' + str(k) + ' ' + str(frozenset(v)))

            for k, v in self.tokens_B.items():
                if len(v) == 0:
                    data.append(('anotador-b', k, frozenset([-1])))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset([-1])))
                else:
                    data.append(('anotador-b', k, frozenset(v)))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset(v)))
            for k, v in self.tokens_C.items():
                if len(v) == 0:
                    data.append(('anotador-c', k, frozenset([-1])))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset([-1])))
                else:
                    data.append(('anotador-c', k, frozenset(v)))
                    #print('anotador-b' + ' ' + str(k) + ' ' + str(frozenset(v)))
                
        task.load_array(data)
        golen_metrics.append(task.alpha())

        return golen_metrics
    
    #Calcula a concordância silver, e retorna um vetor com todos os valores calculados
    def silver_metrics(self):

        silver_metrics = []
        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_A.items():
            v,p = self.silver_change(k, self.tokens_A, self.tokens_B)

            if len(v) == 0:
                data.append(('anotador-a', k, frozenset([-1])))
            else:
                data.append(('anotador-a', k, frozenset(v)))

            if len(p) == 0:
                data.append(('anotador-b', k, frozenset([-1])))
            else:
                data.append(('anotador-b', k, frozenset(p)))

        task.load_array(data)
        silver_metrics.append(task.alpha())

        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_B.items():
            v,p = self.silver_change(k, self.tokens_B, self.tokens_C)

            if len(v) == 0:
                data.append(('anotador-b', k, frozenset([-1])))
            else:
                data.append(('anotador-b', k, frozenset(v)))

            if len(p) == 0:
                data.append(('anotador-c', k, frozenset([-1])))
            else:
                data.append(('anotador-c', k, frozenset(p)))

        task.load_array(data)
        silver_metrics.append(task.alpha())

        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k, v in self.tokens_A.items():
            v,p = self.silver_change(k, self.tokens_A, self.tokens_C)

            if len(v) == 0:
                data.append(('anotador-a', k, frozenset([-1])))
            else:
                data.append(('anotador-a', k, frozenset(v)))

            if len(p) == 0:
                data.append(('anotador-c', k, frozenset([-1])))
            else:
                data.append(('anotador-c', k, frozenset(p)))

        task.load_array(data)
        silver_metrics.append(task.alpha())
    
        task = nltk.AnnotationTask(distance=masi_distance)

        data = []

        for k,v in self.tokens_A.items():
            v,p,q = self.silver_change_for3(k, self.tokens_A, self.tokens_B, self.tokens_C)

        if len(v) == 0:
            data.append(('anotador-a', k, frozenset([-1])))
        else:
            data.append(('anotador-a', k, frozenset(v)))

        if len(p) == 0:
            data.append(('anotador-b', k, frozenset([-1])))
        else:
            data.append(('anotador-b', k, frozenset(p)))

        if len(q) == 0:
            data.append(('anotador-c', k, frozenset([-1])))
        else:
            data.append(('anotador-c', k, frozenset(q)))

        task.load_array(data)
        silver_metrics.append(task.alpha())