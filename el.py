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
    @staticmethod
    def det(v, w):
        return v.x * w.y - v.y * w.x
    @staticmethod
    def convergence(A,v,B,w):
        # A and B point
        # v and w vectors
        # returns intersection I of (A,v) (B,w) if:
        #  - I exists
        #  - AI and v goes in the same direction
        #  - BI and w goes in the same direction
        det = Point.det(v,w)
        if abs(det)/(v.norm()*w.norm()) < 0.01:
            return None
        a = Point.det(w, A-B) / det
        if a <= 0:
            return None
        return A + a * v

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
    def __init__(self, nodes, vertices, params):
        # TODO: verification on validity
        #  -proper structure
        #  -at least one vertex
        #  -raisonable dimensions
        #  ...
        self.nodes = [Node(*node) for node in nodes]
        self.vertices = [Vertex(self.nodes[n1], self.nodes[n2]) for n1,n2 in vertices]
        self.params = params
        self._paths = None

    def dump(self):
        nodes = [(node.pos.x, node.pos.y) for node in self.nodes]
        vertices = [(self.nodes.index(vertex.node1), self.nodes.index(vertex.node2)) for vertex in self.vertices]
        return nodes,vertices,self.params

    @property
    def bounds(self):
        if not self._paths:
            dummy = self.paths
        return self.left, self.right, self.top, self.bottom
    
    @property
    def paths(self):
        if self._paths:
            return self._paths

        self.left = self.right = self.nodes[0].pos.x
        self.top = self.bottom = self.nodes[0].pos.y
        # There is an arc between each middle of adjacent joining segments
        #  an arc is displayed as a Bezier curve and thus described by its two
        #  end points and its two control points
        # Two examples:                          *C1
        #   n2                          C2*  n  /
        #    +                            |  + /
        #     \                           | /|/
        #      \    C2                    |/ *M1
        #    M2 *--*    C1              M2*  |
        #        \     *                 /   +
        #         \     \               /   n1
        #          +-----*-----+ n1    +
        #         n         M1         n2
        # Vertices v1(n,n1) and v2(n,n2) are joining in node n
        # There is no vertex between v1 and v2 and angle n1/n/n2 is positive.
        # Node n keeps its joining vertices sorted like that.
        
        # The control points are computed as C = M + a * D
        # where:
        #  - M - middle point
        #  - D - direction (oriented tangent of arc)
        #      M and D are given by Vertex.begin(n) and Vertex.end(n)
        #  - a is tune so as to draw a nice curve without loop or cusp
        #     There are 3 cases:
        # if D1 and D2 are converging on point I
        #  C1(resp. C2) is set to I
        #
        # else if vertices v1 and v2 draw a convexity (n is at a top of a peak)
        #  a must be set in order for the arc to go in the vicinity of n
        #
        # else (vertices v1 and v2 draw a concavity (n is in the bottom of a hole)
        #  a must be big enough for the arc to be smooth
        #  and small enough to avoid loop/cusp
        #
        #
        #
        self._paths = []
        for n in self.nodes:
            for i,(n1,v1) in enumerate(n.vertices):
                n2,v2 = n.vertices[(i+1)%len(n.vertices)]
                M1,D1,id1 = v1.begin(n)
                M2,D2,id2 = v2.end(n)
                C1 = M1+D1
                C2 = M2+D2
                I = Point.convergence(M1,D1,M2,D2)
                if I:
                    C1 = C2 = I
                self._paths.append((M1,C1,C2,M2))
                self.left = min(self.left, M1.x, C1.x, C2.x, M2.x)
                self.right = max(self.right, M1.x, C1.x, C2.x, M2.x)
                self.bottom = min(self.bottom, M1.y, C1.y, C2.y, M2.y)
                self.top = max(self.top, M1.y, C1.y, C2.y, M2.y)

        return self._paths
