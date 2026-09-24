# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Visibilidad de Apps por Usuario',
    'version': '16.0.2.0.0',
    'category': 'Administration',
    'summary': 'Control granular per-user de la visibilidad de aplicaciones en el menú principal con actualización instantánea en Odoo 16.',
    'description': """
Módulo de Restricción de Visibilidad de Aplicaciones para Odoo 16
==============================================================

- Todas las aplicaciones vienen tildadas por defecto para todos los usuarios.
- El administrador desmarca únicamente las aplicaciones que desea ocultar para cada usuario, desde la pestaña "Visibilidad de Apps" en la ficha del usuario.
- La lista de aplicaciones se genera dinámicamente desde los menús raíz instalados: un módulo nuevo aparece solo, sin tocar código.
- Filtrado en tiempo real a través de load_menus (el método que alimenta el waffle menu / selector de apps).
""",
    'author': 'Desarrollo Custom',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
