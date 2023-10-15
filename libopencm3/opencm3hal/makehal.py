import jinja2
import argparse
import sys
import yaml

hal = "/opencm3hal"
boards = "/boards"
templates = [ "opencm3hal.h", "opencm3hal.c" ]

class Options:
    pass

def getfrequency(opt, jboard, jcpu):
    for jmode in jcpu['general']['clock']:
        if jmode['external'] == jboard['frequency']['cpu']:
            opt.mcu.frequency = jmode['frequency']
            opt.hal.clock = jmode['hal']
            return
    sys.stderr.write("Frequency not found\n")
    exit(2)

def getoptions(srcdir, boardfile):
    with open("{0}{1}/{2}.board".format(srcdir, boards, boardfile)) as fboard:
        jboard = yaml.load(fboard, Loader=yaml.Loader)['board']
    with open("{0}{1}/{2}/{3}.mcu".format(srcdir, hal, jboard['cpu']['family'], jboard['cpu']['options'])) as fcpu:
        jcpu = yaml.load(fcpu, Loader=yaml.Loader)
    opt = Options()
    opt.mcu = Options()
    opt.hal = Options()
    getfrequency(opt, jboard, jcpu)
    return opt

def main():
    parser = argparse.ArgumentParser(description='Generates HAL file')
    parser.add_argument('srcdir', help='source dir')
    parser.add_argument('dstdir', help='destination dir')
    parser.add_argument('board', help='board yaml')
    args = parser.parse_args()

    options = getoptions(args.srcdir, args.board)
    if options == None:
        return 1
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.srcdir + hal))
    for tmpl in templates:
        with open(args.dstdir + '/' + tmpl, mode='w') as target:
            target.write(env.get_template(tmpl+'.jinja').render(options=options))
    return 0

if __name__ == "__main__":
    sys.exit(main())

