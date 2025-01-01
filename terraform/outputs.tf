output "vpn_public_ip" {
  description = "Public IP of the VPN instance"
  value       = aws_instance.vpn.public_ip
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "available_regions" {
  description = "Available AWS regions"
  value = [
    "us-east-1",      # N. Virginia
    "us-east-2",      # Ohio
    "us-west-1",      # N. California
    "us-west-2",      # Oregon
    "eu-west-1",      # Ireland
    "eu-west-2",      # London
    "eu-west-3",      # Paris
    "eu-central-1",   # Frankfurt
    "ap-northeast-1", # Tokyo
    "ap-northeast-2", # Seoul
    "ap-southeast-1", # Singapore
    "ap-southeast-2", # Sydney
    "ap-south-1",     # Mumbai
    "sa-east-1"       # São Paulo
  ]
}