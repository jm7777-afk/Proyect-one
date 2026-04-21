from flask import Flask, request, jsonify, render_template, session
from database import init_db, register_user, verify_user, get_all_destinations, get_user_by_id
import os

app = Flask(__name__, template_folder='frontend', static_folder='frontend')
app.config['SECRET_KEY'] = 'travelup-secret-key-2025'
app.config['DATABASE'] = 'travelup.db'

# Inicializar base de datos al iniciar
with app.app_context():
    init_db()

# Rutas de la API
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'Todos los campos son requeridos'}), 400
        
        success, message = register_user(name, email, password)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error del servidor'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'success': False, 'message': 'Email y contraseña son requeridos'}), 400
        
        success, result = verify_user(email, password)
        
        if success:
            session['user_id'] = result['id']
            session['user_name'] = result['name']
            return jsonify({
                'success': True, 
                'message': 'Inicio de sesión exitoso', 
                'user': result['name']
            })
        else:
            return jsonify({'success': False, 'message': result}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error del servidor'}), 500

@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada'})

@app.route('/api/destinations')
def destinations():
    try:
        destinations_data = get_all_destinations()
        return jsonify(destinations_data)
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al obtener destinos'}), 500

@app.route('/api/user')
def get_user():
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        if user:
            return jsonify({'success': True, 'user': user})
    return jsonify({'success': False, 'message': 'Usuario no autenticado'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
