import random
from datetime import datetime
from colorama import Fore


lista_sucursales = []
clientes = []
# Clases.
class CajeroAutomatico:
    def __init__(self, id_cajero, nombre, id_sucursal):
        self.id_cajero = id_cajero
        self.nombre = nombre
        self.saldo = 0
        self.id_sucursal = id_sucursal
        self.ciudad = None  # La ciudad se obtendrá de la sucursal
        self.direccion = None  # La dirección se obtendrá de la sucursal
        self.billetes = {
            200: 0,
            100: 0,
            50: 0,
            20: 0,
            10: 0
        }

    def agregar_saldo(self, billetes):
        monto = sum(denominacion * cantidad for denominacion, cantidad in billetes.items())
        self.saldo += monto
        for denominacion, cantidad in billetes.items():
            self.billetes[denominacion] += cantidad

    def retirar_saldo(self, monto):
        billetes_retirados = {}
        monto_original = monto
        # Verificar si hay suficientes billetes para el retiro
        billetes_suficientes = True

        for denominacion in sorted(self.billetes.keys(), reverse=True):
            cantidad_necesaria = monto // denominacion
            if cantidad_necesaria > 0:
                cantidad_disponible = self.billetes[denominacion]
                if cantidad_disponible >= cantidad_necesaria:
                    billetes_retirados[denominacion] = cantidad_necesaria
                    monto -= cantidad_necesaria * denominacion
                else:
                    billetes_suficientes = False
                    break
        # Si hay suficientes billetes, proceder con el retiro
        if billetes_suficientes:
            for denominacion, cantidad in billetes_retirados.items():
                self.billetes[denominacion] -= cantidad
            self.saldo -= monto_original
            return billetes_retirados
        else:
            print(Fore.LIGHTRED_EX+"Saldo del cajero insuficiente para realizar esta operación.")
            return None

    def editar_saldo(self, billetes):
        self.billetes = billetes
        self.saldo = sum(denominacion * cantidad for denominacion, cantidad in billetes.items())
        print(Fore.LIGHTGREEN_EX+"Saldo del cajero actualizado correctamente.")

class Sucursal:
    def __init__(self, id_sucursal, nombre, ciudad, direccion):
        self.id_sucursal = id_sucursal
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion
        self.cajeros = []

    def agregar_cajero(self, id_cajero, nombre):
        cajero = CajeroAutomatico(id_cajero, nombre, self.id_sucursal)
        cajero.ciudad = self.ciudad
        cajero.direccion = self.direccion
        self.cajeros.append(cajero)
        return cajero

    def eliminar_cajero(self, id_cajero):
        self.cajeros = [cajero for cajero in self.cajeros if cajero.id_cajero != id_cajero]
class Cuenta:
    def __init__(self, id_cuenta, tipo, saldo_inicial):
        self.id_cuenta = id_cuenta
        self.tipo = tipo
        self.saldo = saldo_inicial
        self.numero_cuenta = None
        self.numero_tarjeta = None
        self.tarjeta_debito = None
        self.movimientos = []
        self.cliente = None

    def generar_numero_tarjeta(self):
        self.numero_tarjeta = ''.join([str(random.randint(0, 9)) for _ in range(16)])

    def registrar_movimiento(self, tipo, monto):
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.movimientos.append((fecha_hora, tipo, monto))

    def obtener_movimientos(self):
        return self.movimientos
class TarjetaDebito:
    def __init__(self, numero_tarjeta, clave_cajero):
        self.numero_tarjeta = numero_tarjeta
        self.clave_cajero = clave_cajero
        self.cuenta = None
class Cliente:
    def __init__(self, id_cliente, nombres, apellidos, telefono, direccion, dni, sucursal=None):
        self.id_cliente = id_cliente
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.direccion = direccion
        self.dni = dni
        self.cuentas = []
        self.sucursal = sucursal
        self.estado = "Activo"

    def crear_cuenta_interactiva(self):
        if self.estado != "Activo":
            print(Fore.LIGHTRED_EX+"El cliente está inactivo, no puedes crear una nueva cuenta para este cliente.")
            return
        tipo_cuenta = input(Fore.LIGHTWHITE_EX+f"Ingrese el tipo de cuenta para {self.nombres} {self.apellidos} (Ahorro/Sueldo): ").strip().capitalize()
        try:
            saldo_inicial = float(input(Fore.LIGHTWHITE_EX+f"Ingrese el saldo inicial para la cuenta {tipo_cuenta}: "))
        except ValueError:
            print(Fore.LIGHTRED_EX+"El Saldo de la cuenta debe ser un monto válido.")
            return
        clave_cajero = input(Fore.LIGHTWHITE_EX+"Ingrese la clave de cajero de 4 dígitos para la tarjeta de débito: ")
        self.crear_cuenta(tipo_cuenta, saldo_inicial, clave_cajero)

    def generar_numero_cuenta(self):
        id_cuenta = len(self.cuentas) + 1
        numero_cuenta = f"{self.id_cliente:04}-{id_cuenta:04}"
        while len(numero_cuenta) < 14:
            numero_cuenta += str(random.randint(0, 9))
        return numero_cuenta

    def crear_cuenta(self, tipo, saldo_inicial, clave_cajero):
        id_cuenta = len(self.cuentas) + 1
        cuenta = Cuenta(id_cuenta, tipo, saldo_inicial)
        cuenta.cliente = self
        cuenta.generar_numero_tarjeta()
        cuenta.numero_cuenta = self.generar_numero_cuenta()
        cuenta.tarjeta_debito = TarjetaDebito(cuenta.numero_tarjeta, clave_cajero)
        cuenta.tarjeta_debito.cuenta = cuenta
        print(Fore.LIGHTBLUE_EX+"----------LOS DATOS DE TU CUENTA SON ---------")
        print(Fore.LIGHTBLUE_EX+"NÚMERO DE CUENTA: ", Fore.LIGHTWHITE_EX+cuenta.numero_cuenta)
        print(Fore.LIGHTBLUE_EX+"TIPO DE CUENTA: ",Fore.LIGHTWHITE_EX+ cuenta.tipo)
        print(Fore.LIGHTBLUE_EX+"TARJETA DE DÉBITO: ",Fore.LIGHTWHITE_EX+ cuenta.numero_tarjeta)
        self.cuentas.append(cuenta)


    def agregar_cuenta_existente(self, cuenta_existente):
        self.cuentas.append(cuenta_existente)
        cuenta_existente.cliente = self
