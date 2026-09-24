# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Visibilidad de Apps por Usuario',
    'version': '16.0.1.2.0',
    'category': 'Administration',
    'summary': 'Control granular per-user de la visibilidad de aplicaciones en el menú principal integrado en Derechos de Acceso de Odoo 16.',
    'description': """
Módulo de Restricción de Visibilidad de Aplicaciones para Odoo 16
==============================================================

Integra casillas de verificación nativas de Odoo en la pestaña 'Derechos de acceso' 
bajo la categoría 'VISIBILIDAD DE APLICACIONES' para habilitar o deshabilitar la 
visibilidad de los módulos en el menú principal (waffle menu / app switcher).
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
