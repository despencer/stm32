import jinja2
import argparse
import sys
import config

templates = [ "opencm3hal.h", "opencm3haldef.h", "opencm3hal.c", "opencm3res.c" ]

def main():
    parser = argparse.ArgumentParser(description='Generates HAL file')
    parser.add_argument('cfgdir', help='config dir')
    parser.add_argument('haldir', help='hal dir')
    parser.add_argument('dstdir', help='destination dir')
    parser.add_argument('board', help='board name')
    args = parser.parse_args()

    options = config.getoptions(args.haldir, args.board)
    if options == None:
        return 1
    cfg = config.getconfig(args.cfgdir, options)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.haldir + config.hal))
    for tmpl in templates:
        with open(args.dstdir + '/' + tmpl, mode='w') as target:
            target.write(env.get_template(tmpl+'.jinja').render(options=options, config=cfg))
    for mapper in cfg.mappers:
        for tmpl in mapper.templates:
            with open(args.dstdir + '/' + tmpl, mode='w') as target:
               target.write(env.get_template(tmpl+'.jinja').render(config=mapper))
    return 0

if __name__ == "__main__":
    sys.exit(main())

