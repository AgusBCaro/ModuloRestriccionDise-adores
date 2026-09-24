# -*- coding: utf-8 -*-
from . import models
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """
    Garantiza que todos los usuarios existentes en la base de datos tengan
    activadas las casillas (show_app_* = True) tras la instalación del módulo,
    evitando que se oculten aplicaciones por valores nulos preexistentes.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    users = env['res.users'].search([])
    fields_to_enable = {
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
    }
    users.write(fields_to_enable)
