# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _get_tsk_code(self):
        increment = 0
        # all records will be searchable
        self.env.cr.commit()
        next_by_code =  self.env['ir.sequence'].next_by_code('project.task')
        _logger.info('getting tsk code default , next by code %s' %
                     next_by_code)
        exists = bool(self.env['project.task'].search([
            ('code', '=', str(next_by_code))]))
        _logger.info('next by code %s exists %s' %
                     (next_by_code, exists) )
        if not exists:
            return next_by_code
        while exists:
            increment += 1
            _logger.info('next by code %s exists %s , increment %s' %
                         (next_by_code, exists, increment) )
            next_code = 'mig_' + str(increment) + '_' + next_by_code
            exists = bool(self.env['project.task'].search([
                ('code', '=', next_code)]))
        return next_code


    code = fields.Char(
        string='Task Number', required=False,
        readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self._get_tsk_code()
        return super(ProjectTask, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].next_by_code('project.task')
        return super(ProjectTask, self).copy(default)

    @api.multi
    def name_get(self):
        result = super(ProjectTask, self).name_get()
        new_result = []

        for task in result:
            rec = self.browse(task[0])
            name = '[%s] %s' % (rec.code, task[1])
            new_result.append((rec.id, name))
        return new_result
