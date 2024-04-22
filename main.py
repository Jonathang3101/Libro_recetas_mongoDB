from pymongo import MongoClient

# conexion a mongo
client = MongoClient("mongodb://localhost:27017/")
db_name = "recetas"
recipes_collection = db_name + ".recetas"


def connect_to_database():
    db = client[db_name]
    return db[recipes_collection]


def add_recipe(recipe_data):
    collection = connect_to_database()
    result = collection.insert_one(recipe_data)
    return result.inserted_id


def search_recipes(search_term):
    collection = connect_to_database()
    query = {"$text": {"$search": search_term}} 
    return list(collection.find(query))


def get_recipe(recipe_id):
    collection = connect_to_database()
    return collection.find_one({"_id": recipe_id})


def update_recipe(recipe_id, update_data):
    collection = connect_to_database()
    result = collection.update_one({"_id": recipe_id}, {"$set": update_data})
    return result.modified_count


def delete_recipe(recipe_id):
    collection = connect_to_database()
    result = collection.delete_one({"_id": recipe_id})
    return result.deleted_count


if __name__ == "__main__":
    # Sample
    recipe_id = add_recipe(
        {
            "nombre": "Pizza Margharita",
            "ingredientes": ["masa", "salsa de tomate ", "Mozzarella"],
            "instrucciones": [
                
            ],
        }
    )
    print(f"agregar receta con h ID: {recipe_id}")

    search_results = search_recipes("cheese")
    print(f"\n recetas que contienen queso  'cheese':")
    for recipe in search_results:
        print(recipe["nombre"])

    updated_count = update_recipe(recipe_id, {"intrucciones": [""]})
    print(f"\nactualizar receta : {updated_count} modificado! ")

    deleted_count = delete_recipe(recipe_id) 
    print(f"\nborrar receta: {deleted_count}  modificado!")
