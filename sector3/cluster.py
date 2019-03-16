import os, math
import numpy as np

class Node:
    def __init__(self, feature_, left_child_=None, right_child_=None, distance_=0.0, id_=-1):
        self.feature = np.array(feature_)
        self.id = id_
        self.left_child = left_child_
        self.right_child = right_child_
        self.distance = distance_

def load_data(path):
    row_names = []
    col_names = []
    data = []
    with open(log_path, 'r') as fp:
        i = 0
        for line in fp.readlines():
            line = line.strip()
            elems = str(line).split('\t')
            if i==0:
                col_names = elems[1:]
            else:
                row_names.append(elems[0])
                data.append([float(x) for x in elems[1:]])
            i+=1
    return col_names, row_names, data

def Pearson_distance(cls1, cls2):
    # calculate sum of the pref
    critic1_sum = sum(cls1)
    critic2_sum = sum(cls2)
    # calculate square sum of the pref
    critic1_sum2 = sum([item**2 for item in cls1])
    critic2_sum2 = sum([item**2 for item in cls2])
    # calculate cross product
    critic12_sum = sum([cls1[i]*cls2[i] for i in range(len(cls1))])
    
    # pearson correlation score
    n = len(cls1)
    num = critic12_sum - (critic1_sum*critic2_sum)/n
    den = math.sqrt((critic1_sum2-(critic1_sum**2)/n)*(critic2_sum2-(critic2_sum**2)/n))
    if den == 0:
        return 0
    
    # print(num/den)
    return 1.0-num/den

# 对每两行的数据进行计算相似度
def get_pairdistance(datas, distance=Pearson_distance):
    # this all be leaf in tree
    clusters = [Node(vc, id=i) for i, vc in enumerate(datas)]
    distances = {}    
    upper_cluster = []
    new_id = -1
    while(len(clusters)>1):
        N = len(clusters)
        min_pair = (0,1)
        min_dis = distance(clusters[0].feature, clusters[1].feature)
        # search all cluster
        for i in range(0, N):
            for j in range(0, N):
                if (clusters[i].id, clusters[j].id) not in distances:
                    distances[(clusters[i].id, clusters[j].id)] = distance(clusters[i].feature, clusters[j].feature)
                dis = distances[ref_cluster.id, clusters[j].id]
                if dis < min_dis:
                    min_dis = dis
                    min_pair = (ref_cluster.id, clusters[j].id)
        
        new_feature = (clusters[min_pair[0]].feature + clusters[min_pair[1]].feature)/2
        new_cluster = Node(new_feature, left_child_= clusters[min_pair[0]], right_child_= clusters[min_pair[1]], distance_= min_dis, id=new_id)

        del clusters[min_pair[0]]
        del clusters[min_pair[1]]
        clusters.append(new_cluster)
        new_id-=1

    return clusters[0]

if __name__=='__main__':
    file_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(file_path, 'blogdata.txt')
    
    col_names, row_names, data = load_data(log_path)
    distance_matrix = get_pairdistance(data, log_path)
    print(distance_matrix)

