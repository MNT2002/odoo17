{
    'name': "Dat Lich Kham Benh",

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
    'depends': ['base', 'website', 'portal'],
    'data': [
        'data/data.xml',
        'data/dose_units.xml',
        'data/lab_test_types.xml',
        'data/medical.speciality.csv',
        'data/medical.medicines_dosage.csv',
        'data/medical.examination_time.csv',
        'data/medical.degree.csv',
        'data/medical.lab_units.csv',
        'data/medical.diagnostic_imaging_types.csv',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/change_state_patient.xml',
        'views/patient.xml',
        'views/pharmacies.xml',
        'views/walkins.xml',
        'views/doctor.xml',
        'views/hospital_infor_system.xml',
        'views/root_menu.xml',
        'views/home_page.xml',
    ],
    "assets": {
        "web.assets_backend": ["/DatLichKhamBenh/static/src/scss/medical.scss"],

        "web.assets_frontend": [
            "https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css",
            "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.slim.min.js",
            "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js",
            "https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js",
            "/DatLichKhamBenh/static/src/css/slider.css"
        ]
    },
    "application": True,
}
