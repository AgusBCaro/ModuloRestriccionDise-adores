# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

    visible_app_ids = fields.Many2many(
        'ir.ui.menu',
        string="Aplicaciones Visibles",
        compute='_compute_visible_app_ids',
        inverse='_inverse_visible_app_ids',
        domain=[('parent_id', '=', False)],
        help="Todas las aplicaciones instaladas aparecen aquí automáticamente, tildadas por defecto. "
             "Desmarque las que quiera ocultar del menú principal de este usuario."
    )

    def _get_app_root_menus(self):
        return self.env['ir.ui.menu'].search([('parent_id', '=', False)])

    @api.depends('restricted_app_ids')
    def _compute_visible_app_ids(self):
        roots = self._get_app_root_menus()
        for user in self:
            user.visible_app_ids = roots - user.restricted_app_ids

    def _inverse_visible_app_ids(self):
        roots = self._get_app_root_menus()
        for user in self:
            user.restricted_app_ids = roots - user.visible_app_ids

    def action_enable_all_apps(self):
        """Habilita todas las aplicaciones para los usuarios seleccionados."""
        self.write({'restricted_app_ids': [(5, 0, 0)]})

    def action_disable_all_apps(self):
        """Deshabilita todas las aplicaciones para los usuarios seleccionados."""
        roots = self._get_app_root_menus()
        self.write({'restricted_app_ids': [(6, 0, roots.ids)]})
