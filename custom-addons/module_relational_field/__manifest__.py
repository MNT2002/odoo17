{
    'name': "module-relational-field",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Minh Nhat Tran",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'data': [
        'views/root_menu.xml',
        'views/people_relational_views.xml',
        'views/house_views.xml',
    ],
    'depends': ['base'],
}
