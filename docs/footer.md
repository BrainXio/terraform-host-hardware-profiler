## Additional Notes

- Requires Python 3.x on the host; no external Python libraries are used.
- The module supports Linux, Windows, and macOS hosts. Memory size uses `/proc/meminfo` (Linux) or defaults to 'unknown' elsewhere. CPU info uses `/proc/cpuinfo` or `dmidecode` (Linux) or platform data.
- Adjust `python_interpreter` if the Python 3 executable has a different name (e.g., `python`).
- The JSON output is a flattened map with string values to comply with Terraform's `external` data source requirements (e.g., `{"cpu_processor": "x86_64", "cpu_max_frequency_ghz": "4.6", "memory_total_mb": "31817", "memory_free_mb": "20415", "memory_speed_mhz": "3200", "disk_0_name": "nvme0n1", "disk_0_model": "Samsung SSD 980 500GB", "disk_0_total_gb": "465", "disk_0_free_gb": "200", "disk_0_type": "SSD", "disk_1_name": "nvme1n1", "disk_1_model": "SAMSUNG MZVL21T0HCLR-00BL2", "disk_1_total_gb": "953", "disk_1_free_gb": "282", "disk_1_type": "SSD", "gpu_brand": "NVIDIA", "gpu_name": "GeForce RTX 3070 Laptop GPU", "gpu_vram_mb": "8192", "gpu_driver_version": "550.144.03", "os_distribution": "Ubuntu 24.04.2 LTS"}`).
- Memory speed (`memory_speed_mhz`) is included only if detected via `dmidecode`, `hwinfo`, `lscpu`, or `/sys/devices` (Linux), `wmic` or PowerShell (Windows), or `system_profiler` or `ioreg` (macOS). Requires `hwinfo` installation for Linux (optional), sudo for `dmidecode`, or appropriate permissions. If undetected, the field is omitted.
- GPU detection requires `nvidia-smi` for NVIDIA GPUs or `rocm-smi` for AMD GPUs (Linux). If unavailable, GPU fields return 'none' or 'unknown'.
- Disk detection requires `lsblk` (Linux) and reads `/sys/block/<device>/queue/rotational` for type; NVMe disks are assumed SSDs unless proven otherwise. Non-Linux systems may return 'unknown' for disk details.
- OS distribution requires `lsb_release` or `/etc/os-release` (Linux); CPU max frequency may require `/sys/devices`, `/proc/cpuinfo`, or `dmidecode`. Unavailable fields default to 'unknown'.
- Generate documentation with `make docs`, which runs `terraform-docs` with headers and footers from `docs/`.
- CI/CD is handled by GitHub Actions workflows (`.github/workflows/lint.yml` for linting and `.github/workflows/validate.yml` for validation).
- See `examples/simple/README.md` for a basic usage example of the module.
- If unexpected files (e.g., `project.json`) appear, ensure they are excluded in `.gitignore` or manually removed before committing.

## Resources
- [Terraform External Data Source](https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external)
- [Terraform Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)
