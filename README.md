# Módulo de Restricción de Visibilidad de Apps por Usuario (Odoo 16)

Módulo personalizado para **Odoo 16** que permite activar o desactivar la visibilidad de aplicaciones en el menú principal (**waffle menu / selector de aplicaciones**) de forma granular y por usuario, combinando un **selector dinámico multiselect** y casillas rápidas por categoría.

---

## 🚀 Características Principales

1. **Selector Dinámico de Aplicaciones Instaladas:**
   - Muestra **todas las aplicaciones instaladas** en su base de datos Odoo (módulos estándar y personalizados como *Diseñador*, *Redes*, *Diseños*, *Mesa de Ayuda*, etc.) mediante casillas de verificación automáticas (`widget="many2many_checkboxes"`).
2. **Casillas Rápidas Predefinidas:**
   - Permite controlar rápidamente las principales aplicaciones mediante booleanos categorizados.
3. **Hook de Inicialización Post-Instalación (`post_init_hook`):**
   - Asegura que al instalar o actualizar el módulo en una base de datos existente, los usuarios conserven `True` por defecto, **evitando que queden con casillas nulas/desmarcadas o que se oculten aplicaciones accidentalmente**.
4. **Acceso Ampliado a Administradores:**
   - Accesible tanto para **Administradores del Sistema** (`base.group_system`) como para **Administradores de Permisos/Derechos de Acceso** (`base.group_erp_manager`).
   - El superusuario administrador (ID 1) mantiene acceso total garantizado.
5. **Botones de Acción Rápida:**
   - **"Habilitar Todas"** y **"Ocultar Todas"** para configurar permisos en un solo clic.

---

## 📋 Aplicaciones Soportadas

| Categoría | Cobertura |
| :--- | :--- |
| **Módulos Personalizados / Todos** | **Detección Dinámica Automática** de cualquier menú principal de Odoo (*Diseñador*, *Redes*, *Diseños*, etc.) |
| **Comunicación y Productividad** | Conversaciones, Calendario, Contactos, Tableros |
| **Ventas y Operaciones Comercial** | CRM, Ventas, Punto de Venta, Facturación / Contabilidad |
| **Proyectos y Servicios** | Proyecto, Partes de Horas, Mesa de Ayuda, Diseños |
| **Inventario y Fabricación** | Inventario, Reparaciones |
| **Recursos Humanos y Marketing** | Empleados, Sitio Web, Encuestas, Rastreador de Enlaces |
| **Sistema y Configuración** | Aplicaciones, Ajustes |

---

## 🛠️ Estructura del Módulo

```text
ModuloRestriccionDiseñadores/
├── __init__.py          # Importación de modelos y post_init_hook
├── __manifest__.py      # Manifiesto Odoo 16 con versión y dependencias
├── README.md
├── models/
│   ├── __init__.py
│   ├── ir_ui_menu.py    # Lógica de filtrado dinámico en _filter_visible_menus()
│   └── res_users.py     # Campo Many2many restricted_app_ids y campos booleanos por usuario
└── views/
    └── res_users_views.xml # Pestaña "Visibilidad de Apps" con selector dinámico
```

---

## 🔧 Modo de Instalación y Actualización

1. **Copiar el módulo** a su carpeta de `addons` personalizada en su servidor Odoo 16.
2. **Reiniciar el servicio de Odoo**.
3. Activar el **Modo Desarrollador** (`Ajustes -> Activar modo desarrollador`).
4. Ir a **Aplicaciones -> Actualizar Lista de Aplicaciones**.
5. Buscar `Restricción de Visibilidad de Apps por Usuario` y hacer clic en **Actualizar / Instalar**.

---

## 💡 Modo de Uso

1. Ir a **Ajustes -> Usuarios y Compañías -> Usuarios**.
2. Seleccionar el usuario al cual desea configurar la visibilidad.
3. Navegar a la pestaña **Visibilidad de Apps**.
4. En **Selector Dinámico de Aplicaciones Instaladas**, marque la casilla de cualquier aplicación (estándar o personalizada) que desee **ocultar** a ese usuario.
5. Hacer clic en **Guardar**.
6. Al recargar la página o iniciar sesión con dicho usuario, la aplicación ocultada dejará de aparecer en su selector de apps (waffle menu).
