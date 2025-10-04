from enhanced_workflow_generator import EnhancedWorkflowGenerator

g = EnhancedWorkflowGenerator()
w = g.generate_enhanced_workflow('Create a scheduled workflow that reads RSS feeds, generates social media posts using AI, and posts them to Twitter and LinkedIn')

print(f'Nodes: {len(w["nodes"])}')
print(f'Connections: {len(w["connections"])}')

# Check LinkedIn parameters
linkedin_nodes = [n for n in w["nodes"] if "linkedin" in n["type"].lower()]
if linkedin_nodes:
    print(f'LinkedIn params: {linkedin_nodes[0]["parameters"]}')
else:
    print('No LinkedIn nodes found')

# Show all node types
print(f'Node types: {[n["type"] for n in w["nodes"]]}')