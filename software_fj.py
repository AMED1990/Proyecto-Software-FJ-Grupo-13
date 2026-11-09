import logging
from abc import ABC, abstractmethod

# ==========================================
# 1. CONFIGURACIÓN DEL ARCHIVO DE LOGS
# ==========================================
logging.basicConfig(
    filename='logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
class SoftwareFJException(Exception):
    pass

class DatoInvalidoException(SoftwareFJException):
    pass

class ServicioNoDisponibleException(SoftwareFJException):
    pass

class ReservaInvalidaException(SoftwareFJException):
    pass

# ==========================================
# 3. CLASES ABSTRACTAS Y ENTIDADES
# ==========================================
class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad

    @abstractmethod
    def obtener_detalles(self):
        pass

# ==========================================
# 4. CLASE CLIENTE (ENCAPSULACIÓN Y VALIDACIÓN)
# ==========================================
class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, email, telefono):
        super().__init__(id_cliente)
        self.__nombre = None
        self.__email = None
        self.__telefono = None
        
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise DatoInvalidoException("El nombre del cliente no puede estar vacío.")
        self.__nombre = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoException(f"El email '{valor}' no es válido.")
        self.__email = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if len(valor) < 7:
            raise DatoInvalidoException("El teléfono debe tener al menos 7 dígitos.")
        self.__telefono = valor

    def obtener_detalles(self):
        return f"Cliente ID: {self._id} | Nombre: {self.__nombre} | Email: {self.__email}"

