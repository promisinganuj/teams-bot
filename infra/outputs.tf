output "webapp_name" {
  description = "Name of the Azure Web App"
  value       = azurerm_linux_web_app.app.name
}

output "webapp_url" {
  description = "URL of the Azure Web App"
  value       = "https://${azurerm_linux_web_app.app.default_hostname}"
}

output "webapp_hostname" {
  description = "Hostname of the Azure Web App"
  value       = azurerm_linux_web_app.app.default_hostname
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.rg.name
}

output "application_insights_instrumentation_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.insights.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Application Insights connection string"
  value       = azurerm_application_insights.insights.connection_string
  sensitive   = true
}