# Esta función se usa al acceder al menu de operaciones del cliente, identifica al cliente y la cuenta que usará para realizar las operaciones.
def autenticar_cliente():
    numero_tarjeta = input(Fore.LIGHTWHITE_EX+"Ingrese su número de tarjeta: ")
    clave_cajero = input(Fore.LIGHTWHITE_EX+"Ingrese su clave de cajero: ")

    for cliente in clientes:
        for cuenta in cliente.cuentas:
            if cuenta.numero_tarjeta == numero_tarjeta and cuenta.tarjeta_debito.clave_cajero == clave_cajero:
                print(Fore.LIGHTGREEN_EX+"Autenticación exitosa.")
                return cuenta, cliente  # Devuelve la cuenta autenticada
    print(Fore.LIGHTRED_EX+"Número de tarjeta o clave de cajero incorrectos.")
    return None, None
# Menu Principal.
def menu_principal():
    while True:
        print(Fore.LIGHTWHITE_EX+"\n------ Menú Principal ------")
        print("1. Ingresar a Menu Administrativo")
        print("2. Ingresar a Menu de Clientes")
        print("3. Salir")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == '1':
            menu_administracion()
        elif opcion == '2':
            cuenta_autenticada, cliente = autenticar_cliente()
            if cuenta_autenticada and cliente:
                menu_operaciones_cliente(cuenta_autenticada, cliente)
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")
# Menus administrativos.
def menu_adm_clientes():
    while True:
        print(Fore.LIGHTWHITE_EX+"\n------ Menú de administración de cientes ------")
        print("1. Crear nuevo cliente")
        print("2. Agregar cuenta a cliente existente")
        print("3. Mostrar lista de clientes ordenados")
        print("4. Ver datos de un cliente específico")
        print("5. Editar información de un cliente")
        print("6. Dar de baja a un cliente")
        print("7. Volver al Menu anterior")
        opcion = input("Seleccione una opción (1-7): ")

        if opcion == '1':
            crear_nuevo_cliente()
        elif opcion == '2':
            agregar_cuenta_a_cliente_existente()
        elif opcion == '3':
            mostrar_clientes_ordenados()
        elif opcion == '4':
            ver_datos_cliente_por_id()
        elif opcion == '5':
            editar_cliente()
        elif opcion == '6':
            dar_baja_cliente()
        elif opcion == '7':
            break
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")
def menu_adm_cajeros():
    while True:
        print(Fore.LIGHTWHITE_EX+"\n------ Menú de administración de cajeros ------")
        print("1. Crear nuevo cajero")
        print("2. Agregar saldo a un cajero")
        print("3. Ver datos de un cajero específico")
        print("4. Editar un Cajero")
        print("5. Eliminar un Cajero")
        print("6. Volver al Menu anterior")
        opcion = input("Seleccione una opción (1-6): ")

        if opcion == '1':
            agregar_cajero_a_sucursal()
        elif opcion == '2':
            agregar_saldo_a_cajero()
        elif opcion == '3':
            ver_datos_cajero_por_id()
        elif opcion == '4':
            editar_informacion_cajero()
        elif opcion == '5':
            eliminar_cajero()
        elif opcion == '6':
            break
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")
def menu_adm_sucursal():
    while True:
        print(Fore.LIGHTWHITE_EX+"\n------ Menú de administración de sucursales ------")
        print("1. Crear Nueva Sucursal")
        print("2. Ver datos de una sucursal específica")
        print("3. Editar una sucursal")
        print("4. Eliminar una sucursal")
        print("5. Volver al Menu anterior")
        opcion = input("Seleccione una opción (1-5): ")

        if opcion == '1':
            agregar_nueva_sucursal()
        elif opcion == '2':
            ver_datos_sucursal_por_id()
        elif opcion == '3':
            editar_informacion_sucursal()
        elif opcion == '4':
            eliminar_sucursal()
        elif opcion == '5':
            break
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")
def menu_administracion():
    while True:
        print(Fore.LIGHTWHITE_EX+"\n------ Menú de Administración  ------")
        print("1. Administrar Clientes")
        print("2. Administrar Cajeros")
        print("3. Administrar Sucursales")
        print("4. Volver al Menu anterior")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == '1':
            menu_adm_clientes()
        elif opcion == '2':
            menu_adm_cajeros()
        elif opcion == '3':
            menu_adm_sucursal()
        elif opcion == '4':
            break
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")
# Menu de operaciones del cliente.
def menu_operaciones_cliente(cuenta, cliente):
    while True:
        print(Fore.LIGHTWHITE_EX+"\n------ Menú de Operaciones del Cliente ------")
        print("1. Retirar dinero")
        print("2. Depositar dinero")
        print("3. Transferir dinero")
        print("4. Pagar servicios")
        print("5. Consultar saldo")
        print("6. Consultar movimientos")
        print("7. Salir")
        opcion = input("Seleccione una opción (1-7): ")

        if opcion == '1':
            retirar_dinero(cuenta, cliente)
        elif opcion == '2':
            depositar_dinero(cuenta, cliente)
        elif opcion == '3':
            transferir_dinero(cuenta, cliente)
        elif opcion == '4':
            pagar_servicios(cuenta, cliente)
        elif opcion == '5':
            consultar_saldo(cuenta)
        elif opcion == '6':
            consultar_movimientos(cuenta)
        elif opcion == '7':
            break
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")