# ==========================================
# 5. SERVICIOS (ABSTRACTA Y DERIVADAS - POLIMORFISMO)
# ==========================================
class Servicio(Entidad, ABC):
    def __init__(self, id_servicio, nombre, tarifa_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        pass

    @abstractmethod
    def describir(self):
        pass

    def obtener_detalles(self):
        return self.describir()

class ReservaSalas(Servicio):
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        costo = self.tarifa_base * duracion
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir(self):
        return f"Reserva de Sala - Tarifa por hora: ${self.tarifa_base}"

class AlquilerEquipos(Servicio):
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        costo = self.tarifa_base * duracion
        if duracion > 10:
            costo += 50000 
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir(self):
        return f"Alquiler de Equipos - Tarifa por hora: ${self.tarifa_base} (Recargo si > 10h)"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        horas_cobro = max(duracion, 2)
        costo = self.tarifa_base * horas_cobro
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir(self):
        return f"Asesoría Especializada - Tarifa por hora: ${self.tarifa_base} (Mínimo 2 horas)"

# ==========================================
# 6. CLASE RESERVA
# ==========================================
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def confirmar(self, impuesto=0.19, descuento=0.0):
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleException(f"El servicio {self.servicio.nombre} no está disponible.")
            if self.duracion <= 0:
                raise ReservaInvalidaException("La duración de la reserva debe ser mayor a 0.")
            
            self.costo_total = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} CONFIRMADA. Total: ${self.costo_total:.2f}")
            return True
        except Exception as e:
            self.estado = "Fallida"
            logging.error(f"Error al confirmar Reserva {self.id_reserva}: {str(e)}")
            raise 

    def cancelar(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaInvalidaException("La reserva ya está cancelada.")
            self.estado = "Cancelada"
            logging.info(f"Reserva {self.id_reserva} CANCELADA.")
        except Exception as e:
            logging.error(f"Error al cancelar Reserva {self.id_reserva}: {str(e)}")
            raise

# ==========================================
# 7. SISTEMA PRINCIPAL Y SIMULACIÓN (10+ OPERACIONES)
# ==========================================
class SoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.contador_id = 1

    def registrar_cliente(self, nombre, email, telefono):
        try:
            cliente = Cliente(self.contador_id, nombre, email, telefono)
        except DatoInvalidoException as e:
            logging.error(f"Fallo al registrar cliente: {e}")
            print(f"❌ Error: {e}")
        else:
            self.clientes.append(cliente)
            self.contador_id += 1
            logging.info(f"Cliente '{nombre}' registrado exitosamente.")
            print(f"✅ Cliente '{nombre}' registrado.")
        finally:
            print("-> Intento de registro de cliente finalizado.\n")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

# ------------------------------------------
# EJECUCIÓN DE LA SIMULACIÓN
# ------------------------------------------
if __name__ == "__main__":
    print("=== INICIANDO SIMULACIÓN SOFTWARE FJ ===\n")
    sistema = SoftwareFJ()

    # 1 y 2: Registro de clientes válidos e inválidos
    print("--- OPERACIÓN 1: Cliente Válido ---")
    sistema.registrar_cliente("Amed Minota", "amed@unad.edu.co", "3101234567")

    print("--- OPERACIÓN 2: Cliente Inválido (Email incorrecto) ---")
    sistema.registrar_cliente("Carlos Perez", "carlos_sin_arroba.com", "3209876543")

    # 3, 4 y 5: Creación de Servicios
    print("--- OPERACIÓN 3, 4 y 5: Creando Servicios ---")
    sala = ReservaSalas(101, "Sala VIP", 50000)
    equipo = AlquilerEquipos(102, "Proyector 4K", 30000)
    asesoria = AsesoriaEspecializada(103, "Asesoría en Python", 80000)
    
    sistema.agregar_servicio(sala)
    sistema.agregar_servicio(equipo)
    sistema.agregar_servicio(asesoria)
    print("✅ 3 Servicios creados exitosamente.\n")

    # 6: Reserva Exitosa
    print("--- OPERACIÓN 6: Reserva Exitosa (Sala) ---")
    if sistema.clientes:
        reserva1 = Reserva(1, sistema.clientes[0], sala, 3)
        try:
            reserva1.confirmar()
            print(f"✅ Reserva {reserva1.id_reserva} Exitosa. Total a pagar: ${reserva1.costo_total}")
        except Exception as e:
            print(f"❌ Fallo: {e}")
        finally:
            print("-> Proceso de reserva finalizado.\n")

    # 7: Reserva con Descuento e Impuestos (Sobrecarga)
    print("--- OPERACIÓN 7: Reserva con Descuento (Equipo) ---")
    if sistema.clientes:
        reserva2 = Reserva(2, sistema.clientes[0], equipo, 12) 
        try:
            reserva2.confirmar(impuesto=0.19, descuento=0.10)
            print(f"✅ Reserva {reserva2.id_reserva} Exitosa. Total con recargo e IVA: ${reserva2.costo_total}")
        except Exception as e:
            print(f"❌ Fallo: {e}")

    # 8: Reserva Fallida (Duración inválida - Encadenamiento)
    print("\n--- OPERACIÓN 8: Reserva Fallida (Duración 0) ---")
    if sistema.clientes:
        reserva3 = Reserva(3, sistema.clientes[0], asesoria, -2)
        try:
            reserva3.confirmar()
        except ReservaInvalidaException as e:
            try:
                raise ValueError("El parametro de duracion no puede ser negativo") from e
            except ValueError as causa_raiz:
                print(f"❌ Fallo Crítico: {causa_raiz}")
                logging.critical(f"Encadenamiento detectado: {causa_raiz}")
        finally:
            print("-> Sistema sigue operando sin caerse.\n")

    # 9: Servicio No Disponible
    print("--- OPERACIÓN 9: Servicio No Disponible ---")
    equipo.disponible = False 
    if sistema.clientes:
        reserva4 = Reserva(4, sistema.clientes[0], equipo, 2)
        try:
            reserva4.confirmar()
        except ServicioNoDisponibleException as e:
            print(f"❌ Fallo: {e}")

    # 10: Cancelación de Reserva
    print("\n--- OPERACIÓN 10: Cancelar Reserva Exitosa ---")
    try:
        reserva1.cancelar()
        print(f"✅ Reserva {reserva1.id_reserva} ahora esta en estado: {reserva1.estado}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n=== FIN DE LA SIMULACIÓN. Revisa el archivo 'logs.txt' ===")
