import mysql.connector


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

    #! TRABAJAR AQUI COMPLETANDO LA CONVERSION A BLOB DE LOS DATOS Y HACER UN TEST.
    # TODO ARREGLAR EL TAMANIO DE SUCURSALES
        # Convert data into tuple format
        insert_blob_tuple = (id_prod, name, price, desc,
                             empPicture, id_cate, id_cat, id_est_prod)
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


insertBLOB(1, "Pan de Chocolate", 3.00, "Pan hecho con chocolate para acompañar a la hora del té.",
           "C:\\Users\\ignac\\Desktop\\PanChocolate.jpeg", 1, 1, 1)
