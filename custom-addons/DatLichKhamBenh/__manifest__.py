{
    'name': "module-dat-lich-kham-benh",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Minh Nhat Tran",
    'website': "https://icsc.vn/?lang=vi",
    'category': 'Uncategorized',
    'version': '0.1',
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/confirm_state_benh_nhan.xml',
        'views/root_menu.xml',
        'views/ql_benh_nhan.xml',

    ],
    'depends': ['base'],
}
