{
    'name': "project cost estimate",
    'version': '18.0',
    'depends': ['base', 'mail', 'project'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_cost_estimate_views.xml',
        'views/project_inherit_views.xml',
    ],
    'installable': True,
    'application': False,
}