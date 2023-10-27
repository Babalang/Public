import time
import itertools
import string
#Cette application est un test pour tester tout les mots de passes en python.
target_password = input("Your password : ")

charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
print(charset)
password_length = len(target_password)

start_time = time.time()

found_password = None

for length in range(1, password_length + 1):
    for candidate in itertools.product(charset, repeat=length):
        candidate_password = ''.join(candidate)
        if candidate_password == target_password:
            found_password = candidate_password
            break

    if found_password:
        break

end_time = time.time()

if found_password:
    print(f"Mot de passe trouvé : {found_password}")
else:
    print("Mot de passe non trouvé")

elapsed_time = end_time - start_time
print(f"Temps écoulé : {elapsed_time:.2f} secondes")
