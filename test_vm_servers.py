import pytest
from vm_servers import VM, PhysicalServer, ResourceAllocator


class TestPhysicalServer:
    def test_can_fit_vm(self):
        # Given
        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        vm = VM(
            required_cores=1,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )

        # When
        result = ps.can_allocate(vm)

        # Then
        assert result

    def test_cannot_fit_vm_due_to_lack_of_cores(self):
        # Given
        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        vm = VM(
            required_cores=5,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )

        # When
        result = ps.can_allocate(vm)

        # Then
        assert not result

    def test_cannot_fit_vm_due_to_lack_of_memory(self):
        # Given
        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=128,
            available_network_bandwidth_kbps=2048,
        )
        vm = VM(
            required_cores=4,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )

        # When
        result = ps.can_allocate(vm)

        # Then
        assert not result

    def test_cannot_fit_vm_due_to_lack_of_bandwidth(self):
        # Given
        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=128,
            available_network_bandwidth_kbps=64,
        )
        vm = VM(
            required_cores=4,
            required_memory_mb=128,
            required_network_bandwidth_kbps=128,
        )

        # When
        result = ps.can_allocate(vm)

        # Then
        assert not result

    def test_allocate_success(self):
        # Given
        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        vm = VM(
            required_cores=1,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )

        # When
        ps.allocate(vm)

        # Then

    def test_allocate_failed(self):
        # Given
        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        vm = VM(
            required_cores=10,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )

        # When, Then
        with pytest.raises(ValueError):
            ps.allocate(vm)


class TestResourceAllocator:
    def test_allocate_on_first_server(self):
        allocator = ResourceAllocator()

        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        allocator.add_physical_server(ps)

        vm = VM(
            required_cores=1,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )

        result = allocator.allocate(vm)

        assert result is ps

    def test_allocate_on_first_available_server(self):
        allocator = ResourceAllocator()

        ps = PhysicalServer(
            available_cores=4,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        allocator.add_physical_server(ps)
        ps_large = PhysicalServer(
            available_cores=10,
            available_memory_mb=2048,
            available_network_bandwidth_kbps=2048,
        )
        allocator.add_physical_server(ps_large)

        vm = VM(
            required_cores=5,
            required_memory_mb=256,
            required_network_bandwidth_kbps=128,
        )
        result = allocator.allocate(vm)

        assert result is ps_large
