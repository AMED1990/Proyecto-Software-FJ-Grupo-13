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
    """Excepción base para el sistema."""
    pass

class DatoInvalidoException(SoftwareFJException):
    """Para errores de validación de datos."""
    pass

class ServicioNoDisponibleException(SoftwareFJException):
    """Para cuando un servicio no está operativo."""
    pass

class ReservaInvalidaException(SoftwareFJException):
    """Para errores al procesar reservas."""
    pass

# ==========================================
# 3. CLASES ABSTRACTAS Y ENTIDADES
# ==========================================
class Entidad(ABC):
    """Clase abstracta base del sistema."""
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
        
        # Uso de setters para validar
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
        """Método sobrecargado: puede recibir solo duración o incluir impuestos/descuentos."""
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
        if duracion > 10: # Recargo por uso prolongado
            costo += 50000
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir(self):
        return f"Alquiler de Equipos - Tarifa por hora: ${self.tarifa_base} (Recargo si > 10h)"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        horas_cobro = max(duracion, 2) # Mínimo 2 horas
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


