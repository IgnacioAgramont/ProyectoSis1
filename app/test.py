import mysql.connector
import re

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(id_prod, name, price, desc, photo, id_cate, id_cat, id_est_prod):
    print("Inserting BLOB into productos table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proyectosis',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO productos
                          (id_producto, nombre, precio, descripcion, imagen, id_categoria, id_catalogo, id_estado_producto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",

        empPicture = convertToBinaryData(photo)
        print (type(empPicture))
        # id_prod = re.sub('[^a-zA-Z]', '', str(id_prod))
        # id_prod = re.sub('[^a-zA-Z]', '', str(id_prod))
        # id_prod = re.sub('[^a-zA-Z]', '', str(id_prod))
        # id_prod = re.sub('[^a-zA-Z]', '', str(id_prod))

        print("id_prod: ",id_prod)
        print(type(id_prod))
        print("name:" , name)
        print(type(name))
        print("price: ", price)
        print(type(price))
        print("desc: ", desc)
        print(type(desc))
        print("photo: ",photo)
        print(type(photo))
        print("id_cate: ",id_cate)
        print(type(id_cate))
        print("id_cat: ",id_cat)
        print(type(id_cat))
        print("id_est_prod: ",id_est_prod)
        print(type(id_est_prod))
        
    #! TRABAJAR AQUI COMPLETANDO LA CONVERSION A BLOB DE LOS DATOS Y HACER UN TEST.
    # TODO ARREGLAR EL TAMANIO DE SUCURSALES
        # Convert data into tuple format
        insert_blob_tuple = (id_prod, name, price, desc, empPicture, id_cate, id_cat, id_est_prod)

        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into productos table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


insertBLOB(1, "Pan de Chocolate", 3.0, "Pan hecho con chocolate", "C:/Users/ignac/Desktop/fotos/PanChocolate.jpg", 3, 1, 1)
