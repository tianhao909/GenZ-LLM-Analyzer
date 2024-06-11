import numpy as np
import math
from src.unit import Unit
class System(object):
    compute_multiplier = {'int8': 0.5, 'bf16': 1, 'f32': 2, 'int4': 0.25, 'int2':0.125, 'fp8': 0.5, 'fp4': 0.25}
    mem_multiplier = {'int8': 1, 'bf16': 2, 'f32': 4, 'int4':0.5, 'int2':0.25, 'fp8':1, 'fp4':0.5}
    def __init__(self, unit=None, onchip_mem_bw=18000, offchip_mem_bw=900, external_mem_bw=100, 
                 on_chip_mem_size=float('Inf'), off_chip_mem_size=float('Inf'),
                 compute_efficiency=1, memory_efficiency=1, flops=123, mxu_shape=None,
                 frequency=940, bits='bf16', interchip_mem_bw = 25, num_cores = 1, interchip_link_latency=1.9):
        
        if unit is None:
            self.unit = Unit()
        else:
            self.unit = unit
        self.onchip_mem_bw = self.unit.unit_to_raw(onchip_mem_bw, type='BW')
        self.offchip_mem_bw = self.unit.unit_to_raw(offchip_mem_bw, type='BW')
        self.interchip_mem_bw = self.unit.unit_to_raw(interchip_mem_bw, type='BW')
        self.interchip_link_latency = interchip_link_latency * 1e-6     ## us
        self.external_mem_bw = self.unit.unit_to_raw(external_mem_bw, type='BW')
        self.on_chip_mem_size = self.unit.unit_to_raw(on_chip_mem_size, type='M')
        self.on_chip_mem_left_size = self.unit.unit_to_raw(on_chip_mem_size, type='M')
        self.off_chip_mem_size = self.unit.unit_to_raw(off_chip_mem_size, type='M')
        self.compute_efficiency = compute_efficiency
        self.memory_efficiency = memory_efficiency
        self.mxu_shape = mxu_shape
        self.num_cores = num_cores

        self.flops = self.unit.unit_to_raw(flops, type='C')
        self.op_per_sec = self.flops/2
        
        self.frequency = self.unit.unit_to_raw(frequency, type='F')
        self.bits = bits

    
    def __str__(self):
        unit = Unit()
        a = f"Accelerator OPS: {unit.raw_to_unit(self.flops,type='C')} TOPS , Freq = {unit.raw_to_unit(self.frequency,type='F')} GHz, Num Cores = {self.num_cores} \n"
        b = f"On-Chip mem size: {unit.raw_to_unit(self.on_chip_mem_size, type='M')} MB , Off-chip mem size:{unit.raw_to_unit(self.off_chip_mem_size, type='M')} MB\n"
        c = f"On-Chip mem BW: {unit.raw_to_unit(self.onchip_mem_bw, type='BW')} GB/s , Off-chip mem BW:{unit.raw_to_unit(self.offchip_mem_bw, type='BW')} GB/s, External-mem BW:{unit.raw_to_unit(self.external_mem_bw, type='BW')} GB/s,\n"
        d = f"Compute type: {self.compute_type} , Realistic mem type: {self.model_on_chip_mem_implications}\n"
        e = f"Sparsity Params: Acc. type: {self.accelerator_type} , Skip compute: {self.skip_compute} , Compress mem: {self.compress_mem}"
        return a+b+c+d+e
    
    def get_params(self):
        unit = Unit()
        a = f"Accelerator OPS: {unit.raw_to_unit(self.flops,type='C')} TOPS , Freq = {unit.raw_to_unit(self.frequency,type='F')} GHz, Num Cores = {self.num_cores}"
        b = f" Off-chip mem size:{unit.raw_to_unit(self.off_chip_mem_size, type='M')/1024} GB "
        c = f" Off-chip mem BW:{unit.raw_to_unit(self.offchip_mem_bw, type='BW')} GB/s, External-mem BW:{unit.raw_to_unit(self.external_mem_bw, type='BW')} GB/s"
        return a+b+c

    def set_pe_min_density_support(self,pe_min_density_support):
        if(self.accelerator_type=="structured" or pe_min_density_support==1):
            self.treat_as_dense = True
            self.pe_min_density_support = pe_min_density_support
        elif(self.accelerator_type=="unstructured"):
            self.pe_min_density_support = 0.000001
            self.treat_as_dense = False

    def set_onchip_mem_bw(self,onchip_mem_bw):
        self.onchip_mem_bw = self.unit.unit_to_raw(onchip_mem_bw, type='BW')

    def set_offchip_mem_bw(self,offchip_mem_bw):
        self.offchip_mem_bw = self.unit.unit_to_raw(offchip_mem_bw, type='BW')

    def get_offchip_mem_bw(self):
        return self.unit.raw_to_unit(self.offchip_mem_bw,type='BW')

    def get_external_mem_bw(self):
        return self.unit.raw_to_unit(self.external_mem_bw,type='BW')

    def get_interchip_mem_bw(self):
        return self.unit.raw_to_unit(self.interchip_mem_bw,type='BW')

    def get_off_chip_mem_size(self):
        return self.unit.raw_to_unit(self.off_chip_mem_size,type='M')


    def claim_onchip_mem(self, data_sz):
        if data_sz > self.on_chip_mem_left_size:
            raise ValueError(f'Not enough on-chip memory: Need {data_sz}, only has {self.on_chip_mem_size}')
        self.on_chip_mem_left_size -= data_sz
        return self.on_chip_mem_left_size

    def release_onchip_mem(self, data_sz):
        self.on_chip_mem_left_size = max(self.on_chip_mem_size, data_sz + self.on_chip_mem_left_size)
        return self.on_chip_mem_left_size

    def get_bit_multiplier(self, type='C', data='a'):
        if self.bits == 'special':
            if data == 'w':
                return 3/8
            else:
                return 2
        if type == 'C':
            return self.compute_multiplier[self.bits]
        elif type == 'M':
            return self.mem_multiplier[self.bits]
        
    