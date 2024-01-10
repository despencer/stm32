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

def getoptions(haldir, boardfile):
    with open("{0}{1}/{2}.board".format(haldir, boards, boardfile)) as fboard:
        jboard = yaml.load(fboard, Loader=yaml.Loader)['board']
    with open("{0}{1}/{2}/{3}.mcu".format(haldir, hal, jboard['cpu']['family'], jboard['cpu']['options'])) as fcpu:
        jcpu = yaml.load(fcpu, Loader=yaml.Loader)
    opt = Options()
    opt.mcu = Options()
    opt.mcu.family = jboard['cpu']['family']
    opt.hal = Options()
    getfrequency(opt, jboard, jcpu)
    return opt

def main():
    parser = argparse.ArgumentParser(description='Generates HAL file')
    parser.add_argument('cfgdir', help='config dir')
    parser.add_argument('haldir', help='hal dir')
    parser.add_argument('dstdir', help='destination dir')
    parser.add_argument('board', help='board name')
    args = parser.parse_args()

    options = getoptions(args.haldir, args.board)
    if options == None:
        return 1
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.haldir + hal))
    for tmpl in templates:
        with open(args.dstdir + '/' + tmpl, mode='w') as target:
            target.write(env.get_template(tmpl+'.jinja').render(options=options))
    return 0

if __name__ == "__main__":
    sys.exit(main())

