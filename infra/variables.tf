variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "australiaeast"
}

variable "prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "addbot"
}

variable "bot_app_id" {
  description = "Microsoft Bot App ID"
  type        = string
  sensitive   = true
}

variable "bot_app_password" {
  description = "Microsoft Bot App Password"
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "Production"
    Project     = "TeamsAddBot"
  }
}
