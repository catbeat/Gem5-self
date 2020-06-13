from m5.objects import Cache

class L1Cache(Cache):
    assoc = 2                       # 2-way set associate
    tag_latency = 2                 # latency for access tag
    data_latency = 2                # latency for access data
    response_latency = 2            # latency for access data when miss
    mshrs = 4                       # number of max outstanding request
    tgts_per_mshr = 20              # max number of access per outstanding request

    def __init__(self, options = None):
        super(L1Cache, self).__init__()
        pass

    def connectCPU(self, cpu):
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.slave


class L1DCache(L1Cache):
    size = '64kB'                   # set default size

    def __init__(self, options = None):
        super(L1DCache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

class L1ICache(L1Cache):
    size = '16kB'                   # set default size

    def __init__(self, options = None):
        super(L1ICache, self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port


class L2Cache(Cache):
    assoc = 8                       # 8-way set associate
    tag_latency = 20                # latency for access tag
    data_latency = 20               # latency for access data
    response_latency = 20           # latency for access data when miss
    mshrs = 20                      # number of max outstanding request
    tgts_per_mshr = 12              # max number of access per outstanding request

    size = '256kB'

    def __init__(self, options = None):
        super(L2Cache, self).__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size

    def connectCpuSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave
