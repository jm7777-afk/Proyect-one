import sqlite3
import hashlib
import os

def init_db():
    """Inicializar la base de datos"""
    conn = sqlite3.connect('travelup.db')
    c = conn.cursor()
    
    # Crear tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password_hash TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Crear tabla de destinos
    c.execute('''CREATE TABLE IF NOT EXISTS destinations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 description TEXT NOT NULL,
                 image_url TEXT NOT NULL,
                 category TEXT NOT NULL)''')
    
    # Insertar datos de ejemplo si no existen
    c.execute("SELECT COUNT(*) FROM destinations")
    if c.fetchone()[0] == 0:
        sample_destinations = [
            ("Descubre el Mundo", "Explora los destinos más increíbles del planeta con Travel Up", "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", "Aventura"),
            ("Playas Paradisíacas", "Relájate en las playas más exóticas y cristalinas del mundo", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", "Playa"),
            ("Cultura y Aventura", "Sumérgete en culturas fascinantes y vive experiencias únicas", "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", "Cultural"),
            ("Naturaleza Salvaje", "Conecta con la naturaleza en los paisajes más impresionantes", "https://images.unsplash.com/photo-1418065460487-3e41a6c84dc5?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", "Naturaleza")
        ]
        c.executemany("INSERT INTO destinations (title, description, image_url, category) VALUES (?, ?, ?, ?)", sample_destinations)
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashear contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password):
    """Registrar nuevo usuario"""
    conn = sqlite3.connect('travelup.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                 (name, email, hash_password(password)))
        conn.commit()
        return True, "Usuario registrado correctamente"
    except sqlite3.IntegrityError:
        return False, "El usuario ya existe"
    finally:
        conn.close()

def verify_user(email, password):
    """Verificar credenciales de usuario"""
    conn = sqlite3.connect('travelup.db')
    c = conn.cursor()
    c.execute("SELECT id, name, password_hash FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):
        return True, {"id": user[0], "name": user[1], "email": email}
    return False, "Credenciales incorrectas"

def get_all_destinations():
    """Obtener todos los destinos"""
    conn = sqlite3.connect('travelup.db')
    c = conn.cursor()
    c.execute("SELECT id, title, description, image_url, category FROM destinations")
    destinations = []
    for row in c.fetchall():
        destinations.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'image_url': row[3],
            'category': row[4]
        })
    conn.close()
    return destinations

def get_user_by_id(user_id):
    """Obtener usuario por ID"""
    conn = sqlite3.connect('travelup.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return {"id": user[0], "name": user[1], "email": user[2]}
    return None