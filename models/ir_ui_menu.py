# -*- coding: utf-8 -*-
from odoo import models, api


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def load_menus(self, debug):
        """
        Sobrescribe load_menus (el método oficial que llama el cliente web de Odoo 16).
        Filtra las aplicaciones del selector de apps (waffle menu) en tiempo real
        según restricted_app_ids del usuario actual. Cualquier menú raíz (app)
        instalado es candidato automáticamente: no hace falta tocar código
        cuando se instala un módulo nuevo.
        """
        res = super(IrUiMenu, self).load_menus(debug)

        user = self.env.user
        if self.env.is_superuser():
            return res

        if not res or 'root' not in res or not res['root'].get('children'):
            return res

        root_children = res['root']['children']
        hidden_root_ids = set(user.sudo().restricted_app_ids.ids) & set(root_children)

        # Un administrador nunca se queda sin el menú de Ajustes, aunque lo haya desmarcado.
        if hidden_root_ids and user.has_group('base.group_system'):
            settings_menu = self.env.ref('base.menu_administration', raise_if_not_found=False)
            if settings_menu:
                hidden_root_ids.discard(settings_menu.id)

        if not hidden_root_ids:
            return res

        # 1. Filtrar las aplicaciones del waffle menu (hijos de root)
        filtered_root_children = [
            cid for cid in root_children
            if cid not in hidden_root_ids
        ]

        # 2. Identificar recursivamente todos los submenús de las aplicaciones ocultas
        all_hidden_ids = set()
        for root_id in hidden_root_ids:
            all_hidden_ids.update(self._get_menu_subtree_ids(res, root_id))

        # 3. Reconstruir el diccionario de menús excluyendo lo deshabilitado
        # (se arma un dict nuevo: el que devuelve super() es el que guarda el ormcache)
        filtered_res = {
            m_id: m_val for m_id, m_val in res.items()
            if m_id not in all_hidden_ids
        }
        filtered_res['root'] = dict(res['root'])
        filtered_res['root']['children'] = filtered_root_children

        return filtered_res

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
