import requests
import psycopg2
from psycopg2 import sql

url = "https://dummyjson.com/products"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    products = data['products']
else:
    print("Failed")
    products = []

try:
    conn = psycopg2.connect(
        dbname="requests",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        price REAL,
        discount_percentage REAL,
        rating REAL,
        stock INTEGER,
        category TEXT,
        thumbnail TEXT,
        weight TEXT DEFAULT 'N/A'
    )
    '''
    cur.execute(create_table_query)
    
    for product in products:
        insert_query = sql.SQL('''
        INSERT INTO products (id, title, description, price, discount_percentage, rating, stock, category, thumbnail)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''')
        cur.execute(insert_query, (
            product['id'], product['title'], product['description'], product['price'], 
            product['discountPercentage'], product['rating'], product['stock'], 
            product['category'], product['thumbnail']
        ))
    
    conn.commit()
    print("Data inserted successfully.")
    
except Exception as e:
    print(f"Exception: {e}")
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()