#!/usr/bin/python3


import numpy
from PIL import Image
import matplotlib.pyplot as plt
from time import sleep

path = ""

def add_image(path):
    print("\nadding image: " + path)
    try:
        i = numpy.array(Image.open(path))
    except:
        print("photo doesn't exist!\ncheck path!")
        quit()

    print("image shape:" + str(i.shape))

    if str(i.shape).split(',').__len__() != 3:
        print("image isn't 3d")
        quit()

    print("image " + path.split('/')[-1] + " added")
    return i

def draw_plot(rgb_matrix, show):
    print("\nstart drawing plot")    

    r = rgb_matrix[0]
    g = rgb_matrix[1]
    b = rgb_matrix[2]

    plot = plt.figure().add_subplot(111, projection='3d')
    plot.scatter(r, g, b, c='red')
    if show:
        plt.show()
    
    name, format = path.split('/')[-1].split('.')
    
    p = ""
    for i in path.split('/'):
        if i != str(name) + '.' + str(format):
            p += str(i) + "/"
    p += str(name) + '-plt.' + str(format)

    try:
        plt.savefig(p)
        print("plot saved as " + p)
    except:
        print("ERROR: something wrong in saving plot photo as " + p)
        print("permision denied??\nusing windows??")

    print("finish drawing plot")    

def cal_average(matrix):
    print("\ncalculating average")
    try:
        matrix.__len__()
        matrix[0].__len__()
        matrix[0][0].__len__()
    except:
        print("bad input matrix in cal_average!\nfind matrix with 3 dimention")
        return

    sum = [0, 0, 0]
    for i in matrix:
        for j in i:
            sum[0] += j[0]
            sum[1] += j[1]
            sum[2] += j[2]

    t = matrix.__len__() * matrix[0].__len__()        
    sum[0] /= t
    sum[1] /= t
    sum[2] /= t

    s = (sum[0] + sum[1] + sum[2]) / 3

    print("average calculated")

    return s, sum

def print_average(total, rgb):
    print("\ntotal average: " + str(total))
    print("average Red:   " + str(rgb[0]))
    print("average Green: " + str(rgb[1]))
    print("average Blue:  " + str(rgb[2]))
    print()

def create_rgb_matrix(matrix):
    print("\nstart creating rgb matrix")
    ii = [[], [], []]
    for i in matrix:
        for j in i:
            ii[0].append(j[0]) # R
            ii[1].append(j[1]) # G
            ii[2].append(j[2]) # B

    print("finish creating rgb matrix")

    return ii

def print_matrix(mat, name):
    print("\n" + name + " matrix:\n")
    l = ""
    
    x = max(str(mat[0][0]).__len__(), str(mat[1][0]).__len__(), str(mat[2][0]).__len__())
    l += (int(x / 2) + 1) * ' ' + 'R' + int(x / 2) * ' '
    y = max(str(mat[0][1]).__len__(), str(mat[1][1]).__len__(), str(mat[2][1]).__len__())
    l += (int(y / 2) + 1) * ' ' + 'G' + int(y / 2) * ' '
    z = max(str(mat[0][2]).__len__(), str(mat[1][2]).__len__(), str(mat[2][2]).__len__())
    l += (int(z / 2) + 1) * ' ' + 'B' + int(z / 2) * ' '

    print(l)

    x += 1
    y += 1
    z += 1

    print("R ", end='')
    s = x - str(mat[0][0]).__len__()
    print(str(mat[0][0]) + ' ' * s, end='')
    s = y - str(mat[0][1]).__len__()
    print(str(mat[0][1]) + ' ' * s, end='')
    s = z - str(mat[0][2]).__len__()
    print(str(mat[0][2]) + ' ' * s)

    print("G ", end='')
    s = x - str(mat[1][0]).__len__()
    print(str(mat[1][0]) + ' ' * s, end='')
    s = y - str(mat[1][1]).__len__()
    print(str(mat[1][1]) + ' ' * s, end='')
    s = z - str(mat[1][2]).__len__()
    print(str(mat[1][2]) + ' ' * s)

    print("B ", end='')
    s = x - str(mat[2][0]).__len__()
    print(str(mat[2][0]) + ' ' * s, end='')
    s = y - str(mat[2][1]).__len__()
    print(str(mat[2][1]) + ' ' * s, end='')
    s = z - str(mat[2][2]).__len__()
    print(str(mat[2][2]) + ' ' * s)

    print('\n')

def print_var(matrix):
    try:
        x = matrix[0]
        print("variance R = " + str(x))
    except:
        return

    try:
        x = matrix[1]
        print("variance G = " + str(x))
    except:
        return

    try:
        x = matrix[2]
        print("variance B = " + str(x))
    except:
        return