# Funciones administrativas para crear, editar, eliminar clientes, cajeros y sucursales.
def crear_nuevo_cliente():
    nombre = input(Fore.LIGHTWHITE_EX+"Ingrese el nombre del cliente: ")
    apellido = input("Ingrese el apellido del cliente: ")
    telefono = input("Ingrese el teléfono del cliente: ")
    direccion = input("Ingrese la dirección del cliente: ")
    dni = input("Ingrese el DNI del cliente: ")

    for cliente in clientes:
        if cliente.dni == dni:
            print(Fore.LIGHTRED_EX+f"¡El cliente con DNI {dni} ya está registrado!")
            return

    cliente_nuevo = Cliente(len(clientes) + 1, nombre, apellido, telefono, direccion, dni)
    cliente_nuevo.crear_cuenta_interactiva()
    clientes.append(cliente_nuevo)
    print(Fore.LIGHTBLUE_EX+"NOMBRES: ", Fore.LIGHTWHITE_EX+nombre)
    print(Fore.LIGHTBLUE_EX+"APELLIDOS: ", Fore.LIGHTWHITE_EX+apellido)
    print(Fore.LIGHTBLUE_EX+"TELÉFONO ", Fore.LIGHTWHITE_EX+telefono)
    print(Fore.LIGHTBLUE_EX+"DIRECCIÓN ", Fore.LIGHTWHITE_EX+direccion)
    print(Fore.LIGHTBLUE_EX+"DNI: ", Fore.LIGHTWHITE_EX+dni)
def dar_baja_cliente():
    try:
        cliente_id = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cliente a dar de baja: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id del cliente debe ser un número entero.")
        return
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    if cliente:
        for cuenta in cliente.cuentas:
            if cuenta.obtener_movimientos():
                print(Fore.LIGHTRED_EX+"El cliente {cliente.nombres} {cliente.apellidos} cuenta con movimientos bancarios y no se puede eliminar.")
                return
        clientes.remove(cliente)
        print(Fore.LIGHTGREEN_EX+"Cliente {cliente.nombres} {cliente.apellidos} eliminado correctamente.")
    else:
        print(Fore.LIGHTRED_EX+"Cliente no encontrado.")
