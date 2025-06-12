data "external" "hardware_profile" {
  program = [var.python_interpreter, "${path.module}/files/hardware_profile.py"]
}

resource "local_file" "hardware_output" {
  content  = jsonencode(data.external.hardware_profile.result)
  filename = "${path.cwd}/hardware_profile.json"
}
