terraform {
  required_version = ">= 1.3.0"
}

module "hardware_profile" {
  source             = "../../"
  python_interpreter = "python3"
}

output "hardware_profile" {
  value = module.hardware_profile.hardware_profile
}

output "profile_file_path" {
  value = module.hardware_profile.profile_file_path
}
