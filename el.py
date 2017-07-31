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
    def unit(self):
        norm = self.norm()
        return Point(self.x / norm, self.y / norm)
    def __add__(self, other):
        if not isinstance(other, Point): return NotImplemented
        return Point(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        if not isinstance(other, Point): return NotImplemented
        return Point(self.x-other.x, self.y-other.y)
    def __neg__(self):
        return Point(-self.x, -self.y)
    def __mul__(self, mul):
#        if isinstance(mul, numbers.Number):
#            return Point(mul*self.x, mul*self.y)
        if isinstance(mul, Point):
            return self.x*mul.x + self.y*mul.y
        else:
            return NotImplemented
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
        b = Point.det(v, A-B) / det
        if a <= 0 or b <=0:
            return None
        return B + b * w
#        return A + a * v

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
        #         2           0
        #          \ o=1-X/Y /
        #           \       /
        #        X<-Y\     /X>=Y
        #             \   /
        #              \ /
        #    o=3+Y/X    +    o=-1+Y/X
        #              / \
        #             /   \
        #         X<Y/     \X>=-Y
        #           /       \
        #          / o=-3-X/Y\
        #        +-4         -2
        othernode,vertex = ov
        X = othernode.pos.x - self.pos.x
        Y = othernode.pos.y - self.pos.y
        if X>=Y:
            if X>=-Y:
                o=-1+Y/X
            else:
                o=-3-X/Y
        else:
            if X>=-Y:
                o=1-X/Y
            else:
                o=3+Y/X
        return o

class Vertex:
    def __new__(cls, node1, node2, symbol, params):
        if symbol == '*':
            return object.__new__(StarVertex)
        if symbol == '+':
            return object.__new__(PlusVertex)
        if symbol == '=':
            return object.__new__(EqualVertex)
        raise Exception("Unknown symbol {!r}".format(symbol))

    def __init__(self, node1, node2, symbol, params):
        self.params = params
        self.node1 = node1
        self.node2 = node2
        self.node1.addvertex(node2, self)
        self.node2.addvertex(node1, self)
        self.reset()

    def reset(self):
            self._NW, self._NE, self._SW, self._SE = self.computepoints()

    @property
    def NW(self):
        return self._NW
    @property
    def NE(self):
        return self._NE
    @property
    def SW(self):
        return self._SW
    @property
    def SE(self):
        return self._SE
        
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

class StarVertex(Vertex):
    def computepoints(self):
        #           node2
        #             +
        #             |
        #    alpha    |   -alpha
        #          NW | NE
        #             *
        #          SW | SE
        #   pi-alpha  |   -pi+alpha
        #             |
        #             +
        #           node1
        mid = (self.node1.pos + self.node2.pos) / 2
        alpha = math.pi/180*self.params['alpha']
        NW = (mid, self.direction(         alpha), (self, False))
        NE = (mid, self.direction(        -alpha), (self, True ))
        SW = (mid, self.direction( math.pi-alpha), (self, True ))
        SE = (mid, self.direction(-math.pi+alpha), (self, False))
        return NW, NE, SW, SE

class PlusVertex(Vertex):
    def computepoints(self):
        #           node2
        #             +
        #             |
        #    pi/2 NW  *  NE -pi/2 ^
        #             |           |
        #             |           | plusgap
        #             |           |
        #    pi/2 SW  *  SE -pi/2 v
        #             |
        #             +
        #           node1
        gap = (self.params['plusgap']/2) * (self.node2.pos-self.node1.pos).unit()
        mid1 = (self.node1.pos + self.node2.pos) / 2 - gap
        mid2 = (self.node1.pos + self.node2.pos) / 2 + gap
        alpha = math.pi/2
        NW = (mid2, self.direction( math.pi/2), (self, True ))
        NE = (mid2, self.direction(-math.pi/2), (self, True ))
        SW = (mid1, self.direction( math.pi/2), (self, False))
        SE = (mid1, self.direction(-math.pi/2), (self, False))
        return NW, NE, SW, SE

class EqualVertex(Vertex):
    def computepoints(self):
        #           node2
        #             +
        #             |
        #          0  |  0
        #          NW | NE
        #           * | *
        #          SW | SE
        #          pi | -pi
        #             |
        #             +
        #           node1
        gap = (self.params['equalgap']/2) * (self.node2.pos-self.node1.pos).rotate(math.pi/2).unit()
        mid1 = (self.node1.pos + self.node2.pos) / 2 - gap
        mid2 = (self.node1.pos + self.node2.pos) / 2 + gap
        NW = (mid2, self.direction(0), (self, True ))
        NE = (mid1, self.direction(0), (self, False ))
        SW = (mid2, self.direction(math.pi), (self, False))
        SE = (mid1, self.direction(math.pi), (self, True))
        return NW, NE, SW, SE

class EL:
    def __init__(self, nodes, vertices, params):
        # TODO: verification on validity
        #  -proper structure
        #  -at least one vertex
        #  -raisonable dimensions
        #  ...
        self.params = params
        self.nodes = [Node(*node) for node in nodes]
        self.vertices = [Vertex(self.nodes[n1], self.nodes[n2], symbol, params) for n1,n2,symbol in vertices]
        self._paths = None

    def reset(self):
        self._paths = None
        for vertex in self.vertices:
            vertex.reset()
        
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
        self._paths = []
        for n in self.nodes:
            for i,(n1,v1) in enumerate(n.vertices):
                n2,v2 = n.vertices[(i+1)%len(n.vertices)]
                M1,D1,id1 = v1.begin(n)
                M2,D2,id2 = v2.end(n)
                
                if n1==n2 or Point.det(n1.pos-n.pos, n2.pos-n.pos) < 0: #convexe
                    A= n.pos+self.params['peak']*((n.pos-n1.pos).unit() + (n.pos-n2.pos).unit())
                    C1 = M1+0.3*D1
                    C2 = A+0.3*D1.norm()*(D1.unit()+D2.unit()).unit().rotate(-math.pi/2)
                    self.appendcurve(M1,C1,C2,A)
                    C1 = A+0.3*D2.norm()*(D1.unit()+D2.unit()).unit().rotate(math.pi/2)
                    C2 = M2+0.3*D2
                    self.appendcurve(A,C1,C2,M2)
                    continue

                c = (1.3 + (n1.pos-n.pos).unit() * (n.pos-n2.pos).unit())/4                
                C1 = M1+c*D1
                C2 = M2+c*D2
                self.appendcurve(M1,C1,C2,M2)

        return self._paths

    def appendcurve(self, P1,C1,C2,P2):
        self._paths.append((P1,C1,C2,P2))
        self.left = min(self.left, P1.x, C1.x, C2.x, P2.x)
        self.right = max(self.right, P1.x, C1.x, C2.x, P2.x)
        self.bottom = min(self.bottom, P1.y, C1.y, C2.y, P2.y)
        self.top = max(self.top, P1.y, C1.y, C2.y, P2.y)
