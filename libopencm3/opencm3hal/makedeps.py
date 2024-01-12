import argparse
import sys
import yaml
import config

def main():
    parser = argparse.ArgumentParser(description='Generates list of HAL files')
    parser.add_argument('cfgdir', help='config dir')
    parser.add_argument('haldir', help='hal dir')
    parser.add_argument('board', help='board name')
    args = parser.parse_args()

    options = config.getoptions(args.haldir, args.board)
    if options == None:
        return 1
    cfg = config.readconfig(args.cfgdir, options)
    templates = []
    for mapper in cfg.mappers:
       templates.extend(mapper.templates)
    templates = map(lambda x: args.haldir + config.hal + '/' + x +'.jinja', templates)
    sys.stdout.write(';'.join(templates))
    return 0

if __name__ == "__main__":
    sys.exit(main())
