import json
import sys
from colorama import Fore, init, Style
init()


'''Nombre del proyecto: Interfaz de gestion de datos de usuario'''
'''Integrantes: Sevilla, Forni, Pigo, Padilla'''
'''Grupo: 1'''




def gestion_usuarios():
    en_sistema = True
    while en_sistema:
        try:
            opcion = modulo_sistema()  # Menú de opciones de sistema
            match opcion:
                case 1:
                    en_usuarios = True
                    while en_usuarios:
                        opcion_usuario = modulo_usuario()
                        match opcion_usuario:
                            case 1:
                                leer_datos()
                                continuar()                                   
                            case 2:
                                user = nuevo_usuario()
                                if user:
                                    lista = cargar_json()
                                    lista[user['id']] = user
                                    actualizar(lista)
                                continuar()
                            case 3:
                                modificar_datos() #agregar opcion de mantener presup. (x def 0)
                                continuar()
                            case 4:
                                eliminar_usuario()
                                continuar()
                            case 0:
                                sys.exit()
                                # Salir del bucle interno cuando se elige '0'
                            case 5:
                                en_usuarios = False  # Retroceso: volver al menú anterior
                            case _:
                                print('ERROR. La opcion seleccionada es incorrecta.')
                case 0:
                    sys.exit()
                    # Salir del bucle principal cuando se elige retroceso
                case _:
                    print('Opcion incorrecta.')
        except Exception as e:
            print(f'Error inesperado: {e}')

def modulo_sistema():
    print(f'\n\t\t{Fore.RED}{Style.BRIGHT}***BIENVENIDO AL GESTOR DE USUARIOS***{Style.RESET_ALL}')
    print(f'\n\n{Fore.YELLOW}{Style.BRIGHT}1.{Style.RESET_ALL} Panel de usuario\n')
    print(f'\n\n{Fore.YELLOW}{Style.BRIGHT}0.{Fore.RED + Style.DIM} Salir{Style.RESET_ALL} del sistema \n')
    op_sistema = int(input(f'{Fore.RED + Style.DIM}Seleccione una opción: {Style.RESET_ALL}'))
    return op_sistema

def modulo_usuario():
    asteriscos = "*" * 3
    print(f'\n\n{asteriscos}{"MODULO DE USUARIO".center(3)}{asteriscos}\n\n')
    print(f'{Fore.YELLOW + Style.BRIGHT}1.{Style.RESET_ALL} Mostrar usuarios existentes\n')
    print(f'{Fore.YELLOW + Style.BRIGHT}2.{Style.RESET_ALL} Crear usuario \n')
    print(f'{Fore.YELLOW + Style.BRIGHT}3.{Style.RESET_ALL} Modificar datos\n')
    print(f'{Fore.YELLOW + Style.BRIGHT}4.{Style.RESET_ALL} Eliminar usuario\n')
    print(f'{Fore.YELLOW + Style.BRIGHT}5.{Style.RESET_ALL} Volver al menú anterior.\n')
    print(f'{Fore.RED + Style.BRIGHT}0.{Style.RESET_ALL} Finalizar sistema.\n')
    op_usuario = int(input(f'{Fore.RED + Style.DIM}Seleccione una opción: {Style.RESET_ALL}'))
    return op_usuario  #DEVUELVE UNA OPCION

def cargar_json():  
    try:
        with open("usuarios.json", "r") as archivo:  #prepara el archivo para la carga (CON USUARIOS.JSON ABIERTO COMO LECTURA)
            dict = json.load(archivo) #carga el json llamado 'archivo' 
    except FileNotFoundError:
        dict = {}  #si no existe devuelve un diccionario nuevo // identificar
    return dict

def leer_datos():
    dict = cargar_json()
    if dict:
        print(f"\n\nUsuarios registrados: ")
        for key, value in dict.items():
            while key == dict[key]:
                key = input('') #agregar condicional
            print(f"ID: {key:2} | Nombre: {value['nombre']:2}")
    else:
        print()
        print("No existen usuarios registrados.")

