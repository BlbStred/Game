import math
import numpy as np
import sympy


def read(msg, type):
    
    while True:
        
        try:
            str = input(msg)
            result = type(str)
            
        except(ValueError):
            print("'%s' is not valid" % str)
            continue

        return result



def print_var_in_dict(var_name, index, var_dict):
    if index == None:
        print("%-20s =" % var_name, var_dict[var_name])
    else:
        vStr = var_name + '[' + str(index) + ']'
        print("%-20s =" % vStr, var_dict[var_name][index])

def pval(var_name, index = None):
    if   var_name in globals(): print_var_in_dict(var_name, index, globals())
    elif var_name in locals():  print_var_in_dict(var_name, index, locals())
    else:                       print(var_name, "does not exist")


def isNone(x):
    if x == None:      return True
    if np.isscalar(x): return False
    
    for e in x:
        if isNone(e):  return True
    return False
    

def relativeIncrease(old, new):
    return (new - old)/old
    
def l2vec(vec):
    s = 0
    for i in range(len(vec)):
        s = s + vec[i]**2
        
    return math.sqrt(s)


def addvec(v1, v2):
    if len(v1) == 2:
        (x1, y1) = v1
        (x2, y2) = v2
        return (x1 + x2, y1 + y2)
    if len(v1) == 3:
        (x1, y1, z1) = v1
        (x2, y2, z1) = v2
        return (x1 + x2, y1 + y2, z1 + z2)



class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def asString(self):
        return str(self.x) + "," +  str(self.y)
    
    def __str__(self):
        
        if isinstance(self.x, Vector):
            separator = '\n'
            flag      = '%s'
        else:
            separator = ', '
            flag      = '%5s'
            
        return (flag + separator + flag) % (str(self.x),  str(self.y))




# sine of angle in degrees
def sind(d):
    return math.sin(math.radians(d))

# cosine of angle in degrees
def cosd(d):
    return math.cos(math.radians(d))



def radius_of_curvature(f, x):
    # Find the first and second derivatives
    f_prime = sympy.diff(f, x)
    f_double_prime = sympy.diff(f_prime, x)

    # Calculate the radius of curvature
    return ((1 + f_prime**2)**(3/2)) / abs(f_double_prime)


def problem12_35():

    alpha = 30
    beta = 20
    mA = 22
    mB = 10
    g = 9.81
    m = mA/mB
    aA = g*(m*sind(alpha) + cosd(beta)*sind(alpha+beta)) / (m + (sind(alpha+beta)**2))
    aB2 = aA*sind(alpha+beta)  # normal
    aB1 = g*sind(beta)         # along A
    aB = l2vec((aB1, aB2))

    print('aA =', aA)
    print('aB1 =', aB1)
    print('aB2 =', aB2)
    print('aB =', aB)

def problemClass():
    
    h = sympy.symbols('h')  #theta
    r = 0.2/h
    
    drdh = sympy.diff(r, h)
    print(drdh)

    tan_psi = r/drdh
    print(tan_psi)

    psi = math.atan(tan_psi.subs(h, math.pi/2))
    print(psi)


    alpha = 0.5669
    beta = 0.5669    
    



