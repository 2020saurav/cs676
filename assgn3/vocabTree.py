import cv2
import os
import math

from sklearn.cluster import KMeans


K    = 3 # 10
L    = 2 # 6
N    = 0
ND   = []
# dirPath = sys.argv[1]

SIFT = cv2.xfeatures2d.SIFT_create()

class VocabTree:
    def __init__(self):
        self.center   = None
        self.children = []
        # only for leaf nodes:
        self.descriptors = []
        self.images = []
        self.scores = []
        self.imageIndices = []

def getAllSiftDescriptors(imagePathList, dirPath):
    descriptors   = []
    imgIndex = 0
    for imagePath in imagePathList:
        img = cv2.imread(os.path.join(dirPath, imagePath), cv2.COLOR_BGR2GRAY)
        (kps, des) = SIFT.detectAndCompute(img, None)
        for d in des:
            descriptors.append((imgIndex, d))
        imgIndex += 1
    return descriptors

def generateVocabTree(descriptors, level=L):
    vtree = VocabTree()
    if level == 0:
        vtree.descriptors = descriptors
        return vtree

    km = KMeans(n_clusters=K)
    ds = [d[1] for d in descriptors]
    clusters = km.fit(ds)
    clusterCenters = clusters.cluster_centers_
    C = []
    for i in range (0, K):
        C.append([])

    for d in descriptors:
        C[clusters.predict(d[1])[0]].append(d)

    for i in range (0, K):
        vtree.children.append(generateVocabTree(C[i], level-1))

    for i in range (0, K):
        vtree.children[i].center = clusterCenters[i]

    return vtree


def computeIFIndex(tree):
    global ND
    if len(tree.children) != 0:
        for child in tree.children:
            computeIFIndex(child)
    else:
        Ni = len(tree.images)
        for img in tree.images:
            ndi = tree.imageIndices.count(img)
            nd  = ND[img]
            tree.scores.append(float(ndi)/nd*math.log(N/Ni))

def computeNDArray(tree):
    global ND
    if len(tree.children) != 0:
        for child in tree.children:
            computeNDArray(child)
    else:
        tree.imageIndices  = [d[0] for d in tree.descriptors]
        tree.images      = list(set(tree.imageIndices))
        for img in tree.images:
            print img
            ND[img] += 1
    return ND


if __name__ == '__main__':
    global N, ND
    dirPath = 'ukbench/small'
    imagePathList = [f for f in os.listdir(dirPath)]
    N = len(imagePathList)
    ND = [0] * N
    descriptors = getAllSiftDescriptors(imagePathList, dirPath)
    tree = generateVocabTree(descriptors)
    computeNDArray(tree)
    computeIFIndex(tree)
