from flask import Flask, render_template, request
import openpyxl
import qrcode
from io import BytesIO

app = Flask(__name__)

# Base de datos temporal en memoria
clientes = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', clientes=clientes)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    clave_cliente = request.form['clave_cliente']
    nombre_contacto = request.form['nombre_contacto']
    correo = request.form['correo']
    telefono = request.form['telefono']
    
    # Validar si la clave de cliente ya existe
    if any(cliente['clave_cliente'] == clave_cliente for cliente in clientes):
        return 'La clave de cliente ya existe. Por favor, utiliza una clave diferente.'

    # Generar el código QR con los datos
    data = f"Clave Cliente: {clave_cliente}\nNombre Contacto: {nombre_contacto}\nCorreo: {correo}\nTeléfono: {telefono}"
    qr = qrcode.make(data)

    # Guardar los datos del cliente y su código QR
    cliente = {
        'clave_cliente': clave_cliente,
        'nombre_contacto': nombre_contacto,
        'correo': correo,
        'telefono': telefono,
        'codigo_qr': qr
    }
    clientes.append(cliente)

    return render_template('index.html', clientes=clientes)

@app.route('/edit_cliente/<clave_cliente>', methods=['GET'])
def edit_cliente(clave_cliente):
    cliente = next((cliente for cliente in clientes if cliente['clave_cliente'] == clave_cliente), None)
    if cliente:
        return render_template('edit_cliente.html', cliente=cliente)
    
    return 'No se encontró el cliente especificado.'

@app.route('/update_cliente', methods=['POST'])
def update_cliente():
    clave_cliente = request.form['clave_cliente']
    nombre_contacto = request.form['nombre_contacto']
    correo = request.form['correo']
    telefono = request.form['telefono']
    
    # Buscar el cliente a actualizar
    cliente = next((cliente for cliente in clientes if cliente['clave_cliente'] == clave_cliente), None)
    if cliente:
        # Actualizar los datos del cliente
        cliente['nombre_contacto'] = nombre_contacto
        cliente['correo'] = correo
        cliente['telefono'] = telefono

        # Generar el nuevo código QR con los datos actualizados
        data = f"Clave Cliente: {clave_cliente}\nNombre Contacto: {nombre_contacto}\nCorreo: {correo}\nTeléfono: {telefono}"
        qr = qrcode.make(data)
        cliente['codigo_qr'] = qr

        return render_template('index.html', clientes=clientes)
    
    return 'No se encontró el cliente especificado.'

@app.route('/delete_cliente/<clave_cliente>', methods=['GET'])
def delete_cliente(clave_cliente):
    # Eliminar el cliente con la clave especificada
    clientes[:] = [cliente for cliente in clientes if cliente['clave_cliente'] != clave_cliente]
    return render_template('index.html', clientes=clientes)

@app.route('/view_qr/<clave_cliente>', methods=['GET'])
def view_qr(clave_cliente):
    # Obtener el código QR del cliente con la clave especificada
    qr = next((cliente['codigo_qr'] for cliente in clientes if cliente['clave_cliente'] == clave_cliente), None)
    if qr:
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)
        return qr_io.getvalue()

    return 'No se encontró el código QR para el cliente especificado.'

if __name__ == '__main__':
    app.run()
