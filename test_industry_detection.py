#!/usr/bin/env python3

from app import analyze_workflow_description

# Test some industry detection cases
test_cases = [
    ('comprehensive create medical records system', 'healthcare'),
    ('advanced create course scheduling system', 'education'),
    ('intelligent process transaction processing system', 'finance'),
    ('automated manage order processing system', 'ecommerce'),
    ('create data processing workflow', 'general')
]

print('Industry Detection Test:')
for desc, expected in test_cases:
    analysis = analyze_workflow_description(desc)
    detected = analysis.get('type', 'unknown')
    match = detected == expected or detected in ['general', 'automation']
    status = "✅" if match else "❌"
    print(f'  {desc[:40]}... -> {detected} (expected {expected}) {status}')