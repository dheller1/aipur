import numpy


def main():
    res = numpy.loadtxt('results.txt')
    print(f'Loaded {len(res)/2} results ({len(res)} scores).')

    p1 = res[::2]
    p2 = res[1::2]

    print('Player 1:')
    print(f'Mean:     {numpy.mean(p1)}')
    print(f'Median:   {numpy.median(p1)}')
    print(f'Min/Max:  {min(p1)}, {max(p1)}')
    print(f'Std.dev.: {numpy.std(p1)}')
    print()
    print('Player 2:')
    print(f'Mean:     {numpy.mean(p2)}')
    print(f'Median:   {numpy.median(p2)}')
    print(f'Min/Max:  {min(p2)}, {max(p2)}')
    print(f'Std.dev.: {numpy.std(p2)}')


if __name__ == '__main__':
    main()
