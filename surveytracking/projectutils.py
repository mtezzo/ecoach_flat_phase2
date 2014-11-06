class InvalidDataError(Exception):
    def __init__(self, key, value, type):
        self.key = key
        self.value = value
        self.type = type
    
    def __str__(self):
        return "The value %(value)s cannot be coerced to " \
            "type %(key)s (%(type)s)" % self.__dict__

def flat_dependency_map(dictionary):
    def desourceify(dependencyname):
        try:
            source, dependencyname = dependencyname.split('.', 1)
            if source not in dictionary.source_index:
                return source
            else:
                dependencyname, rest = dependencyname.split('.', 1)
                if dependencyname not in dictionary.char_index:
                    return '%s.%s' % (dependencyname, rest)
        except ValueError:
            pass
        return dependencyname
    my_map = {}
    for chardef in dictionary.all_chars_topo:
        deps = set()
        if chardef.is_derived:
            deplist = chardef.derivedcalc.dependencies
            for dep in deplist:
                dep = desourceify(dep)
                if dep in my_map and len(my_map[dep]) > 0:
                    deps.update(my_map[dep])
                else:
                    deps.add(dep)
        my_map[chardef.name] = deps
    return my_map

def coerce_data_to_dictionary_types(data, dictionary):
    delete = []
    for key in data:
        cdef = dictionary.char_index.get(key)
        val = data[key]
        if cdef is not None:
            val = cdef.basetype_normalize(val)
            if not isinstance(val, cdef.basetype.pytype):
                delete.append(key)
            else:
                data[key] = val
    for key in delete:
        del data[key]

def data_to_dictionary_types(data, dictionary):
    newdata = {}
    for key in data:
        cdef = dictionary.char_index.get(key)
        if cdef is not None:
            val = data[key]
            if cdef.is_multivalued and not isinstance(val, (list, tuple, set)):
                if val is None:
                    val = []
                else:
                    val = [val]
            val = cdef.basetype_normalize(val)
            if val is None:
                newdata[key] = val
            elif isinstance(val, cdef.basetype.pytype):
                newdata[key] = val
            elif ( cdef.is_multivalued
                and len([v for v in val 
                         if isinstance(v, cdef.basetype.pytype)]) == len(val) ):
                newdata[key] = val
            elif val is not None and val != "":
                raise InvalidDataError(key, val, cdef.basetype.pytype)
    return newdata