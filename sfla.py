import numpy as np
import matplotlib.pyplot as plt
import time

def opt_func(frog, obstacles, w1, w2, target):
    """The mathematical function to optimize.
    
    Arguments:
        frog {np.ndarray} -- An individual value or frog
        obstacles {np.ndarray} -- An array containing the obstacles registered by the sensors
        w1 {int} -- Weight value for obstacle penalization
        w2 {int} -- Weight value for target penalization
        target {np.ndarray} -- An array containing the target coordinates
    
    Returns:
        float -- The output value or fitness of the frog
    """
    # Find the distances between the frog and registered obstacles
    distances = np.array(list(map(np.linalg.norm, obstacles - frog)))
    # Fitness function
    output= w1 * np.exp(-np.amin(distances)) + w2 * np.linalg.norm(target - frog)
    return output

def gen_frogs(frogs, sigma, center):
    """Generates a random frog population from gaussian normal distribution around the given position
    
    Arguments:
        frogs {int} -- Number of frogs
        sigma {int/float} -- Sigma of gaussian distribution
        center {np.ndarray} -- Center of the distribution of the generated frogs
    
    Returns:
        numpy.ndarray -- A frogs x dimension array
    """

    # Create random positions close to the current position
    xi = np.random.normal(center[0], sigma, frogs)
    yi = np.random.normal(center[1], sigma, frogs)
    frogs = np.stack((xi, yi), axis = 1)
    return frogs

def sort_frogs(frogs, mplx_no, obstacles, w1, w2, target):
    """Sorts the frogs in decending order of fitness by the given function.
    
    Arguments:
        frogs {numpy.ndarray} -- Frogs to be sorted
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped
        opt_func {function} -- Function to determine fitness
    
    Returns:
        numpy.ndarray -- A memeplexes x frogs/memeplexes array of indices, [0, 0] will be the greatest frog
    """

    # Find fitness of each frog
    #fitness = np.array(list(map(opt_func, frogs, 1, (2,3))))
    fitness = np.array([opt_func(x, obstacles, w1, w2, target) for x in frogs])
    # Sort the indices in decending order by fitness
    sorted_fitness = np.argsort(fitness)
    # Empty holder for memeplexes
    memeplexes = np.zeros((mplx_no, int(frogs.shape[0]/mplx_no)))
    # Sort into memeplexes
    for j in range(memeplexes.shape[1]):
        for i in range(mplx_no):
            memeplexes[i, j] = sorted_fitness[i+(mplx_no*j)]
    return memeplexes

def local_search(frogs, memeplex, sigma, center, obstacles, w1, w2, target):
    """Performs the local search for a memeplex.
    
    Arguments:
        frogs {numpy.ndarray} -- All the frogs
        memeplex {numpy.ndarray} -- One memeplex
        opt_func {function} -- The function to optimize
        sigma {int/float} -- Sigma for the gaussian distribution by which the frogs were created
        mu {int/float} -- Mu for the gaussian distribution by which the frogs were created
    
    Returns:
        numpy.ndarray -- The updated frogs, same dimensions
    """

    # Select worst, best, greatest frogs
    frog_w = frogs[int(memeplex[-1])]
    frog_b = frogs[int(memeplex[0])]
    frog_g = frogs[0]
    # Move worst wrt best frog
    frog_w_new = frog_w + (np.random.rand() * (frog_b - frog_w))
    # If change not better, move worst wrt greatest frog
    if opt_func(frog_w_new, obstacles, w1, w2, target) > opt_func(frog_w, obstacles, w1, w2, target):
        frog_w_new = frog_w + (np.random.rand() * (frog_g - frog_w))
    # If change not better, random new worst frog
    if opt_func(frog_w_new, obstacles, w1, w2, target) > opt_func(frog_w, obstacles, w1, w2, target):
        frog_w_new = gen_frogs(1, sigma, center)[0]
    # Replace worst frog
    frogs[int(memeplex[-1])] = frog_w_new
    return frogs

def shuffle_memeplexes(memeplexes):
    """Shuffles the memeplexes without sorting them.
    
    Arguments:
        memeplexes {numpy.ndarray} -- The memeplexes
    
    Returns:
        numpy.ndarray -- A shuffled memeplex, unsorted, same dimensions
    """

    # Flatten the array
    temp = memeplexes.flatten()
    #Shuffle the array
    np.random.shuffle(temp)
    # Reshape
    temp = temp.reshape((memeplexes.shape[0], memeplexes.shape[1]))
    return temp

def sfla(startp, target, obstacles, w1=5, w2=12, frogs=30, sigma=1, mplx_no=6, mplx_iters=10, solun_iters=50):
    """Performs the Shuffled Leaping Frog Algorithm.
    
    Arguments:
        opt_func {function} -- The function to optimize.
    
    Keyword Arguments:
        frogs {int} -- The number of frogs to use (default: {30})
        sigma {int/float} -- Sigma for the gaussian normal distribution to create the frogs (default: {1})
        center {int/float} -- 
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped (default: {6})
        mplx_iters {int} -- Number of times a single memeplex will be iterated before shuffling (default: {10})
        solun_iters {int} -- Number of times the memeplexes will be shuffled (default: {50})
    
    Returns:
        tuple(numpy.ndarray, numpy.ndarray, numpy.ndarray) -- [description]
    """

    # Generate frogs around the given position
    frogs = gen_frogs(frogs, sigma, startp)
    # Arrange frogs and sort into memeplexes
    memeplexes = sort_frogs(frogs, mplx_no, obstacles, w1, w2, target)
    # Best solution as greatest frog
    best_solun = frogs[int(memeplexes[0, 0])]
    # For the number of iterations
    for i in range(solun_iters):
        # Shuffle memeplexes
        memeplexes = shuffle_memeplexes(memeplexes)
        # For each memeplex
        for mplx_idx, memeplex in enumerate(memeplexes):
            # For number of memeplex iterations
            for j in range(mplx_iters):
                # Perform local search
                frogs = local_search(frogs, memeplex, sigma, startp, obstacles, w1, w2, target)
            # Rearrange memeplexes
            memeplexes = sort_frogs(frogs, mplx_no, obstacles, w1, w2, target)
            # Check and select new best frog as the greatest frog
            new_best_solun = frogs[int(memeplexes[0, 0])]
            if opt_func(new_best_solun, obstacles, w1, w2, target) < opt_func(best_solun, obstacles, w1, w2, target):
                best_solun = new_best_solun
    return best_solun, frogs, memeplexes.astype(int)

def main():
    # Run algorithm
    obstacles = np.array([[4,5], [6,6], [8,9]])
    t = time.time()
    solun, frogs, memeplexes = sfla((2,3), (15,15), obstacles, frogs = 60)
    print(f"Optimal Solution: {solun} in {time.time()-t}")
    
    fig, ax = plt.subplots()
    ax.scatter(2,3)
    ax.scatter(*obstacles.T)
    ax.scatter(15,15)
    ax.scatter(solun[0], solun[1])
    # Plot properties
    plt.legend()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Shuffled Frogs")
    # Show plot
    plt.show()

if __name__ == '__main__':
    main()