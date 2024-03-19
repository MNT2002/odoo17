from odoo import fields, models, api
from odoo.exceptions import ValidationError
class walkins(models.Model):
    _name = 'medical.walkins'
    _description = 'medical.walkins'
    _order = "create_date desc, id desc"

    name = fields.Char('Số thứ tự #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('walkins.seq')

        # vals['doctor_id'] = self.env.context.get('active_id', [])
        record =  super(walkins, self).create(vals)
        return record

    state = fields.Selection([('scheduled', 'Đã lên lịch'), ('waiting_for_check', 'Chờ khám'), ('checking', 'Đang kiểm tra'), ('waiting_for_invoice', 'Chờ thanh toán'), ('completed', 'Hoàn thành')], string='Trạng thái', default='scheduled')
    
    def btn_scheduled(self):
        self.state = "scheduled"
    def btn_waiting_for_check(self):
        self.state = "waiting_for_check"
    def btn_checking(self):
        self.state = "checking"
    def btn_waiting_for_invoice(self):
        for rec in self:
            if not rec.doctor_id or rec.doctor_id == "":
                raise ValidationError("Lỗi cấu hình!\nKhông tìm thấy bác sĩ nào để tạo hóa đơn !") 
            else:
                self.state = "waiting_for_invoice"
                
    def btn_completed(self):
        self.state = "completed"

    patient_id = fields.Many2one('medical.patient', 'Bệnh nhân', store=True, required=True)

    doctor_id = fields.Many2one('medical.doctor', 'Bác sĩ phụ trách', store=True, required=True, domain="[('department_id', '=', department_id)]")
    
    date = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    today = fields.Datetime('Ngày hôm nay', store=False
                                , default=lambda self: fields.Date.today())

    schedule_selection_id = fields.Many2one('medical.examination_schedule', domain="[('doctor_id','=',doctor_id),('schedule','>=',today)]", 
    store=True, required=True, string='Ngày khám bệnh')

    schedule_date = fields.Datetime('Ngày khám bênh', store=True, compute="_convert_schedule_date")

    @api.depends('schedule_time_id')
    def _convert_schedule_date(self):
        # schedule_selection_id = self.env['medical.examination_schedule'].browse(self.schedule_selection_id)
        # self.schedule_date = self.schedule_selection_id.schedule
        # schedule_time_selected = self.env['medical.examination_time'].search([('id','=',self.schedule_time_id.id)])
       
        date_value = self.schedule_selection_id.schedule
        float_value = self.schedule_time_id.name
        
        if date_value and float_value:
            hours = int(float_value)
            minutes = int((float_value - hours) * 60)
            print(hours, minutes)
            combined_datetime = fields.datetime.strptime(str(date_value), '%Y-%m-%d').replace(hour=(hours - 7), minute=minutes) #(hourse-7 => thời gian khám đang hiển thị là giờ VN)
            # combined_datetime = fields.Datetime.context_timestamp(self, combined_datetime)
        
            self.schedule_date = combined_datetime
            print('=========================', combined_datetime)
        else:
            self.schedule_date = False

    @api.onchange('schedule_selection_id')
    def onchange_schedule_selection(self):
        self.schedule_time_id = False

    shift_id = fields.Many2one('medical.shift', related='schedule_selection_id.shift_id')

    schedule_time_id = fields.Many2one('medical.examination_time', 'Thời gian khám bệnh (24 giờ)', domain="[('shift_id', '=', shift_id)]", required=True, store=True)

    dob = fields.Date('Ngày sinh', compute="_compute_birthday")

    image = fields.Binary('Ảnh đại diện', related='patient_id.image',)
    age = fields.Char('Tuổi', related='patient_id.age', store=True)
    street = fields.Char('Địa chỉ', related='patient_id.street')

    sex = fields.Selection([('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')], "Giới tính", related='patient_id.sex', readonly=True, store=True)

    marital_status = fields.Selection([('single', 'Độc thân'), ('married', 'Đã cưới'), ('widowed', 'Góa phụ'), ('divorced', 'Ly dị'), ('separated', 'Ly thân')], "Tình trạng hôn nhân", related='patient_id.marital_status', readonly=True, store=True)

    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], "Nhóm máu", related='patient_id.blood_type', readonly=True, store=True)

    rh =  fields.Selection([('+', '+'), ('-', '-')], 'Rh', related='patient_id.rh', readonly=True,store=True)

    reason_check = fields.Char('Lý do kiểm tra')

    symptom = fields.Char('Triệu chứng')

    health_center_id = fields.Many2one('medical.health_center', 'Trung tâm y tế', store=True)

    department_id = fields.Many2one('medical.department', 'Khoa', domain="[('health_center_id', '=', health_center_id)]", store=True)

    clinic_id = fields.Many2one('medical.clinic', 'Phòng', domain="[('department_id', '=', department_id), ('health_center_id', '=', health_center_id)]", store=True)

    vaccine_ids = fields.Many2many(comodel_name='medical.vaccine', relation='medical_walkins_vaccine', column1='walkins_id', column2='vaccine_id', string='Vắc xin')

    prescription_ids = fields.One2many('medical.prescription', inverse_name='walkins_id')
    

    @api.depends('patient_id')
    def _compute_birthday(self):
        for rec in self:
            if rec.patient_id:
                rec.dob = rec.patient_id.dob
            else: 
                rec.dob = ""

    diagnosis = fields.Char('Chẩn đoán')

    comments = fields.Char('Bình luận')

    date_re_exam = fields.Date('Ngày tái khám')
    
    diagnostic_imaging_ids = fields.One2many('medical.diagnostic_imaging', 'walkins_id')

