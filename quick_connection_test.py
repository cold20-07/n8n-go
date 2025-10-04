from enhanced_workflow_generator import generate_enhanced_workflow
import json

# Test the enhanced generator directly
workflow = generate_enhanced_workflow(
    'Create a workflow that sends a Slack notification when a webhook is triggered', 
    'webhook', 
    'simple'
)

nodes = workflow.get('nodes', [])
connections = workflow.get('connections', {})

print(f"Direct Generator Results:")
print(f"Nodes: {len(nodes)}")
print(f"Connections: {len(connections)}")

print(f"\nNode Names:")
for i, node in enumerate(nodes, 1):
    print(f"  {i}. {node.get('name')} ({node.get('type')})")

print(f"\nConnections:")
for source, conn_data in connections.items():
    target = conn_data['main'][0][0]['node']
    print(f"  {source} → {target}")

# Save the workflow
with open('direct_test_result.json', 'w') as f:
    json.dump(workflow, f, indent=2)

print(f"\nSaved to: direct_test_result.json")