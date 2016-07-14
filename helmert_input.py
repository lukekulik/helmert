import numpy as np


def helmert_input(data1, data2, corr1, corr2):
    # (by Lukasz)
    # INPUT: two strings/files with coordinates; the second one is the reference; two line counts for the coordinate files
    # OUTPUT: array of 7 parameters - 3 translations, 3 rotations and scale

    names1, pos1, unc1 = data1['1'], data1['4'], data1['6']
    names2, pos2, unc2 = data2['1'], data2['4'], data2['6']


    # weird thing that lennert requested:
    #########
    n0 = len(pos1) / 3.0
    pt1 = np.hsplit(pos1[0:3 * n0], n0)
    nameslennert = names1[0:len(names1):3]
    coordinatesarray = np.column_stack((nameslennert, pt1))
    #########

    # removing non-repeated entries for further comparison:

    intersection = np.intersect1d(names1, names2)
    pointer1 = np.argwhere(np.in1d(names1, intersection) == False)
    pointer2 = np.argwhere(np.in1d(names2, intersection) == False)

    pos1, unc1, names1, corr1 = np.delete(pos1, pointer1), np.delete(unc1, pointer1), np.delete(names1,
                                                                                                pointer1), np.delete(
        corr1, pointer1)
    pos2, unc2, names2, corr2 = np.delete(pos2, pointer2), np.delete(unc2, pointer2), np.delete(names2,
                                                                                                pointer2), np.delete(
        corr2, pointer2)

    n = len(pos1) / 3.0

    # helmert (Closed-form weighted least squares solutions of Helmert transformation parameters):
    # corellations calculations:
    c1 = corr1[0:3 * n:3] * unc1[0:3 * n:3] * unc1[1:3 * n:3]
    c2 = corr1[1:3 * n:3] * unc1[0:3 * n:3] * unc1[2:3 * n:3]
    c3 = corr1[2:3 * n:3] * unc1[1:3 * n:3] * unc1[2:3 * n:3]

    Q = np.diag(np.sum(np.power(np.hsplit(unc1[0:3 * n], n), 2), axis=1) +
                2 * (c1 + c2 + c3))  # covariance matrix

    return pos1, pos2, Q, n, coordinatesarray


def helmert_input_ITRF(data1, data2, corr1, corr2):
    # (by Lukasz)
    # INPUT: two strings/files with coordinates; the second one is the reference; two line counts for the coordinate files
    # OUTPUT: array of 7 parameters - 3 translations, 3 rotations and scale

    names1, pos1, unc1 = data1[:, 0], data1[:, 1], data1[:, 2]
    names2, pos2, unc2 = data2['1'], data2['4'], data2['6']

    pos1 = np.array(pos1, dtype='f8')  # dtype fix (ugly)
    unc1 = np.array(unc1, dtype='f8')

    # removing non-repeated entries for further comparison:
    intersection = np.intersect1d(names1, names2)
    pointer1 = np.argwhere(np.in1d(names1, intersection) == False)
    pointer2 = np.argwhere(np.in1d(names2, intersection) == False)

    pos1, unc1, names1, corr1 = np.delete(pos1, pointer1), np.delete(unc1, pointer1), np.delete(names1,
                                                                                                pointer1), np.delete(
        corr1, pointer1)
    pos2, unc2, names2, corr2 = np.delete(pos2, pointer2), np.delete(unc2, pointer2), np.delete(names2,
                                                                                                pointer2), np.delete(
        corr2, pointer2)
    n = len(pos1) / 3.0

    # helmert (Closed-form and iterative weighted least squares solutions of Helmert transformation parameters):
    # corellations calculations:

    # x = numpy.delete(x, (0), axis=0)
    # To delete the third column, do this:
    # x = numpy.delete(x,(2), axis=1)

    # D=np.diag(unc2)
    # Q=D*R*D # covariance matrix
    Q = np.diag(np.sum(np.power(np.hsplit(unc1[0:3 * n], n), 2), axis=1))

    return pos1, pos2, Q, n
