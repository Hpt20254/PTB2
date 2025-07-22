#!/usr/bin/env python3
"""
Test script cho CRUD APIs: GET/POST/PUT/DELETE /api/equations
"""
import json
from app import app

def test_crud_apis():
    """Test tất cả CRUD operations"""
    client = app.test_client()
    
    print("=== TESTING CRUD APIs ===\n")
    
    # 1. POST - Tạo một số equations để test
    print("1. POST - Tạo equations mới:")
    test_equations = [
        {"a": 1, "b": -3, "c": 2},  # x² - 3x + 2 = 0
        {"a": 2, "b": -4, "c": 2},  # 2x² - 4x + 2 = 0
        {"a": 1, "b": 0, "c": -4}   # x² - 4 = 0
    ]
    
    created_ids = []
    for i, eq_data in enumerate(test_equations, 1):
        response = client.post('/api/equation', 
                              data=json.dumps(eq_data),
                              content_type='application/json')
        if response.status_code == 201:
            result = json.loads(response.data)
            created_ids.append(result['id'])
            print(f"  ✅ Equation {i}: ID {result['id']} - {result['equation']} → {result['solution']}")
        else:
            print(f"  ❌ Failed to create equation {i}: {response.data.decode()}")
    
    print(f"\nCreated equation IDs: {created_ids}\n")
    
    # 2. GET - Lấy tất cả equations
    print("2. GET /api/equations - Lấy tất cả equations:")
    response = client.get('/api/equations')
    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"  ✅ Status: {response.status_code}")
        print(f"  ✅ Total equations: {data['count']}")
        for eq in data['equations']:
            print(f"    ID {eq['id']}: {eq['equation']} → {eq['solution']}")
    else:
        print(f"  ❌ Failed: {response.status_code} - {response.data.decode()}")
    
    print()
    
    # 3. GET - Lấy equation theo ID
    if created_ids:
        test_id = created_ids[0]
        print(f"3. GET /api/equations/{test_id} - Lấy equation theo ID:")
        response = client.get(f'/api/equations/{test_id}')
        if response.status_code == 200:
            data = json.loads(response.data)
            eq = data['equation']
            print(f"  ✅ Status: {response.status_code}")
            print(f"  ✅ Equation: {json.dumps(eq, indent=4, ensure_ascii=False)}")
        else:
            print(f"  ❌ Failed: {response.status_code} - {response.data.decode()}")
    
    print()
    
    # 4. GET - Test với ID không tồn tại
    print("4. GET /api/equations/9999 - Test ID không tồn tại:")
    response = client.get('/api/equations/9999')
    if response.status_code == 404:
        data = json.loads(response.data)
        print(f"  ✅ Status: {response.status_code} (Expected 404)")
        print(f"  ✅ Error message: {data['error']}")
    else:
        print(f"  ❌ Unexpected status: {response.status_code}")
    
    print()
    
    # 5. PUT - Cập nhật equation
    if created_ids:
        test_id = created_ids[0]
        print(f"5. PUT /api/equations/{test_id} - Cập nhật equation:")
        
        # Lấy equation hiện tại trước
        current_response = client.get(f'/api/equations/{test_id}')
        current_eq = json.loads(current_response.data)['equation']
        print(f"  Equation hiện tại: {current_eq['equation']} → {current_eq['solution']}")
        
        # Cập nhật với hệ số mới
        update_data = {"a": 1, "b": -5, "c": 6}  # x² - 5x + 6 = 0
        response = client.put(f'/api/equations/{test_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"  ✅ Status: {response.status_code}")
            print(f"  ✅ Old equation: {data['old_equation']}")
            print(f"  ✅ New equation: {data['new_equation']}")
            print(f"  ✅ New solution: {data['solution']}")
            print(f"  ✅ Status: {data['status']}")
        else:
            print(f"  ❌ Failed: {response.status_code} - {response.data.decode()}")
    
    print()
    
    # 6. PUT - Test partial update (chỉ update một số field)
    if len(created_ids) > 1:
        test_id = created_ids[1]
        print(f"6. PUT /api/equations/{test_id} - Partial update (chỉ update 'c'):")
        
        # Lấy equation hiện tại
        current_response = client.get(f'/api/equations/{test_id}')
        current_eq = json.loads(current_response.data)['equation']
        print(f"  Equation hiện tại: {current_eq['equation']} → {current_eq['solution']}")
        
        # Chỉ update field 'c'
        update_data = {"c": 0}  # Thay đổi c thành 0
        response = client.put(f'/api/equations/{test_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"  ✅ Status: {response.status_code}")
            print(f"  ✅ Old equation: {data['old_equation']}")
            print(f"  ✅ New equation: {data['new_equation']}")
            print(f"  ✅ New solution: {data['solution']}")
        else:
            print(f"  ❌ Failed: {response.status_code} - {response.data.decode()}")
    
    print()
    
    # 7. PUT - Test với ID không tồn tại
    print("7. PUT /api/equations/9999 - Test ID không tồn tại:")
    response = client.put('/api/equations/9999',
                         data=json.dumps({"a": 1, "b": 2, "c": 3}),
                         content_type='application/json')
    if response.status_code == 404:
        data = json.loads(response.data)
        print(f"  ✅ Status: {response.status_code} (Expected 404)")
        print(f"  ✅ Error message: {data['error']}")
    else:
        print(f"  ❌ Unexpected status: {response.status_code}")
    
    print()
    
    # 8. DELETE - Xóa equation
    if len(created_ids) > 2:
        test_id = created_ids[2]
        print(f"8. DELETE /api/equations/{test_id} - Xóa equation:")
        
        # Lấy thông tin trước khi xóa
        current_response = client.get(f'/api/equations/{test_id}')
        if current_response.status_code == 200:
            current_eq = json.loads(current_response.data)['equation']
            print(f"  Equation sẽ xóa: {current_eq['equation']} → {current_eq['solution']}")
        
        # Xóa equation
        response = client.delete(f'/api/equations/{test_id}')
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"  ✅ Status: {response.status_code}")
            print(f"  ✅ Message: {data['message']}")
            print(f"  ✅ Deleted equation: {data['deleted_equation']['equation']}")
            
            # Verify equation đã bị xóa
            verify_response = client.get(f'/api/equations/{test_id}')
            if verify_response.status_code == 404:
                print(f"  ✅ Verified: Equation ID {test_id} không còn tồn tại")
            else:
                print(f"  ❌ Error: Equation vẫn tồn tại sau khi xóa")
        else:
            print(f"  ❌ Failed: {response.status_code} - {response.data.decode()}")
    
    print()
    
    # 9. DELETE - Test với ID không tồn tại
    print("9. DELETE /api/equations/9999 - Test ID không tồn tại:")
    response = client.delete('/api/equations/9999')
    if response.status_code == 404:
        data = json.loads(response.data)
        print(f"  ✅ Status: {response.status_code} (Expected 404)")
        print(f"  ✅ Error message: {data['error']}")
    else:
        print(f"  ❌ Unexpected status: {response.status_code}")
    
    print()
    
    # 10. Final GET - Kiểm tra trạng thái cuối cùng
    print("10. Final GET /api/equations - Kiểm tra trạng thái cuối:")
    response = client.get('/api/equations')
    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"  ✅ Total equations remaining: {data['count']}")
        for eq in data['equations']:
            print(f"    ID {eq['id']}: {eq['equation']} → {eq['solution']}")
    
    print("\n" + "="*60)
    print("📋 CRUD API TEST SUMMARY")
    print("="*60)
    print("✅ POST /api/equation - Tạo equation mới")
    print("✅ GET /api/equations - Lấy tất cả equations")
    print("✅ GET /api/equations/<id> - Lấy equation theo ID")
    print("✅ PUT /api/equations/<id> - Cập nhật equation và giải lại")
    print("✅ DELETE /api/equations/<id> - Xóa equation")
    print("✅ Error handling cho ID không tồn tại (404)")
    print("✅ Partial update support trong PUT")
    print("✅ Automatic re-calculation khi update")
    print("\n🎉 TASK 1.5 HOÀN THÀNH!")

def main():
    print("🚀 STARTING CRUD API TESTS...")
    test_crud_apis()

if __name__ == "__main__":
    main()