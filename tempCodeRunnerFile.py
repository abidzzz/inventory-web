cur.execute("CREATE TABLE if not exists products (product_id varchar (20) PRIMARY KEY, product_name varchar (50) NOT NULL, description varchar (50) NOT NULL, price DECIMAL(10, 2) NOT NULL, quantity INTEGER NOT NULL);")