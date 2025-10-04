# Requirements Document

## Introduction

The Perfect n8n Workflow Generator is a web-based application that allows users to generate valid n8n workflow JSON configurations through an intuitive interface. The application leverages AI (Gemini API) to create production-ready n8n workflows based on user descriptions, with fallback mechanisms to ensure reliability. The tool supports different trigger types, complexity levels, and includes validation to ensure generated workflows are compatible with n8n.

## Requirements

### Requirement 1

**User Story:** As a workflow automation developer, I want to describe my desired workflow in natural language, so that I can quickly generate a valid n8n workflow configuration without manually writing JSON.

#### Acceptance Criteria

1. WHEN a user enters a workflow description THEN the system SHALL accept text input describing the desired automation
2. WHEN a user submits a workflow description THEN the system SHALL validate that the description is not empty
3. WHEN a user provides a workflow description THEN the system SHALL use this description to generate contextually relevant n8n nodes and connections

### Requirement 2

**User Story:** As a workflow developer, I want to specify the trigger type for my workflow, so that I can control how the workflow is initiated.

#### Acceptance Criteria

1. WHEN a user accesses the generator THEN the system SHALL provide options for webhook, schedule, and manual trigger types
2. WHEN a user selects a trigger type THEN the system SHALL generate the appropriate trigger node with correct parameters
3. WHEN webhook trigger is selected THEN the system SHALL include a respondToWebhook node for proper HTTP response handling

### Requirement 3

**User Story:** As a workflow developer, I want to choose the complexity level of my workflow, so that I can control the number of nodes and sophistication of the generated workflow.

#### Acceptance Criteria

1. WHEN a user accesses the complexity selector THEN the system SHALL provide simple (2-3 nodes), medium (4-6 nodes), and complex (7+ nodes) options
2. WHEN simple complexity is selected THEN the system SHALL generate a workflow with 2-3 nodes including trigger and basic processing
3. WHEN medium complexity is selected THEN the system SHALL generate a workflow with 4-6 nodes including conditional logic
4. WHEN complex complexity is selected THEN the system SHALL generate a workflow with 7+ nodes including integrations like Slack

### Requirement 4

**User Story:** As a workflow developer, I want the system to use AI for intelligent workflow generation, so that I can get contextually relevant and sophisticated automation workflows that handle real business scenarios.

#### Acceptance Criteria

1. WHEN a user generates a workflow THEN the system SHALL attempt to use the Gemini 2.5 API for AI-powered generation
2. WHEN the AI generates a workflow THEN the system SHALL parse and validate the JSON response for n8n compatibility
3. WHEN the AI generation fails THEN the system SHALL automatically fall back to a local generation method
4. WHEN using AI generation THEN the system SHALL provide comprehensive prompts that include real-world automation patterns, error handling, and data validation
5. WHEN generating complex workflows THEN the system SHALL ensure proper data flow between nodes and include authentication where needed

### Requirement 5

**User Story:** As a workflow developer, I want the generated workflows to be valid n8n JSON format with accurate node types and parameters, so that I can directly import them into my n8n instance without errors.

#### Acceptance Criteria

1. WHEN a workflow is generated THEN the system SHALL produce JSON that conforms to n8n workflow schema
2. WHEN a workflow is generated THEN the system SHALL include required fields: name, nodes, connections, active, settings, and tags
3. WHEN nodes are created THEN each node SHALL have required properties: id, name, type, typeVersion, position, and parameters
4. WHEN connections are created THEN they SHALL properly link nodes using correct node names and connection structure
5. WHEN a workflow is generated THEN the system SHALL validate the JSON structure and report any errors
6. WHEN nodes are created THEN the system SHALL use ONLY current, valid n8n node types that exist in the latest version
7. WHEN nodes are created THEN the system SHALL include ALL required parameters for each node type
8. WHEN nodes are created THEN the system SHALL use correct typeVersion numbers for each node type

### Requirement 6

**User Story:** As a workflow developer, I want to copy the generated workflow JSON to my clipboard, so that I can easily paste it into n8n or save it for later use.

#### Acceptance Criteria

