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
