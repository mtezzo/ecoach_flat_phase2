class Peekable(object):
    """
    An iterable that wraps another iterable.  In addition to next(), the
    Peekable supports a peek() method which will effectively call next()
    without advancing the underlying iterator. 
    """
    
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        if hasattr(self.iterable, "__next__"):
            self._nextcallable = self.iterable.__next__
        else:
            self._nextcallable = self.iterable.next
        self._getnext()
    
    def __iter__(self):
        return self
    
    def _getnext(self):
        self._next = None
        self._raised = None
        try:
            self._next = self._nextcallable()
        except Exception, e:
            import sys
            exc_info = sys.exc_info()
            self._raised = exc_info
    
    def next(self):
        if self._raised is not None:
            raise self._raised[0], self._raised[1], self._raised[2]
        next = self._next
        self._getnext()
        return next
    
    def peek(self):
        """
        Return the next item without advancing the underlying iterator.
        Exceptions are raised as necessary.
        """
        if self._raised is not None:
            raise self._raised[0], self._raised[1], self._raised[2]
        return self._next
    

def peekable(iterable):
    return Peekable(iterable)

# Below is a 3.0 compatable version
#
# class Peekable(object):
# 
#     def __init__(self, iterable):
#         self.iterable = iter(iterable)
#         if hasattr(self.iterable, "__next__"):
#             self._nextcallable = self.iterable.__next__
#         else:
#             self._nextcallable = self.iterable.next
#         self._getnext()
# 
#     def __iter__(self):
#         return self
# 
#     def _getnext(self):
#         self._next = None
#         self._raised = None
#         try:
#             self._next = self._nextcallable()
#         except Exception as e:
#             self._raised = e
# 
#     def __next__(self):
#         if self._raised is not None:
#             raise self._raised
#         next = self._next
#         self._getnext()
#         return next
# 
#     def peek(self):
#         if self._raised is not None:
#             raise self._raised
#         return self._next

import unittest

class TestPeekable(unittest.TestCase):

    def failingIterator(self):
        for x in range(2):
            yield x
        raise ValueError("Failed Iterator")

    def setUp(self):
        self.seq = (0, 1, 2, 3, 4)
        self.string = 'She sells sea shells by the seashore.'
        self.generator = (x for x in self.seq)

    def soakUp(self, iter, num):
        """call next on the iterable num times"""
        for _ in range(num):
            iter.next()
            
    def testPeekableFunction(self):
        p = peekable(list())
        self.assert_(isinstance(p, Peekable))
        
    def testSequenceIteration(self):
        p = peekable(self.seq)
        r = p.next()
        self.assertEqual(r, 0)
        r = p.next()
        self.assertEqual(r, 1)
        r = p.next()
        self.assertEqual(r, 2)
        r = p.next()
        self.assertEqual(r, 3)
        r = p.next()
        self.assertEqual(r, 4)
        self.assertRaises(StopIteration, p.next)
        
    def testSequencePeek(self):
        p = peekable(self.seq)
        r1 = p.peek()
        r2 = p.next()
        self.assertEqual(r1, r2)
        r1 = p.peek()
        r2 = p.next()
        self.assertEqual(r1, r2)
        r1 = p.peek()
        r2 = p.peek()
        self.assertEqual(r1, r2)
    
    def testEmptyIterable(self):
        p = peekable(list())
        self.assertRaises(StopIteration, p.peek)
        self.assertRaises(StopIteration, p.next)
        
    def testInIterationException(self):
        p = peekable(self.failingIterator())
        self.soakUp(p, 2)
        self.assertRaises(ValueError, p.peek)
        self.assertRaises(ValueError, p.next)

    def testIterableIntegrity(self):
        original_seq = list(self.seq)
        original_string = list(self.string)
        
        peekable_seq = peekable(self.seq)
        peekable_string = peekable(self.string)
        peekable_gen = peekable(self.generator)
        
        seq = list(peekable_seq)
        string = list(peekable_string)
        gen = list(peekable_gen)
        
        self.assertEqual(original_seq, seq)
        self.assertEqual(original_string, string)
        self.assertEqual(original_seq, gen)
        
    def testConsistantStopIteration(self):
        p = peekable(self.seq)
        _ = list(p) # exhaust the iterable
        self.assertRaises(StopIteration, p.peek)
        self.assertRaises(StopIteration, p.peek)
        self.assertRaises(StopIteration, p.next)
        self.assertRaises(StopIteration, p.next)
    

if __name__ == '__main__':
    unittest.main()