1. WHEN a workflow is successfully generated THEN the system SHALL display a copy button
2. WHEN a user clicks the copy button THEN the system SHALL copy the complete JSON to the clipboard
3. WHEN the JSON is copied THEN the system SHALL provide visual feedback confirming the copy action
4. WHEN the copy action completes THEN the button text SHALL temporarily change to indicate success

### Requirement 7

**User Story:** As a workflow developer, I want real-time validation of generated workflows, so that I can be confident the workflow will work in n8n before importing it.

#### Acceptance Criteria

1. WHEN a workflow is generated THEN the system SHALL automatically validate the JSON structure
2. WHEN validation passes THEN the system SHALL display a success message with green styling
3. WHEN validation fails THEN the system SHALL display specific error messages with red styling
4. WHEN validation runs THEN the system SHALL check for required fields, proper node structure, and valid connections
5. WHEN validation completes THEN the results SHALL be clearly visible to the user

### Requirement 8

**User Story:** As a workflow developer, I want a responsive and intuitive user interface, so that I can use the generator effectively on different devices and screen sizes.

#### Acceptance Criteria

1. WHEN a user accesses the application THEN the system SHALL display a responsive layout that works on desktop and mobile
2. WHEN a user interacts with form elements THEN the system SHALL provide clear visual feedback and hover states
3. WHEN the system is processing a request THEN it SHALL show loading indicators and disable the generate button
4. WHEN a workflow is being generated THEN the system SHALL display progress status with appropriate messaging
5. WHEN the application loads THEN it SHALL display helpful instructions and feature descriptions

### Requirement 9

**User Story:** As a workflow developer, I want the system to handle errors gracefully, so that I can still generate workflows even when external services are unavailable.

#### Acceptance Criteria

1. WHEN the Gemini API is unavailable THEN the system SHALL automatically use the fallback generation method
2. WHEN an error occurs during generation THEN the system SHALL display a clear error message to the user
3. WHEN the fallback method is used THEN the system SHALL still produce valid n8n workflow JSON
4. WHEN network errors occur THEN the system SHALL not crash and SHALL provide appropriate user feedback
5. WHEN API rate limits are hit THEN the system SHALL handle the error gracefully and suggest retry options

### Requirement 10

**User Story:** As a workflow developer, I want access to pre-built automation templates, so that I can quickly generate workflows for common business scenarios without starting from scratch.

#### Acceptance Criteria

1. WHEN a user accesses the generator THEN the system SHALL provide template options for common automation patterns
2. WHEN a user selects a template THEN the system SHALL pre-populate the description with a detailed automation scenario
3. WHEN templates are used THEN the system SHALL generate workflows with proper authentication, error handling, and data validation
4. WHEN a template is applied THEN the system SHALL customize the workflow based on user-specific requirements
5. WHEN templates are generated THEN they SHALL include realistic parameters and production-ready configurations

### Requirement 11

**User Story:** As a workflow developer, I want the generator to create workflows with proper error handling and monitoring, so that my automations are reliable and maintainable in production.

#### Acceptance Criteria

1. WHEN a workflow is generated THEN the system SHALL include error handling nodes for critical operations
2. WHEN HTTP requests are included THEN the system SHALL add retry logic and timeout configurations
3. WHEN data processing occurs THEN the system SHALL include validation and error recovery mechanisms
4. WHEN integrations are used THEN the system SHALL include proper authentication and rate limiting
5. WHEN workflows are complex THEN the system SHALL add monitoring and logging capabilities

### Requirement 12

**User Story:** As a workflow developer, I want the system to use only accurate n8n node types and proper data flow syntax, so that generated workflows work correctly when imported into n8n.

#### Acceptance Criteria

1. WHEN AI content generation is needed THEN the system SHALL use "n8n-nodes-base.openAi" or "n8n-nodes-base.httpRequest" for API calls
2. WHEN RSS reading is required THEN the system SHALL use "n8n-nodes-base.rssFeedRead" with actual RSS URLs
3. WHEN Twitter integration is needed THEN the system SHALL use "n8n-nodes-base.twitter" or "n8n-nodes-base.httpRequest" for Twitter API
4. WHEN scheduling is required THEN the system SHALL use "n8n-nodes-base.scheduleTrigger" with proper cron expressions or intervals
5. WHEN data processing is needed THEN the system SHALL use "n8n-nodes-base.code" or "n8n-nodes-base.set"
6. WHEN accessing previous node data THEN the system SHALL use {{ $json.fieldName }} syntax for data flow
7. WHEN creating workflows THEN the system SHALL ensure each node receives the data it needs from the previous node
8. WHEN generating complex workflows THEN the system SHALL include proper error handling paths where needed

