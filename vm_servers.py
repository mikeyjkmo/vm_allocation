from dataclasses import dataclass


class PhysicalServer:
    def __init__(
        self,
        available_cores: int,
        available_memory_mb: int,
        available_network_bandwidth_kbps: int,
    ):
        self._available_cores = available_cores
        self._available_memory_mb = available_cores
        self._available_network_bandwidth_kbps = available_network_bandwidth_kbps
        self._remaining_cores = available_cores
        self._remaining_memory_mb = available_cores
        self._remaining_network_bandwidth_kbps = available_network_bandwidth_kbps

    def can_allocate(self, vm: "VM"):
        return True


@dataclass
class VM:
    required_cores: int
    required_memory_mb: int
    required_network_bandwidth_kbps: int


class ResourceAllocator:
    def __init__(self):
        self._available_servers = []

    def add_physical_server(self, physical_server: PhysicalServer):
        self._available_servers.append(physical_server)