def editar_cliente():
    print(Fore.LIGHTWHITE_EX+"Clientes registrados:")
    for cliente in clientes:
        print(f"{cliente.id_cliente}: {cliente.nombres} {cliente.apellidos} DNI: {cliente.dni}")

    try:
        cliente_id = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cliente a editar: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id del cliente debe ser un número entero")
        return
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    if cliente:
        print(Fore.LIGHTBLUE_EX+"Datos del cliente: ")
        if(cliente.estado != "Activo"):
            print(Fore.LIGHTGREEN_EX+"ESTADO:",Fore.LIGHTWHITE_EX+ cliente.estado)
        else:
            print(Fore.LIGHTRED_EX+"ESTADO:", Fore.LIGHTWHITE_EX+cliente.estado)
        print(Fore.LIGHTBLUE_EX+"Nombres:",Fore.LIGHTWHITE_EX+ cliente.nombres)
        print(Fore.LIGHTBLUE_EX+"Apellidos: ", Fore.LIGHTWHITE_EX+cliente.apellidos)
        print(Fore.LIGHTBLUE_EX+"Dirección: ",Fore.LIGHTWHITE_EX+ cliente.direccion)
        print(Fore.LIGHTBLUE_EX+"DNI: ",Fore.LIGHTWHITE_EX+ cliente.dni)
        print(Fore.LIGHTBLUE_EX+"Teléfono: ",Fore.LIGHTWHITE_EX+ cliente.telefono)
        print(Fore.LIGHTBLUE_EX+"Cuentas del cliente: ")
        for cuenta in cliente.cuentas:
            cont = 1
            print(Fore.CYAN+"-------------------------------Cuenta N°", cont, "-------------------------------")
            print(Fore.LIGHTWHITE_EX+f"  - ID DE LA CUENTA: {cuenta.id_cuenta}")
            print(Fore.LIGHTWHITE_EX+f"  - Número de cuenta: {cuenta.numero_cuenta}")
            print(Fore.LIGHTWHITE_EX+f"    Tipo: {cuenta.tipo}")
            print(Fore.LIGHTWHITE_EX+f"    Saldo: {cuenta.saldo}")
            print(Fore.LIGHTWHITE_EX+f"    Número de tarjeta: {cuenta.numero_tarjeta}")
            cont+=1
        print()
        print(Fore.LIGHTWHITE_EX+"1. Editar Nombres")
        print(Fore.LIGHTWHITE_EX+"2. Editar Apellidos")
        print(Fore.LIGHTWHITE_EX+"3. Editar Dirección")
        print(Fore.LIGHTWHITE_EX+"4. Editar DNI")
        print(Fore.LIGHTWHITE_EX+"5. Editar Teléfono")
        print(Fore.LIGHTWHITE_EX+"6. Editar Estado")
        print(Fore.LIGHTWHITE_EX+"7. Generar nueva tarjeta")
        print(Fore.LIGHTWHITE_EX+"8. Editar clave de tarjeta")
        print(Fore.LIGHTWHITE_EX+"9. Regresar al menu de administrador")
        opcion = input(Fore.LIGHTWHITE_EX+"Seleccione una opción para editar (1-6): ")
        if opcion == '1':
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            cliente.nombres = nuevo_nombre
        elif opcion == '2':
            nuevo_apellido = input("Ingrese el nuevo apellido: ")
            cliente.apellidos = nuevo_apellido
        elif opcion == '3':
            nueva_direccion = input("Ingresa la nueva direccion: ")
            cliente.direccion = nueva_direccion
        elif opcion == '4':
            nuevo_dni = input("Ingrese el nuevo DNI: ")
            cliente.dni = nuevo_dni
        elif opcion == '5':
            nuevo_telefono = input("Ingrese el nuevo número de teléfono: ")
            cliente.telefono = nuevo_telefono
        elif opcion == '6':
            print("Selecciona el nuevo estado del cliente: ")
            print("1. Activo")
            print("2. Inactivo")
            opcion = input("Seleccione una opción (1-2): ")
            if(opcion == '1'):
                cliente.estado = "Activo"
            else:
                cliente.estado = "Inactivo"
        elif opcion == '7':
            try:
                cuenta_id = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la cuenta para generar una nueva tarjeta: "))
            except ValueError:
                print(Fore.LIGHTRED_EX+"El id de la cuenta debe ser un número entero")
                return
            cuenta = next((cuenta for cuenta in cliente.cuentas if cuenta.id_cuenta == cuenta_id), None)
            if cuenta:
                cuenta.generar_numero_tarjeta()
                print(Fore.LIGHTGREEN_EX+"Nueva tarjeta generada: {cuenta.numero_tarjeta}")
            else:
                print(Fore.LIGHTRED_EX+"Cuenta no encontrada.")
        elif opcion == '8':
            try:
                cuenta_id = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la cuenta: "))
            except ValueError:
                print(Fore.LIGHTRED_EX+"El id de la cuenta debe ser un número entero")
                return
            cuenta = next((cuenta for cuenta in cliente.cuentas if cuenta.id_cuenta == cuenta_id), None)
            if cuenta:
                nueva_clave = input(Fore.LIGHTWHITE_EX+"Ingrese la nueva clave de la tarjeta: ")
                cuenta.tarjeta_debito.clave_cajero = nueva_clave
                print(Fore.LIGHTGREEN_EX+"Clave de tarjeta actualizada.")
            else:
                print(Fore.LIGHTRED_EX+"Cuenta no encontrada.")
        elif opcion == '9':
            menu_administracion()
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida.")
    else:
        print(Fore.LIGHTRED_EX+"Cliente no encontrado.")
def mostrar_clientes_ordenados():
    print(Fore.LIGHTWHITE_EX+"1. Ordenar alfabéticamente de forma ascendente")
    print("2. Ordenar alfabéticamente de forma descendente")
    opcion = input("Seleccione una opción (1-2): ")

    if opcion == '1':
        clientes_ordenados = sorted(clientes, key=lambda cliente: cliente.nombres)
    elif opcion == '2':
        clientes_ordenados = sorted(clientes, key=lambda cliente: cliente.nombres, reverse=True)
    else:
        print(Fore.LIGHTRED_EX+"Opción no válida.")
        return

    for cliente in clientes_ordenados:
        print(f"{cliente.id_cliente}: {cliente.nombres} {cliente.apellidos}")
def agregar_cuenta_a_cliente_existente():
    if not clientes:
        print(Fore.LIGHTRED_EX+"No hay clientes registrados.")
        return

    print(Fore.LIGHTWHITE_EX+"Clientes registrados:")
    for cliente in clientes:
        print(f"{cliente.id_cliente}: {cliente.nombres} {cliente.apellidos}")
    try:
        cliente_id = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cliente: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id del cliente debe ser un número entero")
        return
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    if cliente:
        cliente.crear_cuenta_interactiva()
    else:
        print(Fore.LIGHTRED_EX+"Cliente no encontrado.")
