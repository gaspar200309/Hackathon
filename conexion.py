import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="link79743114200309",
    database="derechos_reales"
)

def estado_tramite(nrotramite):
    cursor = conexion.cursor()
    consulta = "SELECT * FROM tramite tr, en_demora de where tr.nrotramite = "+nrotramite+" and tr.idtramite = de.idtramite"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    if len(datos) != 0: return "en_demora"
    
    consulta = "SELECT * FROM tramite tr, listo li where tr.nrotramite = "+nrotramite+" and tr.idtramite = li.idtramite"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    if len(datos) != 0: return "listo"
    
    consulta = "SELECT * FROM tramite tr, observado ob where tr.nrotramite = "+nrotramite+" and tr.idtramite = ob.idtramite"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    if len(datos) != 0: return "observado"


##cursor.close()
#conexion.close()

def en_demora(nrotramite):
    cursor = conexion.cursor()
    consulta = "SELECT de.fecha_limite FROM tramite tr, en_demora de where tr.nrotramite = "+nrotramite+" and tr.idtramite = de.idtramite"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    return datos[0]

def listo(nrotramite):
    cursor = conexion.cursor()
    consulta = "SELECT li.fecha_aceptado,li.fecha_recojo FROM tramite tr, listo li where tr.nrotramite = "+nrotramite+" and tr.idtramite = li.idtramite"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    return datos[0]

def observado(nrotramite):
    cursor = conexion.cursor()
    consulta = "SELECT ob.descripcion, ob.fecha_limite_subsanacion FROM tramite tr, observado ob where tr.nrotramite = "+nrotramite+" and tr.idtramite = ob.idtramite"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    return datos[0]

def agregarTramitador():
    cursor = conexion.cursor()
    nuevo_registro = ("adolfo", "98765432")
    consulta = "INSERT INTO tramitador(nombre, telefono) VALUES (%s, %s)"
    cursor.execute(consulta, nuevo_registro)
    conexion.commit()
    cursor.close()
