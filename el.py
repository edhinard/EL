#! /usr/bin/env python3
# coding: utf-8

import math
import namedtuple

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def xx:
        cc
Point = namedtuple('Point', ['x', 'y'])

class Vector:
    def __init__(self, A, B):
        self.x = B.x - A.x
        self.y = B.y - A.y
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    def __mult__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    
    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        subbed = tuple( a - b for a, b in zip(self, other) )
return Vector(*subbed)

class Node:
    def __init__(self, x, y):
        self.point = Point(x,y)
        self.vertices = []
        self._arcs = None
    def addvertex(self, vertex, othernode):
        assert((vertex.node1==self and othernode==vertex.node2) or
               (vertex.node2==self and othernode==vertex.node1))
        self.vertices.append((othernode,vertex))
        self.vertices.sort(key=self.orient)

    def orient(self, othernode):
        # this function helps sorting vertices by angle
        # it is a increasing function of that angle
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
        X = othernode.point.x - self.point.x
        Y = othernode.point.y - self.point.y
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

    @property
    def arcs(self):
        if self._arcs:
            return self._arcs
        for i,(nodeA,vertexA) in enumerate(self.vertices):
            nodeB,vertexB = self.vertices[(i+1)%len(self.vertices)]
            middleA = 
            cpA = self.controlpoint(nodeA

    def controlpoint(self, point, alpha, gamma):
        #
        # A(self)                B(point)
        # +----------------------+
        #                       /.
        #               alpha  / .
        #                     /  .
        #                    /   .
        #                   +    .
        #                   C(controlpoint)
        # BC = gamma * AB        .
        #                        .
        #                        .
        #                        +
        #                        A'
        bax = self.point.x - point.x
        bay = self.point.y - point.y
        baprimex = self.point.x - bay
        bapriney = self.point.y + bax
        cx = point.x + gamma * (math.cos(alpha)*bax + math.sin(alpha)*baprimex)
        cy = point.y + gamma * (math.cos(alpha)*bay + math.sin(alpha)*baprimey)
        return Point(cx, cy)
        
class Vertex:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.node1.addvertex(self, node2)
        self.node2.addvertex(self, node1)
    
class EL:
    def __init__(self, nodes, vertices):
        self.nodes = nodes
        self.vertices = vertices

        self.arcs= []
        for node in nodes:
            self.arcs.append(node.
