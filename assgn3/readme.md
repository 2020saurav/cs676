# Scalable Vocabulary Recognition Tree
(Nister and Strewenius, CVPR 2006)

This method of instance recognition involves these 3 steps:

 1. Organize the local descriptors of images in a tree using hierachical k-means clustering.
    Inverted files are stored at EACH node with scores (offline)

 2. Generate a score for a given query image based on Term Frequency - Inverse Document Frequency.

 3. Find the images in the database that best match that score.

### Building the tree
 * For each image in the database, extract MSER regions and calculate a set of feature point descriptors (eg 128 SIFT)
 * Run k-means recursively on each of the resulting quantization cells upto a max number of levels L
 * Nodes are the centroids, and leaves are the visual words
 * k defines the branching-factor of the tree, which indicates how fast the tree branches


We shall vary k and L to evaluate the model.

With each node in the tree, there is an associated inverted file with references to the image containing an instance of that node.

### Querying
 * The descriptor vector is propagated down the tree at each level by comparing the descriptor vector to the k candidate cluster centers, represented by k children in the tree, and choosing the closest one.
 * Once the leaf is obtained, ... <TODO>


##### Inverted File Index
To implement scoring efficiently, an inverted file  index is associated to each node of the vocabulary tree (the inverted file of inner node is the concatenation of it's children's inverted files).

Inverted files at each node store the id-­numbers of the images in which a particular node occurs and the term frequency of that image. Indexes back to the new image are then added to the relevant inverted files.

## Running and Evaluation
`vocabTree.py` consists of functions to construct the vocabulary tree from images in `train/` directory.
`query.py` consists of functions to query the database to get a set of possible matches.

The output of `vocabTree.py`, i.e. the vocabulary tree may be saved for persistence. For the purpose of evaluation, we used Python interpreter shell, i.e by keeping the tree in memory.
```python
from vocabTree import *
descriptors = getAllSiftDescriptors()
tree = generateVocabTree(descriptors)
computeNDArray(tree)
computeIFIndex(tree)
computeTopImages(tree)
```
This will make the variable `tree` available in the interpreter. Now, relevant functions from `query.py` can be loaded in the interpreter and evaluation can be performed with code in `__main__` of `query.py`.

## Results
Available in `report.pdf`
