# -*- coding: utf-8 -*-
from odoo import models, api

APP_GROUP_XML_MAP = {
    'group_show_app_discuss': {
        'xml_ids': ['mail.menu_root_discuss'],
        'modules': ['mail'],
        'names': ['conversaciones', 'discuss', 'mail', 'mensajes']
    },
    'group_show_app_calendar': {
        'xml_ids': ['calendar.mail_menu_calendar'],
        'modules': ['calendar'],
        'names': ['calendario', 'calendar']
    },
    'group_show_app_designs': {
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
    'group_show_app_helpdesk': {
        'xml_ids': [
            'helpdesk.menu_helpdesk_root',
            'helpdesk_mgmt.menu_helpdesk_root'
        ],
        'modules': ['helpdesk', 'helpdesk_mgmt'],
        'names': ['mesa de ayuda', 'helpdesk', 'soporte', 'soporte técnico', 'tickets']
    },
    'group_show_app_contacts': {
        'xml_ids': ['contacts.menu_contacts'],
        'modules': ['contacts'],
        'names': ['contactos', 'contacts']
    },
    'group_show_app_crm': {
        'xml_ids': ['crm.crm_menu_root'],
        'modules': ['crm'],
        'names': ['crm', 'iniciativas', 'flujo de ventas']
    },
    'group_show_app_sale': {
        'xml_ids': ['sale.sale_menu_root'],
        'modules': ['sale', 'sale_management'],
        'names': ['ventas', 'sales']
    },
    'group_show_app_dashboard': {
        'xml_ids': [
            'board.menu_board_my_dash',
            'ks_dashboard_ninja.board_menu_root',
            'spreadsheet_dashboard.spreadsheet_dashboard_menu_root'
        ],
        'modules': ['board', 'ks_dashboard_ninja', 'spreadsheet_dashboard'],
        'names': ['tableros', 'tablero', 'dashboards', 'dashboard']
    },
    'group_show_app_pos': {
        'xml_ids': ['point_of_sale.menu_point_root'],
        'modules': ['point_of_sale'],
        'names': ['punto de venta', 'point of sale', 'pos']
    },
    'group_show_app_account': {
        'xml_ids': ['account.menu_finance'],
        'modules': ['account', 'account_accountant'],
        'names': ['facturación', 'contabilidad', 'invoicing', 'accounting', 'facturas']
    },
    'group_show_app_project': {
        'xml_ids': ['project.menu_main_pm'],
        'modules': ['project'],
        'names': ['proyecto', 'proyectos', 'project']
    },
    'group_show_app_timesheet': {
        'xml_ids': [
            'hr_timesheet.timesheet_menu_root',
            'hr_timesheet.menu_hr_time_tracking_menu_to_approve'
        ],
        'modules': ['hr_timesheet'],
        'names': ['partes de horas', 'timesheets', 'partes de hora', 'tiempo']
    },
    'group_show_app_website': {
        'xml_ids': ['website.menu_website_configuration'],
        'modules': ['website'],
        'names': ['sitio web', 'website']
    },
    'group_show_app_survey': {
        'xml_ids': ['survey.menu_surveys'],
        'modules': ['survey'],
        'names': ['encuestas', 'surveys', 'encuesta']
    },
    'group_show_app_stock': {
        'xml_ids': ['stock.menu_stock_root'],
        'modules': ['stock'],
        'names': ['inventario', 'inventory', 'almacén']
    },
    'group_show_app_repair': {
        'xml_ids': ['repair.menu_repair_order'],
        'modules': ['repair'],
        'names': ['reparaciones', 'reparación', 'repairs', 'repair']
    },
    'group_show_app_hr': {
        'xml_ids': ['hr.menu_hr_root'],
        'modules': ['hr'],
        'names': ['empleados', 'employees', 'recursos humanos']
    },
    'group_show_app_link_tracker': {
        'xml_ids': [
            'link_tracker.menu_link_tracker',
            'utm.menu_link_tracker_root'
        ],
        'modules': ['link_tracker', 'utm'],
        'names': ['rastreador de enlaces', 'link tracker']
    },
    'group_show_app_apps': {
        'xml_ids': ['base.menu_management'],
        'modules': ['base'],
        'names': ['aplicaciones', 'apps']
    },
    'group_show_app_settings': {
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
        según las casillas de grupos de acceso tildadas/destildadas por el usuario.
        """
        visible = super(IrUiMenu, self)._filter_visible_menus()
        
        user = self.env.user

        # Evitar bloquear al Superusuario / Administrador raíz (ID 1)
        if self.env.is_superuser() or user.id == 1:
            return visible

        # Buscar la categoría de Visibilidad de Aplicaciones
        category = self.env['ir.module.category'].sudo().search([('name', '=', 'Visibilidad de Aplicaciones')], limit=1)
        if not category:
            return visible

        # Obtener los grupos pertenecientes a esta categoría
        groups = self.env['res.groups'].sudo().search([('category_id', '=', category.id)])
        if not groups:
            return visible

        user_group_ids = set(user.groups_id.ids)
        hidden_menu_ids = set()

        menu_data = self.env['ir.model.data'].sudo().search([
            ('model', '=', 'ir.ui.menu'),
            ('res_id', 'in', visible.ids)
        ])
        xml_id_map = {d.res_id: f"{d.module}.{d.name}" for d in menu_data}

        # Obtener mapeo de XML IDs de los grupos
        group_data = self.env['ir.model.data'].sudo().search([
            ('model', '=', 'res.groups'),
            ('res_id', 'in', groups.ids)
        ])
        group_xml_map = {d.res_id: d.name for d in group_data}

        for group in groups:
            # Si el usuario NO pertenece a este grupo de visibilidad (casilla destildada)
            if group.id not in user_group_ids:
                group_name_key = group_xml_map.get(group.id, '')
                restriction = APP_GROUP_XML_MAP.get(group_name_key)

                if restriction:
                    target_xml_ids = set(restriction['xml_ids'])
                    target_modules = set(restriction['modules'])
                    target_names = restriction['names']

                    for menu in visible:
                        if menu.parent_id:
                            continue

                        xml_id = xml_id_map.get(menu.id, '')
                        web_icon_module = (menu.web_icon or '').split(',')[0].strip() if menu.web_icon else ''
                        menu_name_lower = (menu.name or '').strip().lower()

                        if xml_id in target_xml_ids:
                            hidden_menu_ids.add(menu.id)
                            continue

                        if web_icon_module and web_icon_module in target_modules:
                            hidden_menu_ids.add(menu.id)
                            continue

                        if any(t in menu_name_lower for t in target_names):
                            hidden_menu_ids.add(menu.id)
                            continue
                else:
                    # Coincidencia por nombre de grupo si no está en el mapa estático
                    group_label_lower = (group.name or '').strip().lower()
                    for menu in visible:
                        if menu.parent_id:
                            continue
                        if group_label_lower in (menu.name or '').strip().lower():
                            hidden_menu_ids.add(menu.id)

        if hidden_menu_ids:
            visible = visible.filtered(lambda m: m.id not in hidden_menu_ids)

        return visible
