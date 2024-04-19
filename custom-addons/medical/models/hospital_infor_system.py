from odoo import fields, models, api

from odoo.exceptions import UserError

class HealthCenter(models.Model):
    _name = 'medical.health_center'
    _description = 'Health Center model'

    name = fields.Char('Tên trung tâm y tế', required=True)
    image = fields.Binary("Ảnh đại diện")
    parent_id = fields.Many2one('medical.health_center')
    is_headquarter = fields.Boolean('Trụ sở chính', readonly=True)
    street = fields.Char('Địa chỉ')
    street2 = fields.Char('')
    city = fields.Char('Thành phố')
    zip = fields.Char('Mã bưu điện')
    country_id_new = fields.Many2one('res.country', string="Quốc gia", required=True)
    state_id_new = fields.Many2one('res.country.state', string="Tỉnh/Thành phố", store=True, require=True, domain="[('country_id', '=', country_id_new)]")
    website_link = fields.Char('Website Link')
    phone_number = fields.Char('Điện thoại')
    email = fields.Char('Email')
    extra_infor = fields.Char('Thông tin bổ sung')
    department_ids = fields.One2many(comodel_name='medical.department', inverse_name='health_center_id')

    @api.depends('department_ids')
    def get_count_department(self):
        for rec in self:
            rec.department_count =  len(rec.department_ids)

    department_count = fields.Integer('Specialty', compute="get_count_department")    
    clinic_ids_t = fields.One2many(comodel_name='medical.clinic', inverse_name='health_center_id')

    @api.depends('clinic_ids_t')
    def get_count_clinic_t(self):
        for rec in self:
            rec.clinic_count_t =  len(rec.clinic_ids_t)
    
    clinic_count_t = fields.Integer('Phòng', compute="get_count_clinic_t")

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()

        record = super(HealthCenter, self).create(vals)
        return record


