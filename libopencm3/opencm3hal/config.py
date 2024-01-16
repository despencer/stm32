import sys
import yaml
import output

hal = "/opencm3hal"
mappers = { 'output':output.Mapper() }
boards = "/boards"

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
    opt.board = boardfile
    opt.mcu = Options()
    opt.mcu.family = jboard['cpu']['family']
    opt.hal = Options()
    opt.hal.resources = []
    opt.hal.resheaders = []
    getfrequency(opt, jboard, jcpu)
    return opt

def readconfig(cfgdir, options):
    with open("{0}/board.config".format(cfgdir)) as fconfig:
        jfconfig = yaml.load(fconfig, Loader=yaml.Loader)
    jconfig = None
    for jboard in jfconfig:
        if jboard['board'] == options.board:
            jconfig = jboard
            break
    if jconfig == None:
        sys.stderr.write("Board not found in confguration\n")
        exit(2)
    cfg = Options()
    cfg.mappers = []
    for jmap in jconfig['mapping']:
        mapper = mappers[jmap['type']]
        mapper.addconfig(jmap, options)
        if mapper not in cfg.mappers:
            cfg.mappers.append(mapper)
    return cfg

def getconfig(cfgdir, options):
    cfg = readconfig(cfgdir, options)
    return cfg