class Prescription(models.Model):
    _name = 'medical.prescription'
    _description = 'medical.prescription'
    _order = "create_date desc, id desc"

    name = fields.Char('Đơn thuốc #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('prescription.seq')
        
        record =  super(Prescription, self).create(vals)
        return record

    state = fields.Selection([('draft', 'Dự thảo'), ('sent', 'Đã gửi')], string='Trạng thái', default='draft')        

    def btn_send(self):
        self.state = 'sent'

    @api.model
    def write(self, vals):
        if vals.get('state'):
            if vals.get('state') == 'sent':
                vals_new_rec = {
                    'patient_id': self.patient_id.id,
                    'doctor_id': self.doctor_id.id,
                    'pharmacies_id': self.pharmacies_id.id,
                    'prescription_id': self.id
                    
                }
                self.env['medical.prescription_orders'].create(vals_new_rec)
        return super(Prescription, self).write(vals)
    

    patient_id = fields.Many2one('medical.patient', 'Bệnh nhân', store=True, related='walkins_id.patient_id')

    health_center_id = fields.Many2one('medical.health_center', related='walkins_id.health_center_id')

    department_id = fields.Many2one('medical.department', related='walkins_id.department_id', readonly=True)

    pharmacies_id = fields.Many2one('medical.pharmacies', 'Nhà thuốc', domain="[('health_center_id', '=', health_center_id)]", store=True, required=True)

    doctor_id = fields.Many2one('medical.doctor', 'Bác sĩ', store=True, related='walkins_id.doctor_id' )

    prescription_date = fields.Datetime('Ngày kê đơn', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    walkins_id = fields.Many2one('medical.walkins', 'Số thứ tự #', readonly=True, store=True)

    prescription_details_ids = fields.One2many(comodel_name='medical.prescription_details', inverse_name='prescription_id')

    def action_confirm_and_print(self):
        raise ValidationError('Tính năng đang bảo trì!')

    prescription_orders_ids = fields.One2many('medical.prescription_orders', 'prescription_id')

class PrescriptionDetails(models.Model):
    _name = 'medical.prescription_details'
    _description = 'medical.prescription_details'
    _order = "create_date desc, id desc"

    name = fields.Many2one('medical.medicine_vaccine', 'Thuốc', domain="[('type_of_medicine', '=', 'medicine')]", required=True, store=True)

    prescription_id = fields.Many2one('medical.prescription', 'Đơn thuốc', store=True, readonly=True)

    indication = fields.Char('Chỉ định', related='name.indication', store=True)

    medicines_dosage_id = fields.Many2one('medical.medicines_dosage', 'Liều', store=True, required=True)

    dose_units_id = fields.Many2one('medical.dose_units','Đơn vị liều lường', store=True)

    comment = fields.Char('Bình luận')