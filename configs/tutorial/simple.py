import m5
from m5.objects import *

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

# Create overall system memory bus
system.membus = SystemXBar()

# Connect CPU cache port
# In this case, there are no cache on simulation system,
# connect I-cache and D-cache directly on membus
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

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


