

{
    'name': "To-Do App",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'mail',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'wizards/todo_task_bulk_assign_views.xml',
        'reports/todo_task_report.xml',

],

    'application': True,
}
