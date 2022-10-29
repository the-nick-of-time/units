import argparse

from pyunitx.resistance import from_color


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tolerance", action="store_true")
    parser.add_argument("-s", "--sensitivity", action="store_true")
    parser.add_argument("spec")
    return parser.parse_args()


def main():
    args = parse_args()
    values = from_color(args.spec, args.tolerance, args.sensitivity)
    if args.sensitivity:
        print(
            f"{values[0].to_natural_si()} + {values[2].value} Ω/K ± {values[1].to_natural_si()}"
        )
    elif args.tolerance:
        print(f"{values[0].to_natural_si()} ± {values[1].to_natural_si()}")
    else:
        print(values.to_natural_si())


if __name__ == '__main__':
    main()
