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
        'wizard/change_state_benh_nhan.xml',
        'wizard/change_state_phong.xml',
        'views/root_menu.xml',
        'views/trung_tam.xml',
        'views/bac_si.xml',
        'views/ql_benh_nhan.xml',
        'views/phieu_kham_benh.xml',
    ],
    "assets": {
        "web.assets_backend": ["/DatLichKhamBenh/static/src/scss/dat_lich_kham_benh_css.scss"]
    },
    'depends': ['base'],
    "application": True,
}
