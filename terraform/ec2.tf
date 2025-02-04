resource "aws_instance" "vpn" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  subnet_id                   = aws_subnet.public[0].id
  vpc_security_group_ids      = [aws_security_group.vpn.id]
  associate_public_ip_address = true

  key_name = aws_key_pair.vpn_key.key_name

  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }

  tags = {
    Name    = "${var.project_name}-vpn"
    Project = var.project_name
  }
}