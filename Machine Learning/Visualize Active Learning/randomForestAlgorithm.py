from random import randint, random, sample
from sklearn.ensemble import RandomForestClassifier

def randomForestGetBatch(X, Y, batchSize=10, decay = 0.2, n_jobs=1):
    # To prevent this from taking too long, want Gmod to be the bottleneck, not this
    checkSize = 100000
    if(len(X) > checkSize):
        selection = sample(range(len(X)), checkSize)
        X = [X[i] for i in selection]
        Y = [Y[i] for i in selection]
    # Build decision tree
    clf = RandomForestClassifier(n_estimators=100, n_jobs=n_jobs)
    print("Building")
    clf.fit(X, Y)
    size = len(X[0])
    # Find batch
    batch = []
    threshold = 1/clf.n_classes_
    '''
    threshold = 0.6
    print("Finding")
    while True:
        print(len(batch))
        maybes = [[random() for i in range(size)] for i in range(10*batchSize)]
        probas = clf.predict_proba(maybes)
        for x, p in zip(maybes, probas):
            if max(p) < threshold:
                batch.append(x)
        if len(batch) >= batchSize:
            return batch[:batchSize]
    '''
    while True:
        maybes = [[random() for i in range(size)] for i in range(10*batchSize)]
        probas = clf.predict_proba(maybes)
        for x, p in zip(maybes, probas):
            if max(p) < threshold:
                batch.append(x)
        if len(batch) >= batchSize:
            return batch[:batchSize]
        threshold = (1 - threshold)*decay + threshold
    '''#'''
