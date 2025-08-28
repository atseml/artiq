from migen import *
from misoc.interconnect.csr_eventmanager import *


class EEMPowerControl(Module, AutoCSR):
    def __init__(self, power_en, fault_n):
        # allow software enable only when no fault has ever happened
        self._power_en = CSR()
        never_faulted = Signal(reset=1)
        self.sync += If(~fault_n, never_faulted.eq(0))
        self.comb += power_en.eq(self._power_en.w & never_faulted)

        # trigger event on fault
        self.submodules.ev = EventManager()
        self.ev.fault = EventSourceLevel()
        self.ev.finalize()
        self.sync += self.ev.fault.trigger.eq(~fault_n)
