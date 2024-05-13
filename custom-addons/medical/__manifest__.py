{
    'name': "Medical",

    'summary': "",

    'description': """
        Long description of module's purpose
    """,

    'author': "Minh Nhat Tran",
    'website': "https://icsc.vn/?lang=vi",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'website'],
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
        'data/mail_template_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/change_state_patient.xml',
        'views/patient.xml',
        'views/pharmacies.xml',
        'views/walkins.xml',
        'views/doctor.xml',
        'views/hospital_infor_system.xml',
        'views/root_menu.xml',
        'views/header_website.xml',
        'views/home_page_website.xml',
        'views/department_detail_website.xml',
        'views/doctor_detail_website.xml',
    ],
    "assets": {
        "web.assets_backend": ["/medical/static/src/scss/medical.scss"],

        "web.assets_frontend": [
            "/medical/static/lib/fontawesome-free-6.5.2-web/css/all.min.css",
            "/medical/static/lib/fontawesome-free-6.5.2-web/js/all.min.js",
            "/medical/static/lib/bootstrap-4.6.2/dist/css/bootstrap.min.css",
            "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.slim.min.js",
            "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js",
            "/medical/static/lib/bootstrap-4.6.2/dist/js/bootstrap.bundle.min.js",
            "/medical/static/src/scss/slider.scss",
            "/medical/static/src/scss/main.scss",
            "/medical/static/src/js/validator.js",
            "/medical/static/src/js/booking.js",
            "/medical/static/src/js/sort_doctor.js",
            "/medical/static/src/js/main.js",
        ]
    },
    "application": True,
}
