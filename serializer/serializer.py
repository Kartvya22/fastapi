def convert_user(user) -> dict : 
    return {
        "_id" : str(user["_id"]),
        "fullname" : user["fullname"],
        "email" : user["email"],
        "password" : user["password"],
        "confirm_password" : user["confirm_password"]
    }
    
def convert_users(users) -> list : 
    return [convert_user(user) for user in users]

def convert_sample(sample) -> dict : 
    return {
        "_id" : str(sample["_id"]),
        "title" : sample["title"],
        "price" : sample["price"],
        "rating" : sample["rating"],
        "content" : sample["content"]
    }

def convert_samples(samples) -> list : 
    return [convert_sample(sample) for sample in samples]