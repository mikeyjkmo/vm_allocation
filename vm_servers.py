from dataclasses import dataclass


@dataclass
class PhysicalServer:
    available_cores: int
    available_memory_mb: int
    available_network_bandwidth_kbps: int
    remaining_cores: int
    remaining_memory_mb: int
    remaining_network_bandwidth_kbps: int


@dataclass
class VMSpecification:
    required_cores: int
    required_memory_mb: int
    required_network_bandwidth_kbps: int


class ResourceAllocator:
    def __init__(self):
        self._available_servers = []

    def add_physical_server(self, physical_server: PhysicalServer):
        self._available_servers.append(physical_server)
