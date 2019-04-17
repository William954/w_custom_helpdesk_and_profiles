# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################
from odoo import models, fields, api


class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'



    partner_id = fields.Many2one('res.partner', string='Customer',default=lambda self: self.env.user.partner_id,store=True)

    @api.onchange('team_id')
    def _onchange_team_id(self):
        res = super(HelpDeskTicket, self)._onchange_team_id()
        user_ids = []
        if self.env.user.has_group('helpdesk.group_helpdesk_manager'):
            for user in self.team_id.member_ids:
                if not user.has_group('w_custom_helpdesk_and_profiles.w_groups_normal_user_helpdesk'):
                    user_ids.append(user.id)
            value = {'user_id': [('id', 'in', user_ids)]}
        elif self.env.user.has_group('helpdesk.group_helpdesk_user'):
            value = {'user_id': [('id', '=', self.env.user.id)]}
        return {'domain': value}

