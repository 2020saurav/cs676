import cv2
import os
import math
# import pickle
import sys
import time

from sklearn.cluster import KMeans


K    = 6
L    = 5
# N    = 0
# ND   = []
# dirPath = sys.argv[1]
dirPath = 'train'
# dbFilePath  = 'db/vtree_3_1.pkl'
imagePathList = [f for f in os.listdir(dirPath)]
imagePathList.sort()
N = len(imagePathList)
ND = [0] * N

SIFT = cv2.xfeatures2d.SIFT_create(200)

class VocabTree:
    def __init__(self):
        self.center   = None
        self.children = []
        # only for leaf nodes:
        self.descriptors = []
        self.images = []
        self.scores = []
        self.imageIndices = []
        self.topImages = []

def getAllSiftDescriptors():
    t = time.time()
    descriptors   = []
    imgIndex = 0
    for imagePath in imagePathList:
        try:
            img = cv2.imread(os.path.join(dirPath, imagePath), cv2.COLOR_BGR2GRAY)
            (kps, des) = SIFT.detectAndCompute(img, None)
            for d in des:
                descriptors.append((imgIndex, d))
        except Exception, e:
            print e
            print imagePath
        imgIndex += 1
    print "All SIFT complete in " + str(time.time() -t) + " s"
    return descriptors

def generateVocabTree(descriptors, level=L):
    t = time.time()
    vtree = VocabTree()
    if level == 0:
        vtree.descriptors = descriptors
        return vtree
    try:
        km = KMeans(n_clusters=K)
        ds = [d[1] for d in descriptors]
        clusters = km.fit(ds)
        clusterCenters = clusters.cluster_centers_
        C = []
        for i in range(0, K):
            C.append([])
        for d in descriptors:
            C[clusters.predict(d[1])[0]].append(d)
        for i in range (0, K):
            vtree.children.append(generateVocabTree(C[i], level-1))
        for i in range (0, K):
            vtree.children[i].center = clusterCenters[i]
    except Exception, e:
        vtree.descriptors = descriptors
        print "K Means exception"
        print e
    if level == L:
        print "VTree complete in " + str(time.time() -t) + " s"
    return vtree


def computeIFIndex(tree):
    t = time.time()
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
    if tree.center == None:
        print "IF Index complete in " + str(time.time() -t) + " s"

def computeNDArray(tree):
    t = time.time()
    global ND
    if len(tree.children) != 0:
        for child in tree.children:
            computeNDArray(child)
    else:
        tree.imageIndices  = [d[0] for d in tree.descriptors]
        tree.images      = list(set(tree.imageIndices))
        for img in tree.images:
            ND[img] += 1
    if tree.center == None:
        print "ND Array complete in " + str(time.time() -t) + " s"

def computeTopImages(tree):
    t = time.time()
    global ND
    if len(tree.children) != 0:
        for child in tree.children:
            computeTopImages(child)
    else:
        temp = [(tree.scores[i], tree.images[i]) for i in range (0, len(tree.images))]
        temp.sort(reverse=True)
        tree.topImages = temp[:383]
    if tree.center == None:
        print "Top Images complete in " + str(time.time() -t) + " s"

# def saveTree(tree):
#     with open(dbFilePath, 'wb') as dbFile:
#         pickle.dump(tree, dbFile)

if __name__ == '__main__':
    t = time.time()
    descriptors = getAllSiftDescriptors()
    print "Descriptor computed"
    tree = generateVocabTree(descriptors)
    print "VocabTree generated"
    computeNDArray(tree)
    print "ND Array computed"
    computeIFIndex(tree)
    print "IDF computed"
    computeTopImages(tree)
    print "Top Images computed"

    # saveTree(tree)
    # print "Database " + dbFilePath + " generated in " + str(time.time() - t) + " s."
