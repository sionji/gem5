from m5.objects import Cache

# Make L1 cache
class L1Cache(Cache) :
  assoc = 2
  tag_latency = 2
  data_latency = 2
  response_latency = 2
  mshrs = 4
  tgts_per_mshr = 20

  def __init__(self, options=None):
    super(L1Cache, self).__init__()
    pass

  def connectCPU(self, cpu):
    raise NotImplementedError

  def connectBus(self, bus):
    self.mem_side = bus.slave

# L1Dcache and L1ICache
class L1ICache(L1Cache):
  size = '16kB'

  def __init__(self, options=None):
    super(L1ICache, self).__init__(options)
    if not options or not options.l1i_size:
      return
    self.size = options.l1i_size

  def connectCPU(self, cpu):
    self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
  size = '64kB'

  def __init__(self, options=None):
    super(L1DCache, self).__init__(options)
    if not options or not options.l1d_size:
      return
    self.size = options.l1d_size

  def connectCPU(self, cpu):
    self.cpu_side = cpu.dcache_port

# Make L2 cache using reasonable parameter
class L2Cache(Cache):
  size = '256kB'
  assoc = 8
  tag_latency = 20
  data_latency = 20
  response_latency = 20
  mshrs = 20
  tgts_per_mshr = 12

  def __init__(self, options=None):
    super(L2Cache, self).__init__()
    if not options or not options.l2_size:
      return
    self.size = options.l2_size

  def connectCPUSideBus(self, bus):
    self.cpu_side = bus.master

  def connectMemSideBus(self, bus):
    self.mem_side = bus.slave

# Now that we have specified all of the
# necessary parameters required for BaseCahce,
# all we have to do is instantiate our subclass
# and connect the caches to the interconnect.

# However, connecting lots of objects up to complex
# interconnections can make configureation files quickly
# grows and becomes unreadable.

# Therefore, let's first add some helper functions to our
# sub-classes of Cache.
