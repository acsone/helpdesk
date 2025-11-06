# Copyright 2017 Camptocamp SA
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    ticket_ids = fields.Many2many("helpdesk.ticket")
    ticket_count = fields.Integer(
        string="Tickets Count", compute="_compute_ticket_count", store=True
    )

    @api.depends("ticket_ids")
    def _compute_ticket_count(self):
        for order in self:
            order.ticket_count = len(order.ticket_ids)
