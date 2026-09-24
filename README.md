# Módulo de Restricción de Visibilidad de Apps por Usuario (Odoo 16)

Módulo personalizado para **Odoo 16** que permite activar o desactivar la visibilidad de aplicaciones en el menú principal (**waffle menu / selector de aplicaciones**) de forma granular y por usuario, a través de casillas de verificación (checkboxes) simples y visuales.

---

## 🚀 Características Principales

1. **Control Granular por Usuario:**
   - Cada usuario posee una pestaña dedicada en su ficha de usuario en Odoo (**Visibilidad de Apps**) donde el administrador puede tildar o destildar exactamente qué aplicaciones puede ver.
2. **Protección y Seguridad:**
   - La pestaña de configuración está restringida para que solo los **Administradores del Sistema** (`base.group_system`) puedan modificar los permisos de visibilidad.
   - El superusuario administrador (ID 1) mantiene el acceso para evitar bloqueos accidentales.
3. **Botones de Acción Rápida:**
   - Incluye los botones **"Habilitar Todas"** y **"Deshabilitar Todas"** para configurar permisos en un solo clic.
4. **Triple Estrategia de Coincidencia (Ultra Robusto):**
   - Coincidencia por **XML ID** estándar de Odoo.
   - Coincidencia por **Nombre Técnico del Módulo** (`web_icon`).
   - Coincidencia por **Nombre Visible del Menú** (admite traducciones y módulos personalizados como *Diseños*).
5. **Compatibilidad:**
   - Funciona sin romper los permisos de datos subyacentes (`res.groups`), afectando únicamente la capa visual del menú principal.

---

## 📋 Aplicaciones Soportadas

| Categoría | Aplicaciones Soportadas |
| :--- | :--- |
| **Comunicación y Productividad** | Conversaciones, Calendario, Contactos, Tableros |
| **Ventas y Operaciones Comerciales** | CRM, Ventas, Punto de Venta, Facturación / Contabilidad |
| **Proyectos y Servicios** | Proyecto, Partes de Horas, Mesa de Ayuda, Diseños |
| **Inventario y Fabricación** | Inventario, Reparaciones |
| **Recursos Humanos y Marketing** | Empleados, Sitio Web, Encuestas, Rastreador de Enlaces |
| **Sistema y Configuración** | Aplicaciones, Ajustes |

---

## 🛠️ Estructura del Módulo

```text
ModuloRestriccionDiseñadores/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── ir_ui_menu.py      # Lógica de filtrado de menús en _filter_visible_menus()
│   └── res_users.py       # Campos Booleanos por usuario y métodos de acción masiva
└── views/
    └── res_users_views.xml # Pestaña "Visibilidad de Apps" en la vista formulario de usuarios
```

---

## 🔧 Modo de Instalación

1. **Copiar el módulo** a su carpeta de `addons` personalizada en su servidor Odoo 16.
2. **Reiniciar el servicio de Odoo** o actualizar la lista de módulos.
3. Activar el **Modo Desarrollador** en Odoo (`Ajustes -> Activar modo desarrollador`).
4. Ir a **Aplicaciones -> Actualizar Lista de Aplicaciones**.
5. Buscar `Restricción de Visibilidad de Apps por Usuario` (o `app_menu_restriction`) y hacer clic en **Instalar**.

---

## 💡 Modo de Uso

1. Ir a **Ajustes -> Usuarios y Compañías -> Usuarios**.
2. Seleccionar el usuario al cual desea restringir o habilitar aplicaciones.
3. Navegar a la pestaña **Visibilidad de Apps**.
4. Marcar/desmarcar las casillas según las aplicaciones que el usuario deba visualizar en su menú principal.
5. Hacer clic en **Guardar**.
6. Al iniciar sesión o recargar la página, el usuario solo verá los iconos de las aplicaciones habilitadas en su selector de apps (waffle menu).
