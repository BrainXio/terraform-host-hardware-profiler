output "hardware_profile" {
  description = "Hardware profile information as a flattened JSON object with string values, including CPU (cores, processor, max frequency), memory (total, free, speed if detected), disk (multiple NVMe disks with name, model, total, free, type via /sys/block), GPU (brand, name, VRAM, driver), and system (OS, release, distribution) details"
  value       = data.external.hardware_profile.result
}

output "profile_file_path" {
  description = "Path to the generated hardware profile JSON file"
  value       = local_file.hardware_output.filename
}
