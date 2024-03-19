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
    ],
    "assets": {
        "web.assets_backend": ["/DatLichKhamBenh/static/src/scss/dat_lich_kham_benh_css.scss"]
    },
    'depends': ['base'],
    "application": True,
}