class Department(models.Model):
    _name = 'medical.department'
    _description = 'department'

    name = fields.Char('Tên khoa', required=True)

    @api.depends("clinic_ids.state")
    def _compute_department_state(self):
        for rec in self:
            if any(clinic.state == 'room_available' for clinic in rec.clinic_ids):
                rec.state = "room_available"
            else:
                rec.state = "not_available"

    image = fields.Binary("Ảnh khoa")
    state = fields.Selection([('room_available', 'Có phòng'), ('not_available', 'Không có sẵn')], default='room_available', compute="_compute_department_state",)
    health_center_id = fields.Many2one('medical.health_center', string="Trung tâm sức khoẻ", store=True, required=True)
    floor_number = fields.Integer('Số tầng')
    type = fields.Selection([('normal', 'Bình thường'), ('imaging', 'Hình ảnh'), ('laboratory', 'Phòng xét nghiệm')], 'Loại')
    telephone_access = fields.Boolean('Truy cập điện thoại')
    private_bathroom = fields.Boolean('Phòng tắm riêng')
    television = fields.Boolean('Ti-vi')
    refrigerator = fields.Boolean('Tủ lạnh')
    air_conditioning = fields.Boolean('Điều hoà không khí')
    guest_sofa_bed = fields.Boolean('Giường sofa cho khách')
    internet_access = fields.Boolean('Truy cập Internet')
    cicrowave = fields.Boolean('Lò vi sóng')
    extra_infor = fields.Char('Thông tin chi tiết')
    clinic_ids = fields.One2many(comodel_name='medical.clinic', inverse_name='department_id')

    @api.depends('clinic_ids')
    def get_count_clinic(self):
        for rec in self:
            rec.clinic_count =  len(rec.clinic_ids)

    clinic_count = fields.Integer('Phòng', compute="get_count_clinic")
    doctor_ids = fields.One2many('medical.doctor', 'department_id')

    @api.depends('doctor_ids')
    def get_count_doctor(self):
        for rec in self:
            rec.doctor_count =  len(rec.doctor_ids)
    
    doctor_count = fields.Integer('Đơn thuốc', compute="get_count_doctor")
    prescription_ids = fields.One2many('medical.prescription', 'department_id')

    @api.depends('prescription_ids')
    def get_count_prescription(self):
        for rec in self:
            rec.prescription_count =  len(rec.prescription_ids)

    prescription_count = fields.Integer('Đơn thuốc', compute="get_count_prescription")
    walkins_ids = fields.One2many('medical.walkins', 'department_id')

    @api.depends('walkins_ids')
    def get_count_walkins(self):
        for rec in self:
            rec.walkins_count =  len(rec.walkins_ids)

    walkins_count = fields.Integer('Phiếu khám bệnh', compute="get_count_walkins")
    diagnostic_imaging_ids = fields.One2many('medical.diagnostic_imaging', 'department_id')

    @api.depends('diagnostic_imaging_ids')
    def get_count_diagnostic_imaging(self):
        for rec in self:
            rec.diagnostic_imaging_count =  len(rec.diagnostic_imaging_ids)
    
    diagnostic_imaging_count = fields.Integer('Chẩn đoán hình ảnh', compute="get_count_diagnostic_imaging")
    favorite = fields.Boolean(default=False)

    
    def btn_room_available(self):
        self.state = "room_available"

    def btn_not_available(self):
        self.state = "not_available"

    def action_create_walkins(self):
        # action['domain'] = {'doctor_id': [('id', 'in', self.doctor_ids)]}
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Phiếu khám bệnh',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.walkins',
            'target': 'current',
            'context': {
                'default_health_center_id': self.health_center_id.id,
                'default_department_id': self.id
            }
        }
    def action_create_diagnostic_imaging(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chẩn đoán hình ảnh',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.diagnostic_imaging',
            'target': 'current',
            'context': {
                'default_department_id': self.id
            }
        }
    def btn_count_walkins(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Phiếu khám bệnh',
            'view_type': 'form,kanban,tree,calendar',    
            'view_mode': 'kanban,tree,calendar,form',
            'res_model': 'medical.walkins',
            'context': {
                'default_health_center_id': self.health_center_id.id,
                'default_department_id': self.id,
                'search_default_group_by_state': 1,
                'search_default_group_by_doctor': 2
            },
            'domain': [('department_id', '=', self.id)]
        }
    def btn_count_diagnostic_imaging(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chẩn đoán hình ảnh',
            'view_type': 'form,tree',
            'view_mode': 'tree,form',
            'res_model': 'medical.diagnostic_imaging',
            'context': {
                'default_health_center_id': self.health_center_id.id,
                'default_department_id': self.id,
                'search_default_group_by_state': 1,
                'search_default_group_by_doctor': 2
            },
            'domain': [('department_id', '=', self.id)]
        }
    def btn_count_prescription(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đơn thuốc',
            'view_type': 'form,tree',
            'view_mode': 'tree,form',
            'res_model': 'medical.prescription',
            'context': {
                'default_health_center_id': self.health_center_id.id,
                'default_department_id': self.id,
                'search_default_group_by_state': 1,
                'search_default_group_by_doctor': 2
            },
            'domain': [('department_id', '=', self.id)]
        }
    def btn_count_doctor(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bác sĩ',
            'view_type': 'kanban,form,tree',
            'view_mode': 'kanban,tree,form',
            'res_model': 'medical.doctor',
            'context': {
                'default_health_center_id': self.health_center_id.id,
                'default_department_id': self.id
            },
            'domain': [('department_id', '=', self.id)]
        }

    def toggle_favorite(self):
        self.favorite = self.favorite == False

class Clinic(models.Model):
    _name = 'medical.clinic'    
    _description = 'medical.clinic'

    name = fields.Char('Tên phòng', required=True)
    state = fields.Selection([('room_available', 'Trống'), ('not_available', 'Không có sẵn')], default='room_available')
    health_center_id = fields.Many2one('medical.health_center', string="Trung tâm sức khoẻ", store=True, required=True)
    department_id = fields.Many2one('medical.department', string="Khoa", store=True, domain="[('health_center_id', '=', health_center_id)]")
    extra_infor = fields.Char('Thông tin bổ sung')

        
    def btn_room_available(self):
        self.state = "room_available"
    def btn_not_available(self):
        self.state = "not_available"
        
class Pharmacies(models.Model):
    _name = "medical.pharmacies"
    _description = "medical.pharmacies"

    name = fields.Char('Tên hiệu thuốc')
    image = fields.Binary("Ảnh đại diện")
    health_center_id = fields.Many2one('medical.health_center', string="Trung tâm sức khoẻ", store=True, required=True)
    street = fields.Char('Địa chỉ')
    street2 = fields.Char('')
    city = fields.Char('Thành phố')
    zip = fields.Char('Mã bưu điện')
    country_id_new = fields.Many2one('res.country', string="Quốc gia", required=True)
    state_id_new = fields.Many2one('res.country.state', string="Tỉnh/Thành phố", store=True, required=True, domain="[('country_id', '=', country_id_new)]")
    website_link = fields.Char('Website Link')
    phone_number = fields.Char('Điện thoại')
    email = fields.Char('Email')
    extra_infor = fields.Char('Thông tin bổ sung')

