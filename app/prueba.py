import mysql.connector

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


# def deleteprod(idprod):
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database='proyectosis',
#                                              user='root',
#                                              password='')

#         cursor = connection.cursor()
#         sql_insert_blob_query = """DELETE FROM productos WHERE id_producto = %s"""

        
#         cursor.execute(sql_insert_blob_query,[idprod] )
#         connection.commit()

#     except mysql.connector.Error as error:
#         print("Falla al borrar {}".format(error))

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

def insertBLOB(id_prod, name, price, desc, photo, id_cate, id_cat, id_est_prod):
    
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proyectosis',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO productos
                          (id_producto, nombre, precio, descripcion, imagen, id_categoria, id_catalogo, id_estado_producto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

        empPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (id_prod, name, price, desc, empPicture, id_cate, id_cat, id_est_prod)
        cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            


#insertBLOB(2, "Pan de Canela", 2.0, "Pan de Canela especial para compartir", "C:/Users/ignac/Desktop/fotos/PanCanela.jpeg", 3, 1, 1)

#! Sacar datos de un blob

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB(emp_id, photo, bioData):
    print("Reading BLOB data from python_employee table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proyectosis',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from productos where id = %s"""

        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            image = row[2]
            print("Storing employee image and bio-data on disk \n")
            write_file(image, photo)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# readBLOB(1, "D:\Python\Articles\my_SQL\query_output\eric_photo.png")