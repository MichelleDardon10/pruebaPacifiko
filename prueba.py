from collections import defaultdict


def search_product(products, name):

    name = name.lower()

    # Iterate through the list of products to find a matching product name
    for product in products:
        if product["product_name"].lower() == name:
            return product

    return f"Product '{name}' not found."


# Example usage
products = [
    {"product_id": 1, "product_name": "Laptop", "price": 999.99},
    {"product_id": 2, "product_name": "Smartphone", "price": 499.99},
    {"product_id": 3, "product_name": "Tablet", "price": 299.99},
]


print(search_product(products, "Laptop"))


def calculate_cart_total(cart, products):
    total = 0.0

    product_prices = {product["product_id"]: product["price"] for product in products}

    for item in cart:
        product_id = item["product_id"]
        quantity = item["quantity"]

        price = product_prices.get(product_id, 0)
        total += price * quantity

    return total


products = [
    {"product_id": 1, "product_name": "Laptop", "price": 999.99},
    {"product_id": 2, "product_name": "Smartphone", "price": 499.99},
    {"product_id": 3, "product_name": "Tablet", "price": 299.99},
]

cart = [
    {"product_id": 1, "quantity": 1},
    {"product_id": 2, "quantity": 2},
    {"product_id": 3, "quantity": 1},
]


print("Cart Total: $", calculate_cart_total(cart, products))


def calculate_discounted_total(cart):
    total = 0.0

    for item in cart:
        price = item["price"]
        discount = item.get("discount_percentage", 0)
        discounted_price = price * (1 - discount / 100)
        total += discounted_price

    return round(total, 2)


# Ejemplo
cart = [
    {
        "product_id": 1,
        "product_name": "Laptop",
        "price": 1000.00,
        "discount_percentage": 10,
    },
    {
        "product_id": 2,
        "product_name": "Smartphone",
        "price": 500.00,
        "discount_percentage": 5,
    },
    {
        "product_id": 3,
        "product_name": "Tablet",
        "price": 300.00,
        "discount_percentage": 0,
    },
]


print("Discounted Cart Total: $", calculate_discounted_total(cart))


def top_selling_products(orders, N):

    sales_count = defaultdict(int)

    for order in orders:
        product_id = order["product_id"]
        quantity = order["quantity"]
        sales_count[product_id] += quantity

    top_products = sorted(sales_count.items(), key=lambda x: x[1], reverse=True)[:N]

    result = [
        {"product_id": product_id, "total_quantity_sold": quantity}
        for product_id, quantity in top_products
    ]

    return result


# Ejemplo de uso
orders = [
    {"product_id": 1, "quantity": 10},
    {"product_id": 2, "quantity": 5},
    {"product_id": 1, "quantity": 8},
    {"product_id": 3, "quantity": 15},
    {"product_id": 2, "quantity": 7},
    {"product_id": 4, "quantity": 12},
]

# top 3 en ventas
print("Top Selling Products:", top_selling_products(orders, 3))
