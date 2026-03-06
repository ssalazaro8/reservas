# UniReserve - Sistema de Gestión de Reservas Universitarias

UniReserve es una plataforma digital para la gestión de reservas de espacios y servicios universitarios.  
El sistema centraliza la administración de recursos académicos y deportivos, permitiendo registrar usuarios, consultar recursos, crear reservas, validar disponibilidad y gestionar cancelaciones.

Este proyecto corresponde a la **Entrega 1: Núcleo de Negocio y Exposición de API Profesional** de la asignatura **Arquitectura de Software**.

---

# Objetivo de la entrega

Desarrollar el **backend del sistema UniReserve** aplicando buenas prácticas de arquitectura de software y diseño de APIs.

El sistema implementa:

- API REST con **Django REST Framework**
- **Service Layer** para desacoplar lógica de negocio
- **Patrones de diseño creacionales**
- Validación de reglas de negocio
- Manejo adecuado de códigos HTTP
- Arquitectura modular y extensible

---

# Dominio del sistema

El dominio original del sistema define **7 entidades principales**:

- Usuario
- Recurso
- Reserva
- Horario
- Pago
- InventarioRecurso
- Cancelación

Para esta entrega se implementó el **57.1 % del dominio (4 de 7 entidades)**:

- `User`
- `Resource`
- `Schedule`
- `Reservation`

Esto cumple con el requisito del entregable de implementar entre **50 % y 60 % del dominio**.

---

# Tecnologías utilizadas

- Python 3.11
- Django
- Django REST Framework
- SQLite
- Git + GitHub

---


---

# Arquitectura del sistema

El sistema sigue una arquitectura por capas con separación clara de responsabilidades.

Cliente
│
▼
APIView (views.py)
│
▼
Serializers
│
▼
Service Layer (services.py)
│
▼
Domain Components (builders, factories)
│
▼
Models (models.py)
│
▼
Base de datos


---


---

# Capas de la aplicación

## Models

Representan las entidades persistentes del dominio:

- User
- Resource
- Schedule
- Reservation

---

## Services

Contiene la lógica de negocio y los casos de uso del sistema.

Ejemplos:

- CreateReservationService
- CancelReservationService
- ListUserReservationHistoryService
- ReservationPricingService

Toda la lógica del sistema se ejecuta aquí.

---

## Serializers

Validan y transforman los datos de entrada y salida de la API.

Ejemplos:

- UserSerializer
- ResourceSerializer
- ReservationSerializer
- CreateReservationInputSerializer

---

## Views

Exponen los endpoints usando **APIView** de Django REST Framework.

Las views no contienen lógica de negocio, solo:

- reciben requests
- validan datos
- llaman servicios
- devuelven respuestas HTTP

---

## Domain

Contiene componentes auxiliares del dominio.

### Builders

Implementa el patrón **Builder**.

Se usa `ReservationBuilder` para construir reservas de forma controlada.

---

### Factories

Implementa el patrón **Factory**.

`PaymentGatewayFactory` permite seleccionar diferentes pasarelas de pago.

---

### Exceptions

Centraliza las excepciones de dominio.

Ejemplos:

- UserNotFoundError
- ResourceUnavailableError
- PaymentFailedError
- ReservationAlreadyCancelledError

---

# Patrones de diseño utilizados

## Builder

Se utiliza `ReservationBuilder` para construir la entidad `Reservation`.

Esto permite crear reservas paso a paso y validar los atributos antes de persistirlos.

Beneficios:

- Construcción clara de objetos complejos
- Menor acoplamiento
- Código más legible

---

## Factory

Se utiliza `PaymentGatewayFactory` para abstraer la creación de pasarelas de pago.

Esto permite cambiar fácilmente entre distintos proveedores de pago.

Implementaciones actuales:

- FakePaymentGateway
- RejectedPaymentGateway

---

# Endpoints disponibles

## Listar recursos

GET /api/resources/


Devuelve todos los recursos disponibles en el sistema.

---

## Crear reserva


POST /api/reservations/


Ejemplo de request:

```json
{
  "user_id": 1,
  "resource_id": 1,
  "date": "2026-03-10",
  "start_time": "10:00:00",
  "end_time": "11:00:00"
}

Respuesta esperada:

HTTP 201 Created
Cancelar reserva
DELETE /api/reservations/{reservation_id}/cancel/

Ejemplo:

DELETE /api/reservations/1/cancel/
Historial de reservas de un usuario
GET /api/users/{user_id}/reservations/

Ejemplo:

GET /api/users/1/reservations/


Reglas de negocio implementadas

Un usuario debe estar activo para reservar.

El horario debe ser válido (start_time < end_time).

Un recurso inactivo no puede reservarse.

No pueden existir traslapes de horario para un mismo recurso.

Si el recurso es premium se procesa pago.

Una reserva cancelada no puede cancelarse nuevamente.

Códigos HTTP utilizados
Código	Significado
201	Reserva creada correctamente
400	Datos inválidos
404	Recurso o usuario inexistente
409	Conflicto de horario o reserva cancelada