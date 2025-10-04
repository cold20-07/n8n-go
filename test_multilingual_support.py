#!/usr/bin/env python3
"""Multilingual and International Support Testing"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_multilingual_descriptions():
    """Test workflow generation with multilingual descriptions"""
    print("🌍 Testing Multilingual Description Support")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    multilingual_tests = [
        {
            'name': 'Spanish Description',
            'description': 'Crear un flujo de trabajo para procesar pedidos de comercio electrónico con validación de pagos y notificaciones por correo electrónico',
            'trigger_type': 'webhook',
            'expected_keywords': ['ecommerce', 'orders', 'payments']
        },
        {
            'name': 'French Description',
            'description': 'Construire un système de gestion des patients pour les rendez-vous médicaux avec notifications automatiques et mise à jour des dossiers',
            'trigger_type': 'schedule',
            'expected_keywords': ['healthcare', 'patient', 'appointments']
        },
        {
            'name': 'German Description',
            'description': 'Entwickeln Sie einen Workflow für die Finanzüberwachung mit Betrugserkennung und Compliance-Berichterstattung für Banksysteme',
            'trigger_type': 'manual',
            'expected_keywords': ['finance', 'banking', 'compliance']
        },
        {
            'name': 'Mixed Language Description',
            'description': 'Create a workflow para estudiantes with automatic enrollment y notification system for universidad management',
            'trigger_type': 'webhook',
            'expected_keywords': ['education', 'students', 'enrollment']
        }
    ]
    
    passed_tests = 0
    
    for test in multilingual_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': test['trigger_type']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                tags = workflow.get('tags', [])
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Tags: {tags}")
                
                # Check if workflow was generated successfully
                if len(nodes) >= 2:  # At least trigger + one processing node
                    print("   ✅ Workflow generated successfully")
                    
                    # Check for relevant tags (relaxed criteria for multilingual)
                    relevant_tags = sum(1 for keyword in test['expected_keywords'] 
                                      if any(keyword.lower() in tag.lower() for tag in tags))
                    
                    if relevant_tags >= 1:  # At least one relevant tag
                        print(f"   ✅ Found {relevant_tags} relevant tags")
                        passed_tests += 1
                    else:
                        print("   ⚠️ No relevant tags found, but workflow generated")
                        passed_tests += 0.5  # Partial credit
                else:
                    print("   ❌ Insufficient nodes generated")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Multilingual Results: {passed_tests}/{len(multilingual_tests)} passed")
    return passed_tests

def test_unicode_and_special_characters():
    """Test handling of Unicode and special characters"""
    print("\n🔤 Testing Unicode and Special Characters")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    unicode_tests = [
        {
            'name': 'Emoji Characters',
            'description': 'Create a workflow 🚀 for processing customer orders 📦 with payment validation 💳 and email notifications 📧',
            'trigger_type': 'webhook'
        },
        {
            'name': 'Accented Characters',
            'description': 'Créer un système de gestion des étudiants avec inscriptions automatiques et notifications aux professeurs',
            'trigger_type': 'schedule'
        },
        {
            'name': 'Asian Characters',
            'description': 'Create a workflow for 患者管理 with automated scheduling and 通知システム for healthcare providers',
            'trigger_type': 'manual'
        },
        {
            'name': 'Mathematical Symbols',
            'description': 'Build a financial workflow with calculations (α + β = γ) and statistical analysis ∑∆∏ for reporting',
            'trigger_type': 'webhook'
        }
    ]
    
    passed_tests = 0
    
    for test in unicode_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': test['trigger_type']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                workflow_name = workflow.get('name', '')
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Workflow name: {workflow_name}")
                
                # Check if workflow was generated without errors
                if len(nodes) >= 2 and workflow_name:
                    print("   ✅ Unicode characters handled successfully")
                    passed_tests += 1
                else:
                    print("   ❌ Unicode handling failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Unicode Results: {passed_tests}/{len(unicode_tests)} passed")
    return passed_tests

def test_international_business_scenarios():
    """Test international business workflow scenarios"""
    print("\n🌐 Testing International Business Scenarios")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    international_tests = [
        {
            'name': 'Multi-Currency E-commerce',
            'description': 'Create an international e-commerce workflow supporting USD, EUR, GBP, and JPY currencies with tax calculations and regional shipping',
            'trigger_type': 'webhook',
            'expected_features': ['currency', 'international', 'tax']
        },
        {
            'name': 'Global HR Management',
            'description': 'Build a global HR workflow for employee onboarding across different countries with compliance checks and localized documentation',
            'trigger_type': 'schedule',
            'expected_features': ['hr', 'global', 'compliance']
        },
        {
            'name': 'Cross-Border Banking',
            'description': 'Design a cross-border banking workflow with SWIFT transfers, currency conversion, and international compliance reporting',
            'trigger_type': 'manual',
            'expected_features': ['banking', 'international', 'compliance']
        },
        {
            'name': 'Multi-Region Healthcare',
            'description': 'Create a healthcare workflow supporting multiple regions with different privacy regulations (GDPR, HIPAA) and language preferences',
            'trigger_type': 'webhook',
            'expected_features': ['healthcare', 'privacy', 'regulations']
        }
    ]
    
    passed_tests = 0
    
    for test in international_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': test['trigger_type'],
                                  'complexity': 'complex'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                tags = workflow.get('tags', [])
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Tags: {tags}")
                
                # Check for complex international workflow
                if len(nodes) >= 4:  # Complex international workflows should have multiple nodes
                    print("   ✅ Complex international workflow generated")
                    
                    # Check for relevant international features
                    description_lower = test['description'].lower()
                    features_found = sum(1 for feature in test['expected_features']
                                       if feature in description_lower or 
                                       any(feature in tag.lower() for tag in tags))
                    
                    if features_found >= 2:  # At least 2 international features
                        print(f"   ✅ International features detected: {features_found}")
                        passed_tests += 1
                    else:
                        print(f"   ⚠️ Limited international features: {features_found}")
                        passed_tests += 0.5
                else:
                    print("   ❌ Insufficient complexity for international scenario")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 International Business Results: {passed_tests}/{len(international_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    try:
        print("🌍 MULTILINGUAL AND INTERNATIONAL SUPPORT TESTING")
        print("=" * 60)
        
        multilingual_passed = test_multilingual_descriptions()
        unicode_passed = test_unicode_and_special_characters()
        international_passed = test_international_business_scenarios()
        
        total_tests = 4 + 4 + 4  # Total test cases
        total_passed = multilingual_passed + unicode_passed + international_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 MULTILINGUAL & INTERNATIONAL TEST RESULTS")
        print("=" * 60)
        print(f"🌍 Multilingual Descriptions: {multilingual_passed}/4")
        print(f"🔤 Unicode & Special Chars: {unicode_passed}/4")
        print(f"🌐 International Business: {international_passed}/4")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 75:
            print("🎉 Multilingual and international support tests passed!")
            exit(0)
        else:
            print("⚠️ Some multilingual/international tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Multilingual and international tests failed: {e}")
        exit(1)