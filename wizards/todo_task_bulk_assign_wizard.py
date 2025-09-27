from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TodoTaskBulkAssignWizard(models.TransientModel):
    _name = 'todo.task.bulk.assign.wizard'

    assign_to_id = fields.Many2one('res.users', string='Assign To', required=True)
    note = fields.Text(string='Optional Note')


    def action_assign(self):
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}

        tasks = self.env['todo.task'].browse(active_ids)
        if not tasks:
            return {'type': 'ir.actions.act_window_close'}

        invalid_tasks = tasks.filtered(lambda t: t.state not in ['new', 'in_progress'])
        if invalid_tasks:
            raise ValidationError(_(
                "You can only assign tasks in 'New' or 'In Progress' state.\n"
                "Invalid tasks: %s"
            ) % ", ".join(invalid_tasks.mapped("name")))

        # تحديث المهام المسموح بها فقط
        tasks.write({'assign_to_id': self.assign_to_id.id})

