# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Campo de Selección Dinámica de Menús/Apps Raíz a Ocultar (Soporta CUALQUIER módulo instalado)
    restricted_app_ids = fields.Many2many(
        'ir.ui.menu',
        'res_users_restricted_app_rel',
        'user_id',
        'menu_id',
        string="Aplicaciones Ocultas / Restringidas",
        domain=[('parent_id', '=', False)],
        help="Seleccione las aplicaciones (menús principales) que se deben OCULTAR a este usuario."
    )

    # Visibilidad de Módulos / Apps principales en Waffle Menu
    show_app_discuss = fields.Boolean(
        string="Conversaciones",
        default=True,
        help="Permite visualizar la aplicación 'Conversaciones' en el menú principal."
    )
    show_app_calendar = fields.Boolean(
        string="Calendario",
        default=True,
        help="Permite visualizar la aplicación 'Calendario' en el menú principal."
    )
    show_app_designs = fields.Boolean(
        string="Diseños",
        default=True,
        help="Permite visualizar la aplicación 'Diseños' en el menú principal."
    )
    show_app_helpdesk = fields.Boolean(
        string="Mesa de Ayuda",
        default=True,
        help="Permite visualizar la aplicación 'Mesa de Ayuda' en el menú principal."
    )
    show_app_contacts = fields.Boolean(
        string="Contactos",
        default=True,
        help="Permite visualizar la aplicación 'Contactos' en el menú principal."
    )
    show_app_crm = fields.Boolean(
        string="CRM",
        default=True,
        help="Permite visualizar la aplicación 'CRM' en el menú principal."
    )
    show_app_sale = fields.Boolean(
        string="Ventas",
        default=True,
        help="Permite visualizar la aplicación 'Ventas' en el menú principal."
    )
    show_app_dashboard = fields.Boolean(
        string="Tableros",
        default=True,
        help="Permite visualizar la aplicación 'Tableros / Dashboards' en el menú principal."
    )
    show_app_pos = fields.Boolean(
        string="Punto de venta",
        default=True,
        help="Permite visualizar la aplicación 'Punto de Venta' en el menú principal."
    )
    show_app_account = fields.Boolean(
        string="Facturación / Contabilidad",
        default=True,
        help="Permite visualizar la aplicación 'Facturación / Contabilidad' en el menú principal."
    )
    show_app_project = fields.Boolean(
        string="Proyecto",
        default=True,
        help="Permite visualizar la aplicación 'Proyecto' en el menú principal."
    )
    show_app_timesheet = fields.Boolean(
        string="Partes de horas",
        default=True,
        help="Permite visualizar la aplicación 'Partes de horas' en el menú principal."
    )
    show_app_website = fields.Boolean(
        string="Sitio web",
        default=True,
        help="Permite visualizar la aplicación 'Sitio Web' en el menú principal."
    )
    show_app_survey = fields.Boolean(
        string="Encuestas",
        default=True,
        help="Permite visualizar la aplicación 'Encuestas' en el menú principal."
    )
    show_app_stock = fields.Boolean(
        string="Inventario",
        default=True,
        help="Permite visualizar la aplicación 'Inventario' en el menú principal."
    )
    show_app_repair = fields.Boolean(
        string="Reparaciones",
        default=True,
        help="Permite visualizar la aplicación 'Reparaciones' en el menú principal."
    )
    show_app_hr = fields.Boolean(
        string="Empleados",
        default=True,
        help="Permite visualizar la aplicación 'Empleados' en el menú principal."
    )
    show_app_link_tracker = fields.Boolean(
        string="Rastreador de enlaces",
        default=True,
        help="Permite visualizar la aplicación 'Rastreador de enlaces' en el menú principal."
    )
    show_app_apps = fields.Boolean(
        string="Aplicaciones",
        default=True,
        help="Permite visualizar el módulo 'Aplicaciones' en el menú principal."
    )
    show_app_settings = fields.Boolean(
        string="Ajustes",
        default=True,
        help="Permite visualizar el módulo 'Ajustes' en el menú principal."
    )

    def action_enable_all_apps(self):
        """Habilita el acceso a todas las aplicaciones para los usuarios seleccionados."""
        for user in self:
            user.write({
                'restricted_app_ids': [(5, 0, 0)],
                'show_app_discuss': True,
                'show_app_calendar': True,
                'show_app_designs': True,
                'show_app_helpdesk': True,
                'show_app_contacts': True,
                'show_app_crm': True,
                'show_app_sale': True,
                'show_app_dashboard': True,
                'show_app_pos': True,
                'show_app_account': True,
                'show_app_project': True,
                'show_app_timesheet': True,
                'show_app_website': True,
                'show_app_survey': True,
                'show_app_stock': True,
                'show_app_repair': True,
                'show_app_hr': True,
                'show_app_link_tracker': True,
                'show_app_apps': True,
                'show_app_settings': True,
            })

    def action_disable_all_apps(self):
        """Deshabilita el acceso a todas las aplicaciones para los usuarios seleccionados."""
        all_root_menus = self.env['ir.ui.menu'].search([('parent_id', '=', False)])
        for user in self:
            user.write({
                'restricted_app_ids': [(6, 0, all_root_menus.ids)],
                'show_app_discuss': False,
                'show_app_calendar': False,
                'show_app_designs': False,
                'show_app_helpdesk': False,
                'show_app_contacts': False,
                'show_app_crm': False,
                'show_app_sale': False,
                'show_app_dashboard': False,
                'show_app_pos': False,
                'show_app_account': False,
                'show_app_project': False,
                'show_app_timesheet': False,
                'show_app_website': False,
                'show_app_survey': False,
                'show_app_stock': False,
                'show_app_repair': False,
                'show_app_hr': False,
                'show_app_link_tracker': False,
                'show_app_apps': False,
                'show_app_settings': False,
            })
