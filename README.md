<!-- BEGIN_TF_DOCS -->
# Hardware Profile Module Overview

This module collects hardware specifications from the host machine where Terraform is executed. It uses a Python script with standard library modules to gather details such as CPU, memory (including speed if detected), disk usage, GPU (NVIDIA/AMD), and OS information, outputting the results as a JSON object saved to `hardware_profile.json`.

## Purpose
The module provides a reusable way to profile hardware for inventory, monitoring, or configuration purposes in infrastructure-as-code workflows.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.3.0 |
| <a name="requirement_external"></a> [external](#requirement\_external) | >= 2.2.0 |
| <a name="requirement_local"></a> [local](#requirement\_local) | >= 2.4.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_external"></a> [external](#provider\_external) | >= 2.2.0 |
| <a name="provider_local"></a> [local](#provider\_local) | >= 2.4.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [local_file.hardware_output](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file) | resource |
| [external_external.hardware_profile](https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_python_interpreter"></a> [python\_interpreter](#input\_python\_interpreter) | Python interpreter to use (e.g., 'python3') | `string` | `"python3"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_hardware_profile"></a> [hardware\_profile](#output\_hardware\_profile) | Hardware profile information as a flattened JSON object with string values, including CPU (cores, processor, max frequency), memory (total, free, speed if detected), disk (multiple NVMe disks with name, model, total, free, type via /sys/block), GPU (brand, name, VRAM, driver), and system (OS, release, distribution) details |
| <a name="output_profile_file_path"></a> [profile\_file\_path](#output\_profile\_file\_path) | Path to the generated hardware profile JSON file |

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
- If unexpected files (e.g., `project.json`) appear, ensure they are excluded in `.gitignore` or manually removed before committing.

## Resources
- [Terraform External Data Source](https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external)
- [Terraform Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)
<!-- END_TF_DOCS -->