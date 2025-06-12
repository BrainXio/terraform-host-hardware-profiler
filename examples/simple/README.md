# Example: Basic Usage of brainxio/terraform-host-profiler

## Overview
This example demonstrates how to use the `brainxio/terraform-host-profiler` Terraform module to profile hardware specifications of the host machine where Terraform is executed. The module generates a JSON file (`hardware_profile.json`) containing details such as CPU, memory (including speed if detected), disk usage, GPU, and OS information.

## Prerequisites
- Terraform >= 1.3.0
- Python 3.x installed on the host
- For Linux: Optional tools like `dmidecode` (may require sudo), `hwinfo`, `lscpu`, `lsblk`, `nvidia-smi`, or `rocm-smi` for enhanced detection
- For Windows: `wmic` or PowerShell
- For macOS: `system_profiler` or `ioreg`

## Usage
1. Navigate to the `examples/simple` directory:
   ```bash
   cd examples/simple
   ```
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Review the plan:
   ```bash
   terraform plan
   ```
4. Apply the configuration:
   ```bash
   terraform apply
   ```

This will execute the module, run the `hardware_profile.py` script, and generate `hardware_profile.json` in the current working directory.

## Example Output
- **File**: `hardware_profile.json` (e.g., `{"cpu_processor": "x86_64", "cpu_max_frequency_ghz": "4.6", "memory_total_mb": "31817", "memory_free_mb": "20415", "memory_speed_mhz": "3200", "disk_0_name": "nvme0n1", ...}`)
- **Terraform Outputs**:
  - `hardware_profile`: The JSON object with hardware details
  - `profile_file_path`: Path to `hardware_profile.json`

## Notes
- The `python_interpreter` variable defaults to `python3`. Adjust if your Python executable has a different name (e.g., `python`).
- Memory speed (`memory_speed_mhz`) is included only if detected; otherwise, it is omitted.
- This example is a reference for integrating the module into larger Terraform configurations. See the main module's documentation for advanced usage.
