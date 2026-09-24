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
        'xml_ids': ['account.menu_finance', 'account_accountant.menu_accounting'],
        'modules': ['account', 'account_accountant'],
        'names': ['facturación', 'contabilidad', 'facturacion', 'invoicing', 'accounting', 'facturas']
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
        'names': ['inventario', 'inventory', 'almacén', 'almacen']
    },
    'show_app_repair': {
        'xml_ids': ['repair.menu_repair_order'],
        'modules': ['repair'],
        'names': ['reparaciones', 'reparación', 'reparacion', 'repairs', 'repair']
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
        'names': ['ajustes', 'settings', 'configuración', 'configuracion']
    },
}

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def load_menus(self, debug):
        """
        Sobrescribe load_menus (el método oficial que llama el cliente web de Odoo 16).
        Filtra las aplicaciones del selector de apps (waffle menu) en tiempo real
        según las restricciones del usuario actual.
        """
        res = super(IrUiMenu, self).load_menus(debug)
        
        user = self.env.user
        if self.env.is_superuser():
            return res

        if not res or 'root' not in res or not res['root'].get('children'):
            return res

        # 1. Identificar qué IDs de menús principales están deshabilitados
        hidden_root_ids = self._get_hidden_app_root_ids(user, res)

        if not hidden_root_ids:
            return res

        # 2. Filtrar las aplicaciones del waffle menu (hijos de root)
        filtered_root_children = [
            cid for cid in res['root']['children']
            if cid not in hidden_root_ids
        ]

        # 3. Identificar recursivamente todos los submenús de las aplicaciones ocultas
        all_hidden_ids = set()
        for root_id in hidden_root_ids:
            all_hidden_ids.update(self._get_menu_subtree_ids(res, root_id))

        # 4. Reconstruir el diccionario de menús excluyendo lo deshabilitado
        filtered_res = {
            m_id: m_val for m_id, m_val in res.items()
            if m_id not in all_hidden_ids
        }
        filtered_res['root'] = dict(res['root'])
        filtered_res['root']['children'] = filtered_root_children

        return filtered_res

    @api.model
    def _get_hidden_app_root_ids(self, user, res):
        """Retorna los IDs de las aplicaciones raíz que deben ocultarse."""
        hidden_ids = set()

        # Chequear restricted_app_ids si existe
        if hasattr(user, 'restricted_app_ids') and user.restricted_app_ids:
            hidden_ids.update(user.restricted_app_ids.ids)

        root_children = res['root']['children']

        # Determinar qué campos están explícitamente en False (desmarcados)
        disabled_fields = []
        for field_name in APP_RESTRICTIONS.keys():
            if hasattr(user, field_name):
                # Por defecto True, solo si está explícitamente en False se oculta
                val = getattr(user, field_name, True)
                if val is False:
                    disabled_fields.append(field_name)

        if not disabled_fields and not hidden_ids:
            return hidden_ids

        for root_id in root_children:
            menu_data = res.get(root_id)
            if not menu_data or not isinstance(menu_data, dict):
                continue

            xmlid = (menu_data.get('xmlid') or '').strip()
            web_icon = (menu_data.get('web_icon') or '').strip()
            web_icon_module = web_icon.split(',')[0].strip() if web_icon else ''
            name_lower = (menu_data.get('name') or '').strip().lower()

            for field_name in disabled_fields:
                restriction = APP_RESTRICTIONS[field_name]
                target_xml_ids = set(restriction['xml_ids'])
                target_modules = set(restriction['modules'])
                target_names = restriction['names']

                # 1. Coincidencia por XML ID
                if xmlid and xmlid in target_xml_ids:
                    hidden_ids.add(root_id)
                    break

                # 2. Coincidencia por módulo del ícono web
                if web_icon_module and web_icon_module in target_modules:
                    hidden_ids.add(root_id)
                    break

                # 3. Coincidencia por nombre visible
                if any(t in name_lower for t in target_names):
                    hidden_ids.add(root_id)
                    break

        return hidden_ids

    @api.model
    def _get_menu_subtree_ids(self, res, parent_id):
        """Retorna el ID del menú y todos sus descendientes en el árbol res."""
        subtree = {parent_id}
        stack = [parent_id]
        while stack:
            curr_id = stack.pop()
            curr_menu = res.get(curr_id)
            if curr_menu and isinstance(curr_menu, dict):
                children = curr_menu.get('children', [])
                for child in children:
                    c_id = child if isinstance(child, int) else child.get('id') if isinstance(child, dict) else None
                    if c_id and c_id not in subtree:
                        subtree.add(c_id)
                        stack.append(c_id)
        return subtree
