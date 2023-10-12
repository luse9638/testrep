######################################################################## imports

import numpy as np
import jax
import jax.numpy as jnp
import math
import time

#################################################################### subroutines

def jacobian(F, x: jnp.array):
    '''
    Compute jacobian of F at x
    Inputs:
        F: F = (f_1(x), ..., f_n(x))
        x: x = (x_1, x_2, ..., x_n)
    Outputs:
        J: n x n Jacobian matrix of f evaluated at x
    '''
    return jnp.array(jax.jacfwd(F)(x))


def nDNewton(x0: jnp.array, F, tol, nMax):
    '''
    Run Newton's Method on a vector valued function F
    Inputs:
        x0: initial guess, x0 = (x_1, ..., x_n)
        F: F = (f_1(x), ..., f_n(x))
        tol: tolerance
        nMax: max iterations
    Outputs:
        [xStar, err, its] where:
            xStar: approximate root
            err: error message
            its: number of iterations run
    '''

    # run until we reach nMax or tolerance
    for its in range(nMax):
        # compute jacobian and it's inverse
        J = jacobian(F, x0)
        Jinv = jnp.linalg.inv(J)
        
        # iterate
        x1 = x0 - jnp.dot(Jinv, F(x0))

        # terminate if within tolerance
        if (jnp.linalg.norm(x1 - x0) < tol):
            xStar = x1
            err = 0
            return [xStar, err, its]

        x0 = x1
    
    # exceeded max iterations
    xStar = x1
    err = 1
    return [xStar, err, its]

def nDLazyNewton(x0: jnp.array, F, tol, nMax):
    '''
    Run Newton's Method on a vector valued function F
    Inputs:
        x0: initial guess, x0 = (x_1, ..., x_n)
        F: F = (f_1(x), ..., f_n(x))
        tol: tolerance
        nMax: max iterations
    Outputs:
        [xStar, err, its] where:
            xStar: approximate root
            err: error message
            its: number of iterations run
    '''

    # compute Jacobian and inverse only once
    J = jacobian(F, x0)
    Jinv = jnp.linalg.inv(J)
    
    # run until we reach nMax or tolerance
    for its in range(nMax):
        # iterate
        x1 = x0 - jnp.dot(Jinv, F(x0))

        # terminate if within tolerance
        if (jnp.linalg.norm(x1 - x0) < tol):
            xStar = x1
            err = 0
            return [xStar, err, its]

        x0 = x1
    
    # exceeded max iterations
    xStar = x1
    err = 1
    return [xStar, err, its]


############################################################################# 1)
print("")
print("Problem 1)")

# F_1(x, y) = [f_1(x, y), f_2(x, y)]
# f_1(x, y) = x^2 + y^2 - 4 = 0
# f_2(x, y) = e^x + y - 1 = 0
def F_1(x: jnp.array):
    F = []
    F.append(x[0] ** 2 + x[1] ** 2 - 4)
    F.append(jnp.exp(x[0]) + x[1] - 1)
    return jnp.array([F[0], F[1]])

###################################### i)
print("")
print("i)")

# x0 = [1, 1]
iNewton = nDNewton(jnp.array([1., 1.]), F_1, 1E-16, 100)
iLazyNewton = nDLazyNewton(jnp.array([1., 1.]), F_1, 1E-16, 5)
print("Iterations needed for Newton's Method: " + str(iNewton[2]) +\
      ", approximated root: " + str(iNewton[0]) + ", error code: " +\
        str(iNewton[1]))
print("Iterations needed for Lazy Newton's Method: " + str(iLazyNewton[2]) +\
      ", approximated root: " + str(iLazyNewton[0]) + ", error code: " +\
        str(iLazyNewton[1]))


##################################### ii)
print("")
print("ii)")




