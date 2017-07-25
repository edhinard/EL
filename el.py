#! /usr/bin/env python3
# coding: utf-8

import math
import numbers

class Point:
    # and Vector as well
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __add__(self, other):
        if not isinstance(other, Point): return NotImplemented
        return Point(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        if not isinstance(other, Point): return NotImplemented
        return Point(self.x-other.x, self.y-other.y)
    def __mult__(self, mul):
        if not isinstance(mul, numbers.Number): return NotImplemented
        return Point(mul*self.x, mul*self.y)
    def __rmul__(self, mul):
        if not isinstance(mul, numbers.Number): return NotImplemented
        return Point(mul*self.x, mul*self.y)
    def __truediv__(self, div):
        if not isinstance(div, numbers.Number): return NotImplemented
        return Point(self.x/div, self.y/div)
    def rotate(self, alpha):
        cosalpha = math.cos(alpha)
        sinalpha = math.sin(alpha)
        return Point(
            cosalpha*self.x-sinalpha*self.y,
            sinalpha*self.x+cosalpha*self.y)

class Node:
    def __init__(self, x, y):
        self.pos = Point(x,y)
        self.vertices = []
        
    def addvertex(self, othernode, vertex):
        assert (vertex.node1==self and othernode==vertex.node2) or (vertex.node2==self and othernode==vertex.node1)
        self.vertices.append((othernode,vertex))
        self.vertices.sort(key=self.orient)

    def orient(self, ov):
        # this function helps sorting vertices by angle
        # it is a increasing function of that angle
        # from -3pi/4 (-4) to 5pi/4 (+4)
        #
        #          \ o=1-X/Y /
        #           \       /
        #        X<-Y\     /X>=Y
        #             \   /
        #              \ /
        #    o=3+Y/X    +    o=-1-Y/X
        #              / \
        #             /   \
        #         X<Y/     \X>=-Y
        #           /       \
        #          / o=-3-X/Y\
        othernode,vertex = ov
        X = othernode.pos.x - self.pos.x
        Y = othernode.pos.y - self.pos.y
        if X>=Y:
            if X>=-Y:
                o=-1-Y/X
            else:
                o=-3-X/Y
        else:
            if X>=-Y:
                o=1-X/Y
            else:
                o=3+Y/X
        return o

class Vertex:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.node1.addvertex(node2, self)
        self.node2.addvertex(node1, self)

        #
        #           node2
        #             +
        #             |
        #             |
        #  alpha      |     -alpha
        #         NW  |  NE
        #           + | +
        #             *
        #           + | +
        #         SW  |  SE
        # pi-alpha    |     -pi+alpha
        #             |
        #             |
        #             +
        #           node1
        #
        mid = (node1.pos + node2.pos) / 2
        alpha = math.pi/4
        self.SW = (mid, self.direction( math.pi-alpha), (self, True ))
        self.SE = (mid, self.direction(-math.pi+alpha), (self, False))
        self.NW = (mid, self.direction(         alpha), (self, False))
        self.NE = (mid, self.direction(        -alpha), (self, True ))
        
    def begin(self, relativeto):
        if relativeto == self.node1:
            return self.SW
        elif relativeto == self.node2:
            return self.NE
        else:
            assert True
    def end(self, relativeto):
        if relativeto == self.node1:
            return self.SE
        elif relativeto == self.node2:
            return self.NW
        else:
            assert True

    def direction(self, alpha):
        v = self.node2.pos - self.node1.pos
        return v.rotate(alpha)
        
class EL:
    def __init__(self, nodes, vertices):
        self.nodes = nodes
        self.vertices = vertices
        self._paths = None

    @property
    def paths(self):
        if self._paths:
            return self._paths
        
        # There is an arc between each middle of adjacent joining segments
        #  an arc is described by its two end points and its two control points
        # Two examples:                          *c1
        #   n2                          c2*  n  /
        #    +                            |  + /
        #     \                           | /|/
        #      \    c2                    |/ *m1
        #    m2 *--*    c1              m2*  |
        #        \     *                 /   +
        #         \     \               /   n1
        #          +-----*-----+ n1    +
        #         n         m1         n2
        # Vertices v1(n,n1) and v2(n,n2) are joining in node n
        # There is no vertex between v1 and v2 and angle n1/n/n2 is positive.
        # Node n keeps its joining vertices sorted like that.
        
        # Each vertex knows where are its middle m and direction d
        # relative to node n for begin and end of arcs
        # The more the two directions are facing the less the control points
        # are away from middle
        self._paths = []
        for n in self.nodes:
            for i,(n1,v1) in enumerate(n.vertices):
                n2,v2 = n.vertices[(i+1)%len(n.vertices)]
                m1,d1,id1 = v1.begin(n)
                m2,d2,id2 = v2.end(n)
                self._paths.append((m1,m1+d1,m2+d2,m2))

        return self._paths
