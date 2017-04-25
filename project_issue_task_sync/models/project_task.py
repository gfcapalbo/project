# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sync_tasks_issues = fields.Boolean(
        related=['project_id', 'sync_tasks_issues']
    )
    issue_ids = fields.One2many('project.issue', 'task_id', 'Issues')


    @api.multi
    def set_issue_vals(self):
        for this in self:
            # If I see that on write or create my task has no issue , create
            # it obviously as a sync_operation / no mail
            issue = this.issue_ids[:-1]
            if not issue:
                issue = self.env['project.issue'].with_context(
                    mail_notrack=True, is_sync_operation=True).create({
                        'project_id':  this.project_id.id,
                        'name': this.name,
                        'task_id':  this.id,
                        'user_id': this.user_id.id,
                        'stage_id': this.stage_id.id,
                        'description': this.description or 'No Description'
                        })
            if (this.project_id.sync_tasks_issues and not
                    this.env.context.get('is_sync_operation')):
                vals = self.env['project.issue'].get_changed_vals(this, issue)
                # NOTE we will write on all issues if they are multiple
                if vals:
                    this.issue_ids.with_context(
                        mail_notrack=True, is_sync_operation=True
                    ).write(vals)

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        this = super(ProjectTask, self).create(vals)
        this.set_issue_vals()
        return this

    @api.multi
    def write(self, vals):
        result = super(ProjectTask, self).write(vals)
        self.set_issue_vals()
        return result
