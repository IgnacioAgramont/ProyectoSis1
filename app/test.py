import mysql.connector


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, desc, photo):
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

        # Convert data into tuple format
        insert_blob_tuple = (name, desc, empPicture)
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

insertBLOB("Ignacio", "Ignacio apellida Agramont",
           "C:/Users/ignac/Desktop/Speaker1.jpg")
insertBLOB("Javier", "Javier es buena onda",
           "C:/Users/ignac/Desktop/perronaldo.png")