# -*- coding: utf-8 -*-
from odoo import models, api

APP_RESTRICTIONS = {
    'show_app_discuss': {
        'xml_ids': ['mail.menu_root_discuss'],
        'modules': ['mail'],
        'names': ['conversaciones', 'discuss', 'mail', 'mensajes']
    },
    'show_app_calendar': {
        'xml_ids': ['calendar.mail_menu_calendar'],
        'modules': ['calendar'],
        'names': ['calendario', 'calendar']
    },
    'show_app_designs': {
        'xml_ids': [
            'design.menu_design_root',
            'web_studio.studio_menu_root',
            'diseños.menu_root',
            'disenos.menu_root',
            'modulo_disenos.menu_root'
        ],
        'modules': ['design', 'diseños', 'disenos', 'modulo_disenos', 'web_studio'],
        'names': ['diseños', 'diseño', 'design', 'designs', 'diseno', 'disenos', 'diseñador', 'diseñadores']
    },
    'show_app_helpdesk': {
        'xml_ids': [
            'helpdesk.menu_helpdesk_root',
            'helpdesk_mgmt.menu_helpdesk_root'
        ],
        'modules': ['helpdesk', 'helpdesk_mgmt'],
        'names': ['mesa de ayuda', 'helpdesk', 'soporte', 'soporte técnico', 'tickets']
    },
    'show_app_contacts': {
        'xml_ids': ['contacts.menu_contacts'],
        'modules': ['contacts'],
        'names': ['contactos', 'contacts']
    },
    'show_app_crm': {
        'xml_ids': ['crm.crm_menu_root'],
        'modules': ['crm'],
        'names': ['crm', 'iniciativas', 'flujo de ventas']
    },
    'show_app_sale': {
        'xml_ids': ['sale.sale_menu_root'],
        'modules': ['sale', 'sale_management'],
        'names': ['ventas', 'sales']
    },
    'show_app_dashboard': {
        'xml_ids': [
            'board.menu_board_my_dash',
            'ks_dashboard_ninja.board_menu_root',
            'spreadsheet_dashboard.spreadsheet_dashboard_menu_root'
        ],
        'modules': ['board', 'ks_dashboard_ninja', 'spreadsheet_dashboard'],
        'names': ['tableros', 'tablero', 'dashboards', 'dashboard']
    },
    'show_app_pos': {
        'xml_ids': ['point_of_sale.menu_point_root'],
        'modules': ['point_of_sale'],
        'names': ['punto de venta', 'point of sale', 'pos']
    },
    'show_app_account': {
        'xml_ids': ['account.menu_finance'],
        'modules': ['account', 'account_accountant'],
        'names': ['facturación', 'contabilidad', 'invoicing', 'accounting', 'facturas']
    },
    'show_app_project': {
        'xml_ids': ['project.menu_main_pm'],
        'modules': ['project'],
        'names': ['proyecto', 'proyectos', 'project']
    },
    'show_app_timesheet': {
        'xml_ids': [
            'hr_timesheet.timesheet_menu_root',
            'hr_timesheet.menu_hr_time_tracking_menu_to_approve'
        ],
        'modules': ['hr_timesheet'],
        'names': ['partes de horas', 'timesheets', 'partes de hora', 'tiempo']
    },
    'show_app_website': {
        'xml_ids': ['website.menu_website_configuration'],
        'modules': ['website'],
        'names': ['sitio web', 'website']
    },
    'show_app_survey': {
        'xml_ids': ['survey.menu_surveys'],
        'modules': ['survey'],
        'names': ['encuestas', 'surveys', 'encuesta']
    },
    'show_app_stock': {
        'xml_ids': ['stock.menu_stock_root'],
        'modules': ['stock'],
        'names': ['inventario', 'inventory', 'almacén']
    },
    'show_app_repair': {
        'xml_ids': ['repair.menu_repair_order'],
        'modules': ['repair'],
        'names': ['reparaciones', 'reparación', 'repairs', 'repair']
    },
    'show_app_hr': {
        'xml_ids': ['hr.menu_hr_root'],
        'modules': ['hr'],
        'names': ['empleados', 'employees', 'recursos humanos']
    },
    'show_app_link_tracker': {
        'xml_ids': [
            'link_tracker.menu_link_tracker',
            'utm.menu_link_tracker_root'
        ],
        'modules': ['link_tracker', 'utm'],
        'names': ['rastreador de enlaces', 'link tracker']
    },
    'show_app_apps': {
        'xml_ids': ['base.menu_management'],
        'modules': ['base'],
        'names': ['aplicaciones', 'apps']
    },
    'show_app_settings': {
        'xml_ids': ['base.menu_administration'],
        'modules': ['base'],
        'names': ['ajustes', 'settings', 'configuración']
    },
}

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _filter_visible_menus(self):
        """
        Filtra el conjunto de menús para ocultar las aplicaciones deshabilitadas
        según la configuración granular del usuario actual en res.users.
        """
        visible = super(IrUiMenu, self)._filter_visible_menus()
        
        try:
            user = self.env.user

            # Evitar bloquear al Superusuario / Administrador raíz (ID 1)
            if self.env.is_superuser() or user.id == 1:
                return visible

            hidden_menu_ids = set()

            # 1. Menús explícitamente ocultos en el selector dinámico Many2many
            if 'restricted_app_ids' in user._fields:
                try:
                    if user.restricted_app_ids:
                        hidden_menu_ids.update(user.restricted_app_ids.ids)
                except Exception:
                    # Si la tabla res_users_restricted_app_rel aún no fue creada en DB via -u
                    pass

            # 2. Filtrado por casillas booleanas predefinidas
            menu_data = self.env['ir.model.data'].sudo().search([
                ('model', '=', 'ir.ui.menu'),
                ('res_id', 'in', visible.ids)
            ])
            xml_id_map = {d.res_id: f"{d.module}.{d.name}" for d in menu_data}

            for field_name, restriction in APP_RESTRICTIONS.items():
                if field_name not in user._fields:
                    continue
                try:
                    val = getattr(user, field_name, None)
                except Exception:
                    val = None

                # Solo si el valor es explícitamente False (no None, no True)
                if val is False:
                    target_xml_ids = set(restriction['xml_ids'])
                    target_modules = set(restriction['modules'])
                    target_names = restriction['names']

                    for menu in visible:
                        # Aplicar solo a menús raíz (menús principales / app switcher)
                        if menu.parent_id:
                            continue

                        xml_id = xml_id_map.get(menu.id, '')
                        web_icon_module = (menu.web_icon or '').split(',')[0].strip() if menu.web_icon else ''
                        menu_name_lower = (menu.name or '').strip().lower()

                        # Coincidencia por XML ID exacto
                        if xml_id in target_xml_ids:
                            hidden_menu_ids.add(menu.id)
                            continue

                        # Coincidencia por nombre de módulo en el icono web (web_icon)
                        if web_icon_module and web_icon_module in target_modules:
                            hidden_menu_ids.add(menu.id)
                            continue

                        # Coincidencia por nombre visible del menú
                        if any(t in menu_name_lower for t in target_names):
                            hidden_menu_ids.add(menu.id)
                            continue

            if hidden_menu_ids:
                visible = visible.filtered(lambda m: m.id not in hidden_menu_ids)

        except Exception:
            # Captura de protección total para evitar crash 500 ante desactualización de DB
            pass

        return visible