def nuevo_usuario():
    while True:
        try:
            id = int(input('\nIngrese numero de ID de usuario: '))
        except ValueError:
            print("Error: Ingrese un número entero para el ID.")
        try:
            nombre = input("Ingrese usuario: ")
            validar_nombre(nombre)
            presupuesto = int(input('Ingrese un presupuesto inicial: '))
            usuario = {"id": id, "nombre": nombre, "presupuesto": presupuesto}
            return usuario
        except Exception as e:
            print(f'Error inesperado: {e}')
            
def validar_nombre(nombre):
    if len(nombre) < 7:
        raise ValueError('ERROR. El nombre debe tener al menos 7 caracteres.')
    if ' ' in nombre:
        raise ValueError('ERROR. El nombre no puede contener espacios.')

def actualizar(nuevo):
    with open("usuarios.json", "w") as archivo: #prepara el arhivo para la escritura (con USUARIOS.JSON ABIERTO COMO SOBREESCRITURA)
        json.dump(nuevo, archivo, indent =4)

def modificar_datos():
    dict = cargar_json()
    if dict:
        try:
            id_mod = input('Ingrese el número de ID de usuario: ')
            if id_mod in dict: #si el id esta dentro del diccionario ppal
                user = dict[id_mod] #guarda los datos de la posicion del id_mod en user 
                print(f'Datos de usuario: {user}') #los imprime
                # Aquí puedes agregar la lógica para modificar el usuario
                nuevo_nombre = input("\nIngrese el nuevo nombre de usuario: ")
                validar_nombre(nuevo_nombre)
                presupuesto = user['presupuesto'] #lee lo que esta guardado en el presupuesto y lo guarda en una variable
                nuevo_presupuesto = modificar_presupuesto(presupuesto) #opera con el monto y lo guarda en una nueva variable
                user['nombre'] = nuevo_nombre
                user['presupuesto'] = nuevo_presupuesto #actualiza la variable con el nuevo monto
                dict[id_mod] = user
                actualizar(dict)
                print(f'{Fore.RED + Style.BRIGHT}Usuario modificado correctamente.{Style.RESET_ALL}')
            else:
                print('El usuario no existe.')
        except ValueError:
            print('Ha ingresado un número inválido.')
        except Exception as error:
            print('Ha ocurrido un error de tipo: ', type(error))
    else:
        print('No hay usuarios para modificar.')

def eliminar_usuario():
    dict = cargar_json()
    if dict:
        try:
            id_eliminar = input('Ingrese el numero de ID del usuario a eliminar: ')
            if id_eliminar in dict:
                del dict[id_eliminar] #eliminar dato
                print('\nUsuario eliminado correctamente.')
                actualizar(dict)
        except ValueError:
            print('El numero de ID no corresponde a ningun usuario.')
        except Exception as error:
            print('Ha ocurrido un error de tipo: ', type(error))
    else:
        print('No existe el usuario indicado.')

def operaciones():
    try:
        op_operaciones = int(input('1. Ingresar monto: \n2. Retirar monto: '))
    except ValueError:
        op_operaciones = 0

    while op_operaciones != 1 and op_operaciones != 2:
        try:
            op_operaciones = int(input('ERROR. Ha ingresado una opcion incorrecta. '))
        except ValueError:
            continue
        
    return op_operaciones #devuelve 1 o 2

def suma(total):
    num2 = int(input('Ingrese monto: '))
    total += num2
    print(f'\nSu nuevo saldo es de: {total}')
    return total

def resta(total):
    num2 = int(input('Ingrese monto: '))
    while num2 > total:
        num2 = int(input('ERROR. El monto ingresado supera el disponible. Ingrese nuevamente por favor: '))
    total -= num2  
    print(f'Su nuevo saldo es de {total}')
    return total

def modificar_presupuesto(total):
    solicitud = operaciones()
    match solicitud:
        case 1:
            nuevo_saldo = suma(total)
            return nuevo_saldo
        case 2:
            nuevo_saldo = resta(total)
            return nuevo_saldo

def continuar():
    print()
    while True:
        continuar = input('Continuar? s/n: ')
        while continuar != 'n' and continuar != 's':
            continuar = input('ERROR. Opcion incorrecta. Continuar? s/n: ')
        
        if continuar == 'n':
            sys.exit()
        elif continuar == 's':
            break
        
            



#app
gestion_usuarios()

