from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.project'

    estimate_ids = fields.One2many(
        'project.cost.estimate',
        'project_id',
        string='All Cost Estimates'
    )
    amount = fields.Float(string='Amount', compute='_compute_latest_cost_estimate', store=True)

    @api.depends('estimate_ids.estimated_total_cost')
    def _compute_latest_cost_estimate(self):
        for rec in self:
            estimate_ids = self.env['project.cost.estimate'].search(
                [('project_id', '=', rec.id)]
            )
            rec.amount = sum(estimate_ids.mapped('estimated_total_cost'))

    def action_view_latest_cost_estimate(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cost Estimates',
            'res_model': 'project.cost.estimate',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
            },
        }
