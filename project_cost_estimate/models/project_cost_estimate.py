from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProjectCostEstimate(models.Model):
    _name = 'project.cost.estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    estimated_total_cost = fields.Float(string='Estimated Total Cost', compute='_compute_estimated_total_cost', store=True)
    breakdown_ids = fields.One2many('project.cost.breakdown', 'cost_estimate_id', string='Cost Breakdown')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.depends('breakdown_ids.amount')
    def _compute_estimated_total_cost(self):
        for record in self:
            total_cost = sum(record.breakdown_ids.mapped('amount'))
            record.estimated_total_cost = total_cost

    def action_set_draft(self):
        self.state='draft'

    def action_submit(self):
        #Submit estimate: only Project Admins or members allowed
        if not self.env.user.has_group('project_cost_estimate.group_project_cost_estimate_admin') and not self.env.user.has_group('project_cost_estimate.group_project_cost_estimate_user'):
            raise UserError(_('You do not have permission to submit estimates.'))
        self.state = 'submitted'

    def action_approve(self):
        if not self.env.user.has_group('project_cost_estimate.group_approval'):
            raise UserError(_('Only approvers can approve estimates.'))
        if self.state != 'submitted':
            raise UserError(_('Only submitted estimates can be approved.'))
        self.state = 'approved'
        # Send notification to creator
        template = self.env.ref('project_cost_estimate.email_template_cost_estimate_notification', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_reject(self, note=False):
        self.ensure_one()
        if not self.env.user.has_group('project_cost_estimate.group_approval'):
            raise UserError(_('Only approvers can reject estimates.'))
        if self.state != 'submitted':
            raise UserError(_('Only submitted estimates can be rejected.'))
        self.state = 'rejected'
        template = self.env.ref('project_cost_estimate.email_template_cost_estimate_notification', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)


class ProjectCostBreakdown(models.Model):
    _name = 'project.cost.breakdown'
    _description = 'Project Cost Breakdown'

    name = fields.Char(string='Description', required=True)
    cost_estimate_id = fields.Many2one('project.cost.estimate', string='Cost Estimate')
    amount = fields.Float(string='Amount', required=True)



