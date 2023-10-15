import jinja2
import argparse
import sys
import yaml

hal = "/opencm3hal"
boards = "/boards"
templates = [ "opencm3hal.h" ]

class Options:
    pass

def getoptions(srcdir, optfile):
#    with open(srcdir + '/settings.yaml') as fset:
#        jset = yaml.load(fset, Loader=yaml.Loader)
#    with open(srcdir + '/' + optfile) as fopt:
#        jopt = yaml.load(fopt, Loader=yaml.Loader)
    opt = Options()
    opt.mcu = Options()
    opt.mcu.frequency = 54000
#    opt.greeting = jset['greeting'][jopt['greeting']]
    return opt

def main():
    parser = argparse.ArgumentParser(description='Generates greetings file')
    parser.add_argument('srcdir', help='source dir')
    parser.add_argument('dstdir', help='destination dir')
    parser.add_argument('board', help='board yaml')
    args = parser.parse_args()

    options = getoptions(args.srcdir, args.board)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.srcdir + hal))
    for tmpl in templates:
        with open(args.dstdir + '/' + tmpl, mode='w') as target:
            target.write(env.get_template(tmpl+'.jinja').render(options=options))
    return 0

if __name__ == "__main__":
    sys.exit(main())

