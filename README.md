# Módulo de Restricción de Visibilidad de Apps por Usuario (Odoo 16)

Módulo personalizado para **Odoo 16** que permite activar o desactivar la visibilidad de aplicaciones en el menú principal (**waffle menu / selector de aplicaciones**) con **actualización instantánea en tiempo real**.

---

## 🚀 Características Clave

1. **Todas las Aplicaciones Tildadas por Defecto:**
   - Nadie pierde acceso accidentalmente al instalar el módulo. Todos los usuarios (existentes y nuevos) comienzan con todas las casillas activadas ($\checkmark$).
   - El administrador simplemente desmarca ($\square$) las aplicaciones que no desea que ese usuario vea.

2. **Lista de Apps 100% Dinámica — Se Adapta Sola a Módulos Nuevos:**
   - La pestaña "Visibilidad de Apps" se arma a partir de los menús raíz (`ir.ui.menu` con `parent_id = False`) realmente instalados en la base de datos.
   - **Cuando se instala un módulo nuevo, su app aparece sola como checkbox (tildada por defecto), sin tocar código.** No hay ningún diccionario ni lista hardcodeada que mantener.

3. **Filtrado en Tiempo Real en `load_menus`:**
   - Intercepta directamente el método oficial `load_menus()` que consume el cliente web de Odoo 16 para renderizar los iconos del menú principal (waffle menu / app switcher).
   - Elimina la aplicación y todos sus submenús del árbol JSON retornado al navegador, cruzando IDs reales de `ir.ui.menu` (sin heurísticas de nombre).
   - Un administrador (`base.group_system`) nunca se queda sin el menú de Ajustes, aunque lo desmarque o use "Desmarcar Todas".

4. **Única Fuente de Verdad:**
   - El dato real es `restricted_app_ids` (Many2many a `ir.ui.menu`) en `res.users`: la lista de apps ocultas para ese usuario.
   - La pestaña muestra `visible_app_ids`, un campo calculado (compute/inverse) sobre el anterior, con `widget="many2many_checkboxes"`.
   - No se usan grupos de seguridad nativos de Odoo (`res.groups` / categorías) para esto: se descartaron porque `load_menus()` no los lee y generaban una sección redundante y no funcional en "Derechos de Acceso" (ver Changelog).

---

## 📝 Changelog

- **16.0.2.0.0:** Reemplazados los 20 campos booleanos `show_app_*` y el diccionario heurístico `APP_RESTRICTIONS` (matching por xmlid/módulo/nombre) por un esquema dinámico basado en `restricted_app_ids` + `visible_app_ids` (compute/inverse) sobre los menús raíz reales. Las apps nuevas ya no requieren cambios de código. Se quita `post_init_hook` (ya no hace falta: lista vacía = todo visible).
- **16.0.1.4.0:** Se eliminaron los grupos de seguridad nativos (`security/app_visibility_security.xml`) y toda la sincronización `show_app_* -> groups_id`. Esos grupos generaban checkboxes automáticos en la pestaña nativa "Derechos de Acceso" que Odoo nunca conecta con `load_menus()`, por lo que no tenían ningún efecto real y solo confundían al admin.

---

## 🛠️ Estructura del Módulo

```text
ModuloRestriccionDiseñadores/
├── __init__.py                      # Importación de models
├── __manifest__.py                  # Manifiesto Odoo 16
├── README.md
├── models/
│   ├── __init__.py
│   ├── ir_ui_menu.py                # Interceptación de load_menus() en tiempo real
│   └── res_users.py                 # restricted_app_ids / visible_app_ids
└── views/
    └── res_users_views.xml          # Pestaña "Visibilidad de Apps" en ficha de usuario
```

---

## ➕ ¿Cómo se agrega una aplicación nueva?

No hay que hacer nada. Al instalar cualquier módulo que registre un menú raíz propio, ese menú aparece automáticamente como checkbox tildado en la pestaña "Visibilidad de Apps" de todos los usuarios, sin editar ningún archivo de este módulo.

---

## 🔧 Instalación / Actualización en el Servidor VPS

```bash
/opt/odoo2/odoo-venv/bin/python3 /opt/odoo2/odoo/odoo-bin -c /etc/odoo.conf -d VEODATA-ORIGINAL -u ModuloRestriccionDise-adores --stop-after-init
systemctl restart odoo
```
