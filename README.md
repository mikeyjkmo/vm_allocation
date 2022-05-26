# VM Server Allocation

This is basic CLI for allocating VMs to physical servers. It uses “best fit”
approximation algorithm to compute the required amount of physical servers and
the allocation of virtual machines to physical servers.

## Requirements

- Python3.9+
- Python Poetry

## Installation

```bash
> poetry install
```

## Run

```bash
> poetry run python vm_servers.py <required_cores> <required_memory_mb> <required_network_bandwidth_kbps>
```

## Limitations

- PhysicalServers are hardcoded
- Allocations are not persisted between runs, so CLI is not particularly useful in the current state.

## Future Improvements

- Allow physical servers to be added/removed via the CLI
- Persist state between runs
- Allow VMs to be deallocated