def ver_datos_cliente_por_id():
    if not clientes:
        print(Fore.LIGHTRED_EX + "No hay clientes registrados.")
        return

    print(Fore.LIGHTWHITE_EX+"Clientes registrados:")
    for cliente in clientes:
        print(f"{cliente.id_cliente}: {cliente.nombres} {cliente.apellidos}")
    
    try:
        cliente_id = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cliente: "))
    except ValueError:
        print(Fore.LIGHTRED_EX + "El id del cliente debe ser un número entero")
        return
    
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    if cliente:
        print(Fore.LIGHTWHITE_EX+ f"Cliente: {cliente.nombres} {cliente.apellidos}")
        print(Fore.LIGHTWHITE_EX+ f"ESTADO: {cliente.estado}")
        print(Fore.LIGHTWHITE_EX+ f"Teléfono: {cliente.telefono}")
        print(Fore.LIGHTWHITE_EX+ f"Dirección: {cliente.direccion}")
        print(Fore.LIGHTWHITE_EX+ f"DNI: {cliente.dni}")
        print(Fore.LIGHTWHITE_EX+ "Cuentas:")
        for cuenta in cliente.cuentas:
            print(Fore.LIGHTWHITE_EX+ f"  - Número de cuenta: {cuenta.numero_cuenta}")
            print(Fore.LIGHTWHITE_EX+ f"    Tipo: {cuenta.tipo}")
            print(Fore.LIGHTWHITE_EX+ f"    Saldo: {cuenta.saldo}")
            print(Fore.LIGHTWHITE_EX+ f"    Número de tarjeta: {cuenta.numero_tarjeta}")
    else:
        print(Fore.LIGHTRED_EX + "Cliente no encontrado.")

def agregar_nueva_sucursal():
    nombre = input(Fore.LIGHTWHITE_EX+"Ingrese el nombre de la sucursal: ")
    ciudad = input("Ingrese la ciudad de la sucursal: ")
    direccion = input("Ingrese la dirección de la sucursal: ")
    id_sucursal = len(lista_sucursales) + 1
    sucursal = Sucursal(id_sucursal, nombre, ciudad, direccion)
    lista_sucursales.append(sucursal)
    print(Fore.LIGHTGREEN_EX + f"Sucursal '{nombre}' agregada con éxito.")

def agregar_cajero_a_sucursal():
    if not lista_sucursales:
        print(Fore.LIGHTRED_EX+"No hay sucursales registradas.")
        return

    print(Fore.LIGHTWHITE_EX+"Sucursales registradas:")
    for sucursal in lista_sucursales:
        print(Fore.LIGHTWHITE_EX+f"{sucursal.id_sucursal}: {sucursal.nombre}")

    try:
        id_sucursal = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la sucursal: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"Error: El ID de la sucursal debe ser un número entero.")
        return

    sucursal = next((s for s in lista_sucursales if s.id_sucursal == id_sucursal), None)
    if sucursal:
        nombre = input(Fore.LIGHTWHITE_EX+"Ingrese el nombre del cajero: ")
        if not nombre:
            print(Fore.LIGHTRED_EX+"Error: El nombre del cajero no puede estar vacío.")
            return
        id_cajero = len(sucursal.cajeros) + 1
        sucursal.agregar_cajero(id_cajero, nombre)
        print(Fore.LIGHTGREEN_EX+f"Cajero '{nombre}' agregado con éxito a la sucursal '{sucursal.nombre}'.")
    else:
        print(Fore.LIGHTRED_EX+"Sucursal no Encontrada.")

def agregar_saldo_a_cajero():
    if not lista_sucursales:
        print(Fore.LIGHTRED_EX+"No hay sucursales registradas.")
        return

    print(Fore.LIGHTWHITE_EX+"Sucursales registradas:")
    for sucursal in lista_sucursales:
        print(f"{sucursal.id_sucursal}: {sucursal.nombre}")

    try:
        id_sucursal = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la sucursal: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id del la sucursal debe ser un número entero")
        return
    sucursal = next((s for s in lista_sucursales if s.id_sucursal == id_sucursal), None)
    if sucursal:
        if not sucursal.cajeros:
            print(Fore.LIGHTRED_EX+"No hay cajeros registrados en esta sucursal.")
            return

        print(Fore.LIGHTWHITE_EX+"Cajeros registrados:")
        for cajero in sucursal.cajeros:
            print(f"{cajero.id_cajero}: {cajero.nombre}")
        try:
            id_cajero = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cajero: "))
        except ValueError:
            print(Fore.LIGHTRED_EX+"El id del cajero debe ser un número entero")
            return
        cajero = next((c for c in sucursal.cajeros if c.id_cajero == id_cajero), None)
        if cajero:
            billetes = {}
            for denominacion in [200, 100, 50, 20, 10]:
                try:
                    cantidad = int(input(Fore.LIGHTWHITE_EX+f"Ingrese la cantidad de billetes de {denominacion}: "))
                except ValueError:
                    print(Fore.LIGHTRED_EX+"La cantidad de billetes debe ser un número entero")
                    return
                billetes[denominacion] = cantidad
            cajero.agregar_saldo(billetes)
            print(Fore.LIGHTGREEN_EX+f"Saldo agregado con éxito al cajero '{cajero.nombre}'.")
        else:
            print(Fore.LIGHTRED_EX+"Cajero no Encontrado.")
    else:
        print(Fore.LIGHTRED_EX+"Sucursal no Encontrada.")
