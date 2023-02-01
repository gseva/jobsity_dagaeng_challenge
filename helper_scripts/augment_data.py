
import sys


def repeat_file(input_file, output_file, n):
    with open(input_file) as f:
        header = next(f)
        s = f.read()
        with open(output_file, 'w') as output:
            output.write(header)
            for _ in range(n):
                output.write(s)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('This script creates a csv file by repeating the contents of a given csv file N times')
        print('Parameters are: input file, output filename, number of iterations')
        print('Example usage: python augment_data.py trips.csv output.csv 100000')
    else:
        repeat_file(sys.argv[1], sys.argv[2], int(sys.argv[3]))
