class Matrix(list):
    def __matmul__(self, B):
        # Fuente: https://www.codingem.com/numpy-at-operator/
        # Equivalente a @
        return [sum(a*b for a,b in zip(C,B)) for C in self]  

def matmul(A, B):
    # Fuente: https://www.codingem.com/numpy-at-operator/
    # Equivalente a @
    columnas = list(zip(*B))
    
    return ([[dot(x,y) for x in columnas] for y in A])  



def mul(A, B): # np.multiply || a*b Vector3
    if isinstance(B,(float,int)):
        return [C*B for C in A]
    
    return [sum(a*b for a,b in zip(C,B)) for C in A] 

def dot(a,b): # np.dot
    return sum(a*b for a,b in zip(a,b))

def sub(a,b): # np.subtract || a-b
    if any(isinstance(x, list) for x in a):
        return [sub(a[i],b[i]) for i in range(len(a))]
    return [a[i]-b[i] for i in range(len(a))]

def add(a,b): # np.add || a+b
    if any(isinstance(x, list) for x in a):
        return [add(a[i],b[i]) for i in range(len(a))]
    return [a[i]+b[i] for i in range(len(a))]

def cross(a,b): # np.cross 
    # For Vector3
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def norm(a): # np.linalg.norm
    return (sum(a[i]**2 for i in range(len(a))))**0.5

def div(a,b): # np.divide || a/b
    # a: Matrix,Vector || b: Scalar
    if b == 0:
        return a
    if any(isinstance(x, list) for x in a):
        return [div(x,b) for x in a]
    return [a[i]/b for i in range(len(a))]

def transpose(a): 
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

def minor(a,i,j): 
    return [row[:j] + row[j+1:] for row in (a[:i]+a[i+1:])]

def determinant(a): 
    if len(a) == 2: 
        return a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return sum([(-1)**(i) * a[0][i] * determinant(minor(a,0,i)) for i in range(len(a))])

def inverse(a): # np.linalg.inv
    det = determinant(a)
    if det == 0: 
        raise ValueError("Matrix is not invertible, determinant is zero.")
    adj = [[(-1)**(i+j) * determinant(minor(a,i,j)) for j in range(len(a))] for i in range(len(a))]
    return div(transpose(adj),det)
                
def flatten(a):
    """Turn a nested list into a flat list.

    Args:
        a (list): List of lists to flatten, 2 dimensional matrix.

    Returns:
        list: Flattened list.
    Example:
        [[1,2],[3,4]] -> [1,2,3,4]
    """
    return [i for x in a for i in x]