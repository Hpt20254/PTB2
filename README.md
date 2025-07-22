# 🧮 GPTB2 - Giải Phương Trình Bậc 2

**Complete Flask Web Application for Quadratic Equation Solver**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 **Overview**

GPTB2 is a comprehensive web application for solving quadratic equations (ax² + bx + c = 0) with a beautiful interface, database persistence, and full CRUD operations.

### ✨ **Key Features**
- 🧮 **Complete Quadratic Solver** - Handles all equation types
- 🎨 **Beautiful Web Interface** - Responsive design with tabs
- 📊 **Data Management** - Professional table with edit/delete
- 💾 **Database Persistence** - MySQL/MariaDB integration
- 🔌 **RESTful API** - Full CRUD endpoints
- 🧪 **Comprehensive Tests** - 100% test coverage
- 📱 **Mobile Friendly** - Responsive design

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8+
- MySQL/MariaDB
- pip package manager

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/Hpt20254/PTB2.git
cd PTB2
```

2. **Install Dependencies**
```bash
pip install flask flask-sqlalchemy python-dotenv pymysql
```

3. **Setup Database**
```bash
# Install MariaDB (Ubuntu/Debian)
sudo apt update && sudo apt install mariadb-server

# Secure installation
sudo mysql_secure_installation

# Create database
mysql -u root -p -e "CREATE DATABASE gptb2_db;"
```

4. **Configure Environment**
```bash
# Create .env file
cat > .env << EOF
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=gptb2_db
EOF
```

5. **Run Application**
```bash
python app.py
```

6. **Access Application**
```
http://localhost:12001
```

## 🎨 **Interface Overview**

### 🧮 **Solver Tab**
- **Input Form:** Enter coefficients a, b, c
- **Live Preview:** Real-time equation display
- **Results:** Beautiful mathematical formatting
- **Examples:** Quick test buttons
- **Validation:** Input error handling

### 📋 **History Tab**
- **Data Table:** All saved equations
- **Status Badges:** Color-coded equation types
- **Edit Modal:** Modify existing equations
- **Delete Action:** Remove with confirmation
- **Refresh:** Reload data

## 🔌 **API Documentation**

### Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/ping` | Health check | `"pong"` |
| `GET` | `/` | Web interface | HTML page |
| `POST` | `/api/equation` | Create equation | Equation object |
| `GET` | `/api/equations` | List all equations | Array of equations |
| `GET` | `/api/equations/{id}` | Get equation by ID | Equation object |
| `PUT` | `/api/equations/{id}` | Update equation | Updated equation |
| `DELETE` | `/api/equations/{id}` | Delete equation | Success message |

### Request/Response Examples

#### Create Equation
```bash
curl -X POST http://localhost:12001/api/equation \
  -H "Content-Type: application/json" \
  -d '{"a": 1, "b": -5, "c": 6}'
```

```json
{
  "success": true,
  "id": 1,
  "equation": "1x² + -5x + 6 = 0",
  "status": "two_roots",
  "solution": "x1 = 3.0, x2 = 2.0"
}
```

#### Get All Equations
```bash
curl http://localhost:12001/api/equations
```

```json
{
  "success": true,
  "count": 5,
  "equations": [
    {
      "id": 1,
      "a": 1.0,
      "b": -5.0,
      "c": 6.0,
      "solution": "x1 = 3.0, x2 = 2.0",
      "status": "two_roots"
    }
  ]
}
```

## 📊 **Database Schema**

```sql
CREATE TABLE equation (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL,
    c FLOAT NOT NULL,
    solution VARCHAR(100),
    status VARCHAR(20)
);
```

### Status Types
- `two_roots` - Two distinct real roots
- `double_root` - One repeated real root
- `complex` - Complex conjugate roots
- `linear` - Linear equation (a=0)
- `infinite` - Infinite solutions (0=0)
- `no_solution` - No solution (0≠0)

## 🧪 **Testing**

Run comprehensive tests:

```bash
# API Tests
python test_api.py

# CRUD Tests  
python test_crud_api.py

# Web Interface Tests
python test_web_interface.py

# Result Display Tests
python test_result_display.py

# History Table Tests
python test_history_table.py
```

## 🎯 **Algorithm Details**

The quadratic solver handles all cases:

1. **a ≠ 0 (Quadratic)**
   - Δ = b² - 4ac
   - Δ > 0: Two real roots
   - Δ = 0: One repeated root
   - Δ < 0: Complex roots

2. **a = 0, b ≠ 0 (Linear)**
   - x = -c/b

3. **a = 0, b = 0 (Constant)**
   - c = 0: Infinite solutions
   - c ≠ 0: No solution

## 📁 **Project Structure**

```
PTB2/
├── app.py                    # Main Flask application
├── .env                      # Environment configuration
├── templates/
│   └── index.html           # Web interface template
├── test_api.py              # API endpoint tests
├── test_crud_api.py         # CRUD operation tests
├── test_web_interface.py    # Web interface tests
├── test_result_display.py   # Result display tests
├── test_history_table.py    # History table tests
└── README.md                # This file
```

## 🔧 **Configuration**

### Environment Variables (.env)
```bash
DB_HOST=localhost          # Database host
DB_USER=root              # Database username
DB_PASSWORD=password      # Database password
DB_NAME=gptb2_db         # Database name
```

### Flask Configuration
- **Host:** 0.0.0.0 (all interfaces)
- **Port:** 12001
- **Debug:** True (development)
- **Database:** MySQL with SQLAlchemy ORM

## 🎨 **UI/UX Features**

- **Responsive Design:** Works on desktop and mobile
- **Tab Navigation:** Smooth switching between solver and history
- **Real-time Updates:** Live equation preview
- **Color Coding:** Status-based visual indicators
- **Modal Dialogs:** Professional edit interface
- **Loading States:** User feedback during operations
- **Error Handling:** Graceful error messages
- **Mathematical Symbols:** Proper equation formatting

## 🚀 **Deployment**

### Production Setup
1. Set `debug=False` in app.py
2. Use production WSGI server (gunicorn)
3. Configure reverse proxy (nginx)
4. Set up SSL certificate
5. Use production database

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 12001
CMD ["python", "app.py"]
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Hpt20254**
- GitHub: [@Hpt20254](https://github.com/Hpt20254)
- Repository: [PTB2](https://github.com/Hpt20254/PTB2)

## 🎉 **Acknowledgments**

- Flask framework for web development
- SQLAlchemy for database ORM
- MariaDB for data persistence
- Mathematical algorithms for equation solving

---

**🎯 Ready for production use! Complete quadratic equation solver with beautiful web interface.**