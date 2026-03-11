# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestHelpdeskTicketPurchase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner", "email": "testpartner@example.com"}
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "Test Helpdesk Ticket",
                "partner_id": cls.partner.id,
                "description": "Test Helpdesk Ticket",
            }
        )
        cls.purchase_order_1 = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner.id,
                "ticket_ids": [Command.set([cls.ticket.id])],
            }
        )
        cls.purchase_order_2 = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner.id,
                "ticket_ids": [Command.set([cls.ticket.id])],
            }
        )

    def test_purchase_orders_associated_with_ticket(self):
        self.assertEqual(len(self.ticket.purchase_order_ids), 2)
        self.assertIn(self.purchase_order_1, self.ticket.purchase_order_ids)
        self.assertIn(self.purchase_order_2, self.ticket.purchase_order_ids)

    def test_partner_association_in_purchase_order(self):
        self.assertEqual(self.purchase_order_1.partner_id, self.partner)
        self.assertEqual(self.purchase_order_2.partner_id, self.partner)

    def test_smartbutton_sale_order_count(self):
        self.ticket._compute_po_count()
        self.assertEqual(self.ticket.po_count, 2)

    def test_action_view_purchase_orders(self):
        action = self.ticket.action_view_purchase_orders()
        self.assertEqual(action["domain"], [("ticket_ids", "in", [self.ticket.id])])
        self.assertDictEqual(
            action["context"],
            {
                "default_ticket_ids": [Command.set(self.ticket.ids)],
                "default_partner_id": self.ticket.partner_id.id,
            },
        )

    def test_action_view_helpdesk_tickets(self):
        action = self.purchase_order_1.action_view_helpdesk_tickets()
        self.assertEqual(
            action["domain"], [("purchase_order_ids", "in", [self.purchase_order_1.id])]
        )
        self.assertDictEqual(
            action["context"],
            {
                "default_purchase_order_ids": [Command.set(self.purchase_order_1.ids)],
                "default_po_count": 1,
            },
        )
