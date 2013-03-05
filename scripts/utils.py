class BinarySolver(object):
    """
    Simple class to do a binary search to find
    max/min x where binary function evaluates to true
    """
    def __init__(self, verbose=False):
        self.verbose = verbose

    def solve(self, problem,
             prob_type="min", 
             tol=0.001,
             x_min=-1e10,
             x_max=1e10,
             x_guess=0,
             loop_max=200,
             start_search_depth=100):

        if prob_type not in ["min", "max"]:
            raise IOError("unknown problem type")

        # find a true value to start with that 
        # doesn't throw an exception, search in
        # the direction of xmax first
        loop_count = 0
        x_start_next = x_guess
        search_direction = x_max

        # do linear search for start value
        while True:

            # set new param
            x_start = x_start_next

            # status
            if self.verbose:
                print 'i:', loop_count, \
                 'start:', x_start

            # setup
            problem.setup(param=x_start)

            # if solution found
            if problem.solve():
                break
            else:
                if x_start > x_max:
                    search_direction = x_min
                    x_start_next = x_guess
                    x_start_next = -1
                elif x_start < x_min:
                    break
                else:
                    # step in search direction
                    x_start_next = x_start + (search_direction-x_guess)/start_search_depth

            # break if max loop count exceeded
            loop_count += 1
            if loop_count > loop_max:
                raise RuntimeError('loop count exceeded')

        # find the boundary
        if prob_type == "max":
            left = x_start_next
            right = x_max
        elif prob_type == "min":
            left = x_start_next
            right = x_min
            
        param_next = (right + left) /2
        loop_count = 0

        while True:
            # set new param
            param = param_next
            diff = abs(left-right)

            # status
            if self.verbose:
                print 'i:', loop_count, \
                 'param:', param, \
                 'diff:', diff

            # setup
            problem.setup(param=param)

            # if solution found
            if problem.solve():
                if (loop_count > 1 and diff < tol):
                    if self.verbose:
                        print 'converged'
                    return problem.results
                else:
                    if self.verbose:
                        print 'increase'
                    left = param
                    param_next = left + (right - left)*0.5
            # solver failed, move to last value that worked
            else:
                if self.verbose:
                    print 'decrease'
                right = param
                param_next = right - (right - left)*0.5

            # break if max loop count exceeded
            loop_count += 1
            if loop_count > loop_max:
                raise RuntimeError('loop count exceeded')
