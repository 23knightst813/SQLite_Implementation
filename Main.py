from flask import Flask, render_template, redirect, render_template, request #Flask library and functions
import sqlite3 #Our database
import datetime #Used to display current date & time

#Instantiate Flask App
app = Flask(__name__)

#Connection to DB
connection = sqlite3.connect('BeanBrew.db', check_same_thread=False) #Will create DB if it doesn't already exist

# Set up product table if it doesn't exist already
query = """CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, productName TEXT NOT NULL, productDescription TEXT NOT NULL, price REAL NOT NULL);"""
cursor = connection.cursor()
cursor.execute(query)
cursor.close()

# Add Customers Table
query = """CREATE TABLE IF NOT EXISTS customer(CustomerID INTEGER PRIMARY KEY, firstName TEXT NOT NULL, lastName TEXT NOT NULL, email TEXT NOT NULL, Phone TEXT NOT NULL);"""
cursor = connection.cursor()
cursor.execute(query)
cursor.close()

# Add Sales Table
query = """CREATE TABLE IF NOT EXISTS sale(id INTEGER PRIMARY KEY, productID INTEGER NOT NULL, customerID INTEGER NOT NULL, date TEXT NOT NULL, time TEXT NOT NULL, FOREIGN KEY(productID) REFERENCES product(id), FOREIGN KEY(customerID) REFERENCES customer(id));"""
cursor = connection.cursor()
cursor.execute(query)
cursor.close()

def getCurrentDateTime():
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    return date.strftime("%d/%m/%Y"), time.strftime("%X") #Format the date and time correctly before returning.

def getProducts(): #Query our table to retrieve all of our products
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        products = cursor.fetchall() #fetchone() vs fetchall() depending on the situation. We want all of the data here.
    except sqlite3.Error as error:
        print("Database error:", error)
    finally: #finally will always run after both a try and except. In other words: no matter if successful or not, this code will run.
        cursor.close()
        
    print(products)
    return products

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
        print(f"Retrieved {len(sales)} sales records")  # Add this line
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    return sales

#Starting (index) page & /home page are the same Note: You can use multiple routes attached to one function.
@app.route('/')
@app.route('/home')
def home():
    date, time = getCurrentDateTime()
    return render_template('home.html', date = date, time = time)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/edit_records')
def edit_records():
        if request.method == "POST":

            table_name = request.form["table"]

            


        if request.method == "GET":
          return render_template('edit_records.html')

@app.route('/products')
def products():
    products = getProducts()
    return render_template('products.html', products = products)

@app.route('/sales')
def sales():
    sales = joinTables()
    print(sales)  # Add this line to check the contents
    return render_template('sales.html', sales=sales)

#Run in debug mode.
if __name__ == '__main__':
    app.run(debug = True)