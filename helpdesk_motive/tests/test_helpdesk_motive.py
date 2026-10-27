# Copyright (C) 2023 Binhex - Adasat Torres
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import Form, new_test_user
from odoo.tests.common import TransactionCase


class TestHelpdeskMotive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Initialize the class object
        helpdesk_ticket_team = cls.env["helpdesk.ticket.team"]
        ctx = {
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.user_team = new_test_user(
            cls.env,
            login="helpdesk_mgmt-user_team",
            groups="helpdesk_mgmt.group_helpdesk_user_team",
            context=ctx,
        )
        cls.user = new_test_user(
            cls.env,
            login="helpdesk_mgmt-user",
            groups="helpdesk_mgmt.group_helpdesk_user",
            context=ctx,
        )
        cls.team_a = helpdesk_ticket_team.create(
            {"name": "Team A", "user_ids": [Command.set([cls.user.id])]}
        )
        cls.team_b = helpdesk_ticket_team.create(
            {"name": "Team B", "user_ids": [Command.set([cls.user_team.id])]}
        )

        cls.motive = cls.env["helpdesk.ticket.motive"].create(
            {"name": "motive_test", "team_id": cls.team_a.id}
        )

        cls.ticket_a_user_team = cls._create_ticket(
            cls, cls.team_a, cls.motive, cls.user_team
        )

    def _create_ticket(self, team, motive, user=False):
        return self.env["helpdesk.ticket"].create(
            {
                "name": "Ticket %s (%s)"
                % (team.name, user.login if user else "unassigned"),
                "description": "Description",
                "team_id": team.id,
                "user_id": user.id if user else False,
                "priority": "1",
                "motive_id": motive.id,
            }
        )

    def test_compute_team_user_helpdesk_motive(self):
        self.assertTrue(self.ticket_a_user_team.motive_id)
        self.ticket_a_user_team.write({"team_id": self.team_b.id})
        self.assertFalse(self.ticket_a_user_team.motive_id)
        self.ticket_a_user_team.write({"motive_id": self.motive.id})
        self.assertTrue(self.ticket_a_user_team.motive_id)
        self.ticket_a_user_team.write({"user_id": self.user.id})
        self.assertFalse(self.ticket_a_user_team.motive_id)

    def test_default_description(self):
        motive_with_default = self.env["helpdesk.ticket.motive"].create(
            {
                "name": "Motive with Default Description",
                "team_id": self.team_a.id,
                "default_description": "Default motive Description.",
            }
        )
        motive_without_default = self.env["helpdesk.ticket.motive"].create(
            {
                "name": "Motive without Default Description",
                "team_id": self.team_a.id,
            }
        )

        # Selecting motive with default description sets description
        with Form(self.env["helpdesk.ticket"]) as ticket_form:
            ticket_form.name = "Ticket 1"
            ticket_form.team_id = self.team_a
            ticket_form.motive_id = motive_with_default
            self.assertIn(
                motive_with_default.default_description, ticket_form.description
            )

        # Selecting motive without default description leaves description empty
        with Form(self.env["helpdesk.ticket"]) as ticket_form:
            ticket_form.name = "Ticket 2"
            ticket_form.team_id = self.team_a
            ticket_form.motive_id = motive_without_default
            self.assertFalse(ticket_form.description)
            ticket_form.description = "Test description"
        ticket_2 = ticket_form.save()

        # Updating motive to one with default description on existing record
        with Form(ticket_2) as ticket_form:
            ticket_form.description = False
            ticket_form.motive_id = motive_with_default
            self.assertIn(
                motive_with_default.default_description, ticket_form.description
            )
