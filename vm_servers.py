from dataclasses import dataclass
import typer


class PhysicalServer:
    def __init__(
        self,
        name: str,
        available_cores: int,
        available_memory_mb: int,
        available_network_bandwidth_kbps: int,
    ):
        self.name = name
        self._available_cores = available_cores
        self._available_memory_mb = available_memory_mb
        self._available_network_bandwidth_kbps = available_network_bandwidth_kbps
        self._remaining_cores = available_cores
        self._remaining_memory_mb = available_memory_mb
        self._remaining_network_bandwidth_kbps = available_network_bandwidth_kbps
        self.allocated_vms = []

    def can_allocate(self, vm: "VM"):
        if self._available_cores < vm.required_cores:
            return False
        if self._available_memory_mb < vm.required_memory_mb:
            return False
        if self._available_network_bandwidth_kbps < vm.required_network_bandwidth_kbps:
            return False

        return True

    def allocate(self, vm: "VM"):
        if not self.can_allocate(vm):
            raise ValueError("VM cannot be allocated due to insufficient resource")

        self._available_cores -= vm.required_cores
        self._available_memory_mb -= vm.required_memory_mb
        self._available_network_bandwidth_kbps -= vm.required_network_bandwidth_kbps
        self.allocated_vms.append(vm)

    def post_allocated_capacity(self, vm: "VM"):
        """
        Get the capacity of this physical server if it were to allocate this VM
        """
        return sum((
            self._available_cores - vm.required_cores,
            self._available_memory_mb - vm.required_memory_mb,
            self._available_network_bandwidth_kbps - vm.required_network_bandwidth_kbps,
        ))


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

    def allocate(self, vm: VM):
        """
        Allocate VM on the most appropriate PhysicalServer using
        "best-fit" approximation algorithm
        """
        min_post_allocated_capacity = float('inf')
        most_suitable_ps = None

        for ps in self._available_servers:
            if ps.can_allocate(vm):
                if ps.post_allocated_capacity(vm) < min_post_allocated_capacity:
                    most_suitable_ps = ps
                    min_post_allocated_capacity = ps.post_allocated_capacity(vm)

        if not most_suitable_ps:
            raise ValueError("No suitable physical server can host this VM")

        most_suitable_ps.allocate(vm)
        return most_suitable_ps


def main():
    app = typer.Typer()

    allocator = ResourceAllocator()

    ps = PhysicalServer(
        name="one",
        available_cores=4,
        available_memory_mb=2048,
        available_network_bandwidth_kbps=2048,
    )
    allocator.add_physical_server(ps)
    ps2 = PhysicalServer(
        name="two",
        available_cores=5,
        available_memory_mb=2048,
        available_network_bandwidth_kbps=2048,
    )
    allocator.add_physical_server(ps2)
    ps3 = PhysicalServer(
        name="three",
        available_cores=3,
        available_memory_mb=2048,
        available_network_bandwidth_kbps=2048,
    )
    allocator.add_physical_server(ps3)

    @app.command()
    def allocate(
        required_cores: int,
        required_memory_mb: int,
        required_network_bandwidth_kbps: int,
    ):
        new_vm = VM(
            required_cores=required_cores,
            required_memory_mb=required_memory_mb,
            required_network_bandwidth_kbps=required_network_bandwidth_kbps
        )
        ps = allocator.allocate(new_vm)
        typer.echo(f"Successfully allocated on PhysicalServer: {ps.name}")

    app()


if __name__ == "__main__":
    main()
