from app.core.security import hash_password, verify_password

password = "hello123"

hashed = hash_password(password)

print("Hashed:", hashed)
print("Correct:", verify_password(password, hashed))
print("Wrong:", verify_password("wrong123", hashed))