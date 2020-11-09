# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

from odoo import api, fields, models, _


class UserConcerns(models.Model):
    _name = 'user.concerns'
    _description = 'Activity'
    _inherit = ['mail.thread', 'portal.mixin']
    _order = 'date_deadline ASC'
    _rec_name = 'sequence'

    # @api.model
    # def default_get(self, fields):
    #     res = super(UserConcerns, self).default_get(fields)
    #     if not fields or 'res_model_id' in fields and res.get('res_model'):
    #         res['res_model_id'] = self.env['ir.model'].
    # _get(res['res_model']).id
    #     return res

    # owner
    sequence = fields.Char('Sequence')
    project_id = fields.Many2one('project.project', 'Project Name', store=True)
    res_id = fields.Integer('Related Document ID', index=True,
                            required=True, store=True)
    # res_model_id = fields.Many2one(
    #     'ir.model', 'Related Document Model',
    #     index=True, ondelete='cascade', required=True)
    # res_model = fields.Char(
    #     'Related Document Model',
    #     index=True, related='res_model_id.model', store=True, readonly=True)
    # res_name = fields.Char(
    #     'Document Name', compute='_compute_res_name', store=True,
    #     help="Display name of the related document.", readonly=True)
    # activity
    activity_type_id = fields.Many2one(
        'user.concerns.type', 'Conveyed By')
    # activity_type_id = fields.Many2one(
    #     'user.concerns.type', 'Conveyed By',
    #     domain="['|', ('res_model_id', '=', False),
    #             ('res_model_id', '=', res_model_id)]")
    activity_category = fields.Selection(related='activity_type_id.category')
    icon = fields.Char('Icon', related='activity_type_id.icon')
    summary = fields.Char('Summary', store=True)
    note = fields.Html('Note')
    feedback = fields.Html('Feedback')
    date_deadline = fields.Date('Date', index=True, required=True,
                                default=fields.Date.today, store=True)
    # description
    user_id = fields.Many2one(
        'res.users', 'Raised By',
        default=lambda self: self.env.user,
        index=True, required=True)
    notice_customer = fields.Boolean(string="Notified Customer")
    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], 'State',
        compute='_compute_state')
    recommended_activity_type_id = fields.Many2one(
        'user.concerns.type', string="Recommended Activity Type")
    previous_activity_type_id = fields.Many2one(
        'user.concerns.type', string='Previous Activity Type')
    has_recommended_activities = fields.Boolean(
        'Next activities available',
        compute='_compute_has_recommended_activities',
        help='Technical field for UX purpose')
    task_count = fields.Integer(compute='_compute_task', string='# of Task')
    task_ids = fields.One2many('project.task', 'concern_id', string='Task')
    attachment_count = fields.Integer(compute='_count_attachments')

    @api.model
    def create(self, vals):
        serial_no = self.env['ir.sequence'].search(
            [('code', '=', 'user.concerns')], limit=1)
        project_name = self.env['project.project'].browse(
            vals['project_id']).name
        serial_no.update({'prefix': project_name + '/'})
        seq = self.env['ir.sequence'].next_by_code('user.concerns') or '/'
        vals['sequence'] = seq

        return super(UserConcerns, self).create(vals)

    @api.multi
    def action_view_task(self):
        self.ensure_one()
        view_ref = self.env['ir.model.data'].get_object_reference(
            'project', 'view_task_form2')
        view_id = view_ref[1] if view_ref else False
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Tasks'),
            'res_model': 'project.task',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {'default_name': self.summary,
                        'default_project_id': self.project_id.id,
                        'default_date_deadline': self.date_deadline,
                        'default_res_id': self.res_id,
                        'default_concern_id': self.id,
                        },
            }
        return res

    @api.multi
    def action_view_task_tree(self):
        self.ensure_one()
        view_ref = self.env['ir.model.data'].get_object_reference(
            'project', 'view_task_tree2')
        view_id = view_ref[1] if view_ref else False
        domain = [('project_id', '=', self.project_id.id)]
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Tasks'),
            'res_model': 'project.task',
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id': view_id,
            'target': 'current',
            'context': {},
            'domain': domain,
            }
        return res

    @api.multi
    def action_ir_attachment_form(self):
        self.ensure_one()
        view_ref = self.env['ir.model.data'].get_object_reference(
            'mail', 'view_document_file_kanban')
        view_id = view_ref[1] if view_ref else False
        domain = [('concern_id', '=', self.id)]
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Attachments'),
            'res_model': 'ir.attachment',
            'view_type': 'form',
            'view_mode': 'kanban',
            'view_id': view_id,
            'target': 'current',
            'context': {},
            'domain': domain,
            }
        return res

    @api.multi
    def action_add_attachment(self):
        self.ensure_one()
        view_ref = self.env['ir.model.data'].get_object_reference(
            'user_concerns', 'ir_attachment_demo_wizard')
        view_id = view_ref[1] if view_ref else False
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Attachment'),
            'res_model': 'ir.attachment',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context':  {'default_concern_id': self.id},
            }
        return res

    @api.depends('sequence')
    def _compute_task(self):
        for rec in self:
            task = rec.env['project.task'].search(
                [('concern_id', '=', rec.id)])
            rec.task_count = len(task)

    @api.depends('sequence')
    def _count_attachments(self):
        for rec in self:
            attachment = rec.env['ir.attachment'].search(
                [('concern_id', '=', rec.id)])
            rec.attachment_count = len(attachment)

    @api.multi
    @api.onchange('previous_activity_type_id')
    def _compute_has_recommended_activities(self):
        for record in self:
            record.has_recommended_activities = bool(
                record.previous_activity_type_id.next_type_ids)

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for activity in self:
            activity.res_name = self.env[activity.res_model].browse(
                activity.res_id).name_get()[0][1]

    @api.depends('date_deadline')
    def _compute_state(self):
        today = date.today()
        for record in self.filtered(lambda activity: activity.date_deadline):
            date_deadline = fields.Date.from_string(record.date_deadline)
            diff = (date_deadline - today)
            if diff.days == 0:
                record.state = 'today'
            elif diff.days < 0:
                record.state = 'overdue'
            else:
                record.state = 'planned'

    @api.onchange('activity_type_id')
    def _onchange_activity_type_id(self):
        if self.activity_type_id:
            self.summary = self.activity_type_id.summary
            self.date_deadline = (datetime.now() +
                                  timedelta(days=self.activity_type_id.days))

    @api.onchange('previous_activity_type_id')
    def _onchange_previous_activity_type_id(self):
        if self.previous_activity_type_id.next_type_ids:
            self.recommended_activity_type_id = self.previous_activity_type_id.next_type_ids[0]

    @api.onchange('recommended_activity_type_id')
    def _onchange_recommended_activity_type_id(self):
        self.activity_type_id = self.recommended_activity_type_id


