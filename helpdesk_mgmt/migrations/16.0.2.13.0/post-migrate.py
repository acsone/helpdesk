# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.upgrade.util import remove_column

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "Removing useless computed column 'partner_email' "
        "and 'partner_name' from 'helpdesk_ticket' table"
    )
    remove_column(cr, "helpdesk_ticket", "partner_name")
    remove_column(cr, "helpdesk_ticket", "partner_email")
