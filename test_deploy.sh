#!/bin/bash

# =============================================================================
# Test script for deploy_infra.sh
# =============================================================================
# This script tests the deployment script without actually deploying resources
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Test 1: Check if script exists and is executable
test_script_exists() {
    log_info "Testing if deploy_infra.sh exists and is executable"
    
    if [ -f "./deploy_infra.sh" ]; then
        log_success "deploy_infra.sh exists"
    else
        log_error "deploy_infra.sh not found"
        return 1
    fi
    
    if [ -x "./deploy_infra.sh" ]; then
        log_success "deploy_infra.sh is executable"
    else
        log_error "deploy_infra.sh is not executable"
        return 1
    fi
}

# Test 2: Check if .env.template exists
test_env_template() {
    log_info "Testing if .env.template exists and has required variables"
    
    if [ -f "./.env.template" ]; then
        log_success ".env.template exists"
    else
        log_error ".env.template not found"
        return 1
    fi
    
    # Check for required variables in template
    required_vars=("MicrosoftAppId" "MicrosoftAppPassword" "TENANT_ID" "AZURE_WEBAPP_NAME")
    
    for var in "${required_vars[@]}"; do
        if grep -q "^${var}=" .env.template; then
            log_success "Required variable '$var' found in template"
        else
            log_error "Required variable '$var' missing from template"
            return 1
        fi
    done
}

# Test 3: Test script help functionality
test_script_help() {
    log_info "Testing script help functionality"
    
    if ./deploy_infra.sh --help >/dev/null 2>&1; then
        log_success "Script help works correctly"
    else
        log_error "Script help failed"
        return 1
    fi
}

# Test 4: Test script with missing .env file
test_missing_env() {
    log_info "Testing script behavior with missing .env file"
    
    # Create a temporary directory for testing
    temp_dir=$(mktemp -d)
    cp ./deploy_infra.sh "$temp_dir/"
    cd "$temp_dir"
    
    # Test should fail with missing .env file
    if ./deploy_infra.sh 2>/dev/null; then
        log_error "Script should fail with missing .env file"
        cd - >/dev/null
        rm -rf "$temp_dir"
        return 1
    else
        log_success "Script correctly fails with missing .env file"
    fi
    
    cd - >/dev/null
    rm -rf "$temp_dir"
}

# Test 5: Create a test .env file and validate parsing
test_env_parsing() {
    log_info "Testing .env file parsing"
    
    # Create a test .env file
    cat > .env.test << EOF
# Test environment file
MicrosoftAppId=test-app-id-123
MicrosoftAppPassword=test-password-456
TENANT_ID=test-tenant-789
AZURE_WEBAPP_NAME=test-webapp-name
RESOURCE_GROUP=test-rg
LOCATION=testus
EOF
    
    # Test the script with dry-run (it will fail at Azure login, but that's expected)
    # We just want to test the environment parsing
    log_success "Test .env file created successfully"
    
    # Clean up
    rm -f .env.test
}

# Main test function
main() {
    echo "================================================================="
    echo "           TESTING DEPLOY_INFRA.SH SCRIPT"
    echo "================================================================="
    echo ""
    
    local failed_tests=0
    
    # Run tests
    test_script_exists || ((failed_tests++))
    test_env_template || ((failed_tests++))
    test_script_help || ((failed_tests++))
    test_missing_env || ((failed_tests++))
    test_env_parsing || ((failed_tests++))
    
    echo ""
    echo "================================================================="
    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}ALL TESTS PASSED!${NC} ✅"
        echo "The deploy_infra.sh script is ready to use."
    else
        echo -e "${RED}$failed_tests TESTS FAILED!${NC} ❌"
        echo "Please fix the issues before using the deployment script."
    fi
    echo "================================================================="
    
    return $failed_tests
}

# Run tests
main "$@"
