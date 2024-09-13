import sqlite3
connection = sqlite3.connect('BeanBrew.db', check_same_thread=False) #Will create DB if it doesn't already exist


def joinTables():
    sales = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Sale.id, Product.productName, Product.productDescription, Product.price,
                   Customer.firstName, Customer.lastName, Customer.email, Customer.Phone, 
                   Sale.date, Sale.time
            FROM Sale
            JOIN Product ON Sale.productID = Product.id
            JOIN Customer ON Sale.customerID = Customer.rowid
        """)
        sales = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()

    print(sales)


joinTables()



joinTables()



joinTables()
