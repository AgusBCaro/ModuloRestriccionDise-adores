# Módulo de Restricción de Visibilidad de Apps por Usuario (Odoo 16)

Módulo personalizado para **Odoo 16** que permite activar o desactivar la visibilidad de aplicaciones en el menú principal (**waffle menu / selector de aplicaciones**) con **actualización instantánea en tiempo real**.

---

## 🚀 Características Clave

1. **Todas las Aplicaciones Tildadas por Defecto:**
   - Nadie pierde acceso accidentalmente al instalar el módulo. Todos los usuarios (existentes y nuevos) comienzan con todas las casillas activadas ($\checkmark$).
   - El administrador simplemente desmarca ($\square$) las aplicaciones que no desea que ese usuario vea.

2. **Filtrado en Tiempo Real en `load_menus`:**
   - Intercepta directamente el método oficial `load_menus()` que consume el cliente web de Odoo 16 para renderizar los iconos del menú principal (waffle menu / app switcher).
   - Elimina la aplicación y todos sus submenús del árbol JSON retornado al navegador.

3. **Actualización Instantánea en la Interfaz:**
   - Invalida la memoria caché (`ormcache`) de Odoo inmediatamente al hacer clic en **Guardar** (`write()`).
   - El cambio se refleja de forma instantánea al recargar la página (F5) o navegar, sin necesidad de reiniciar el servicio ni el servidor.

4. **Doble Acceso Sincronizado:**
   - En la pestaña **Visibilidad de Apps** (con botones "Habilitar Todas" y "Desmarcar Todas").
   - En la pestaña nativa **Derechos de acceso** bajo la sección **VISIBILIDAD DE APLICACIONES**.

---

## 🛠️ Estructura del Módulo

```text
ModuloRestriccionDiseñadores/
├── __init__.py                      # Importación y post_init_hook (asigna True a todos en BD)
├── __manifest__.py                  # Manifiesto Odoo 16
├── README.md
├── security/
│   └── app_visibility_security.xml  # Categoría y grupos de seguridad Odoo
├── models/
│   ├── __init__.py
│   ├── ir_ui_menu.py                # Interceptación de load_menus() en tiempo real
│   └── res_users.py                 # Campos booleanos, sincronización y limpieza inmediata de caché
└── views/
    └── res_users_views.xml          # Pestaña "Visibilidad de Apps" en ficha de usuario
```

---

## 🔧 Instalación / Actualización en el Servidor VPS

```bash
/opt/odoo2/odoo-venv/bin/python3 /opt/odoo2/odoo/odoo-bin -c /etc/odoo.conf -d VEODATA-ORIGINAL -u ModuloRestriccionDise-adores --stop-after-init
systemctl restart odoo
```
