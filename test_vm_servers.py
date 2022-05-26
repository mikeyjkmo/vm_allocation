from vm_servers import VM, PhysicalServer


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
