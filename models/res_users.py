# -*- coding: utf-8 -*-
from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Al crear un nuevo usuario, se asignan por defecto todos los grupos
        de Visibilidad de Aplicaciones para que empiece con todas las casillas activadas.
        """
        users = super(ResUsers, self).create(vals_list)
        visibility_category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
        if visibility_category:
            groups = self.env['res.groups'].sudo().search([('category_id', '=', visibility_category.id)])
            if groups:
                for user in users:
                    user.sudo().write({'groups_id': [(4, g.id) for g in groups]})
        return users
