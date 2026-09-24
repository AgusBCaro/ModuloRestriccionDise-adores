# Módulo de Restricción de Visibilidad de Apps por Usuario (Odoo 16)

Módulo personalizado para **Odoo 16** que permite activar o desactivar la visibilidad de aplicaciones en el menú principal (**waffle menu / selector de aplicaciones**) de forma 100% nativa mediante **Grupos de Acceso (`res.groups`)** en la pestaña **Derechos de acceso**.

---

## 🚀 Características Principales

1. **Integración 100% Nativa en Derechos de Acceso:**
   - Añade una nueva sección llamada **VISIBILIDAD DE APLICACIONES** directamente en la pestaña estándar **Derechos de acceso** de cada usuario.
   - Funciona exactamene igual que los grupos de acceso nativos de Odoo (como *PROJECT*, *TECHNICAL*, *SALES*, etc.), mostrando casillas de verificación (checkboxes) con tooltip explicativo `?`.
2. **Casillas Tildables para Cada Aplicación:**
   - Permite tildar o destildar exactamente qué aplicaciones (*Conversaciones, Calendario, Diseños, Mesa de Ayuda, CRM, Ventas, Proyecto, Inventario, Facturación, etc.*) tiene permitidas cada usuario.
3. **Activas por Defecto:**
   - Todos los usuarios (existentes y nuevos) comienzan con todas las casillas de visibilidad tildadas por defecto. Al destildar una casilla, la aplicación correspondiente se oculta del menú principal del usuario.
4. **Hook de Inicialización Post-Instalación (`post_init_hook`):**
   - Asigna a todos los usuarios existentes los grupos de visibilidad al instalar o actualizar el módulo.

---

## 🛠️ Estructura del Módulo

```text
ModuloRestriccionDiseñadores/
├── __init__.py                      # Importación de modelos y post_init_hook
├── __manifest__.py                  # Manifiesto Odoo 16 con versión y dependencias
├── README.md
├── security/
│   └── app_visibility_security.xml  # Categoría ir.module.category y res.groups de Visibilidad
├── models/
│   ├── __init__.py
│   ├── ir_ui_menu.py                # Lógica de filtrado en _filter_visible_menus() basada en grupos
│   └── res_users.py                 # Auto-asignación de grupos al crear nuevos usuarios
└── views/
    └── res_users_views.xml
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
2. Seleccionar cualquier usuario.
3. En la pestaña nativa **Derechos de acceso**, ubicar la sección **VISIBILIDAD DE APLICACIONES**.
4. Tilde o destilde las casillas de las aplicaciones según corresponda.
5. Hacer clic en **Guardar**.
6. Al recargar o iniciar sesión con dicho usuario, las aplicaciones destildadas ya no aparecerán en su menú principal.
