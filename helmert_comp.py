import numpy as np
from scipy import linalg


def helmert(pos1, pos2, Q, n):
    pt1 = np.hsplit(pos1[0:3 * n], n)
    pt2 = np.hsplit(pos2[0:3 * n], n)
    e = np.matrix(np.ones(n)).T
    sig = np.identity(3)

    # outlier loop start 
    i = 0  # iterator preventing infinite loops
    tst2 = np.array([7])  # loop starter, arbitrary

    # Q=np.eye(n) 
    treshold = 0.01  # outlier treshold, arbitrary

    while tst2[(np.abs(tst2)) > treshold].size != 0 and i < 20:

        X = np.transpose(np.matrix(pt1))
        Y = np.transpose(np.matrix(pt2))

        Xdash = (X * e * e.T) / n
        Ydash = (Y * e * e.T) / n

        Xs = X - Xdash
        Ys = Y - Ydash

        P = np.linalg.inv(Q)  # transforming covariance matrix into weight matrix

        sx2 = np.trace(Xs * P * Xs.T) / n
        sy2 = np.trace(Ys * P * Ys.T) / n

        C = Xs * P * Ys.T  # (This is Qx^-1 from experimental)
        U, s, VT = linalg.svd(C.T,full_matrices=False)  # singular value decomposition, partial matrices added recently for a speedup 
        U = np.matrix(U)
        VT = np.matrix(VT)

        #D = np.diag(s)  # diagonalisation of singular values

        sig[-1][-1] = np.linalg.det(U) * np.linalg.det(VT.T)  # overwriting last parameter
        R = U * sig * VT  # calculating rotation matrix

        sxy = np.trace(R * C) / n

        k = sxy / sx2

        T = Ydash - k * R * Xdash
        t = T * e / n

        # outlier detection method:

        
        s02 = sy2 - (sxy * sxy) / sx2  # mean square residual of least squares fitting
        eps = np.matrix(Y - t - k * R * X)  # residual vector matrix of all points

        if s02 != 0:
            tst = (P * eps.T * eps) / (3.0 * s02)  # test parameter for outliers
        else:
            tst = np.zeros(n)

        tst2 = np.diag(np.diag(tst))

        # normalize with sth to get sigma and better feeling

        Q[np.where(
            (np.abs(tst2) == np.max(np.abs(tst2))) & (np.abs(tst2) > treshold))] = 1000  # explode the sd of top outlier

        i += 1


    #print i,len(Q[Q>999])
    #print '\n'
    
    #print R,k

    return np.array([R, t, k - 1])
