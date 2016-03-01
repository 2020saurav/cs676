from vocabTree import *

# dbFile     = open(dbFilePath, 'rb')
# VTree      = pickle.load(dbFile)
# VTree = tree # for loading in the interpreter.
testImgDir = 'test/'

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
    return votes[:383]

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

def distance(v1, v2):
    sum = 0
    for i in range(0, len(v1)):
        sum += ((v1[i] - v2[i]) * (v1[i] - v2[i])) # L2 : good
        # sum += abs(v1[i] - v2[i]) # L1 : bad
    return sum

testImgPaths = [f for f in os.listdir(testImgDir)]
testImgPaths.sort()

if __name__ == '__main__':
    score = [0.0, 0.0, 0.0, 0.0, 0.0]
    for testImg in testImgPaths:
        print testImg
        matches = bestMatches(testImgDir + testImg)
        matchNames = [int(imagePathList[m[1]][7:-4]) for m in matches]
        imgNameInt = int(testImg[7:-4])
        if imgNameInt+1 in matchNames[:76]:
            score[0] += 0.33
        if imgNameInt+2 in matchNames[:76]:
            score[0] += 0.34
        if imgNameInt+3 in matchNames[:76]:
            score[0] += 0.33
        if imgNameInt+1 in matchNames[:153]:
            score[1] += 0.33
        if imgNameInt+2 in matchNames[:153]:
            score[1] += 0.34
        if imgNameInt+3 in matchNames[:153]:
            score[1] += 0.33
        if imgNameInt+1 in matchNames[:230]:
            score[2] += 0.33
        if imgNameInt+2 in matchNames[:230]:
            score[2] += 0.34
        if imgNameInt+3 in matchNames[:230]:
            score[2] += 0.33
        if imgNameInt+1 in matchNames[:306]:
            score[3] += 0.33
        if imgNameInt+2 in matchNames[:306]:
            score[3] += 0.34
        if imgNameInt+3 in matchNames[:306]:
            score[3] += 0.33
        if imgNameInt+1 in matchNames[:383]:
            score[4] += 0.33
        if imgNameInt+2 in matchNames[:383]:
            score[4] += 0.34
        if imgNameInt+3 in matchNames[:383]:
            score[4] += 0.33
    print "Accuracy:"
    print float(score[0])*100/len(testImgPaths)
    print float(score[1])*100/len(testImgPaths)
    print float(score[2])*100/len(testImgPaths)
    print float(score[3])*100/len(testImgPaths)
    print float(score[4])*100/len(testImgPaths)
