import logging

from odoo import tools

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.debug("Create parent_id columns with values")
    cr.execute("""
        UPDATE project_project set  project_parent_id = parent_id """)
