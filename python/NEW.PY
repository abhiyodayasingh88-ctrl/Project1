import hashlib

stored_hash = ""
while True:
     password = input("Enter password: ")
    
     hashed_password = hashlib.sha256(password.encode()).hexdigest()

     if hashed_password == stored_hash:
       print("Correct Password")
       break
     else:
         print("Wrong Password, try again!\n")




