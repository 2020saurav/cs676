from vocabTree import *

dbFile     = open(dbFilePath, 'rb')
VTree      = pickle.load(dbFile)
testImgDir = 'train_small/'

def bestMatches(imagePath):
    img = cv2.imread(imagePath, cv2.COLOR_BGR2GRAY)
    (kps, des) = SIFT.detectAndCompute(img, None)
    allVotedImages = {}
    for d in des:
        leaf = getLeaf(VTree, d)
        for image in leaf.topImages:
            imgId = image[1]
            score = image[0]
            if imgId in allVotedImages:
                allVotedImages[imgId] += score
            else:
                allVotedImages[imgId] = score
    votes = [(v, k) for k, v in allVotedImages.iteritems()]
    votes.sort(reverse=True)
    return votes[:5]

def getLeaf(tree, descriptor):
    if len(tree.children) != 0:
        index = 0
        minDist = sys.maxint
        for i in range(0, K):
            d = distance(tree.children[i].center, descriptor)
            if d < minDist:
                minDist = d
                index = i
        return getLeaf(tree.children[index], descriptor)
    else:
        return tree

def distance(v1, v2): #L1 norm
    sum = 0
    for i in range(0, len(v1)):
        sum += abs(v1[i] - v2[i])
    return sum

if __name__ == '__main__':
    testImgPaths = [f for f in os.listdir(testImgDir)]
    testImgPaths.sort()
    for testImg in testImgPaths:
        matches = bestMatches(testImgDir + testImg)
        print testImg,
        for m in matches:
            print imagePathList[m[1]][7:] + "(" + str(m[0]) + ")  ",
        print

