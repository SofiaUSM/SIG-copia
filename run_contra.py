# Leer contraseñas del archivo


secrets_file_path = 'pass.txt'



with open(secrets_file_path, 'r') as file:
    secrets = file.readlines()

# Buscar un usuario específico
for secret in secrets:
    saved_user, saved_password = secret.strip().split(':')
    if saved_user == "emanuel.venegas":
        print(f"La contraseña para {saved_user} es: {saved_password}")