class UserConcernsType(models.Model):
    _name = 'user.concerns.type'
    _description = 'Activity Type'
    _rec_name = 'name'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    summary = fields.Char('Summary', translate=True)
    sequence = fields.Integer('Sequence', default=10)
    days = fields.Integer(
        '# Days', default=0,
        help="""Number of days before executing the action. \n
        'It allows to plan the action deadline.""")
    icon = fields.Char('Icon', help="Font awesome icon e.g. fa-tasks")
    # res_model_id = fields.Many2one(
    #     'ir.model', 'Model', index=True,
    #     help='Specify a model if the activity should be specific to a model'
    #          ' and not available when managing activities for other models.')
    next_type_ids = fields.Many2many(
        'user.concerns.type', 'mail_activity_rel', 'activity_id',
        'recommended_id',
        string='Recommended Next Activities')
    previous_type_ids = fields.Many2many(
        'user.concerns.type', 'mail_activity_rel', 'recommended_id',
        'activity_id',
        string='Preceding Activities')
    category = fields.Selection([
        ('default', 'Other'), ('meeting', 'Meeting')], default='default',
        string='Category',
        help="""Categories may trigger specific behavior like opening calendar
         view""")


class UserConcernsMixin(models.AbstractModel):
    _name = 'user.concerns.mixin'
    _description = 'Activity Mixin'

    activity_ids = fields.One2many(
        'user.concerns', 'res_id', 'Activities',
        auto_join=True,
        groups="base.group_user",
        domain=lambda self: [('res_model', '=', self._name)])
    activity_state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], string='State',
        compute='_compute_activity_state',
        groups="base.group_user")
    activity_user_id = fields.Many2one(
        'res.users', 'Responsible',
        related='activity_ids.user_id',
        search='_search_activity_user_id',
        groups="base.group_user")
    activity_type_id = fields.Many2one(
        'user.concerns.type', 'Next Activity Type',
        related='activity_ids.activity_type_id',
        search='_search_activity_type_id',
        groups="base.group_user")
    activity_date_deadline = fields.Date(
        'Next Activity Deadline', related='activity_ids.date_deadline',
        readonly=True, store=True,  # store to enable ordering + search
        groups="base.group_user")
    activity_summary = fields.Char(
        'Next Activity Summary',
        related='activity_ids.summary',
        search='_search_activity_summary',
        groups="base.group_user",)

    @api.depends('activity_ids.state')
    def _compute_activity_state(self):
        for record in self:
            states = record.activity_ids.mapped('state')
            if 'overdue' in states:
                record.activity_state = 'overdue'
            elif 'today' in states:
                record.activity_state = 'today'
            elif 'planned' in states:
                record.activity_state = 'planned'

    @api.model
    def _search_activity_user_id(self, operator, operand):
        return [('activity_ids.user_id', operator, operand)]

    @api.model
    def _search_activity_type_id(self, operator, operand):
        return [('activity_ids.activity_type_id', operator, operand)]

    @api.model
    def _search_activity_summary(self, operator, operand):
        return [('activity_ids.summary', operator, operand)]

    @api.multi
    def write(self, vals):
        # Delete activities of archived record.
        if 'active' in vals and vals['active'] is False:
            self.env['mail.activity'].sudo().search(
                [('res_model', '=', self._name), ('res_id', 'in', self.ids)]
            ).unlink()
        return super(UserConcernsMixin, self).write(vals)

    @api.multi
    def unlink(self):
        record_ids = self.ids
        result = super(UserConcernsMixin, self).unlink()
        self.env['mail.activity'].sudo().search(
            [('res_model', '=', self._name), ('res_id', 'in', record_ids)]
        ).unlink()
        return result


class Task(models.Model):
    _inherit = 'project.task'

    from_concerned = fields.Char(related='concern_id.sequence',
                                 string="From Concerns")
    concern_id = fields.Many2one('user.concerns', string="Concerns")


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    concern_id = fields.Many2one('user.concerns', string="Concerns")
