from odoo import fields , models


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'To-Do Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name =fields.Char('Task Name')
    due_date = fields.Date()
    description = fields.Text()
    assign_to_id = fields.Many2one('res.partner')
    state = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
    ],
        default='new'
    )

    def actions_in_progress(self):
        for rec in self:
            rec.state='in_progress'

    def actions_new(self):
        for rec in self:
            rec.state='new'

    def actions_completed(self):
        for rec in self:
            rec.state='completed'
