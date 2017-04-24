# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models, fields 


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    sync_tasks_issues = fields.Boolean(
        related=['project_id', 'sync_tasks_issues']
    )
    def get_changed_vals(self, origin, paired):
        vals = {}
        if paired.stage_id != origin.stage_id:
            vals['stage_id'] = origin.stage_id.id
        if paired.user_id != origin.user_id:
            vals['user_id'] = origin.user_id.id
        if paired.description != origin.description:
            vals['description'] = origin.description
        if paired.project_id != origin.project_id:
            vals['project_id'] = origin.project_id.id
        return vals

    def set_issue_vals(self):
        for this in self:
            task = this.sudo().task_id[:1]
            # currently task creation is done on the first time write
            # this needs to be rectified and made on creation.
            # making the task on creation will cause no problem to the old
            # code, because it will find that the associated task is already
            # there and skip creation
            if not len(task) > 0:
                task = self.env['project.task'].with_context(
                    mail_notrack=True, is_sync_operation=True).create({
                        'project_id':  this.project_id.id,
                        'name': this.name,
                        'issue_ids': [(4, this.id)],
                        'user_id': this.user_id.id,
                        'stage_id': this.stage_id.id,
                        'description': this.description or 'No Description'
                    })
            if (this.project_id.sync_tasks_issues and task and not
                    this.env.context.get('is_sync_operation')):
                vals = this.get_changed_vals(this, task)
                if vals:
                    task.with_context(
                        mail_notrack=True, is_sync_operation=True
                    ).write(vals)

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        this = super(ProjectIssue, self).create(vals)
        this.set_issue_vals()
        return this

    @api.multi
    def write(self, vals):
        result = super(ProjectIssue, self).write(vals)
        self.set_issue_vals()
        return result
