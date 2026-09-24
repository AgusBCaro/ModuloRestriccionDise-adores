# -*- coding: utf-8 -*-
from . import models
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """
    Garantiza que todos los usuarios existentes en la base de datos tengan
    activadas las casillas de visibilidad de apps en Derechos de Acceso por defecto.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    all_users = env['res.users'].search([])
    visibility_category = env['ir.module.category'].search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
    if visibility_category:
        groups = env['res.groups'].search([('category_id', '=', visibility_category.id)])
        for g in groups:
            g.write({'users': [(4, u.id) for u in all_users]})
