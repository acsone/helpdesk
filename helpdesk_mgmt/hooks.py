# Copyright 2025 ACSONE SA/NV
from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID

from odoo.upgrade.util import module_installed


def pre_init_hook(cr):
    if not module_installed(cr, "helpdesk"):
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    _remove_views(env)
    _set_uninstallable(env)
    _rename_sequence(env)
    _rename_fields(env)
    _rename_stages(env)
    _rename_module(env)
    _rename_accesses(env)
    
   
def _remove_views(env):
    # Remove views
    query = """
        DELETE FROM ir_ui_view
        WHERE inherit_id IN (SELECT res_id FROM ir_model_data WHERE model = 'ir.ui.view' AND module IN ('helpdesk', 'helpdesk_sale', 'helpdesk_sms', 'crm_helpdesk'));
    """
    openupgrade.logged_query(env.cr, query=query)
    query = """
        DELETE FROM ir_ui_view
        WHERE id IN (SELECT res_id FROM ir_model_data WHERE model = 'ir.ui.view' AND module IN ('helpdesk', 'helpdesk_sale', 'helpdesk_sms', 'crm_helpdesk'))
    """
    openupgrade.logged_query(env.cr, query=query)

def _set_uninstallable(env):
    openupgrade.logged_query(env.cr, """ UPDATE ir_module_module SET state = 'uninstallable' WHERE name IN ('helpdesk', 'helpdesk_sale', 'helpdesk_sms', 'crm_helpdesk')""")

def _rename_sequence(env):
    sequence = [("helpdesk.seq_helpdesk_ticket", "helpdesk_mgmt.helpdesk_ticket_sequence")]
    openupgrade.rename_xmlids(env.cr, sequence)

def _rename_fields(env):
    # Rename fields, models and tables
    fields_spec = [
        ("helpdesk.ticket", "helpdesk_ticket", "ticket_ref", "number")
    ]
    openupgrade.rename_fields(env, field_spec=fields_spec)

    ticket_type_table = [
        ("helpdesk_ticket_type", "helpdesk_ticket_category")
    ]
    openupgrade.rename_tables(env.cr, table_spec=ticket_type_table)

    ticket_type = [
        ("helpdesk.ticket.type", "helpdesk.ticket.category")
    ]
    openupgrade.rename_models(env.cr, model_spec=ticket_type
    )

    fields_spec = [("helpdesk.ticket", "helpdesk_ticket", "ticket_type_id", "category_id")]
    openupgrade.rename_fields(env, field_spec=fields_spec)

    team_stage_rel = [("team_stage_rel", "helpdesk_ticket_stage_helpdesk_ticket_team_rel")]

    openupgrade.rename_tables(env.cr, table_spec=team_stage_rel)

    columns = {
        "helpdesk_ticket_stage_helpdesk_ticket_team_rel": [("helpdesk_team_id", "helpdesk_ticket_team_id"), ("helpdesk_stage_id", "helpdesk_ticket_stage_id")],
    }
    openupgrade.rename_columns(env.cr, column_spec=columns)

    models = [("helpdesk.stage", "helpdesk.ticket.stage")]
    openupgrade.rename_models(env.cr, models)
    tables = [("helpdesk_stage", "helpdesk_ticket_stage")]
    openupgrade.rename_tables(env.cr, tables)

    models = [("helpdesk.team", "helpdesk.ticket.team")]
    openupgrade.rename_models(env.cr, models)
    tables = [("helpdesk_team", "helpdesk_ticket_team")]
    openupgrade.rename_tables(env.cr, tables)

def _rename_stages(env):
    stages = [
        ("helpdesk.stage_new", "helpdesk_mgmt.helpdesk_ticket_stage_new"),
        ("helpdesk.stage_in_progress", "helpdesk_mgmt.helpdesk_ticket_stage_in_progress"),
        ("helpdesk.stage_solved", "helpdesk_mgmt.helpdesk_ticket_stage_done"),
        ("helpdesk.stage_on_hold", "helpdesk_mgmt.helpdesk_ticket_stage_awaiting"),
        ("helpdesk.stage_cancelled", "helpdesk_mgmt.helpdesk_ticket_stage_cancelled"),
    ]
    openupgrade.rename_xmlids(env.cr, stages, allow_merge=True)

def _rename_module(env):
    modules = [("helpdesk", "helpdesk_mgmt")]
    openupgrade.update_module_names(env.cr, modules, merge_modules=True)

def _rename_accesses(env):
     # Manage accesses
    accesses = [
        ("helpdesk.access_helpdesk_tag", "hepldesk_mgmt.access_helpdesk_ticket_tag_user"),
        ("helpdesk.access_helpdesk_stage", "helpdesk_mgmt.access_helpdesk_ticket_stage_user"),
        ("helpdesk.access_helpdesk_stage_manager", "helpdesk_mgmt.access_helpdesk_ticket_stage_manager"),
        ("helpdesk.access_helpdesk_stage_portal", "helpdesk_mgmt.access_helpdesk_ticket_stage_portal"),
        ("helpdesk.access_helpdesk_ticket_portal", "helpdesk_mgmt.access_helpdesk_ticket_portal"),
        ("helpdesk.access_helpdesk_ticket", "helpdesk_mgmt.access_helpdesk_ticket_user"),
        ("helpdesk.access_helpdesk_team_public", "helpdesk_mgmt.access_helpdesk_ticket_team_portal"),
        ("helpdesk.access_helpdesk_team_manager", "helpdesk_mgmt.access_helpdesk_ticket_team_manager"),
        ("helpdesk.access_helpdesk_ticket_type_user", "hdelpdesk_mgmt.access_helpdesk_ticket_category_user"),
        ("helpdesk.access_helpdesk_ticket_type_manager", "helpdesk_mgmt.access_helpdesk_ticket_category_manager"),
    ]
    openupgrade.rename_xmlids(env.cr, accesses, allow_merge=True)
