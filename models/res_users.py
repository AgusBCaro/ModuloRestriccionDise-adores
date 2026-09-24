# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Campo Many2many de Selección Dinámica de Menús Ocultos
    restricted_app_ids = fields.Many2many(
        'ir.ui.menu',
        'res_users_restricted_app_rel',
        'user_id',
        'menu_id',
        string="Aplicaciones Ocultas / Restringidas",
        domain=[('parent_id', '=', False)],
        help="Seleccione las aplicaciones (menús principales) que se deben OCULTAR a este usuario."
    )

    # Campos Booleanos de Visibilidad por Aplicación
    show_app_discuss = fields.Boolean(string="Conversaciones", default=True)
    show_app_calendar = fields.Boolean(string="Calendario", default=True)
    show_app_designs = fields.Boolean(string="Diseños", default=True)
    show_app_helpdesk = fields.Boolean(string="Mesa de Ayuda", default=True)
    show_app_contacts = fields.Boolean(string="Contactos", default=True)
    show_app_crm = fields.Boolean(string="CRM", default=True)
    show_app_sale = fields.Boolean(string="Ventas", default=True)
    show_app_dashboard = fields.Boolean(string="Tableros", default=True)
    show_app_pos = fields.Boolean(string="Punto de venta", default=True)
    show_app_account = fields.Boolean(string="Facturación / Contabilidad", default=True)
    show_app_project = fields.Boolean(string="Proyecto", default=True)
    show_app_timesheet = fields.Boolean(string="Partes de horas", default=True)
    show_app_website = fields.Boolean(string="Sitio web", default=True)
    show_app_survey = fields.Boolean(string="Encuestas", default=True)
    show_app_stock = fields.Boolean(string="Inventario", default=True)
    show_app_repair = fields.Boolean(string="Reparaciones", default=True)
    show_app_hr = fields.Boolean(string="Empleados", default=True)
    show_app_link_tracker = fields.Boolean(string="Rastreador de enlaces", default=True)
    show_app_apps = fields.Boolean(string="Aplicaciones", default=True)
    show_app_settings = fields.Boolean(string="Ajustes", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        users = super(ResUsers, self).create(vals_list)
        visibility_category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
        if visibility_category:
            groups = self.env['res.groups'].sudo().search([('category_id', '=', visibility_category.id)])
            if groups:
                for user in users:
                    user.sudo().write({'groups_id': [(4, g.id) for g in groups]})
        return users