def ver_datos_sucursal_por_id():

    if not lista_sucursales:
        print(Fore.LIGHTRED_EX+"No hay sucursales registradas.")
        return

    print(Fore.LIGHTWHITE_EX+"Sucursales registradas:")
    for sucursal in lista_sucursales:
        print(Fore.LIGHTWHITE_EX+f"{sucursal.id_sucursal}: {sucursal.nombre}")

    try:
        id_sucursal = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la sucursal: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id de la sucursal debe ser un número entero")
        return

    sucursal = next((s for s in lista_sucursales if s.id_sucursal == id_sucursal), None)
    if sucursal:
        print(Fore.LIGHTWHITE_EX+f"Sucursal: {sucursal.nombre}")
        print(f"Ciudad: {sucursal.ciudad}")
        print(f"Dirección: {sucursal.direccion}")
        print("Cajeros:")
        for cajero in sucursal.cajeros:
            print(f"  - Cajero: {cajero.nombre}")
            print(f"  -  Saldo: {cajero.saldo}")
            print(f"  -  Ciudad: {cajero.ciudad}")
            print(f"  -  Dirección: {cajero.direccion}")
    else:
        print(Fore.LIGHTRED_EX+"Sucursal no Encontrada.")

def ver_datos_cajero_por_id():
    if not lista_sucursales:
        print(Fore.LIGHTRED_EX+"No hay sucursales registradas.")
        return

    print(Fore.LIGHTWHITE_EX+"Sucursales registradas:")
    for sucursal in lista_sucursales:
        print(f"{sucursal.id_sucursal}: {sucursal.nombre}")

    try:
        id_sucursal = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la sucursal: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"Error al seleccionar la sucursal, intente nuevamente.")
        return

    sucursal = next((s for s in lista_sucursales if s.id_sucursal == id_sucursal), None)
    if sucursal:
        if not sucursal.cajeros:
            print(Fore.LIGHTRED_EX+"No hay cajeros registrados en esta sucursal.")
            return

        print(Fore.LIGHTWHITE_EX+"Cajeros registrados:")
        for cajero in sucursal.cajeros:
            print(f"{cajero.id_cajero}: {cajero.nombre}")

        try:
            id_cajero = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cajero: "))
        except ValueError:
            print(Fore.LIGHTRED_EX+"El id del cajero debe ser un número entero")
            return

        cajero = next((c for c in sucursal.cajeros if c.id_cajero == id_cajero), None)
        if cajero:
            print(Fore.LIGHTWHITE_EX+f"Cajero: {cajero.nombre}")
            print(f"Saldo: {cajero.saldo}")
            print(f"Ciudad: {cajero.ciudad}")
            print(f"Dirección: {cajero.direccion}")
            print(f"Billetes disponibles:")
            for denominacion, cantidad in cajero.billetes.items():
                print(Fore.LIGHTWHITE_EX+f"  - {denominacion}: {cantidad}")
        else:
            print(Fore.LIGHTRED_EX+"Cajero no Encontrado.")
    else:
        print(Fore.LIGHTRED_EX+"Sucursal no Encontrada.")
#Algoritmo de busquedad por igualación
def seleccionar_cajero():
    if not lista_sucursales:
        print(Fore.LIGHTRED_EX+"No hay sucursales registradas...")
        return None

    print(Fore.LIGHTWHITE_EX+"Sucursales registradas:")
    for sucursal in lista_sucursales:
        print(Fore.LIGHTWHITE_EX+f"{sucursal.id_sucursal}: {sucursal.nombre}")
    try:
        id_sucursal = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la sucursal: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id de la sucursal debe ser un número entero")
        return
    sucursal = next((s for s in lista_sucursales if s.id_sucursal == id_sucursal), None)
    if sucursal:
        if not sucursal.cajeros:
            print(Fore.LIGHTRED_EX+"No hay cajeros registrados en esta sucursal.")
            return None

        print(Fore.LIGHTWHITE_EX+"Cajeros registrados:")
        for cajero in sucursal.cajeros:
            print(Fore.LIGHTWHITE_EX+f"{cajero.id_cajero}: {cajero.nombre}")
        try:
            id_cajero = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID del cajero: "))
        except ValueError:
            print(Fore.LIGHTRED_EX+"El id del cajero debe ser un número entero")
            return
        cajero = next((c for c in sucursal.cajeros if c.id_cajero == id_cajero), None)
        if cajero:
            return cajero
        else:
            print(Fore.LIGHTRED_EX+"Cajero no Encontrado.")
            return None
    else:
        print(Fore.LIGHTRED_EX+"Sucursal no Encontrada.")
        return None
