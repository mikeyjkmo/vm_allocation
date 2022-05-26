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
