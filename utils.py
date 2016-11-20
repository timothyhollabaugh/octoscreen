def get(obj, indexes, e, debug = False):

    data = obj

    if debug:
        print obj
        print indexes

    for i in indexes:
        if data != None and i in data.keys():
            data = data[i]
        else:
            return e

    if obj != None and data != None:
        return data
    else:
        return e

def time(t):
    if isinstance(t, int) or isinstance(t, float) or isinstance(t, long):
        m, s = divmod(int(t), 60)
        h, m = divmod(m, 60)
    else:
        h, m, s = 0, 0, 0

    return str("%02d:%02d:%02d" % (h, m, s))
