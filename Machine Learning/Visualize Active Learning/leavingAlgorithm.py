from random import randint, random
from sklearn.tree import DecisionTreeClassifier

def leavingGetBatch(X, Y, batchSize=10):
    # Build decision tree
    clf = DecisionTreeClassifier()
    clf.fit(X, Y)
    tree = clf.tree_
    size = len(X[0])
    # Get graph of connected leaf nodes (This is different than the tree structure)
    class Leaf:
        def __init__(self, boundary):
            self.boundary = boundary

    leaves = []
    def createLeaves(n, boundary):
        feat = tree.feature[n]
        if feat < 0: # Then it is a leaf
            leaves.append(Leaf(boundary))
            return
        threshold = tree.threshold[n]
        bot, top = boundary[feat]
        # Go down left child
        leftBoundary = boundary[:]
        leftBoundary[feat] = (bot, threshold)
        createLeaves(tree.children_left[n], leftBoundary)
        # Right child
        rightBoundary = boundary[:]
        rightBoundary[feat] = (threshold, top)
        createLeaves(tree.children_right[n], rightBoundary)

    rootBoundary = [(0, 1) for i in range(size)]
    createLeaves(0, rootBoundary)

    # Find batch
    batch = []
    for i in range(batchSize):
        leaf = leaves[randint(0, len(leaves) - 1)]
        x = []
        for bot, top in leaf.boundary:
            x.append((top - bot)*random() + bot)
        batch.append(x)
    return batch
