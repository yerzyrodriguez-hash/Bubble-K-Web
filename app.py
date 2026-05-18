from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'bubbleklzt_secreto_super_seguro' 
PRODUCTOS = [
    {
        "id": 1, 
        "nombre": "Álbum 'Glitch Mode' (Digipack) - NCT Dream", 
        "precio": 25.00, 
        "imagen": "/static/img/glitch_mode.jpg", 
        "desc": "¡Novedad! Ya puedes conseguir tu álbum versión digipack."
    },
    {
        "id": 2, 
        "nombre": "Álbum 'Shalala' (Smini) - Taeyong (NCT)", 
        "precio": 25.00, 
        "imagen": "/static/img/shalala.jpg", 
        "desc": "¡Novedad! Álbum debut de Taeyong versión Smini."
    },
    {
        "id": 3, 
        "nombre": "Álbum 'Hate XX' (Like & Hate) - Yena", 
        "precio": 29.00, 
        "imagen": "/static/img/hateXX.jpg", 
        "desc": "¡Novedad! Mini álbum Hate XX con versiones Like y Hate."
    },
    {
        "id": 4, 
        "nombre": "Cesta K-Pop (Cumpleaños)", 
        "precio": 30.00, 
        "imagen": "/static/img/Cesta_cumpleaños.jpeg", 
        "desc": "Formato cesta con regalitos sorpresa. *Pedir con 5 días de antelación."
    },
    {
        "id": 5, 
        "nombre": "Cesta K-Pop (San Valentín)", 
        "precio": 30.00, 
        "imagen": "/static/img/Cesta_SanValentin.jpeg", 
        "desc": "Ideal para sorprender. Incluye regalitos sorpresa. *Pedir con 5 días de antelación."
    },
    {
        "id": 6, 
        "nombre": "Cesta K-Pop (Aniversario)", 
        "precio": 30.00, 
        "imagen": "/static/img/Cesta_aniversario.jpeg", 
        "desc": "Celebra fechas especiales con regalitos extra. *Pedir con 5 días de antelación."
    }
]

@app.route('/')
def inicio():
    return render_template('index.html', productos=PRODUCTOS)

# NUEVA RUTA: Para procesar el clic en "Agregar"
@app.route('/agregar_carrito/<int:id>', methods=['POST'])
def agregar_carrito(id):
    if 'carrito' not in session:
        session['carrito'] = []
    producto = next((p for p in PRODUCTOS if p['id'] == id), None)
    if producto:
        carrito_actual = session['carrito']
        carrito_actual.append(producto)
        session['carrito'] = carrito_actual
    return jsonify({
        "success": True,
        "cantidad_carrito": len(session['carrito'])
    })

# NUEVA RUTA: Para ver la página del carrito
@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] for item in carrito)
    return render_template('cart.html', carrito=carrito, total=total)

# NUEVA RUTA: Para eliminar un producto del carrito
@app.route('/eliminar_carrito/<int:index>', methods=['POST'])
def eliminar_carrito(index):
    if 'carrito' in session:
        carrito_actual = session['carrito']
        if 0 <= index < len(carrito_actual):
            carrito_actual.pop(index)
            session['carrito'] = carrito_actual
    return redirect(url_for('ver_carrito'))

# NUEVA RUTA: Pantalla exclusiva para llenar los datos
@app.route('/checkout')
def checkout():
    carrito = session.get('carrito', [])
    if not carrito:
        return redirect(url_for('inicio'))
    total = sum(item['precio'] for item in carrito)
    return render_template('checkout.html', carrito=carrito, total=total)

# RUTA ACTUALIZADA: Pantalla final de éxito que vacía el carrito
@app.route('/pagar')
def pagar():
    session.pop('carrito', None)
    return render_template('exito.html')


if __name__ == '__main__':
    app.run(debug=True)
    
