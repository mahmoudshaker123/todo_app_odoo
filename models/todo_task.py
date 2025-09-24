from odoo import fields , models , api
from odoo.exceptions import ValidationError


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
        ('closed','Closed'),
    ],
        default='new' , tracking=True
    )
    estimated_time = fields.Float(string='Estimated Time (Hours)')
    timesheet_ids = fields.One2many('todo.task.line','task_id' , string='Timesheets')
    active = fields.Boolean(default=True)

    def actions_in_progress(self):
        for rec in self:
            rec.state='in_progress'

    def actions_closed(self):
        for rec in self:
            rec.state='closed'

    def actions_new(self):
        for rec in self:
            rec.state='new'

    def actions_completed(self):
        for rec in self:
            rec.state='completed'

    @api.constrains('timesheet_ids', 'estimated_time')
    def _check_timesheet_total(self):
        for rec in self:
            total = sum(line.time_spent for line in rec.timesheet_ids)
            if rec.estimated_time and total > rec.estimated_time:
                raise ValidationError(
                    f"Total time ({total}h) exceeds estimated time ({rec.estimated_time}h) for task {rec.name}."
                )



class TodoTaskLine(models.Model):
    _name = 'todo.task.line'
    task_id = fields.Many2one('todo.task')
    description = fields.Char()
    time_spent = fields.Float(string='Time Spent (Hours)')
    date = fields.Date(default=fields.Date.today)




