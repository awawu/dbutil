# -*- coding: utf-8 -*-

import re
import sqlalchemy

class AbstractCreator(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, connect_args):
        self.connect_args = connect_args
        self.session

    def update(self, new_objects):
        if isinstance(new_objects, (list, tuple)):
            self.session.add_all(new_objects)
        else:
            self.session.add(new_objects)

        self.commit()

    def delete(self, objects):
        if isinstance(objects, (list, tuple)):
            for obj in objects:
                self.session.delete(obj)
        else:
            self.session.delete(objects)
    def roolback(self):
        self.session.roolback()

    def query(self, cols, options, orders, lines = None):
        replace_sub = re.compile(', $')
        
        if isinstance(cols, (list, tuple)):
            queryer = 'self.session.query('
            for col in cols:
                queryer = '{}{}, '.format(queryer, col)    
            queryer = replace_sub.sub(', ', queryer)
        elif cols:
            queryer = 'self.session.query({})'.format(cols.__str__)
        else:
            return []

        if isinstance(options, (list, tuple)):
            queryer = '{}.filter('.format(queryer)
            for opt in options:
                queryer = '{}{}, '.format(queryer, opt)
            queryer = replace_sub.sub(', ', queryer)
        elif options:
            queryer = '{}.filter({})'.format(queryer, options.__str__)
                
