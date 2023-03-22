# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL


import numpy as np
from lxml import etree
from lxml.etree import ElementTree as ET


from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.files_op import Filesop

__all__ = ['Xmlop']


@Decorator.cdec(Cfg.default['param'])
class Xmlop(Filesop):


    def __new__(cls, *args, **kw):
        ob = super().__new__(cls, *args, **kw)
        ob.default = cls.default
        return ob

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return

    @staticmethod
    def read(xml_path):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        return tree

    @staticmethod
    def getroot(tree):
        root = tree.getroot()
        return root

    @staticmethod
    def write(out_path, tree):
        tree.write(out_path, pretty_print=True, xml_declaration=False, encoding="utf-8")

    @staticmethod
    def delnodes(tree, node):  # 删除指定tag名的所有节点
        for elem in tree.xpath("//" + node):
            elem.getparent().remove(elem)
        return tree

    @staticmethod
    def addnodes(tree, parent_node, child_node, child_text=None):  # 指定tag名的所有节点下增加子节点及text
        for elem in tree.xpath("//" + parent_node):
            child = etree.SubElement(elem, child_node)
            if child_text != None:
                child.text = child_text

    @staticmethod
    def changenodes(
            tree, node_oldtag, node_newtag, node_newtext=None
            ):  # 指定tag名的所有节点改tag及text
        for elem in tree.xpath("//" + node_oldtag):
            elem.tag = node_newtag
            if node_newtext != None:
                elem.text = node_newtext

    @staticmethod
    def tostring(elem):
        return etree.tostring(elem)
