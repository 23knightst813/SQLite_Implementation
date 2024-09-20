from flask import Flask, render_template, redirect, request , flash
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'khanya smells like a bad fart'
# Use a function to get a new database connection for each request
def get_db_connection():
    conn = sqlite3.connect('BeanBrew.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database tables
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY, 
        productName TEXT NOT NULL, 
        productDescription TEXT NOT NULL, 
        price REAL NOT NULL
    )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS customer(
        CustomerID INTEGER PRIMARY KEY, 
        firstName TEXT NOT NULL, 
        lastName TEXT NOT NULL, 
        email TEXT NOT NULL, 
        Phone TEXT NOT NULL
    )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS sale(
        id INTEGER PRIMARY KEY, 
        productID INTEGER NOT NULL, 
        customerID INTEGER NOT NULL, 
        date TEXT NOT NULL, 
        time TEXT NOT NULL, 
        FOREIGN KEY(productID) REFERENCES product(id), 
        FOREIGN KEY(customerID) REFERENCES customer(CustomerID)
    )""")
    
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

def getCurrentDateTime():
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y"), now.strftime("%X")

def getProducts():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM Product").fetchall()
    conn.close()
    return products

def joinTables():
    conn = get_db_connection()
    sales = conn.execute("""
        SELECT Sale.id, Product.productName, Product.productDescription, Product.price,
               Customer.firstName, Customer.lastName, Customer.email, Customer.Phone,
               Sale.date, Sale.time
        FROM Sale
        JOIN Product ON Sale.productID = Product.id
        JOIN Customer ON Sale.customerID = Customer.CustomerID
    """).fetchall()
    conn.close()
    return sales

@app.route('/')
@app.route('/home')
def home():
    date, time = getCurrentDateTime()
    return render_template('home.html', date=date, time=time)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/add_records', methods=['GET', 'POST'])
def add_records():
    if request.method == "POST":
        record_type = request.form["record_type"]
        conn = get_db_connection()
        cur = conn.cursor()

        try:



            if record_type == "Product":

                existing_product = cur.execute("SELECT productName FROM product WHERE productName = ?", (request.form["productName"],)).fetchone()

                if existing_product:
                    flash('Product already exists. Please use a different product name.', 'error')
                else:

                    cur.execute("INSERT INTO Product (productName, productDescription, price) VALUES (?, ?, ?)",
                                (request.form["productName"], request.form["productDescription"], request.form["price"]))
                    flash('Product added successfully!', 'success')


            elif record_type == "Customer":

                existing_email = cur.execute("SELECT email FROM Customer WHERE email = ?", (request.form["customer_email"],)).fetchone()
                
                if existing_email:
                    flash('Email already exists. Please use a different email.', 'error')
                else:
                    cur.execute("INSERT INTO Customer (firstName, lastName, email, Phone) VALUES (?, ?, ?, ?)",
                                (request.form["firstName"], request.form["lastName"], request.form["customer_email"], request.form["Phone"]))
                    flash('Customer added successfully!', 'success')

            elif record_type == "sale":

                cur.execute("INSERT INTO Sale (productID, customerID, date, time) VALUES (?, ?, ?, ?)",
                            (request.form["productID"], request.form["customerID"], request.form["date"], request.form["time"]))
                flash('Sale added successfully!', 'success')
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            flash('An error occurred while adding the record.', 'error')
        finally:
            conn.close()

        return redirect('/add_records')

    return render_template('edit_records.html')

@app.route('/edit_records')
def edit_records():
    return redirect('/add_records')

@app.route('/products')
def products():
    products = getProducts()
    return render_template('products.html', products=products)

@app.route('/sales')
def sales():
    sales = joinTables()
    return render_template('sales.html', sales=sales)

if __name__ == '__main__':
    app.run(debug=True)