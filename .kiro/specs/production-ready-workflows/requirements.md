# Requirements Document

## Introduction

This specification enhances the existing n8n workflow generator to produce production-ready workflows with proper validation, error handling, and industry best practices. The focus is on creating workflows that are not just syntactically correct but also robust, secure, and maintainable for real-world business scenarios like real estate lead processing.

## Requirements

### Requirement 1

**User Story:** As a workflow developer, I want generated Code nodes to use n8n helpers directly instead of string interpolation, so that my workflows are more reliable and less prone to expression parsing errors.

#### Acceptance Criteria

1. WHEN a Code node is generated THEN the system SHALL use direct helper access like `$workflow.id` instead of `'{{ $workflow.id }}'`
2. WHEN accessing workflow metadata THEN the system SHALL use `$workflow.id`, `$workflow.name`, and other helpers directly in JavaScript
3. WHEN processing input data THEN the system SHALL use `$input.all()` and `$input.first()` methods properly
4. WHEN generating timestamps THEN the system SHALL use `new Date().toISOString()` instead of expression interpolation
5. WHEN referencing node data THEN the system SHALL use proper JavaScript object access patterns

### Requirement 2

**User Story:** As a workflow developer, I want Respond to Webhook nodes to be properly configured with response codes and JSON bodies, so that API clients receive appropriate HTTP responses.

#### Acceptance Criteria

1. WHEN a Respond to Webhook node is generated THEN the system SHALL set `Respond With` to "First Incoming Item" or "JSON"
2. WHEN responding to successful operations THEN the system SHALL set Response Code to 201 for resource creation or 200 for success
3. WHEN responding to validation errors THEN the system SHALL set Response Code to 400 with error details
4. WHEN configuring webhook responses THEN the system SHALL ensure proper JSON content-type headers
5. WHEN using webhook patterns THEN the system SHALL maintain `responseMode = "responseNode"` on the trigger

### Requirement 3

**User Story:** As a workflow developer, I want generated workflows to include comprehensive input validation, so that my automations can handle malformed or incomplete data gracefully.

#### Acceptance Criteria

1. WHEN processing lead data THEN the system SHALL validate required fields like name, phone, and email
2. WHEN validation fails THEN the system SHALL return structured error responses with missing field details
3. WHEN phone numbers are processed THEN the system SHALL normalize formats by removing non-digits
4. WHEN email addresses are processed THEN the system SHALL validate format using proper regex patterns
5. WHEN data is validated THEN the system SHALL enrich it with processing metadata like timestamps and workflow IDs

### Requirement 4

**User Story:** As a workflow developer, I want webhook nodes to include security configurations, so that my public endpoints are protected from misuse and unauthorized access.

#### Acceptance Criteria

1. WHEN webhook nodes are generated THEN the system SHALL include CORS configuration options
2. WHEN public endpoints are created THEN the system SHALL suggest setting Allowed Origins appropriately
3. WHEN webhook security is configured THEN the system SHALL include rate limiting considerations
4. WHEN authentication is needed THEN the system SHALL include basic auth or API key validation patterns
5. WHEN webhooks are generated THEN the system SHALL recommend using Test URLs during development

### Requirement 5

**User Story:** As a workflow developer, I want Code nodes to implement proper error handling and data normalization, so that my workflows can process real-world data reliably.

#### Acceptance Criteria

1. WHEN Code nodes process data THEN the system SHALL wrap operations in try-catch blocks
2. WHEN data normalization occurs THEN the system SHALL handle missing or null values gracefully
3. WHEN processing arrays THEN the system SHALL use proper mapping functions with error handling
4. WHEN validation fails THEN the system SHALL return consistent error response structures
5. WHEN data is processed THEN the system SHALL add processing metadata like status and timestamps

### Requirement 6

**User Story:** As a workflow developer, I want generated workflows to follow n8n best practices for production deployment, so that my automations are maintainable and scalable.

#### Acceptance Criteria

1. WHEN workflows are generated THEN the system SHALL include proper node naming conventions
2. WHEN complex workflows are created THEN the system SHALL organize nodes with clear data flow patterns
3. WHEN integrations are included THEN the system SHALL use proper credential management patterns
4. WHEN HTTP requests are made THEN the system SHALL include timeout and retry configurations
5. WHEN workflows are generated THEN the system SHALL include appropriate tags and metadata for organization

### Requirement 7

**User Story:** As a workflow developer, I want industry-specific workflow templates with production-ready patterns, so that I can quickly deploy reliable automations for common business scenarios.

#### Acceptance Criteria

1. WHEN real estate lead processing is selected THEN the system SHALL generate workflows with proper lead validation and CRM integration patterns
2. WHEN e-commerce workflows are generated THEN the system SHALL include order processing, inventory checks, and notification patterns
3. WHEN data sync workflows are created THEN the system SHALL include proper error handling and data consistency checks
4. WHEN notification workflows are generated THEN the system SHALL include multiple channel support and fallback mechanisms
5. WHEN monitoring workflows are created THEN the system SHALL include health checks and alerting patterns

### Requirement 8

**User Story:** As a workflow developer, I want generated Code nodes to include comprehensive data processing examples, so that I can understand and modify the logic for my specific needs.

#### Acceptance Criteria

1. WHEN Code nodes are generated THEN the system SHALL include clear comments explaining the processing logic
2. WHEN data validation is implemented THEN the system SHALL show examples of field checking and normalization
3. WHEN error handling is included THEN the system SHALL demonstrate proper error response formatting
4. WHEN data transformation occurs THEN the system SHALL show examples of common data manipulation patterns
5. WHEN helper functions are used THEN the system SHALL include documentation about available n8n helpers

### Requirement 9

**User Story:** As a workflow developer, I want workflows to include proper logging and monitoring capabilities, so that I can troubleshoot issues and monitor performance in production.

#### Acceptance Criteria

1. WHEN workflows are generated THEN the system SHALL include logging nodes for critical operations
2. WHEN errors occur THEN the system SHALL log error details with context information
3. WHEN data processing happens THEN the system SHALL log processing statistics and timing
4. WHEN integrations are used THEN the system SHALL log API call results and response times
5. WHEN workflows complete THEN the system SHALL log success metrics and processed item counts

### Requirement 10

**User Story:** As a workflow developer, I want the generator to create workflows with proper data persistence patterns, so that my automations can reliably store and retrieve business data.

#### Acceptance Criteria

1. WHEN database operations are needed THEN the system SHALL generate proper connection and query patterns
2. WHEN data is stored THEN the system SHALL include proper error handling for database failures
3. WHEN data retrieval occurs THEN the system SHALL include proper query validation and result handling
4. WHEN transactions are needed THEN the system SHALL implement proper commit/rollback patterns
5. WHEN data consistency is critical THEN the system SHALL include proper locking and validation mechanisms