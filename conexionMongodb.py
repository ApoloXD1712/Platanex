import pymongo

mongoHost = "localhost"
mongoPuerto = "27017"
tiempoFuera = 1000
url = "mongodb://"+mongoHost+":"+mongoPuerto+"/"
mongoBaseDatos = "platanex"
mongoColeccion = "cosecha"
mongoColeccion1 = "embarque"



try:
    cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS = tiempoFuera)
    #cliente.server_info()
    #print("Conexion establecida")
    cliente.close()
except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("tiempo excedido")
except pymongo.errors.ConnectionFailure as errorConexion:
    print("La conexion ha fallado")