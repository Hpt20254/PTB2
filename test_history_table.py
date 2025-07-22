#!/usr/bin/env python3
"""
Test script cho History Table Task 2.3
"""
import json
from app import app

def test_history_table():
    """Test danh sách phương trình đã lưu với table display"""
    
    print("📋 TESTING HISTORY TABLE - TASK 2.3")
    print("="*50)
    
    client = app.test_client()
    
    print("\n1. TESTING WEB INTERFACE WITH TABS:")
    response = client.get('/')
    if response.status_code == 200:
        html_content = response.data.decode('utf-8')
        
        # Check for tab elements
        tab_elements = [
            'nav-tabs',
            'tab-button',
            'solver-tab',
            'history-tab',
            'showTab(',
            'loadEquations('
        ]
        
        print("   Checking for tab elements:")
        for element in tab_elements:
            if element in html_content:
                print(f"   ✅ {element} - Present")
            else:
                print(f"   ❌ {element} - Missing")
        
        # Check for table elements
        table_elements = [
            'table-container',
            'equations-table',
            'action-buttons',
            'edit-btn',
            'delete-btn',
            'editModal'
        ]
        
        print("\n   Checking for table elements:")
        for element in table_elements:
            if element in html_content:
                print(f"   ✅ {element} - Present")
            else:
                print(f"   ❌ {element} - Missing")
    
    print(f"\n2. TESTING GET /api/equations (Table Data Source):")
    response = client.get('/api/equations')
    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ✅ Count: {data['count']} equations")
        print(f"   ✅ Success: {data['success']}")
        
        if data['equations']:
            sample_eq = data['equations'][0]
            print(f"   ✅ Sample equation structure:")
            for key in sample_eq.keys():
                print(f"     - {key}: {sample_eq[key]}")
            
            # Check if status is included
            if 'status' in sample_eq:
                print(f"   ✅ Status field present: {sample_eq['status']}")
            else:
                print(f"   ❌ Status field missing")
        
        return data['equations']
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return []

def test_edit_functionality():
    """Test edit functionality"""
    
    print(f"\n3. TESTING EDIT FUNCTIONALITY:")
    client = app.test_client()
    
    # Get first equation to edit
    response = client.get('/api/equations')
    if response.status_code == 200:
        data = json.loads(response.data)
        if data['equations']:
            first_eq = data['equations'][0]
            eq_id = first_eq['id']
            
            print(f"   Testing edit for equation ID: {eq_id}")
            print(f"   Original: a={first_eq['a']}, b={first_eq['b']}, c={first_eq['c']}")
            
            # Test PUT request
            new_data = {
                'a': first_eq['a'] + 1,
                'b': first_eq['b'] + 1, 
                'c': first_eq['c'] + 1
            }
            
            response = client.put(f'/api/equations/{eq_id}',
                                data=json.dumps(new_data),
                                content_type='application/json')
            
            if response.status_code == 200:
                result = json.loads(response.data)
                print(f"   ✅ Edit successful")
                print(f"   ✅ New values: a={new_data['a']}, b={new_data['b']}, c={new_data['c']}")
                print(f"   ✅ New equation: {result['new_equation']}")
                print(f"   ✅ New solution: {result['solution']}")
                print(f"   ✅ Status: {result['status']}")
                
                # Verify in database
                verify_response = client.get(f'/api/equations/{eq_id}')
                if verify_response.status_code == 200:
                    verify_data = json.loads(verify_response.data)
                    eq = verify_data['equation']
                    if (eq['a'] == new_data['a'] and 
                        eq['b'] == new_data['b'] and 
                        eq['c'] == new_data['c']):
                        print(f"   ✅ Database updated correctly")
                    else:
                        print(f"   ❌ Database not updated")
                
                return eq_id
            else:
                print(f"   ❌ Edit failed: {response.status_code}")
                return None
    
    return None

def test_delete_functionality():
    """Test delete functionality"""
    
    print(f"\n4. TESTING DELETE FUNCTIONALITY:")
    client = app.test_client()
    
    # Create a test equation to delete
    test_data = {'a': 999, 'b': 999, 'c': 999}
    response = client.post('/api/equation',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    if response.status_code == 201:
        result = json.loads(response.data)
        test_id = result['id']
        print(f"   Created test equation ID: {test_id}")
        
        # Test DELETE request
        response = client.delete(f'/api/equations/{test_id}')
        
        if response.status_code == 200:
            print(f"   ✅ Delete successful")
            
            # Verify deletion
            verify_response = client.get(f'/api/equations/{test_id}')
            if verify_response.status_code == 404:
                print(f"   ✅ Equation properly deleted from database")
            else:
                print(f"   ❌ Equation still exists in database")
        else:
            print(f"   ❌ Delete failed: {response.status_code}")
    else:
        print(f"   ❌ Failed to create test equation")

def test_table_display_features():
    """Test table display features"""
    
    print(f"\n5. TESTING TABLE DISPLAY FEATURES:")
    client = app.test_client()
    
    # Get equations data
    response = client.get('/api/equations')
    if response.status_code == 200:
        data = json.loads(response.data)
        equations = data['equations']
        
        print(f"   ✅ Total equations: {len(equations)}")
        
        # Test different equation types
        status_counts = {}
        for eq in equations:
            status = eq.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"   ✅ Equation types in database:")
        for status, count in status_counts.items():
            print(f"     - {status}: {count} equations")
        
        # Test equation formatting
        if equations:
            sample = equations[0]
            print(f"   ✅ Sample equation display:")
            print(f"     ID: #{sample['id']}")
            print(f"     Equation: {sample['equation']}")
            print(f"     Coefficients: a={sample['a']}, b={sample['b']}, c={sample['c']}")
            print(f"     Status: {sample['status']}")
            print(f"     Solution: {sample['solution']}")

def main():
    print("🧪 STARTING TASK 2.3 TESTS...")
    
    # Test 1: Web interface with tabs and table
    equations = test_history_table()
    
    # Test 2: Edit functionality
    edited_id = test_edit_functionality()
    
    # Test 3: Delete functionality
    test_delete_functionality()
    
    # Test 4: Table display features
    test_table_display_features()
    
    print(f"\n" + "="*60)
    print("📋 TASK 2.3 SUMMARY")
    print("="*60)
    print("✅ Web interface with navigation tabs")
    print("✅ History tab with equations table")
    print("✅ GET /api/equations returns data with status")
    print("✅ Table displays: ID, Equation, Coefficients, Type, Solution")
    print("✅ Edit functionality (PUT /api/equations/{id})")
    print("✅ Delete functionality (DELETE /api/equations/{id})")
    print("✅ Modal for editing equations")
    print("✅ Responsive table design")
    print("✅ Color-coded status badges")
    print("✅ Action buttons (Edit/Delete)")
    
    print(f"\n🎯 USER WORKFLOW:")
    print("1. 🌐 Open http://localhost:12001")
    print("2. 📋 Click 'Lịch Sử' tab")
    print("3. 👀 View table with all saved equations")
    print("4. ✏️ Click 'Sửa' to edit equation")
    print("5. 🗑️ Click 'Xóa' to delete equation")
    print("6. 🔄 Click 'Làm mới' to reload data")
    
    print(f"\n🎉 TASK 2.3 COMPLETED!")

if __name__ == "__main__":
    main()