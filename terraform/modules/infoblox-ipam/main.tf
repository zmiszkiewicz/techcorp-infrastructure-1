terraform {
  required_providers {
    bloxone = {
      source = "infobloxopen/bloxone"
    }
  }
}

resource "bloxone_ipam_ip_space" "main" {
  name    = var.ip_space_name
  comment = "Managed by Terraform - Source of truth for cloud IPs"
}

resource "bloxone_ipam_address_block" "main" {
  address = var.address_block.address
  cidr    = var.address_block.cidr
  space   = bloxone_ipam_ip_space.main.id
  name    = var.address_block.name
  comment = var.address_block.comment
}

resource "bloxone_ipam_subnet" "subnets" {
  for_each = var.subnets

  address = each.value.address
  cidr    = each.value.cidr
  space   = bloxone_ipam_ip_space.main.id
  name    = each.value.name
  comment = each.value.comment

  depends_on = [bloxone_ipam_address_block.main]
}