class Speciality(models.Model):
    _name = 'medical.speciality'
    _description = 'medical.speciality'

    name = fields.Char('Mô tả', required=True)
    code = fields.Char('Mã')

class Degree(models.Model):
    _name = 'medical.degree'
    _description = 'medical.degree'

    name = fields.Char('Trình độ', required=True)
    full_name = fields.Char('Họ và tên', required=True)

class MedicineVaccine(models.Model):
    _name = 'medical.medicine_vaccine'
    _description = 'medical.medicine_vaccine'

    name = fields.Char('Tên thuốc', translate=True, required=True)
    type_of_medicine = fields.Selection([('medicine', 'Thuốc'), ('vaccine', 'Vaccine')], 'Loại thuốc', required=True, default="medicine")
    sale_price = fields.Integer('Giá bán')
    therapeutic_effect = fields.Char('Hiệu quả điều trị')
    pregnancy_warning = fields.Boolean('Cảnh bảo mang thai')
    quantity_on_hand = fields.Integer('Số lượng hiện có', default=0, readonly=True)
    extra_infor = fields.Char('Thông tin thêm')
    pregnancy_and_lactancy = fields.Char('Mang thai và cho con bú')
    composition = fields.Char('Thành phần')
    dosage_instructions = fields.Char('Hướng dẫn sử dụng liều lượng')
    adverse_reactions = fields.Char('Phản ứng bất lợi')
    indication = fields.Char('Chỉ định')
    overdosage = fields.Char('Quá liều')
    storage_conditions = fields.Char('Điều kiện bảo quản')

class DoseUnits(models.Model):
    _name = 'medical.dose_units'
    _description = 'medical.dose_units'

    name = fields.Char('Đơn vị', required=True)
    description = fields.Char('Mô tả')
class MedicinesDosage(models.Model):
    _name = 'medical.medicines_dosage'
    _description = 'medical.medicines_dosage'

    name = fields.Char('Tần số', required=True)
    code = fields.Char('Mã')
    abbreviation = fields.Char('Viết tắt')

class Vaccine(models.Model):
    _name = 'medical.vaccine'
    _description = 'medical.vaccine'

    name = fields.Many2one('medical.medicine_vaccine', 'Vaccine', domain="[('type_of_medicine', '=', 'vaccine')]", required=True, store=True)
    patient_id = fields.Many2one('medical.patient', 'Bệnh nhân', required=True, store=True)
    doctor_id = fields.Many2one('medical.doctor', 'Bác sĩ', required=True, store=True)
    dose = fields.Integer('Liều #', default=1)
    date = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())
    health_center_id = fields.Many2one('medical.health_center', 'Nơi thực hiện', store=True)
    observation = fields.Char('Quan sát/Theo dõi')

class LabUnits(models.Model):
    _name = 'medical.lab_units'
    _description = 'medical.lab_units'

    name = fields.Char('Tên đơn vị')
    code = fields.Char('Mã')

class LabTestTypes(models.Model):
    _name = 'medical.lab_test_types'
    _description = 'medical.lab_test_types'

    name = fields.Char('Tên xét nghiệm', required=True)
    code = fields.Char('Mã')
    test_charge = fields.Integer('Phí xét nghiệm')
    lab_test_case_ids = fields.One2many('medical.lab_test_case', 'lab_test_types_id')
    extra_infor = fields.Char('Thông tin thêm')

class LabTestCase(models.Model):
    _name = 'medical.lab_test_case'
    _description = 'medical.lab_test_case'
    
    name = fields.Char('Xét nghiệm', required=True)
    sequence = fields.Integer('Mã thứ tự')
    normal_range = fields.Text('Phạm vi bình thường')
    units = fields.Many2one('medical.lab_units', 'Đơn vị')
    lab_test_types_id = fields.Many2one('medical.lab_test_types', 'Loại xét nghiệm')

