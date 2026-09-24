# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Visibilidad de Apps por Usuario',
    'version': '16.0.1.0.0',
    'category': 'Administration',
    'summary': 'Control granular per-user de la visibilidad de aplicaciones en el menú principal de Odoo 16.',
    'description': """
Módulo de Restricción Visibilidad de Aplicaciones para Odoo 16
==============================================================

Permite configurar de forma granular y por usuario qué aplicaciones/módulos
puede visualizar cada uno en el menú principal (waffle menu / app switcher).

Aplicaciones soportadas:
------------------------
- Conversaciones
- Calendario
- Diseños
- Mesa de Ayuda
- Contactos
- CRM
- Ventas
- Tableros
- Punto de Venta
- Facturación / Contabilidad
- Proyecto
- Partes de Horas
- Sitio Web
- Encuestas
- Inventario
- Reparaciones
- Empleados
- Rastreador de Enlaces
- Aplicaciones
- Ajustes
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
