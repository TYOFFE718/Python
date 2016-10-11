import sys
from   collections import defaultdict

#Parse all exchange file and identify which Exbytes contain Tick Type 11 and Tick Type 12(TT_11, TT_12) trade ticks 

if len(sys.argv) != 2:
    print('Usage: {} file'.format(sys.argv[0])) a
    sys.exit(1)

with open(sys.argv[1]) as fh:

    exbyte = ''
    contained_tags = set()
    t_127 = []

    print('TT_11 and TT_12:')
    for line in fh:
        line = line.strip()

        if line.startswith('Exbyte='):

            if exbyte:
                if 'TT_11' in contained_tags and 'TT_12' in contained_tags:
                    print(exbyte)
                    if 'TT_127' in contained_tags:
                        t_127.append(exbyte)
                contained_tags.clear()

            exbyte, ticks = line.split(',', 1)
            exbyte = exbyte.split('=', 1)[-1]
            continue

        if exbyte:
            tag_name, tag_value = line.split('=', 1)
            contained_tags.add(tag_name)

    if contained_tags:
        if 'TT_11' in contained_tags and 'TT_12' in contained_tags:
            print(exbyte)
            if 'TT_127' in contained_tags:
                t_127.append(exbyte)

    if t_127:
        print('TT_11 and TT_12 and TT_127:')
        print('\n'.join(t_127))

