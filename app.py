from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import math

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'gptb2_db')

# Create database connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configure Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Equation model
class Equation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float)
    b = db.Column(db.Float)
    c = db.Column(db.Float)
    solution = db.Column(db.String(100))
    status = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<Equation {self.id}: {self.a}x² + {self.b}x + {self.c} = 0>'

def solve_quadratic(a, b, c):
    """
    Giải phương trình bậc 2: ax² + bx + c = 0
    Trả về tuple (status, solution_text)
    """
    if a == 0:
        if b == 0:
            if c == 0:
                return "infinite", "Vô số nghiệm"
            else:
                return "no_solution", "Vô nghiệm"
        else:
            # Phương trình bậc 1: bx + c = 0
            x = -c / b
            return "linear", f"x = {x}"
    
    # Phương trình bậc 2
    discriminant = b * b - 4 * a * c
    
    if discriminant > 0:
        # Hai nghiệm phân biệt
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return "two_roots", f"x1 = {x1}, x2 = {x2}"
    elif discriminant == 0:
        # Nghiệm kép
        x = -b / (2 * a)
        return "double_root", f"x = {x}"
    else:
        # Vô nghiệm (nghiệm phức)
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-discriminant) / (2 * a)
        return "complex", f"x1 = {real_part} + {imaginary_part}i, x2 = {real_part} - {imaginary_part}i"

@app.route('/')
def index():
    """Trang chủ - giao diện nhập hệ số"""
    return render_template('index.html')

@app.route('/ping')
def ping():
    return "pong"

@app.route('/api/equation', methods=['POST'])
def create_equation():
    try:
        # Lấy dữ liệu từ request JSON
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'a' not in data or 'b' not in data or 'c' not in data:
            return jsonify({"error": "Missing required fields: a, b, c"}), 400
        
        try:
            a = float(data['a'])
            b = float(data['b'])
            c = float(data['c'])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number format for a, b, or c"}), 400
        
        # Giải phương trình
        status, solution = solve_quadratic(a, b, c)
        
        # Lưu vào database
        equation = Equation(a=a, b=b, c=c, solution=solution, status=status)
        db.session.add(equation)
        db.session.commit()
        
        # Trả về kết quả
        return jsonify({
            "success": True,
            "id": equation.id,
            "equation": f"{a}x² + {b}x + {c} = 0",
            "status": status,
            "solution": solution,
            "coefficients": {
                "a": a,
                "b": b,
                "c": c
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/equations', methods=['GET'])
def get_all_equations():
    """GET: Lấy tất cả equations từ database"""
    try:
        equations = Equation.query.all()
        result = []
        for eq in equations:
            result.append({
                "id": eq.id,
                "a": eq.a,
                "b": eq.b,
                "c": eq.c,
                "solution": eq.solution,
                "status": eq.status,
                "equation": f"{eq.a}x² + {eq.b}x + {eq.c} = 0"
            })
        return jsonify({
            "success": True,
            "count": len(result),
            "equations": result
        })
    except Exception as e:
        return jsonify({"error": f"Error retrieving equations: {str(e)}"}), 500

@app.route('/api/equations/<int:equation_id>', methods=['GET'])
def get_equation_by_id(equation_id):
    """GET: Lấy một equation theo ID"""
    try:
        equation = Equation.query.get(equation_id)
        if not equation:
            return jsonify({"error": f"Equation with ID {equation_id} not found"}), 404
        
        return jsonify({
            "success": True,
            "equation": {
                "id": equation.id,
                "a": equation.a,
                "b": equation.b,
                "c": equation.c,
                "solution": equation.solution,
                "status": equation.status,
                "equation": f"{equation.a}x² + {equation.b}x + {equation.c} = 0"
            }
        })
    except Exception as e:
        return jsonify({"error": f"Error retrieving equation: {str(e)}"}), 500

@app.route('/api/equations/<int:equation_id>', methods=['PUT'])
def update_equation(equation_id):
    """PUT: Cập nhật equation theo ID, sửa a,b,c và giải lại"""
    try:
        # Tìm equation theo ID
        equation = Equation.query.get(equation_id)
        if not equation:
            return jsonify({"error": f"Equation with ID {equation_id} not found"}), 404
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate input (có thể update từng phần hoặc tất cả)
        a = float(data.get('a', equation.a))
        b = float(data.get('b', equation.b))
        c = float(data.get('c', equation.c))
        
        # Giải lại phương trình với hệ số mới
        status, solution = solve_quadratic(a, b, c)
        
        # Cập nhật equation
        old_equation = f"{equation.a}x² + {equation.b}x + {equation.c} = 0"
        equation.a = a
        equation.b = b
        equation.c = c
        equation.solution = solution
        equation.status = status
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Equation updated successfully",
            "id": equation.id,
            "old_equation": old_equation,
            "new_equation": f"{a}x² + {b}x + {c} = 0",
            "status": status,
            "solution": solution,
            "coefficients": {
                "a": a,
                "b": b,
                "c": c
            }
        })
        
    except ValueError:
        return jsonify({"error": "Invalid number format for a, b, or c"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating equation: {str(e)}"}), 500

@app.route('/api/equations/<int:equation_id>', methods=['DELETE'])
def delete_equation(equation_id):
    """DELETE: Xóa equation theo ID"""
    try:
        # Tìm equation theo ID
        equation = Equation.query.get(equation_id)
        if not equation:
            return jsonify({"error": f"Equation with ID {equation_id} not found"}), 404
        
        # Lưu thông tin trước khi xóa
        deleted_info = {
            "id": equation.id,
            "equation": f"{equation.a}x² + {equation.b}x + {equation.c} = 0",
            "solution": equation.solution
        }
        
        # Xóa equation
        db.session.delete(equation)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Equation with ID {equation_id} deleted successfully",
            "deleted_equation": deleted_info
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting equation: {str(e)}"}), 500

@app.route('/db-test')
def db_test():
    try:
        # Test database connection
        from sqlalchemy import text
        result = db.session.execute(text("SELECT 1 as test"))
        return {"status": "success", "message": "Database connection successful", "result": result.fetchone()[0]}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}

@app.route('/create-tables')
def create_tables():
    try:
        # Create all tables
        db.create_all()
        return {"status": "success", "message": "Tables created successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to create tables: {str(e)}"}

@app.route('/test-model')
def test_model():
    try:
        # Test creating an equation record
        equation = Equation(a=1.0, b=-5.0, c=6.0, solution="x1=2, x2=3")
        db.session.add(equation)
        db.session.commit()
        
        # Query the record back
        saved_equation = Equation.query.first()
        return {
            "status": "success", 
            "message": "Model test successful",
            "equation": {
                "id": saved_equation.id,
                "a": saved_equation.a,
                "b": saved_equation.b,
                "c": saved_equation.c,
                "solution": saved_equation.solution
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Model test failed: {str(e)}"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12001)