def seleccionar_sucursal():
    if not lista_sucursales:
        print(Fore.LIGHTRED_EX+"No hay sucursales registradas.")
        return None

    print("Sucursales registradas:")
    for sucursal in lista_sucursales:
        print(Fore.LIGHTWHITE_EX+f"{sucursal.id_sucursal}: {sucursal.nombre}")
    try:
        id_sucursal = int(input(Fore.LIGHTWHITE_EX+"Ingrese el ID de la sucursal: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El id de la sucursal debe ser un número entero")
        return
    sucursal = next((s for s in lista_sucursales if s.id_sucursal == id_sucursal), None)
    if sucursal:
        return sucursal
    else:
        print(Fore.LIGHTRED_EX+"Sucursal no Encontrada.")
        return None
def editar_sucursal_cajero(cajero):
    nueva_sucursal = seleccionar_sucursal()
    if nueva_sucursal:
        # Eliminar cajero de la sucursal actual
        sucursal_actual = next((s for s in lista_sucursales if s.id_sucursal == cajero.id_sucursal), None)
        if sucursal_actual:
            sucursal_actual.eliminar_cajero(cajero.id_cajero)

        # Actualizar datos del cajero
        cajero.id_sucursal = nueva_sucursal.id_sucursal
        cajero.ciudad = nueva_sucursal.ciudad
        cajero.direccion = nueva_sucursal.direccion

        # Agregar cajero a la nueva sucursal
        nueva_sucursal.cajeros.append(cajero)
        print(Fore.LIGHTGREEN_EX+f"Sucursal del cajero '{cajero.nombre}' actualizada con éxito.")
def editar_informacion_cajero():
    cajero = seleccionar_cajero()
    if cajero:
        print(Fore.LIGHTWHITE_EX+f"Editar información del cajero '{cajero.nombre}':")
        print("1. Editar nombre")
        print("2. Editar saldo del cajero")
        print("3. Editar sucursal del cajero")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == '1':
            nuevo_nombre = input("Ingrese el nuevo nombre del cajero: ")
            cajero.nombre = nuevo_nombre
            print(Fore.LIGHTGREEN_EX+f"Nombre del cajero actualizado a '{nuevo_nombre}'.")
        elif opcion == '2':
            billetes = {}
            for denominacion in [200, 100, 50, 20, 10]:
                try:
                    cantidad = int(input(Fore.LIGHTWHITE_EX+f"Ingrese la cantidad de billetes de {denominacion}: "))
                except ValueError:
                    print(Fore.LIGHTRED_EX+"La cantidad de billetes debe ser un número entero")
                    return
                billetes[denominacion] = cantidad
            cajero.editar_saldo(billetes)
        elif opcion == '3':
            editar_sucursal_cajero(cajero)
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida. Por favor, seleccione una opción válida.")
def eliminar_cajero():
    cajero = seleccionar_cajero()
    if cajero:
        if cajero.saldo > 0:
            print(Fore.LIGHTRED_EX+"El cajero tiene dinero disponible, no se puede eliminar.")
        else:
            for sucursal in lista_sucursales:
                if cajero in sucursal.cajeros:
                    sucursal.cajeros.remove(cajero)
                    print(Fore.LIGHTGREEN_EX+f"El cajero '{cajero.nombre}' se eliminó correctamente.")
                    break
def editar_informacion_sucursal():
    sucursal = seleccionar_sucursal()
    if sucursal:
        print(Fore.LIGHTWHITE_EX+"\nSucursal encontrada:")
        print(f"ID: {sucursal.id_sucursal}")
        print(f"Nombre: {sucursal.nombre}")
        print(f"Ciudad: {sucursal.ciudad}")
        print(f"Dirección: {sucursal.direccion}")

        print("\nOpciones de edición:")
        print("1. Editar nombre")
        print("2. Editar ciudad")
        print("3. Editar dirección")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == '1':
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            sucursal.nombre = nuevo_nombre
            print(Fore.LIGHTGREEN_EX+"Nombre de la sucursal actualizado correctamente.")
        elif opcion == '2':
            nueva_ciudad = input(Fore.LIGHTWHITE_EX+"Ingrese la nueva ciudad: ")
            sucursal.ciudad = nueva_ciudad
            for cajero in sucursal.cajeros:
                cajero.ciudad = nueva_ciudad
            print(Fore.LIGHTGREEN_EX+"Ciudad de la sucursal actualizada correctamente.")
        elif opcion == '3':
            nueva_direccion = input(Fore.LIGHTWHITE_EX+"Ingrese la nueva dirección: ")
            sucursal.direccion = nueva_direccion
            for cajero in sucursal.cajeros:
                cajero.direccion = nueva_direccion
            print(Fore.LIGHTGREEN_EX+"Dirección de la sucursal actualizada correctamente.")
        else:
            print(Fore.LIGHTRED_EX+"Opción no válida.")
def eliminar_sucursal():
    sucursal = seleccionar_sucursal()
    if sucursal:
        if sucursal.cajeros:
            print(Fore.LIGHTRED_EX+"La sucursal tiene cajeros registrados, no se puede eliminar.")
        else:
            lista_sucursales.remove(sucursal)
            print(Fore.LIGHTGREEN_EX+"Sucursal eliminada correctamente.")

# Funciones del cliente para realizar retiros, depósitos, transferencias, pagos de servicios, consultas de saldos y movimientos.
def retirar_dinero(cuenta, cliente):
    if cliente.estado != "Activo":
        print(Fore.LIGHTRED_EX+"Tu cuenta está inactiva, no puedes realizar retiros.")
        return

    cajero = seleccionar_cajero()
    if not cajero:
        return
    
    try:
        monto = float(input(Fore.LIGHTWHITE_EX+"Ingrese el monto a retirar: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El monto que ha ingresado no es válido. vuelve a intentar")
        return
    if monto > cuenta.saldo:
        print(Fore.LIGHTRED_EX+"Saldo insuficiente en la cuenta.")
        return

    if monto % 10 != 0:
        print(Fore.LIGHTRED_EX+"Monto Ingresado inválido para retirar.")
        return

    billetes_retirados = cajero.retirar_saldo(monto)
    if billetes_retirados:
        cuenta.saldo -= monto
        cuenta.registrar_movimiento("retiro", monto)
        print(Fore.LIGHTGREEN_EX+f"Se han retirado {monto} de su cuenta. Saldo actual: {cuenta.saldo}")
        print(Fore.LIGHTWHITE_EX+"Desglose de billetes:")
        for denominacion, cantidad in billetes_retirados.items():
            print(Fore.LIGHTWHITE_EX+f"Billetes de {denominacion}: {cantidad}")
    else:
        print(Fore.LIGHTRED_EX+"No se pudo realizar el retiro. Intente con otro monto o cajero.")
def depositar_dinero(cuenta, cliente):
    if cliente.estado != "Activo":
        print(Fore.LIGHTRED_EX+"Tu cuenta está inactiva, no puedes realizar depósitos.")
        return

    cajero = seleccionar_cajero()
    if not cajero:
        print(Fore.LIGHTRED_EX+"No se pudo realizar el depósito. Contacte a soporte.")
        return

    billetes = {}
    for denominacion in [200, 100, 50, 20, 10]:
        try:
            cantidad = int(input(Fore.LIGHTWHITE_EX+f"Ingrese la cantidad de billetes de {denominacion}: "))
        except ValueError:
            print(Fore.LIGHTRED_EX+"La cantidad de billetes debe ser un número entero")
            return 
        billetes[denominacion] = cantidad

    monto = sum(denominacion * cantidad for denominacion, cantidad in billetes.items())
    cuenta.saldo += monto
    cuenta.registrar_movimiento("deposito", monto)
    cajero.agregar_saldo(billetes)

    print(Fore.LIGHTGREEN_EX+f"Se han depositado {monto} a su cuenta. Saldo actual: {cuenta.saldo}")
def transferir_dinero(cuenta, cliente):
    if cliente.estado != "Activo":
        print(Fore.LIGHTRED_EX+"Tu cuenta está inactiva, no puedes realizar transferencias.")
        return

    numero_cuenta_destino = input(Fore.LIGHTWHITE_EX+"Ingrese el número de cuenta destino: ")
    try:
        monto = float(input(Fore.LIGHTWHITE_EX+"Ingrese el monto a transferir: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El monto ingresado no es válido. intente nuevamente")
        return

    cuenta_destino = None
    for cliente in clientes:
        for c in cliente.cuentas:
            if c.numero_cuenta == numero_cuenta_destino:
                cuenta_destino = c
                break
        if cuenta_destino:
            break

    if not cuenta_destino:
        print(Fore.LIGHTRED_EX+"Cuenta de destino no encontrada.")
        return



    if cuenta_destino.cliente.estado != "Activo":
        print(Fore.LIGHTRED_EX+"La cuenta de destino está inactiva, no puede recibir ni enviar dinero.")
        return

    if monto > cuenta.saldo:
        print(Fore.LIGHTRED_EX+"Saldo insuficiente en la cuenta.")
    else:
        cuenta.saldo -= monto
        cuenta.registrar_movimiento("transferencia retiro", monto)
        cuenta_destino.saldo += monto
        cuenta_destino.registrar_movimiento("transferencia ingreso", monto)
        print(Fore.LIGHTGREEN_EX+f"Se han transferido {monto} a la cuenta {numero_cuenta_destino}. Saldo actual: {cuenta.saldo}")
def pagar_servicios(cuenta, cliente):
    if cliente.estado != "Activo":
        print(Fore.LIGHTRED_EX+"Tu cuenta está inactiva, no puedes realizar pagos de servicios.")
        return

    try:
        monto = float(input(Fore.LIGHTWHITE_EX+"Ingrese el monto a pagar por el servicio: "))
    except ValueError:
        print(Fore.LIGHTRED_EX+"El monto ingresado no es válido. intente nuvamente")

    if monto > cuenta.saldo:
        print(Fore.LIGHTRED_EX+"Saldo insuficiente en la cuenta.")
    else:
        cuenta.saldo -= monto
        print(Fore.LIGHTGREEN_EX+f"Se han pagado {monto} por el servicio. Saldo actual: {cuenta.saldo}")
        cuenta.registrar_movimiento("pago de servicio", monto)
def consultar_saldo(cuenta):
    print(Fore.LIGHTWHITE_EX+f"El saldo de la cuenta es: {cuenta.saldo}")
    return cuenta.saldo
def consultar_movimientos(cuenta):
    movimientos = cuenta.obtener_movimientos()
    print(Fore.LIGHTWHITE_EX+"\n------ Movimientos de la Cuenta ------")
    for movimiento in movimientos:
        fecha_hora, tipo, monto = movimiento
        if tipo == "retiro" or tipo == "transferencia retiro" or tipo == "pago de servicio":
            print(Fore.LIGHTRED_EX+f"Fecha y Hora: {fecha_hora} | Tipo: {tipo} | Monto: {monto}")
        else:
            print(Fore.LIGHTWHITE_EX+f"Fecha y Hora: {fecha_hora} | Tipo: {tipo} | Monto: {monto}")
# Ejecución del programa
menu_principal()
