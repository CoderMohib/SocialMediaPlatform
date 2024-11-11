import msvcrt

def get_password():
    print("Enter Password:", end=" ", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()  # Reads a single key press
        if char == b'\r':  # Enter key is pressed
            break
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)  # Prints an asterisk for each character typed
    print()  # To move to the next line after password is entered
    return password


get_password()