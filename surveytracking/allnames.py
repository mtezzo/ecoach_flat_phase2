from peekable import peekable
from keyword import iskeyword
import tokenize
from StringIO import StringIO

_COMMON_NAMES = frozenset(('intersection', 'containsOnly', 'isEmpty', 'None'))

def filtered(names):
    for name in _COMMON_NAMES:
        names.discard(name)
    return names

def joined_dotted(names):
    names = peekable(names)
    temp = []
    for name in names:
        try:
            peek = names.peek()
        except StopIteration:
            peek = None
        if peek == '.':
            temp.append(name)
            names.next() # soak up the dot op
            continue
        if temp:
            temp.append(name)
            yield '.'.join(temp)
            temp = []
            continue
        yield name
    if temp:
        yield '.'.join(temp)

def tokenized_get_names(expression):
    namegen = (t for t in tokenize.generate_tokens(iter(StringIO(expression)).next))
    namegen = (t for t in namegen if t[0] == tokenize.NAME or ( t[0] == tokenize.OP and t[1] == '.'))
    namegen = (t[1] for t in namegen)
    namegen = (name for name in namegen if not iskeyword(name))
    return namegen    

def get_names(expression):
    return filtered(set(joined_dotted(tokenized_get_names(expression))))

def main():
    import time
    t = time.time()
    print get_names("Gender == 'Male'"), time.time() - t
    t = time.time()
    print get_names("Bob.Hope is Dead"), time.time() - t
    t = time.time()
    print get_names('GS01.FrGoalSet==0 and intersection(FrSupHL, ["Some", "Alot"])'), time.time() - t

if __name__ == '__main__':
    main()