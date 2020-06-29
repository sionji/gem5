import m5
from m5.objects import *
from caches import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--l1i_size', help="L1 instruction cache size")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l2_size', help="Unified L2 cache size")

(options, args) = parser.parse_args()

# Create first SimObject
system = System()  # Now we have system reference.

# Create a clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set simulation mode
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Now we can make CPU
system.cpu = TimingSimpleCPU()

# Create cpus
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

# Connect cache to CPU port
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# To connect L1 cache to L2 cache, we make L2 bus first
# We can connect L1 to L2 using helper.
system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Next, we can make L2 cache and connect it to bus and memory
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

# Create overall system memory bus
system.membus = SystemXBar()

system.l2cache.connectMemSideBus(system.membus)

# Connect other ports
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# Make memory controller and connect it to membus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Create process (another SimObject)
process = Process ()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

# Instance system and execute
root = Root(full_system = False, system = system)
m5.instantiate()

# Now we can run real simulation!
print("Beginning simulation!")
exit_event = m5.simulate()

print('Existing @ tick {} because {}'
                  .format(m5.curTick(), exit_event.getCause()))


