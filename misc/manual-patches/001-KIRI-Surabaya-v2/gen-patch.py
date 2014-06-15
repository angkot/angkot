import csv
import sys

def main():
    tsv = sys.argv[1]
    r = csv.reader(open(tsv), delimiter="\t")

    ops = {
        'RENAME': [],
        'DEACTIVATE': [],
    }
    for line in r:
        n1, i1, n2, i2, a = line
        if a == '':
            continue

        if a == 'Baru v2':
            ops['RENAME'].append((i2, n2))
        elif a == 'Update v2':
            ops['RENAME'].append((i2, n2))
            ops['DEACTIVATE'].append(i1)
        elif a.endswith('kosong'):
            if i1 != '':
                ops['DEACTIVATE'].append(i1)
            if i2 != '':
                ops['DEACTIVATE'].append(i2)
        else:
            raise Error('Unknown action: {}'.format(a))

    print('from angkot.route.models import Transportation as T')
    for i, n in ops['RENAME']:
        nn = n.replace('v2', '')
        print('t = T.objects.get(pk={})'.format(i))
        print('t.number = "{}"'.format(nn))
        print('t.save_as_new_submission()')

    for i in ops['DEACTIVATE']:
        print('t = T.objects.get(pk={})'.format(i))
        print('t.active = False')
        print('t.save_as_new_submission()')

if __name__ == '__main__':
    main()

