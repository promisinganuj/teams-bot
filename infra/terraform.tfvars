# Terraform variables file
# Update these values according to your environment

resource_group_name = "rg-addbot-prod"
location           = "australiaeast"
prefix             = "addbot"

# Bot credentials - these should be set as environment variables or via Azure Key Vault
# bot_app_id          = "your-bot-app-id-here"
# bot_app_password    = "your-bot-app-password-here"

tags = {
  Environment = "Production"
  Project     = "TeamsAddBot"
  Owner       = "DevOps Team"
}
