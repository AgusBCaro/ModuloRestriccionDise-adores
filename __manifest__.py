# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Visibilidad de Apps por Usuario',
    'version': '16.0.1.3.0',
    'category': 'Administration',
    'summary': 'Control granular per-user de la visibilidad de aplicaciones en el menú principal con actualización instantánea en Odoo 16.',
    'description': """
Módulo de Restricción de Visibilidad de Aplicaciones para Odoo 16
==============================================================

- Todas las aplicaciones vienen tildadas por defecto para todos los usuarios.
- El administrador desmarca únicamente las aplicaciones que desea ocultar para cada usuario.
- Filtrado en tiempo real a través de load_menus (el método que alimenta el waffle menu / selector de apps).
- Actualización instantánea: invalida la caché de menús de inmediato al guardar en la interfaz sin necesidad de reiniciar el servicio.
""",
    'author': 'Desarrollo Custom',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/app_visibility_security.xml',
        'views/res_users_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
