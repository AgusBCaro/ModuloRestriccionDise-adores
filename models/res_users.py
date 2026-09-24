# -*- coding: utf-8 -*-
from odoo import models, fields, api

FIELD_TO_GROUP_NAME = {
    'show_app_discuss': 'Conversaciones',
    'show_app_calendar': 'Calendario',
    'show_app_designs': 'Diseños',
    'show_app_helpdesk': 'Mesa de Ayuda',
    'show_app_contacts': 'Contactos',
    'show_app_crm': 'CRM',
    'show_app_sale': 'Ventas',
    'show_app_dashboard': 'Tableros',
    'show_app_pos': 'Punto de Venta',
    'show_app_account': 'Facturación / Contabilidad',
    'show_app_project': 'Proyecto',
    'show_app_timesheet': 'Partes de Horas',
    'show_app_website': 'Sitio Web',
    'show_app_survey': 'Encuestas',
    'show_app_stock': 'Inventario',
    'show_app_repair': 'Reparaciones',
    'show_app_hr': 'Empleados',
    'show_app_link_tracker': 'Rastreador de Enlaces',
    'show_app_apps': 'Aplicaciones',
    'show_app_settings': 'Ajustes',
}

class ResUsers(models.Model):
    _inherit = 'res.users'

    restricted_app_ids = fields.Many2many(
        'ir.ui.menu',
        'res_users_restricted_app_rel',
        'user_id',
        'menu_id',
        string="Aplicaciones Ocultas / Restringidas",
        domain=[('parent_id', '=', False)],
        help="Seleccione las aplicaciones (menús principales) que se deben OCULTAR a este usuario."
    )

    # Todas las aplicaciones tildadas (True) por defecto para que nadie pierda acceso inicialmente
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
        # Asignar grupos de visibilidad por defecto a todos los nuevos usuarios
        category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
        if category:
            groups = self.env['res.groups'].sudo().search([('category_id', '=', category.id)])
            if groups:
                for user in users:
                    user.sudo().write({'groups_id': [(4, g.id) for g in groups]})
        # Limpiar caché de menús de inmediato
        self.env['ir.ui.menu'].clear_caches()
        return users

    def write(self, vals):
        res = super(ResUsers, self).write(vals)

        # Si se modificó algún campo de visibilidad o de grupos
        visibility_fields = list(FIELD_TO_GROUP_NAME.keys())
        has_vis_change = any(f in vals for f in visibility_fields) or 'groups_id' in vals or 'restricted_app_ids' in vals

        if has_vis_change:
            category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
            if category:
                groups_by_name = {g.name: g for g in self.env['res.groups'].sudo().search([('category_id', '=', category.id)])}
                for user in self:
                    for field_name, group_name in FIELD_TO_GROUP_NAME.items():
                        if field_name in vals:
                            target_group = groups_by_name.get(group_name)
                            if target_group:
                                if vals[field_name] and target_group not in user.groups_id:
                                    user.sudo().write({'groups_id': [(4, target_group.id)]})
                                elif not vals[field_name] and target_group in user.groups_id:
                                    user.sudo().write({'groups_id': [(3, target_group.id)]})

            # ACTUALIZACIÓN INSTANTÁNEA: Limpia la memoria caché de menús en el servidor Odoo
            self.env['ir.ui.menu'].clear_caches()
            self.clear_caches()

        return res

    def action_enable_all_apps(self):
        """Habilita todas las aplicaciones para los usuarios seleccionados."""
        category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
        groups = self.env['res.groups'].sudo().search([('category_id', '=', category.id)]) if category else False
        for user in self:
            vals = {field: True for field in FIELD_TO_GROUP_NAME.keys()}
            vals['restricted_app_ids'] = [(5, 0, 0)]
            if groups:
                vals['groups_id'] = [(4, g.id) for g in groups]
            user.write(vals)
        self.env['ir.ui.menu'].clear_caches()

    def action_disable_all_apps(self):
        """Deshabilita todas las aplicaciones para los usuarios seleccionados."""
        category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
        groups = self.env['res.groups'].sudo().search([('category_id', '=', category.id)]) if category else False
        for user in self:
            vals = {field: False for field in FIELD_TO_GROUP_NAME.keys()}
            if groups:
                vals['groups_id'] = [(3, g.id) for g in groups]
            user.write(vals)
        self.env['ir.ui.menu'].clear_caches()
