import sys
import os
sys.path.append(os.path.dirname(__file__) + '/comm')
import yaml
import output
import usart
import slpx

hal = "/opencm3hal"
mappers = { 'output':output.Mapper(), 'usart':usart.Mapper() }
protocols = {'SLPX': slpx.Mapper() }
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

def readoptions(jopt):
    if isinstance(jopt, list):
        return list(map(readoptions, jopt))
    if isinstance(jopt, dict):
        ret = Options()
        for k,v in jopt.items():
            setattr(ret, k, readoptions(v))
        return ret
    return jopt

def getoptions(haldir, boardfile):
    ''' Reads a board definition file and a MCU definition file '''
    with open("{0}{1}/{2}.board".format(haldir, boards, boardfile)) as fboard:
        jboard = yaml.load(fboard, Loader=yaml.Loader)['board']
    with open("{0}{1}/{2}/{3}.mcu".format(haldir, hal, jboard['cpu']['family'], jboard['cpu']['options'])) as fcpu:
        jcpu = yaml.load(fcpu, Loader=yaml.Loader)
    opt = Options()
    opt.board = boardfile
    opt.mcu = Options()
    opt.mcu.family = jboard['cpu']['family']
    opt.mcu.pins = {}
    for p in readoptions(jboard['cpu']['pins']):
        opt.mcu.pins[p.name] = p
    opt.hal = Options()
    opt.hal.resources = []
    opt.hal.resheaders = []
    getfrequency(opt, jboard, jcpu)
    return opt

def readconfig(cfgdir, options):
    ''' Reads a project config file over board options '''
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
    if 'mapping' in jconfig:
        for jmap in jconfig['mapping']:
            addmapper(cfg, options, mappers[jmap['type']], jmap)
    if 'protocols' in jconfig:
        for jproto in jconfig['protocols']:
            addmapper(cfg, options, protocols[jproto['type']], jproto)
    return cfg

def addmapper(cfg, options, mapper, jmap):
    mapper.addconfig(jmap, options)
    if mapper not in cfg.mappers:
        cfg.mappers.append(mapper)

def getfunc(mcu, type, index, signal, port, pin):
    if isinstance(pin, int):
        pin = str(pin)
    if (port+pin) not in mcu.pins:
        sys.stderr.write(f"Pin {port+pin} is not found in the board specification\n")
        exit(2)
    for af in mcu.pins[port+pin].altfuncs:
        if af.function.type == type and af.function.index == index and af.function.signal == signal:
            return af.index
    sys.stderr.write(f"Alternate function {type}{index} is not found for pin {name+pin} and signal {signal} in the board specification\n")
    exit(2)

def getconfig(cfgdir, options):
    cfg = readconfig(cfgdir, options)
    return cfg