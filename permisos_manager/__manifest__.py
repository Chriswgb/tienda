{
    'name': "Permisos Manager",
    'summary': """
        Restrict Menu Items from Specific Users""",
    'description': """
        Restrict Menu Items from Specific Users""",
    'author': 'Christopher Gonzalez',
    'category': 'Extra Rights',
    'version': "1.0",
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/res_partner_form.xml',
        'views/res_users.xml',
    ],
}