### Requirement 13

**User Story:** As a workflow developer, I want all node parameters to be properly configured with required authentication and settings, so that workflows are production-ready upon generation.

#### Acceptance Criteria

1. WHEN Schedule Trigger nodes are created THEN the system SHALL include proper cron expression or interval parameters
2. WHEN RSS Feed nodes are created THEN the system SHALL require actual RSS URLs, not placeholder URLs
3. WHEN AI nodes are created THEN the system SHALL include model selection, API key reference, and proper prompts
4. WHEN Social Media nodes are created THEN the system SHALL include all required authentication parameters
5. WHEN Analytics nodes are created THEN the system SHALL use proper event tracking with valid parameters
6. WHEN HTTP Request nodes are created THEN the system SHALL include proper authentication, headers, and error handling
7. WHEN database nodes are created THEN the system SHALL include connection parameters and query validation

### Requirement 14

**User Story:** As a workflow developer, I want the system to enforce strict accuracy validation and use only official current node types, so that generated workflows are guaranteed to work when imported into n8n.

#### Acceptance Criteria

1. WHEN any node is created THEN the system SHALL use ONLY current, valid n8n node types from the latest stable n8n release
2. WHEN nodes are generated THEN the system SHALL use accurate and up-to-date typeVersion numbers for each node type
3. WHEN workflows are created THEN the system SHALL avoid deprecated or unofficial node types completely
4. WHEN node parameters are set THEN the system SHALL include ALL required parameters for each node type including API credentials references, URLs, and operation fields
5. WHEN API nodes are created THEN the system SHALL include proper authentication (OAuth2 or API keys) references with realistic credential names
6. WHEN trigger nodes are created THEN the system SHALL use valid interval or cron expressions, not placeholder values
7. WHEN accessing previous node data THEN the system SHALL always use correct n8n expressions like {{ $json["fieldName"] }}
8. WHEN transforming data THEN the system SHALL use Set, Code or parsing nodes before passing to next nodes where needed

### Requirement 15

**User Story:** As a workflow developer, I want workflows to have clear and logical connections with proper data flow, so that the automation works exactly as intended without manual fixes.

#### Acceptance Criteria

1. WHEN creating node connections THEN the system SHALL guarantee node connections reflect the intended data flow exactly as specified
2. WHEN connecting nodes THEN the system SHALL ensure nodes representing different platforms are connected properly in sequence or parallel as per design
3. WHEN generating workflows THEN the system SHALL avoid extraneous nodes or platforms outside the user's request
4. WHEN setting URLs or API endpoints THEN the system SHALL use realistic endpoints or clearly mark as placeholders when explicitly requested
5. WHEN handling credentials THEN the system SHALL reference credentials by credential names, never hardcode sensitive values
6. WHEN creating complex workflows THEN the system SHALL include error branches or fallback nodes where critical API calls or data fetching happens
7. WHEN validating data THEN the system SHALL use IF or Switch nodes for validation of required data before publishing or logging

### Requirement 16

**User Story:** As a workflow developer, I want consistent naming conventions and comprehensive metadata, so that generated workflows are maintainable and well-documented.

#### Acceptance Criteria

1. WHEN creating nodes THEN the system SHALL use clear, meaningful names for all nodes that reflect node function and step order
2. WHEN generating workflows THEN the system SHALL include metadata fields (tags, descriptions) specifying auto-generated status
3. WHEN possible THEN the system SHALL include comments to guide manual editing and maintenance
4. WHEN creating workflows THEN the system SHALL add versioning to track updates and include timestamp or generation date in workflow settings
5. WHEN naming workflows THEN the system SHALL generate descriptive workflow names based on the automation purpose