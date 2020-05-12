"""
Small utility function to count neural avalanches in spike raster plots.

Pedro Mediano, May 2020
"""
import numpy as np

def avalanche_parse(X, th=1e-12):
    """
    Extract distributions of avalanche size and duration from neural data.

    Parameters
    ----------
    X : np.array
        Data to compute avalanches from. Must be either a 1D array, or a 2D
        array of size T-by-D, with T time bins and D neurons.
    th : float (default=0)
        Avalanche threshold. Any time bins not exceeding the threshold will be
        considered quiescent and not count towards the avalanche distribution.

    Returns
    -------
    sizes : np.array
        sizes of all avalanches detected
    durations : np.array
        durations of all avalanches detected, counted in number of steps
    """

    ## Parameter checks and initialisation
    s = X.shape
    if len(s) > 2:
        raise RuntimeError('Input matrix must be 1D or 2D.')
    elif len(s) == 2:
        T, D = s
        if D > T:
            raise RuntimeWarning('It seems your data has more variables than ' +
                    'time points. Perhaps you forgot to transpose your matrix?')
        d = X.sum(axis=1)
    elif len(s) == 1:
        d = X


    ## Compute durations and sizes of all avalanches
    if all(d <= th):
        # Short-cut in case the array has either no avalanches ...
        sizes     = np.array([])
        durations = np.array([])

    elif all(d > th):
        # ... or just one huge avalanche
        sizes     = np.array([d.sum()])
        durations = np.array([len(d)])

    else:
        # In normal conditions, find start and end points of avalanches
        avl_start = np.where(np.logical_and(d[:-1] <= th, d[1:] > th))[0] + 1
        avl_end   = np.where(np.logical_and(d[:-1] > th, d[1:] <= th))[0] + 1

        # Correct in case array started or ended in avalanche
        if d[-1] > th:
            avl_end = np.concatenate((avl_end, [len(d)]))
        if d[0] > th:
            avl_start = np.concatenate(([0], avl_start))

        durations = avl_end - avl_start
        sizes     = np.array([np.sum(d[s:e]) for s,e in zip(avl_start, avl_end)])

    return sizes, durations

