# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Visibilidad de Apps por Usuario',
    'version': '16.0.1.1.0',
    'category': 'Administration',
    'summary': 'Control granular y dinámico per-user de la visibilidad de aplicaciones en el menú principal de Odoo 16.',
    'description': """
Módulo de Restricción de Visibilidad de Aplicaciones para Odoo 16
==============================================================

Permite configurar de forma granular y por usuario qué aplicaciones/módulos
puede visualizar cada uno en el menú principal (waffle menu / app switcher).

Características:
----------------
- Selector dinámico mediante casillas de verificación (many2many_checkboxes) para TODAS las aplicaciones instaladas en la base de datos (módulos estándar y personalizados).
- Casillas booleanas rápidas predefinidas por categorías.
- Botones de acción masiva "Habilitar Todas" y "Ocultar Todas".
- Hook de inicialización post-instalación para evitar bloqueos por valores nulos.
- Acceso para Administradores de Sistema y Administradores de Usuarios (base.group_erp_manager).
""",
    'author': 'Desarrollo Custom',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/res_users_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
