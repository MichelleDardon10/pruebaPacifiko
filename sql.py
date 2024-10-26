from datetime import date
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    func,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Database setup
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ORM Models
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    order_date = Column(Date, nullable=False)
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")


# Create tables
Base.metadata.create_all(bind=engine)


# Seed data
def seed_data():
    db = SessionLocal()

    # Check if the database is already seeded
    if db.query(Customer).first() is not None:
        print("Database already seeded. Skipping seed data insertion.")
        db.close()
        return

    # Add customers
    customer1 = Customer(
        first_name="Alice",
        last_name="Johnson",
        email="alice.johnson@example.com",
        phone="123-456-7890",
    )
    customer2 = Customer(
        first_name="Bob",
        last_name="Smith",
        email="bob.smith@example.com",
        phone="098-765-4321",
    )
    db.add_all([customer1, customer2])
    db.commit()

    # Add products
    product1 = Product(product_name="Laptop", price=1000.00, stock_quantity=50)
    product2 = Product(product_name="Tablet", price=300.00, stock_quantity=30)
    product3 = Product(product_name="Smartphone", price=600.00, stock_quantity=75)
    db.add_all([product1, product2, product3])
    db.commit()

    # Add orders
    order1 = Order(customer_id=customer1.customer_id, order_date=date(2024, 10, 20))
    order2 = Order(customer_id=customer2.customer_id, order_date=date(2024, 10, 21))
    order3 = Order(customer_id=customer1.customer_id, order_date=date(2024, 10, 22))
    db.add_all([order1, order2, order3])
    db.commit()

    # Add order items
    order_item1 = OrderItem(
        order_id=order1.order_id,
        product_id=product1.product_id,
        quantity=2,
        subtotal=2000.00,
    )
    order_item2 = OrderItem(
        order_id=order1.order_id,
        product_id=product2.product_id,
        quantity=1,
        subtotal=300.00,
    )
    order_item3 = OrderItem(
        order_id=order2.order_id,
        product_id=product3.product_id,
        quantity=1,
        subtotal=600.00,
    )
    order_item4 = OrderItem(
        order_id=order3.order_id,
        product_id=product1.product_id,
        quantity=1,
        subtotal=1000.00,
    )
    db.add_all([order_item1, order_item2, order_item3, order_item4])
    db.commit()

    db.close()
    print("Sample data added to the database.")


db = SessionLocal()

# Insertar nuevo producto
new_product = Product(product_name="Laptop", price=1000.00, stock_quantity=50)
db.add(new_product)
db.commit()
print("New product added:", new_product)

# Hacer update

product_to_update = db.query(Product).filter(Product.product_id == 3).first()
if product_to_update:
    product_to_update.stock_quantity = 75
    db.commit()
    print("Product updated:", product_to_update)
else:
    print("Product with product_id = 3 not found")


# eliminar
order_to_delete = db.query(Order).filter(Order.order_id == 10).first()
if order_to_delete:
    # Delete associated order items
    db.query(OrderItem).filter(OrderItem.order_id == 10).delete()
    db.delete(order_to_delete)
    db.commit()
    print("Order and associated items deleted")
else:
    print("Order with order_id = 10 not found")


# llamar

order = db.query(Order).filter(Order.order_id == 5).first()
if order:
    customer = order.customer
    print("Customer who placed order 5:", customer.first_name, customer.last_name)
else:
    print("Order with order_id = 5 not found")


# calcular total de actividades

from sqlalchemy import func

# Calculate total revenue generated by each product
total_revenue = (
    db.query(Product.product_name, func.sum(OrderItem.subtotal).label("total_revenue"))
    .join(OrderItem, Product.product_id == OrderItem.product_id)
    .group_by(Product.product_name)
    .all()
)
for product, revenue in total_revenue:
    print(f"Product: {product}, Total Revenue: ${revenue:.2f}")


# almacenamiento


def calculate_total_revenue_by_product():
    db = SessionLocal()
    total_revenue = (
        db.query(
            Product.product_name, func.sum(OrderItem.subtotal).label("total_revenue")
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .group_by(Product.product_name)
        .all()
    )

    for product, revenue in total_revenue:
        print(f"Product: {product}, Total Revenue: ${revenue:.2f}")

    db.close()


# Example usage
calculate_total_revenue_by_product()


# utilidad por consumidor
def calculate_total_revenue_by_customer(customer_id):
    db = SessionLocal()
    total_revenue = (
        db.query(func.sum(OrderItem.subtotal).label("total_revenue"))
        .join(Order, OrderItem.order_id == Order.order_id)
        .filter(Order.customer_id == customer_id)
        .scalar()
    )

    if total_revenue is None:
        total_revenue = 0.0

    print(f"Total revenue generated by customer {customer_id}: ${total_revenue:.2f}")
    db.close()


# Example usage
calculate_total_revenue_by_customer(1)  # Replace 1 with the desired customer_id


##TASK 4

from datetime import date
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    func,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Database setup
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ORM Models
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    order_date = Column(Date, nullable=False)
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")


# Create tables
Base.metadata.create_all(bind=engine)

# Task 4 Functions


# 1. Display a list of products and their stock quantities
def display_products():
    db = SessionLocal()
    products = db.query(Product).all()
    print("Product List and Stock Quantities:")
    for product in products:
        print(f"Product: {product.product_name}, Stock: {product.stock_quantity}")
    db.close()


# 2. Search for products by name
def search_product_by_name(name):
    db = SessionLocal()
    products = db.query(Product).filter(Product.product_name.ilike(f"%{name}%")).all()
    print(f"Search results for '{name}':")
    if products:
        for product in products:
            print(
                f"Product: {product.product_name}, Price: ${product.price:.2f}, Stock: {product.stock_quantity}"
            )
    else:
        print("No products found.")
    db.close()


# 3. Place an order by selecting a customer and adding order items
def place_order(customer_id, order_items):
    db = SessionLocal()

    # Create a new order for the specified customer
    new_order = Order(customer_id=customer_id, order_date=date.today())
    db.add(new_order)
    db.flush()  # Get the new order ID before committing

    # Add order items and update stock quantities
    for item in order_items:
        product_id = item["product_id"]
        quantity = item["quantity"]

        # Fetch product to check stock
        product = db.query(Product).filter(Product.product_id == product_id).first()

        if product and product.stock_quantity >= quantity:
            # Calculate subtotal and add order item
            subtotal = product.price * quantity
            order_item = OrderItem(
                order_id=new_order.order_id,
                product_id=product_id,
                quantity=quantity,
                subtotal=subtotal,
            )
            db.add(order_item)

            # Reduce product stock quantity
            product.stock_quantity -= quantity
        else:
            print(
                f"Insufficient stock for product {product_id}. Order not placed for this item."
            )

    # Commit the transaction to save the order and updates
    db.commit()
    print(f"Order placed successfully for customer {customer_id}.")
    db.close()


# Example usage
display_products()
search_product_by_name("Laptop")  # Replace "Laptop" with any search term
order_items = [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]
place_order(customer_id=1, order_items=order_items)
