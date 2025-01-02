resource "aws_key_pair" "vpn_key" {
  key_name   = "${var.project_name}-key"
  public_key = file("~/.ssh/vpn-key.pub")
}