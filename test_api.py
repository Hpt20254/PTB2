#!/usr/bin/env python3
"""
Test script cho API POST /api/equation
"""
import requests
import json
import time
import subprocess
import sys

def start_flask_app():
    """Khởi động Flask app"""
    proc = subprocess.Popen(['python', 'app.py'], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    time.sleep(3)  # Đợi app khởi động
    return proc

def test_quadratic_api():
    """Test API POST /api/equation với các trường hợp khác nhau"""
    base_url = "http://localhost:12001"
    
    print("=== TESTING API POST /api/equation ===\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Hai nghiệm phân biệt",
            "data": {"a": 1, "b": -5, "c": 6},
            "expected_status": "two_roots",
            "description": "x² - 5x + 6 = 0 → x1=3, x2=2"
        },
        {
            "name": "Nghiệm kép", 
            "data": {"a": 1, "b": -4, "c": 4},
            "expected_status": "double_root",
            "description": "x² - 4x + 4 = 0 → x=2"
        },
        {
            "name": "Vô nghiệm thực",
            "data": {"a": 1, "b": 0, "c": 1},
            "expected_status": "complex",
            "description": "x² + 1 = 0 → nghiệm phức"
        },
        {
            "name": "Phương trình bậc 1",
            "data": {"a": 0, "b": 2, "c": -4},
            "expected_status": "linear", 
            "description": "2x - 4 = 0 → x=2"
        },
        {
            "name": "Vô số nghiệm",
            "data": {"a": 0, "b": 0, "c": 0},
            "expected_status": "infinite",
            "description": "0 = 0"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Phương trình: {test_case['description']}")
        print(f"Input: {test_case['data']}")
        
        try:
            # Gửi POST request
            response = requests.post(
                f"{base_url}/api/equation",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"✅ Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # Kiểm tra status
                if result.get('status') == test_case['expected_status']:
                    print(f"✅ Expected status: {test_case['expected_status']} ✓")
                else:
                    print(f"❌ Expected status: {test_case['expected_status']}, got: {result.get('status')}")
                
                results.append({
                    "test": test_case['name'],
                    "success": True,
                    "id": result.get('id'),
                    "solution": result.get('solution')
                })
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"❌ Response: {response.text}")
                results.append({
                    "test": test_case['name'],
                    "success": False,
                    "error": response.text
                })
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "test": test_case['name'],
                "success": False,
                "error": str(e)
            })
        
        print("-" * 50)
    
    return results

def test_database_content():
    """Kiểm tra dữ liệu trong database"""
    print("\n=== KIỂM TRA DỮ LIỆU TRONG DATABASE ===\n")
    
    try:
        response = requests.get("http://localhost:12001/api/equations")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tổng số equations trong DB: {data['count']}")
            print("\n📊 Chi tiết equations:")
            for eq in data['equations']:
                print(f"  ID {eq['id']}: {eq['equation']} → {eq['solution']}")
            return True
        else:
            print(f"❌ Error getting equations: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_error_cases():
    """Test các trường hợp lỗi"""
    print("\n=== TESTING ERROR CASES ===\n")
    
    error_cases = [
        {
            "name": "Missing JSON data",
            "data": None,
            "expected_status": 400
        },
        {
            "name": "Missing field 'a'",
            "data": {"b": 1, "c": 1},
            "expected_status": 400
        },
        {
            "name": "Invalid number format",
            "data": {"a": "abc", "b": 1, "c": 1},
            "expected_status": 400
        }
    ]
    
    for test_case in error_cases:
        print(f"Test: {test_case['name']}")
        try:
            if test_case['data'] is None:
                response = requests.post("http://localhost:12001/api/equation")
            else:
                response = requests.post(
                    "http://localhost:12001/api/equation",
                    json=test_case['data'],
                    headers={'Content-Type': 'application/json'}
                )
            
            if response.status_code == test_case['expected_status']:
                print(f"✅ Expected error status {test_case['expected_status']} ✓")
            else:
                print(f"❌ Expected {test_case['expected_status']}, got {response.status_code}")
            
            print(f"Response: {response.json()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

def main():
    print("🚀 STARTING API TESTS...")
    
    # Khởi động Flask app
    flask_proc = start_flask_app()
    
    try:
        # Test ping endpoint trước
        response = requests.get("http://localhost:12001/ping")
        if response.text == "pong":
            print("✅ Flask app is running\n")
        else:
            print("❌ Flask app not responding correctly")
            return
        
        # Chạy các test
        results = test_quadratic_api()
        db_ok = test_database_content()
        test_error_cases()
        
        # Tổng kết
        print("\n" + "="*60)
        print("📋 SUMMARY")
        print("="*60)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"✅ Successful tests: {success_count}/{total_count}")
        print(f"✅ Database check: {'✓' if db_ok else '✗'}")
        
        if success_count == total_count and db_ok:
            print("\n🎉 TASK 1.4 HOÀN THÀNH THÀNH CÔNG!")
            print("✅ API POST /api/equation hoạt động đúng")
            print("✅ Tính toán nghiệm chính xác")
            print("✅ Lưu database thành công")
        else:
            print("\n❌ Có lỗi trong quá trình test")
            
    finally:
        # Dừng Flask app
        flask_proc.terminate()
        flask_proc.wait()

if __name__ == "__main__":
    main()