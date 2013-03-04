class BinarySolver(object):
    """
    Simple class to do a binary search
    """
    def __init__(self, verbose=False):
        self.verbose = verbose

    def solve(self, problem,
             tol=0.001,
             x_min=-1e10,
             x_max=1e10,
             x_guess=0,
             loop_max=200,
             speed=0.9,
             maximize=False):

        # find a true value to start with
        loop_count = 0
        x_start_next = x_guess
        search_direction = x_max
        start_search_depth = 100

        # do search for start value
        while True:

            # set new param
            x_start = x_start_next

            # status
            if self.verbose:
                print 'i:', loop_count, \
                 'start:', x_start

            # solve
            problem.setup(param=x_start)
            try:
                result = problem.solve()
            except Exception as e:
                print e
                result['status'] == 'exception'

            # if solver ok
            if result['status'] == 'optimal':
                break
            else:
                if x_start > x_max:
                    search_direction = x_min
                    x_start_next = x_guess
                    x_start_next = -1
                elif x_start < x_min:
                    break
                else:
                    x_start_next = x_start + (search_direction-x_guess)/start_search_depth

            # break if max loop count exceeded
            loop_count += 1
            if loop_count > loop_max:
                result['term_cond'] = 'loop count exceeded'
                return result

        # find the boundary
        lower_bound = x_start_next
        upper_bound = x_max
        param_next = (x_start_next + x_max)/2
        loop_count = 0

        while True:
            # set new param
            param = param_next
            diff = abs(param-lower_bound)

            # status
            if self.verbose:
                print 'i:', loop_count, \
                 'param:', param, \
                 'diff:', diff

            # solve
            problem.setup(param=param)
            try:
                result = problem.solve()
            except Exception as e:
                print e
                result['status'] == 'exception'

            # if solver ok
            if result['status'] == 'optimal':
                if (diff < tol):
                    if self.verbose:
                        print 'converged'
                    result['term_cond'] = 'converged'
                    return result
                else:
                    if self.verbose:
                        print 'increase'
                    lower_bound = param
                    param_next = param + (upper_bound - param)*speed
            # solver failed, move to last value that worked
            else:
                if self.verbose:
                    print 'decrease'
                upper_bound = param
                param_next = param + (lower_bound - param)*speed

            # break if max loop count exceeded
            loop_count += 1
            if loop_count > loop_max:
                result['term_cond'] = 'loop count exceeded'
                return result
