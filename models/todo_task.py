from odoo import fields , models , api , _
from odoo.exceptions import ValidationError
from datetime import date



class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'To-Do Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name =fields.Char('Task Name')
    ref = fields.Char(string="Reference", default="New", readonly=True, copy=False)
    due_date = fields.Date()
    description = fields.Text()
    assign_to_id = fields.Many2one('res.users')
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
    reminder_email = fields.Char(string="Reminder Email")


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

    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('task_seq')
        return res

    @api.constrains('timesheet_ids', 'estimated_time')
    def _check_timesheet_total(self):
        for rec in self:
            total = sum(line.time_spent for line in rec.timesheet_ids)
            if rec.estimated_time and total > rec.estimated_time:
                raise ValidationError(
                    f"Total time ({total}h) exceeds estimated time ({rec.estimated_time}h) for task {rec.name}."
                )

    def write(self, vals):
        user = self.env.user

        # لو في تغيير على الـ state
        if 'state' in vals and vals['state'] == 'completed':
            if user.has_group('todo_app.group_todo_task_user'):
                for task in self:
                    if task.state != 'in_progress':
                        raise ValidationError(
                            _("You can only move a task from 'In Progress' to 'Completed'.")
                        )
        return super(TodoTask, self).write(vals)

    # Cron

    def send_due_date_reminder_email(self):
        today = date.today()
        overdue_tasks = self.search([
            ('due_date','<',today),
            ('state','in',['new','in_progress'])
        ])
        for task in overdue_tasks:
            if not task.reminder_email:
                continue

            subject = f"⚠️ Task Overdue Reminder: {task.name}"
            body_html = f"""
                            <div style="font-family:Arial, sans-serif; color:#333; line-height:1.6;">
                                <h3 style="color:#e74c3c;">⚠️ تذكير: المهمة متأخرة</h3> 
                                <p>مرحبًا,</p>
                                <p>المهمة <b>{task.name}</b> تأخرت حيث كان تاريخ الاستحقاق: <b>{task.due_date}</b>.</p>
                                <p>الحالة الحالية: <b>{task.state}</b></p>

                                <hr style="margin:20px 0;"/>

                                <h3 style="color:#2980b9;">⚠️ Overdue Task Reminder</h3>
                                <p>Hello,</p>
                                <p>The task <b>{task.name}</b> is overdue since <b>{task.due_date}</b>.</p>
                                <p>Current state: <b>{task.state}</b></p>

                                <p style="margin-top:20px;">Thanks,<br/><b>Task Management System</b></p>
                            </div>
                        """

            self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body_html,
                'email_to': task.reminder_email,
            }).send()




class TodoTaskLine(models.Model):
    _name = 'todo.task.line'
    task_id = fields.Many2one('todo.task')
    description = fields.Char()
    time_spent = fields.Float(string='Time Spent (Hours)')
    date = fields.Date(default=fields.Date.today)




