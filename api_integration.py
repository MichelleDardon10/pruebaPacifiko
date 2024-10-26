import requests


BASE_URL = "https://dummyjson.com/users"


# Todos los usuarios
def get_all_users():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all users: {e}")
        return None


# Usuarios por id
def get_user_by_id(user_id):
    try:
        response = requests.get(f"{BASE_URL}/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user {user_id}: {e}")
        return None


# Ejemplo
if __name__ == "__main__":
    # Todos los usuarios
    # all_users = get_all_users()
    # print("All Users:", all_users)

    # user por Id
    user_id = 1  # replace with any valid user ID
    single_user = get_user_by_id(user_id)
    # print(f"User {user_id}:", single_user)


# Así se podría hacer si se tuviera una columna de data con los datos de salarios
"""
def salario():
    all_users = get_all_users()
    if all_users:
        mayor = [user for user in all_users if user.get("salary", 0) > 300000]
        return len(mayor)
    return 0


# Llamada
print("Empleados mayor con salario mayor a $300,000:", salario())
"""
# Creacion de record con mi nombre con data random


def get_last_user_id():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        users = response.json().get("users", [])
        if users:
            last_id = max(user["id"] for user in users)
            return last_id
        return 0  # Default if no users are found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}")
        return None


def create_user_with_next_id():
    last_id = get_last_user_id()
    if last_id is None:
        print("Could not retrieve last ID.")
        return None

    new_user = {
        "id": last_id + 1,
        "firstName": "Michelle",
        "lastName": "Dardon",
        "maidenName": "",
        "age": 26,
        "gender": "female",
        "email": "michelle.dardon@ufm.edu",
        "username": "michelled",
        "birthDate": "1998-10-10",
        # solo data basica
    }

    print("New User Record:", new_user)
    return new_user


# llamada
michelle_user = create_user_with_next_id()

# 3. mi user id=31
# print(get_user_by_id(32))
