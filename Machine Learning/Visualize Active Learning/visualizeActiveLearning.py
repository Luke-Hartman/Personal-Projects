import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from random import random
from LukesAlgorithm import LukesGetBatch, ImprovedLukesGetBatch
from leavingAlgorithm import leavingGetBatch
from randomForestAlgorithm import randomForestGetBatch
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
# from simpleNN import createNN

if __name__ == '__main__':

    hiddenLayer = (100, 30, 30, 10)

    #clf = MLPClassifier(hidden_layer_sizes = hiddenLayer, max_iter=10000, solver='lbfgs', learning_rate_init=0.0001, warm_start=False, tol=0.000000001, verbose=True, learning_rate='adaptive')
    # Best so far of NN clf = MLPClassifier(hidden_layer_sizes = hiddenLayer, max_iter=10000, solver='lbfgs', warm_start=True, tol=0.000000001, verbose=True, learning_rate='adaptive')
    #clf = DecisionTreeClassifier(max_depth=10)
    #clf = RandomForestClassifier(n_estimators=3)
    #clf = MLPClassifier(hidden_layer_sizes = hiddenLayer, max_iter=10000, solver='lbfgs', warm_start=False, tol=0.000000001, verbose=True, learning_rate='adaptive', alpha=0.00001)
    clf = KNeighborsClassifier(n_neighbors=5)
    #clf = LinearSVC(dual=False, verbose=True)

	# Speed is roughly the number of samples to get per batch. (Depends on Active Learning Algorithm)
    speed = 50

    img = mpimg.imread('images/ZigZag.png')

    H = len(img)
    W = len(img[0])
    if len(img[0][0]) == 4:
        newImg = np.zeros((H,W,3))
        for py in range(H):
            for px in range(W):
                for c in range(3):
                    newImg[py][px][c] = img[py][px][c]
        img = newImg

    classes = []
    for row in img:
        for cell in row:
            t = tuple(cell)
            if t not in classes:
                classes.append(t)

    def getPos(x):
        return (int(x[0]*W), int(x[1]*H))

    def getLabel(x):
        px, py = getPos(x)
        return classes.index(tuple(img[py][px]))
    #    ''' Batch size of 1 is causing predictions to stall
    if speed <= 1000:
        batch_size = 1
    else:
        batch_size = 32
    '''#'''
    #clf = createNN((2,), len(classes), n_layers=1, layer_size=1, patience=100, dropout=0, min_delta=0.0001, batch_size=batch_size)
    #clf = RandomForestClassifier()

    X = [(random(), random()) for i in range(speed)]
    Y = [getLabel(x) for x in X]

    oldBatch = np.zeros((W, H, 3))
    oldPred = np.zeros((W, H, 3))
    oldSamples = np.zeros((W, H, 3))
    newX = []
    newY = []

    while True:
        clf.fit(X, Y)

        Xactual = img

        imgX = []
        for py in range(H):
            for px in range(W):
                imgX.append((px/W, py/H))
        predictions = clf.predict(imgX)
        if type(predictions[0]) == np.ndarray:
            predictions = [p[0] for p in predictions]
        a = np.array([classes[p] for p in predictions])
        imgPred = np.reshape(a, (W, H, 3))

        #'''
        probas = clf.predict_proba(imgX)
        a = np.array([(max(p), max(p), max(p)) for p in probas])
        imgConf = np.reshape(a, (W, H, 3))
        '''
        imgConf = imgPred
		'''#'''
		
        imgSamples = np.zeros((W, H, 3))
        for x, y in zip(X, Y):
            px, py = getPos(x)
            imgSamples[py][px] = classes[y]


        fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
        axs[0][0].set_title('New Predictions f(x,y)')
        axs[0][0].imshow(oldBatch)
        axs[0][1].set_title('Old Predicted f(x,y)')
        axs[0][1].imshow(oldPred)
        axs[0][2].set_title('Confidence f(x,y)')
        axs[0][2].imshow(imgConf)
        axs[1][0].set_title('Actual f(x,y)')
        axs[1][0].imshow(img)
        axs[1][1].set_title('Predicted f(x,y)')
        axs[1][1].imshow(imgPred)
        axs[1][2].set_title('Known f(x,y)')
        axs[1][2].imshow(imgSamples)
        plt.show()

        oldPred = imgPred
        oldSamples = imgSamples
        #newX = LukesGetBatch(X, Y, batchSize=speed)
        #newX = ImprovedLukesGetBatch(X, Y, batchSize=speed)
		#newX = leavingGetBatch(X, Y, batchSize=speed)
        newX = randomForestGetBatch(X, Y, batchSize=speed)
        #newX = [(random(), random()) for i in range(speed)]
        newY = [getLabel(x) for x in newX]

        oldBatch = np.zeros((W, H, 3))
        for x, y in zip(newX, newY):
            px, py = getPos(x)
            oldBatch[py][px] = classes[y]

        X += newX
        Y += newY
