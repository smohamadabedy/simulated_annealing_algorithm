import numpy as np

#optimization function 
def cost(arg):
    return (arg[0,0]+2*arg[0,1] - 7)**2 + (2*arg[0,0]+arg[0,1] - 5)**2
# chose size of search space
n = 2;
# intial neighborhood radius vector 
Delta = np.random.rand(1,n)
# intial start point
X0 = np.random.rand(1,n)
# calc inital tempereture 
T0 = 300
# probabilty of uphill move
Pn = lambda f2,f1,Tk : np.exp(-np.divide(np.subtract(f2,f1),Tk))
# number of iteration
maxit = 600
# default move
move = 0
for i in range(1,maxit):
    # candidate point and previous point at each iterations
    prevPoint = X0
    r         = (Delta*np.random.uniform(low=-1, high=1, size=(1,n)))
    newPoint  = X0 + r
    # calc new points
    prevF = cost(prevPoint)
    newF  = cost(newPoint)
    # SA creteria
    if(newF < prevF):
        X0 = newPoint
        move = 1
    else:
        prob  = Pn(newF,prevF,T0)
        randv = np.random.rand(1)
        cond  = randv < prob
        if(cond):
            X0 = newPoint
            move = 1
        else:
            move = 0
            
    # summery
    # print(i,':',T0,prevPoint,r,prevF,newPoint,newF,prob,randv,cond)
    # update temp       
    if(move == 1):
        T0 = .95*T0
    # check creteria
    if(T0 < .05):
        break;
        
        
        
print('<=================================>')
print(X0)
print(cost(X0))
print('iteration: ',i,'/',maxit)
