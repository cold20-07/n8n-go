#!/bin/bash

# N8N Workflow Generator Deployment Script
set -e

# Configuration
ENVIRONMENT=${1:-production}
VERSION=${2:-latest}
COMPOSE_FILE="docker-compose.prod.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f ".env.${ENVIRONMENT}" ]; then
        error ".env.${ENVIRONMENT} file not found"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Load environment variables
load_environment() {
    log "Loading environment variables for ${ENVIRONMENT}..."
    
    # Copy environment-specific .env file
    cp ".env.${ENVIRONMENT}" .env
    
    # Source the environment file
    set -a
    source .env
    set +a
    
    # Set Docker image with version
    export DOCKER_IMAGE="${DOCKER_USERNAME:-n8n-workflow-generator}/n8n-workflow-generator:${VERSION}"
    
    success "Environment variables loaded"
}

# Backup current deployment
backup_deployment() {
    log "Creating backup of current deployment..."
    
    BACKUP_DIR="backups/$(date +'%Y%m%d_%H%M%S')"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    if docker-compose -f $COMPOSE_FILE ps db | grep -q "Up"; then
        log "Backing up database..."
        docker-compose -f $COMPOSE_FILE exec -T db pg_dump -U "${POSTGRES_USER:-n8n_user}" "${POSTGRES_DB:-n8n_workflows}" > "$BACKUP_DIR/database.sql"
    fi
    
    # Backup application data
    if docker-compose -f $COMPOSE_FILE ps app | grep -q "Up"; then
        log "Backing up application data..."
        docker-compose -f $COMPOSE_FILE exec -T app tar -czf - /app/data > "$BACKUP_DIR/app_data.tar.gz"
    fi
    
    # Backup configuration
    cp .env "$BACKUP_DIR/"
    cp $COMPOSE_FILE "$BACKUP_DIR/"
    
    success "Backup created in $BACKUP_DIR"
}

# Pull latest images
pull_images() {
    log "Pulling latest Docker images..."
    
    docker-compose -f $COMPOSE_FILE pull
    
    success "Images pulled successfully"
}

# Deploy application
deploy() {
    log "Deploying N8N Workflow Generator..."
    
    # Stop existing containers
    log "Stopping existing containers..."
    docker-compose -f $COMPOSE_FILE down
    
    # Start new containers
    log "Starting new containers..."
    docker-compose -f $COMPOSE_FILE up -d
    
    success "Deployment completed"
}

# Health check
health_check() {
    log "Performing health checks..."
    
    # Wait for services to start
    sleep 30
    
    # Check application health
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log "Health check attempt $attempt/$max_attempts..."
        
        if curl -f -s "http://localhost:${APP_PORT:-5000}/health" > /dev/null; then
            success "Application is healthy"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            error "Health check failed after $max_attempts attempts"
            return 1
        fi
        
        sleep 10
        ((attempt++))
    done
    
    # Check database connection
    if docker-compose -f $COMPOSE_FILE exec -T db pg_isready -U "${POSTGRES_USER:-n8n_user}" > /dev/null; then
        success "Database is healthy"
    else
        warning "Database health check failed"
    fi
    
    # Check Redis connection
    if docker-compose -f $COMPOSE_FILE exec -T redis redis-cli ping | grep -q "PONG"; then
        success "Redis is healthy"
    else
        warning "Redis health check failed"
    fi
}

# Run smoke tests
smoke_tests() {
    log "Running smoke tests..."
    
    local base_url="http://localhost:${APP_PORT:-5000}"
    
    # Test health endpoint
    if curl -f -s "$base_url/health" | grep -q "healthy"; then
        success "Health endpoint test passed"
    else
        error "Health endpoint test failed"
        return 1
    fi
    
    # Test configuration endpoint
    if curl -f -s "$base_url/api/config/status" | grep -q "success"; then
        success "Configuration endpoint test passed"
    else
        warning "Configuration endpoint test failed"
    fi
    
    # Test workflow generation (basic)
    local test_payload='{"description":"Test workflow","trigger":"webhook","complexity":"simple"}'
    if curl -f -s -X POST -H "Content-Type: application/json" -d "$test_payload" "$base_url/generate" | grep -q "success"; then
        success "Workflow generation test passed"
    else
        warning "Workflow generation test failed"
    fi
    
    success "Smoke tests completed"
}

# Cleanup old images
cleanup() {
    log "Cleaning up old Docker images..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove old versions (keep last 3)
    docker images "${DOCKER_USERNAME:-n8n-workflow-generator}/n8n-workflow-generator" --format "table {{.Tag}}\t{{.ID}}" | \
    tail -n +2 | sort -V | head -n -3 | awk '{print $2}' | xargs -r docker rmi
    
    success "Cleanup completed"
}

# Rollback function
rollback() {
    error "Deployment failed. Rolling back..."
    
    # Find latest backup
    local latest_backup=$(ls -1t backups/ | head -n 1)
    
    if [ -n "$latest_backup" ]; then
        log "Rolling back to backup: $latest_backup"
        
        # Stop current deployment
        docker-compose -f $COMPOSE_FILE down
        
        # Restore configuration
        cp "backups/$latest_backup/.env" .env
        
        # Start with previous configuration
        docker-compose -f $COMPOSE_FILE up -d
        
        warning "Rollback completed. Please check the application status."
    else
        error "No backup found for rollback"
    fi
}

# Send notification
send_notification() {
    local status=$1
    local message=$2
    
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        local color="good"
        if [ "$status" = "error" ]; then
            color="danger"
        elif [ "$status" = "warning" ]; then
            color="warning"
        fi
        
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"attachments\":[{\"color\":\"$color\",\"text\":\"$message\"}]}" \
            "$SLACK_WEBHOOK_URL"
    fi
}

# Main deployment function
main() {
    log "Starting deployment of N8N Workflow Generator"
    log "Environment: $ENVIRONMENT"
    log "Version: $VERSION"
    
    # Trap errors for rollback
    trap 'rollback; send_notification "error" "Deployment failed for version $VERSION"; exit 1' ERR
    
    check_prerequisites
    load_environment
    backup_deployment
    pull_images
    deploy
    health_check
    smoke_tests
    cleanup
    
    success "Deployment completed successfully!"
    send_notification "good" "N8N Workflow Generator $VERSION deployed successfully to $ENVIRONMENT"
    
    # Display deployment info
    log "Deployment Information:"
    log "- Environment: $ENVIRONMENT"
    log "- Version: $VERSION"
    log "- Application URL: http://localhost:${APP_PORT:-5000}"
    log "- Grafana Dashboard: http://localhost:3000"
    log "- Prometheus: http://localhost:9090"
}

# Script usage
usage() {
    echo "Usage: $0 [environment] [version]"
    echo ""
    echo "Arguments:"
    echo "  environment  Deployment environment (default: production)"
    echo "  version      Docker image version (default: latest)"
    echo ""
    echo "Examples:"
    echo "  $0 production v1.2.3"
    echo "  $0 staging latest"
    echo ""
    echo "Prerequisites:"
    echo "  - Docker and Docker Compose installed"
    echo "  - .env.[environment] file configured"
    echo "  - Proper permissions for Docker operations"
}

# Handle script arguments
case "${1:-}" in
    -h|--help)
        usage
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac