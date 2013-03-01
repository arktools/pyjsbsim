
cdef extern from "cpp_rect.h":
    ctypedef struct c_Rectangle "Rectangle":
        int x0, y0, x1, y1
        int getLength()
        int getHeight()
        int getArea()
        void move(int dx, int dy)
        c_Rectangle add "operator+"(c_Rectangle right)
    c_Rectangle *new_Rectangle "new Rectangle" (int x0, int y0, int x1, int y1)
    void del_Rectangle "delete" (c_Rectangle *rect)

cdef class Rectangle:
    cdef c_Rectangle *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.thisptr = new_Rectangle(x0, y0, x1, y1)
    def __dealloc__(self):
        del_Rectangle(self.thisptr)
    def getLength(self):
        return self.thisptr.getLength()
    def getHeight(self):
        return self.thisptr.getHeight()
    def getArea(self):
        return self.thisptr.getArea()
    def move(self, dx, dy):
        self.thisptr.move(dx, dy)
        
    def __add__(Rectangle left, Rectangle right):
        cdef c_Rectangle c = left.thisptr.add(right.thisptr[0])
        cdef Rectangle sum = Rectangle(c.x0, c.y0, c.x1, c.y1)
        return sum
        
    def __repr__(self):
        return "Rectangle[%s,%s,%s,%s]" % (self.thisptr.x0, 
                                           self.thisptr.y0, 
                                           self.thisptr.x1, 
                                           self.thisptr.y1)

"""
cdef Rectangle r = Rectangle(1, 2, 3, 4)
print r
print "Original area:", r.getArea()
r.move(1,2)
print r
print "Area is invariante under rigid motions:", r.getArea()
r += Rectangle(0,0,1,1)
print r
print "Now the aread is:", r.getArea()
"""
