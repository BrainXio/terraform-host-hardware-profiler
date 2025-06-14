# Hardware Profile Module Overview

This module collects hardware specifications from the host machine where Terraform is executed. It uses a Python script with standard library modules to gather details such as CPU, memory (including speed if detected), disk usage, GPU (NVIDIA/AMD), and OS information, outputting the results as a JSON object saved to `hardware_profile.json`.

## Purpose
The module provides a reusable way to profile hardware for inventory, monitoring, or configuration purposes in infrastructure-as-code workflows.
