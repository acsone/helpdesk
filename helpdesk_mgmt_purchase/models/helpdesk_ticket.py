# Copyright 2017 Camptocamp SA
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    purchase_order_ids = fields.Many2many("purchase.order")
    po_count = fields.Integer(
        string="Sale Order Count", compute="_compute_po_count", store=True
    )

    @api.depends("purchase_order_ids")
    def _compute_po_count(self):
        for ticket in self:
            ticket.po_count = len(ticket.purchase_order_ids)

    def action_view_purchase_orders(self):
        """Returns action to view sale orders related to this ticket."""
        action = {
            "name": "Purchase Orders",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "tree,form",
            "target": "current",
        }
        action["domain"] = [("ticket_ids", "in", [self.id])]
        action["context"] = {
            "default_ticket_ids": [(4, [self.id])],
            "default_partner_id": self.partner_id.id,
        }
        return action
