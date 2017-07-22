#! /usr/bin/env python3
# coding: utf-8

import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vertices = []
        self.directions = []
    def addvertex(self, vertex):
        self.vertices.append(vertex)
    
class Vertex:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.node1.addvertex(self)
        self.node2.addvertex(self)
    
class EL:
    def __init__(self, nodes, vertices):
        self.nodes = nodes
        self.vertices = vertices
