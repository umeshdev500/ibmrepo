#!/usr/bin/env python
# coding: utf-8

import math
import re
import inspect

calc_operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    '**': lambda x, y: x ** y,
    '//': lambda x, y: x // y,
    'pow': lambda x, y: x ** y,
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'tan': lambda x: math.tan(x),
    'asin': lambda x: math.asin(x),
    'acos': lambda x: math.acos(x),
    'atan': lambda x: math.atan(x),
    'sqrt': lambda x: math.sqrt(x),
    'floor': lambda x: math.floor(x),
    'ceil': lambda x: math.ceil(x),
    'abs': lambda x: abs(x),
    'round': lambda x: round(x),
}


def get_num_args(func):
    try:
        sp = inspect.getargspec(func)
    except TypeError:
        return None
    else:
        return len(sp.args)


class Calculator:
    
    rnum = re.compile(r'^[-+]?\d+(?:\.\d+)?(?:[-+]?[eE]\d+)?$', re.M)
    
    def __init__(self):
        self.stack = [0.0]
    
    def isnum(self, val):
        return not not self.rnum.match(val)
    
    def push(self, val):
        self.stack.append(float(val))
        return self
    
    def pop(self):
        last = self.last()
        self.stack = self.stack[:-1]
        return last
    
    def calc(self, terms):
        if not isinstance(terms, basestring):
            term = str(terms)
        terms = terms.split()
        for term in terms:
            if self.isnum(term):
                self.push(term)
            elif term in calc_operators:
                self.operate(term)
            else:
                raise ValueError('operator \'{}\' is not defined.'.format(term))
        return self
    
    def operate(self, operator):
        func = calc_operators[operator]
        n = get_num_args(func)
        if n:
            args = []
            for i in xrange(n):
                args.append(self.pop())
            args.reverse()
            result = func(*args)
            self.push(result)
        return self
    
    def last(self):
        if len(self.stack) == 0:
            self.stack.append(0.0)
        return self.stack[-1]
    
    def clear(self):
        self.stack = [0.0]
        return self
    
    def reverse(self):
        v1 = self.pop()
        v2 = self.pop()
        self.push(v1).push(v2)


commands = {
    'C': lambda c: c.clear(),
    'R': lambda c: c.reverse(),
    'D': lambda c: c.pop()
}


def quit_message():
    print 'bye!'


def show_stacks(c):
    stack = c.stack
    L = len(stack)
    for i in xrange(L):
        print '[{}] {}'.format(L - i - 1, stack[i])


def main():
    c = Calculator()
    while True:
        try:
            i = raw_input('> ')
        except (EOFError, KeyboardInterrupt):
            print
            quit_message()
            break
        if i:
            i = i.strip()
            i_ = i.upper()
            if i_ in commands:
                commands[i_](c)
                print '=>', c.last()
            elif i_ in ('Q', 'QUIT'):
                quit_message()
                break
            elif i_ in ('L', 'LS'):
                show_stacks(c)
            else:
                try:
                    c.calc(i)
                except BaseException:
                    print 'ERROR!'
                finally:
                    print '=>', c.last()
            print


if __name__ == '__main__':
    main()
