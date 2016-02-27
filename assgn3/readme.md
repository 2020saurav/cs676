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
 * k dot products are performed at each level, resulting in a total of kL dot products, which is bery efficient if k is not too large. The path down the tree can be encoded by a single integer and is then available for use in scoring.
 * The relevance of a database image to the query image is based on how similar the paths down the vocabulary tree are, for the descriptors from the database image and the query image. The scheme assigns weights to the tree nodes and defines relevance scores associated to images.


### Scoring

At each node i a weight w<sub>i</sub> is assigned that can be defined accoding to one of the different schemes:
 * constant weighing scheme w<sub>i</sub> = k
 * entropy weighing scheme w<sub>i</sub> = log (N/N<sub>i</sub>)
    where N is the number of database images and N<sub>i</sub> is the number of images with atleast one descriptor vector path through node i

Query q<sub>i</sub> and database vector d<sub>i</sub> are defined according to assigned weights as
 - q<sub>i</sub> = m<sub>i</sub> w<sub>i</sub>
 - d<sub>i</sub> = n<sub>i</sub> w<sub>i</sub>

 where m<sub>i</sub> is the number of the descriptor vectors of the query with a path along the node i, and w<sub>i</sub> its weight
 n<sub>i</sub> is the number of the descriptor vectors of each database image with a path along the node i

Each database image is given a relevance score based on the L1 normalized difference between the query and the databse vectors
    s(q, d) = || (q / ||q||) - (d / ||d||) ||

Scores for the images in the database are accumulated, and winner is the image with the most common information with imput image.

##### Inverted File Index
To implement scoring efficiently, an inverted file  index is associated to each node of the vocabulary tree (the inverted file of inner node is the concatenation of it's children's inverted files).

Inverted files at each node store the id-­numbers of the images in which a particular node occurs and the term frequency of that image. Indexes back to the new image are then added to the relevant inverted files.
