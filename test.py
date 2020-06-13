import m5
from m5.objects import *
from caches import *
from optparse import OptionParser

# let the user input the configuration for the system
parser = OptionParser()
parser.add_option('--l1i_size', help = 'L1 instruction cache size')
parser.add_option('--l1d_size', help = 'L1 data cache size')
parser.add_option('--l2_size', help = 'L2 cache size')

(options, args) = parser.parse_args()

system = System()

# setting clock

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# setting main memory

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# setting timing CPU

system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()

# setting cache

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()                     # create bus to connect L1 and L2
system.cpu.icache.connectBus(system.l2bus)         # connect L1 to bus
system.cpu.dcache.connectBus(system.l2bus)         

system.l2cache = L2Cache(options)                          # create L2 cache
system.l2cache.connectCpuSideBus(system.l2bus)      # connect L2 to l2 bus
system.l2cache.connectMemSideBus(system.membus)     # connect L2 to bus to memory

# setting necessary port

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# setting memory controller

system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# giving a test process

process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print ('Beginning simulation!')
exit_event = m5.simulate()

print ('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
