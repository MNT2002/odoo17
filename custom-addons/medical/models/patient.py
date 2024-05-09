import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'medical.patient'
    _description = 'Bệnh nhân'
    _order = "create_date desc, id desc"

    name = fields.Char('Họ và tên', required=True)
    identification_code = fields.Char('ID của bệnh nhân', readonly=True)
    image = fields.Binary("Ảnh đại diện")

    @api.depends("dob")
    def _compute_age(self):
        currentDay = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.dob and rec.dob < currentDay:
                start = rec.dob
                years_calc = (currentDay - start).days / 365
                days_calc = (currentDay - start).days % 365
                str_years = str(int(years_calc)) + ' tuổi'
                str_days = str(days_calc) + ' ngày'
                if years_calc > 0.0:
                    rec.age = " ".join([str_years, str_days])
            elif rec.dob and rec.dob > currentDay:
                return {'warning': {'title': 'Cảnh báo',
                                    'message': 'Vui lòng nhập ngày sinh phù hợp!'}}

    age = fields.Char('Tuổi bệnh nhân', compute='_compute_age', store=True)
    marital_status = fields.Selection([('single', 'Độc thân'), ('married', 'Đã cưới'), ('widowed', 'Góa phụ'), ('divorced', 'Ly dị'), ('separated', 'Ly thân')], "Tình trạng hôn nhân")
    sex = fields.Selection([('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')], "Giới tính")
    dob = fields.Date('Ngày sinh', required=True)

    @api.onchange("dob")
    def _compute_year_of_birth(self):
        for record in self:
            if record.dob:
                date_object =  fields.Date.from_string(record.dob).year
                record.yob = date_object

    yob = fields.Char('Năm sinh', compute='_compute_year_of_birth')
    id_card = fields.Char('CMND, CCCD/ Hộ chiếu')
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], "Nhóm máu")
    rh = fields.Selection([('+', '+'), ('-', '-')], "Rh")
    doctor = fields.Char("Bác sĩ gia đình")
    state = fields.Selection([('waiting', 'Đang Chờ'), ('examined', 'Đã Khám')], string='Trạng thái', default='waiting')
    # Tai Khoan Nguoi Dung Page
    street = fields.Char('Địa chỉ')
    street2 = fields.Char('')
    ward = fields.Char('Phường/Xã')
    district = fields.Char('Quận/Huyện')
    city = fields.Char('Thành phố')
    zip = fields.Char('Mã bưu điện')
    country_id = fields.Many2one('res.country', string="country")
    state_id = fields.Many2one('res.country.state', string="State", store=True, domain="[('country_id', '=', country_id)]")
    website_link = fields.Char('Website Link')
    function = fields.Char('Chức vụ')
    phone = fields.Char('Điện thoại', required=True)
    email = fields.Char('Email', required=True)
    note = fields.Char('Ghi chú')
    #Lifestyle page
    exercise = fields.Boolean('Tập thể dục')
    exercise_minutes_day = fields.Integer('Phút / ngày')

    sleep_during_daytime = fields.Boolean('Ngủ vào ban ngày')
    sleep_hours = fields.Integer('Giỡ ngủ')

    number_of_meals = fields.Integer('Bữa ăn / ngày')
    eats_alone = fields.Boolean('Ăn một mình')
    coffee = fields.Boolean('Cà phê')
    coffee_cups = fields.Integer('Ly / ngày')

    soft_drinks = fields.Boolean('Nước giải khát (đường)')
    salt = fields.Boolean('Muối')
    diet = fields.Boolean('Trong chế độ ăn kiêng')
    diet_info = fields.Char('Thông tin về chế độ ăn uống')

    smoking = fields.Boolean('Hút thuốc')
    ex_smoker = fields.Boolean('Từng hút thuốc')
    age_start_smoking = fields.Integer('Tuổi bắt đầu hút thuốc')
    smoking_number = fields.Integer('Điếu thuốc một ngày')
    second_hand_smoker = fields.Boolean('Người hút thuốc thụ động')
    age_quit_smoking = fields.Integer('Tuổi bỏ thuốc')

    alcohol = fields.Boolean('Uống rượu / bia')
    age_start_drinking = fields.Integer('Tuổi bắt đầu uống')
    alcohol_beer_number = fields.Integer('Bia / ngày')
    alcohol_liquor_number = fields.Integer('Rượu / ngày')
    ex_alcoholic = fields.Boolean('Từng uống rượu / bia')
    last_month_drink_beer = fields.Integer('Tháng gần nhất uống rượu')
    age_quit_drinking = fields.Integer('Tuổi bỏ rượu / bia')

    drug_usage = fields.Boolean('Sử dụng thuốc kích thích')
    age_start_drugs = fields.Integer('Tuổi bắt đầu sử dụng thuốc')
    drug_iv = fields.Selection([('dope', 'Ma tuý'), ('heroin', 'Heroin'), ('nicotin', 'Nicotin')],'Loại thuốc kích thích hay dùng',)
    ex_drug_addict = fields.Boolean('Từng nghiện thuốc')
    age_quit_drugs = fields.Integer('Tuổi bỏ thuốc kích thích')

    motorcycle_rider = fields.Boolean('Chạy xe máy')
    helmet = fields.Boolean('Đội nón bảo hiểm')
    traffic_laws = fields.Boolean('Tuân thủ luật giao thông')
    car_revision = fields.Boolean('Sửa xe')
    car_rider = fields.Boolean('Chạy xe ô tô')
    car_seat_belt = fields.Boolean('Thắt dây an toàn')
    vaccine_ids = fields.One2many(comodel_name='medical.vaccine', inverse_name='patient_id')

    @api.depends('vaccine_ids')
    def get_count_vaccine(self):
        for rec in self:
            rec.vaccine_count =  len(rec.vaccine_ids)

    vaccine_count = fields.Integer('Vaccine count', compute="get_count_vaccine", store=True)
    walkins_ids = fields.One2many(comodel_name='medical.walkins', inverse_name='patient_id')
    prescription_ids = fields.One2many('medical.prescription', 'patient_id')
    diagnostic_imaging_ids = fields.One2many('medical.diagnostic_imaging', 'patient_id')


    # Chạy hàm bên dưới khi tạo một bản ghi
    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()

        vals['identification_code'] = self.env['ir.sequence'].next_by_code('patient.seq')

        record =  super(Patient, self).create(vals)
        return  record

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        record =  super(Patient, self).write(vals)
        return record
    # def unlink(self):
    #     for patient in self:
    #         if patient.blood_type or patient.blood_type == '':
    #             raise ValidationError('Cannot delete benh nhan defined "nhom mau" already!')
    #     return super(Patient, self).unlink()
    
    # def copy(self, default=None):
    #     default = default or {}
    #     departments = self.env['ten_model'].search([('description', '!=', False), ('description', '!=', '')], order='name', limit=1)
    #     default['department_id'] = departments.id
    #     return super(Employee, self).copy(default)

    def btn_examined(self):
        self.state = "examined"
    def btn_waiting(self):
        self.state = "waiting"
