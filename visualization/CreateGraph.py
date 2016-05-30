import itertools
import sys
import operator
import numpy
from numpy import linalg as LA

def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def trans_matrix( seq_list, edges ):
    T_arr = numpy.zeros(shape=(len(seq_list),len(seq_list)))
    for x,y in edges:
        x_ind = seq_list.index(x)
        y_ind = seq_list.index(y)
        T_arr[x_ind,y_ind] = 1
        T_arr[y_ind,x_ind] = 1
    totals=T_arr.sum(axis=0)
    totals_a = numpy.add(totals,1)
    #totals[totals == 0] = 1
    div = T_arr / totals_a
    T_mat = numpy.asmatrix(div)
    return T_mat

def raise_matrix( T_matrix, power, canon_ind ):
    raised_mat = LA.matrix_power(T_matrix,power)   
    total=numpy.count_nonzero(raised_mat[canon_ind])
    mat_size=float(raised_mat[canon_ind].size)
    return total/mat_size

def main(args):

    with open(args[1]) as strings:
        str_list = strings.read().splitlines()

    canon_seq=args[2]
    
    tokens=args[1].rsplit('.',1)
    file=tokens[0]
    outfile_hamm = '%s_hamm.txt' % (file)
    outfile_mat1 = '%s_mat1.txt' % (file)
    outfile_mat5 = '%s_mat5.txt' % (file)
    outfile_mat10 = '%s_mat10.txt' % (file)
    outfile_mat20 = '%s_mat20.txt' % (file)

    edges = [(seq2,seq) for seq,seq2 in itertools.combinations(str_list,2) if hamdist(seq2,seq) < 2 ]
    #sorted_hamm_t = sorted(dist_dict.items(), key=operator.itemgetter(1))
    #sorted_hamm = [ key for key,val in sorted_hamm_t]
    
    #random.shuffle(str_list)
    
    #step = (len(str_list)-1)/(num_seq-1)
    #end = len(str_list)

    hamm_out = open(outfile_hamm,"w")
    hamm_out.write("\n".join("{0},{1}".format(x[0],x[1]) for x in edges))

    numpy.set_printoptions(threshold='nan')

    canon_ind=str_list.index(canon_seq)

    T_mat = trans_matrix(str_list,edges)
    #print raise_matrix(T_mat,1)
    #numpy.savetxt(hamm_out1,T)
    #print raise_matrix(T_mat,3)
    #numpy.savetxt(hamm_out5,T)
    #T = raise_matrix(T_mat,10)
    #numpy.savetxt(hamm_out10,T)
    #T = raise_matrix(T_mat,20)
    #numpy.savetxt(hamm_out20,T)
    for i in range(1,15):
        print i
        print raise_matrix(T_mat,i,canon_ind)

if __name__ == "__main__":

    main(sys.argv)

