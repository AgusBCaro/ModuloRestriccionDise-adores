# -*- coding: utf-8 -*-
from . import models
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """
    Garantiza que todos los usuarios existentes en la base de datos tengan
    activadas todas las casillas por defecto tras la instalación/actualización.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    # 1. Establecer en TRUE todas las columnas de visibilidad para todos los usuarios existentes
    cr.execute("""
        UPDATE res_users SET
            show_app_discuss = TRUE,
            show_app_calendar = TRUE,
            show_app_designs = TRUE,
            show_app_helpdesk = TRUE,
            show_app_contacts = TRUE,
            show_app_crm = TRUE,
            show_app_sale = TRUE,
            show_app_dashboard = TRUE,
            show_app_pos = TRUE,
            show_app_account = TRUE,
            show_app_project = TRUE,
            show_app_timesheet = TRUE,
            show_app_website = TRUE,
            show_app_survey = TRUE,
            show_app_stock = TRUE,
            show_app_repair = TRUE,
            show_app_hr = TRUE,
            show_app_link_tracker = TRUE,
            show_app_apps = TRUE,
            show_app_settings = TRUE;
    """)

    # 2. Asignar todos los usuarios a todos los grupos de la categoría Visibilidad de Aplicaciones
    all_users = env['res.users'].search([])
    visibility_category = env['ir.module.category'].search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
    if visibility_category:
        groups = env['res.groups'].search([('category_id', '=', visibility_category.id)])
        for g in groups:
            g.write({'users': [(4, u.id) for u in all_users]})

    # 3. Limpiar caché de menús de inmediato
    env['ir.ui.menu'].clear_caches()