def cal_covariance(matrix):
    print("\nstart calculating covariance")
    
    cov = []
    for i in range(0, matrix.__len__()):
        ii = []
        for j in range(0, matrix.__len__()):
            i_mean = numpy.mean(matrix[i])
            j_mean = numpy.mean(matrix[j])
            s = 0
            for k in range(0, matrix[i].__len__()):
                s += (matrix[i][k] - i_mean) * (matrix[j][k] - j_mean)
            ii.append(s / (matrix[i].__len__() - 1))

        cov.append(ii)

    print("covariance matrix calculated")

    return cov

def cal_correlation(matrix):
    print("\nstart calculating correlation")
    
    corr = []
    
    for i in range(0, matrix.__len__()):
        ii = []
        for j in range(0, matrix.__len__()):
            ii.append(numpy.corrcoef(matrix[i], matrix[j])[0][1])
        corr.append(ii)

    print("correlation matrix calculated")

    return corr

def cal_variance(matrix):
    print("\nstart calculating variance")
    
    var = []
    for i in matrix:
        i_mean = numpy.mean(i)
        s = 0
        for k in range(0, i.__len__()):
            s += (i[k] - i_mean) * (i[k] - i_mean)
        var.append(s / (i.__len__() - 1))
        
    print("variance matrix calculated")

    return var

def dim_reduction_low_variance(rgb_matrix, variance):
    print("\nstart reducing dimention with low variance filter")
    min = 0
    if variance[1] < variance[min]:
        min = 1
    if variance[2] < variance[min]:
        min = 2

    print("-> ", end='')
    if min == 0:
        print("red", end='')
    elif min == 1:
        print("green", end='')
    else:
        print("blue", end='')
    print(" have the lowest variance")

    rgb = []
    for i in [0, 1, 2]:
        if i != min:
            rgb.append(rgb_matrix[i])

    print("finish reducing dimention with low variance filter")

    return rgb

def pca(matrix, pcanum):
    cov = matrix - numpy.mean(matrix)
    eig_val, eig_vec = numpy.linalg.eigh(numpy.cov(cov))

    idx = numpy.argsort(eig_val)
    idx = idx[::-1]

    eig_vec = eig_vec[:,idx]
    eig_val = eig_val[idx]  
    if pcanum < numpy.size(eig_vec) or pcanum > 0:
    	eig_vec = eig_vec[:, range(pcanum)]
        
    abso = numpy.dot(eig_vec, numpy.dot(eig_vec.T, cov)) + numpy.mean(matrix).T
    img_mat = numpy.uint8(numpy.absolute(abso)) 

    return img_mat

def new_image_with_pca(matrix, pcanum):
    print("\nstart creating new image with pca")
    
    r = matrix[:,:,0]
    g = matrix[:,:,1]
    b = matrix[:,:,2]
 
    rr = pca(r, pcanum)
    gg = pca(g, pcanum)
    bb = pca(b, pcanum)

    img = Image.fromarray(numpy.dstack((rr, gg, bb)))

    name, format = path.split('/')[-1].split('.')
    
    p = ""
    for i in path.split('/'):
        if i != str(name) + '.' + str(format):
            p += str(i) + "/"
    p += str(name) + '-pca.' + str(format)

    try:
        img.save(p)
        print("pca generated photo saved as " + p)
    except:
        print("ERROR: something wrong in saving pca generated photo as " + p)
        print("permision denied??\nusing windows??")

    print("finish creating new image with pca")

    img.show()



if __name__ == '__main__' :
    ## get full path to image
    print("enter full path to image: ", end='')
    path = input()

    print("\n\n-------------------------------------------------------------\nINFO: better use linux based OS to avoid saving errors or ...\n-------------------------------------------------------------")
    sleep(5)

    ## read image
    image = add_image(path)

    ## creage 3*n matrix, first row: red, second row: green, third row: blue
    rgb_matrix = create_rgb_matrix(image)

    ## draw and save metadata plot
    print("\nDo you want to show plot after draw? (WARNING: make system slow)[y/N]: ", end='')
    c = input()
    if c == 'y':
        c = True
    else:
        c = False
    draw_plot(rgb_matrix, c)

    ## calculate total and red & green & blue average
    average_array = []
    average, average_array = cal_average(image)
    print_average(average, average_array)    

    ## calculate covariance
    covariance = cal_covariance(rgb_matrix)
    print_matrix(covariance, "covariance")

    ## calculate correlation
    correlation = cal_correlation(rgb_matrix)
    print_matrix(correlation, "correlation")

    ## calculate variance
    variance = cal_variance(rgb_matrix)
    print_var(variance)

    ## reducing dimention with low variance filter
    rgb_reduced = dim_reduction_low_variance(rgb_matrix, variance)
    print("\ndimention reduced (low variance filter)\ndo you want to print reducted array? (WARNING: might too large array)[y/N]: ", end='')
    c = input()
    if c == 'y':
        print(rgb_reduced)

    ## calculate pca of image and show and save
    pcanum = 10
    new_image_with_pca(image, pcanum)