class DiagnosticImagingTypes(models.Model):
    _name = 'medical.diagnostic_imaging_types'
    _description = 'medical.diagnostic_imaging_types'
    
    name = fields.Char('Tên', required=True)
    code = fields.Char('Mã')
    test_charge = fields.Integer('Phí xét nghiệm')
    extra_infor = fields.Char('Thông tin thêm')

class DiagnosticImaging(models.Model):
    _name = 'medical.diagnostic_imaging'
    _description = 'Chẩn đoán hình ảnh'
    
    name = fields.Char('Số xét nghiệm #', required=True, default='/', readonly=True)
    state = fields.Selection([('draft', 'Dự thảo'),('invoiced', 'Đã xuất hoá đơn'), ('test_in_profgress', 'Đang thực hiện'), ('completed', 'Hoàn thành')], 'Trạng thái', default='draft')
    diagnostic_imaging_types_id = fields.Many2one('medical.diagnostic_imaging_types', 'Loại chẩn đoán', store=True, required=True)
    identification_code = fields.Char('Mã bệnh nhân',related='patient_id.identification_code', readonly=True)
    patient_id = fields.Many2one('medical.patient', 'Bệnh nhân', store=True, related='walkins_id.patient_id')
    date_requested = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())
    date_of_birth = fields.Date('Ngày sinh', related='patient_id.dob',)
    sex = fields.Selection([('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')], "Giới tính", related='patient_id.sex')
    doctor_id = fields.Many2one('medical.doctor','Bác sĩ', store=True, related='walkins_id.doctor_id')
    walkins_id = fields.Many2one('medical.walkins', 'Phiếu khám bệnh', required=True, domain="[('department_id', '=', department_id)]")
    department_id = fields.Many2one('medical.department' , 'Khoa',store=True, related='walkins_id.department_id')
    date_of_the_anlysis = fields.Datetime('Ngày phân tích', select=True)
    image_1 = fields.Binary('Ảnh 1')
    image_2 = fields.Binary('Ảnh 2')
    image_3 = fields.Binary('Ảnh 3')
    image_4 = fields.Binary('Ảnh 4')
    image_5 = fields.Binary('Ảnh 5')
    image_6 = fields.Binary('Ảnh 6')
    analysis = fields.Char('Phân tích')
    conclusion = fields.Char('Kết luận')
    material_consumption_ids = fields.One2many('medical.material_consumption', 'diagnostic_imaging_id')


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('diagnostic_imaging.seq')

        record =  super(DiagnosticImaging, self).create(vals)
        return record

    def btn_invoiced(self):
        self.state = 'invoiced'

    def btn_test_in_profgress(self):
        self.state = 'test_in_profgress'
        current_dt = fields.datetime.now()
        self.date_of_the_anlysis = current_dt

    def btn_completed(self):
        self.state = 'completed'
        current_dt = fields.datetime.now()
        self.date_of_the_anlysis = current_dt

    def in_diagnostic_imaging(self):
        raise UserError('Message: Tính năng đang bảo trì!')

class MaterialConsumption(models.Model):
    _name = 'medical.material_consumption'
    _description = 'medical.material_consumption'
    
    name = fields.Char('Sản phẩm')
    sequence = fields.Integer('Mã thứ tự', default=lambda self: self.env['ir.sequence'].next_by_code('material_consumption.seq'))
    quantity = fields.Integer('Số lượng', default='1')
    # units = fields.Many2one('uom.uom', 'Đơn vị')
    units = fields.Char('Dơn vị')
    diagnostic_imaging_id = fields.Many2one('medical.diagnostic_imaging', 'Chẩn đoán hình ảnh', store=True)

class ExaminationTime(models.Model):
    _name = 'medical.examination_time'
    _description = 'medical.examination_time'

    name = fields.Float('Thời gian khám (Định dạng 24 giờ)')
    description = fields.Char('Mô tả')
    time =  fields.Float('Thời lượng (1 giờ)', default='1')
    shift_id = fields.Many2one('medical.shift', 'Ca', store=True)

class Shift(models.Model):
    _name = 'medical.shift'
    _description = 'medical.shift'

    name = fields.Selection([('morning', 'Sáng'), ('evening', 'Tối')], 'Ca làm việc')
    description = fields.Char('Mô tả')
    time_ids = fields.One2many('medical.examination_time', 'shift_id', 'Thời gian khám bệnh')