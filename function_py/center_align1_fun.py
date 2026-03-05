import numpy as np


def center_align1(A,B):
    """
    Pads array B with zeros so that its length matches that of array A,
    and centers the elements of B within the resulting array.
    """
    len_A = len(A)
    len_B = len(B)
    len_B0 = len(B[0])
    np_zero = np.zeros((int( (len_A-1)/2-(len_B-1)/2 ),
                 len_B0 ))
    result = np.concatenate((np_zero, B), axis=0)
    result = np.concatenate((result, np_zero), axis=0)
    return result

    
    
    
    
    
    
    
    
    
    
