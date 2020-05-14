# Copyright 2019 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade



@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, [('parent_id', 'project_parent_id')])
