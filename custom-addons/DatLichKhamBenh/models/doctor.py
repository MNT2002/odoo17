from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class DoctorResUser(models.Model):
    _inherit = 'res.users'

    @api.onchange('groups_id')
    def _get_res_user_field(self):
        users_search = self.env['res.users'].search([])
        users = []
        for user in users_search:
            if user.has_group('DatLichKhamBenh.group_employee_doctor'):
                users.append(user.id)
        if self.id in users:
            self._is_invisible = False
        else: 
            self._is_invisible = True
    
    # password = fields.Char(
    #     compute='_compute_password', inverse='_set_password', copy=False,
    #     help="Keep empty if you don't want the user to be able to connect on the system.")
            
    _is_invisible = fields.Boolean(compute="_get_res_user_field")
    doctor_ids = fields.One2many('medical.doctor', 'res_users_id', 'Bác sĩ liên kết', domain="[('res_users_id', '=', None)]")

class Doctor(models.Model):
    _name = 'medical.doctor'
    _description = 'medical.doctor'

    name = fields.Char('Tên bác sĩ', required=True)

    def _get_res_user_field(self):
        users_search = self.env['res.users'].search([])
        users = []
        for user in users_search:
            if user.has_group('DatLichKhamBenh.group_employee_doctor'):
                users.append(user.id)
        return [('id', 'in', users)]
        
    res_users_id = fields.Many2one('res.users', 'Tài khoản bác sĩ', store=True, domain=_get_res_user_field)
    image = fields.Binary("Ảnh đại diện")
    speciality_id = fields.Many2one('medical.speciality', 'Chuyên môn', store=True)
    degree_id = fields.Many2many(comodel_name='medical.degree', relation='medical_doctor_degree_rel', column1='doctor_id', column2='degree_id', string='Trình độ/Bằng cấp')
    consultancy_price = fields.Integer('Phí khám bệnh',default=0)
    lience_id = fields.Char('ID giấy phép')
    is_pharmacist = fields.Boolean('Dược sĩ')
    is_nurse = fields.Boolean('Y tá')
    is_receptionist = fields.Boolean('Điều dưỡng')
    health_center_id = fields.Many2one('medical.health_center', 'Trung tâm y tế', store=True, required=True)
    department_id = fields.Many2one('medical.department', 'Khoa', store=True, domain="[('health_center_id', '=', health_center_id)]", required=True)
    street = fields.Char('Địa chỉ')
    street2 = fields.Char('')
    ward = fields.Char('Phường/Xã')
    district = fields.Char('Quận/Huyện')
    city = fields.Char('Thành phố')
    zip = fields.Char('Mã bưu điện')
    country_id = fields.Many2one('res.country', string="country")
    state_id = fields.Many2one('res.country.state', string="State", store=True, domain="[('country_id', '=', country_id)]")
    phone_number = fields.Char('Số điện thoại')
    work_phone = fields.Char('Điện thoại văn phòng')
    email = fields.Char('Email')
    description = fields.Char('Mô tả')
    extra_infor = fields.Char('Thông tin thêm')
    examination_schedule_ids = fields.One2many("medical.examination_schedule", "doctor_id", domain=[('schedule','>=', fields.Date.today())])
    walkins_ids = fields.One2many(comodel_name='medical.walkins', inverse_name='doctor_id')

    @api.depends('walkins_ids')
    def get_count_walkins(self):
        for rec in self:
            rec.walkins_count =  len(rec.walkins_ids)
    walkins_count = fields.Integer('Phiếu khám bệnh', compute="get_count_walkins", store=True)
    prescription_ids = fields.One2many(comodel_name='medical.prescription', inverse_name='doctor_id')

    @api.depends('prescription_ids')
    def get_count_prescription(self):
        for rec in self:
            rec.prescription_count =  len(rec.prescription_ids)
    prescription_count = fields.Integer('Đơn thuốc', compute="get_count_prescription", store=True)
class Pharmacist(models.Model):
    _name = 'medical.pharmacist'
    _description = 'medical.pharmacist'

    name = fields.Char('Tên dược sĩ', required=True)
    image = fields.Binary("Ảnh đại diện")
    speciality_id = fields.Many2one('medical.speciality', 'Chuyên môn', store=True)
    degree_id = fields.Many2many(comodel_name='medical.degree', relation='medical_pharmacist_degree_rel', column1='pharmacist_id', column2='degree_id', string='Trình độ/Bằng cấp')
    consultancy_price = fields.Integer('Phí khám bệnh',default=0)
    lience_id = fields.Char('ID giấy phép')
    pharmacies_id = fields.Many2one('medical.pharmacies', 'Hiệu thuốc', store=True, required=True)
    street = fields.Char('Địa chỉ')
    street2 = fields.Char('')
    ward = fields.Char('Phường/Xã')
    district = fields.Char('Quận/Huyện')
    city = fields.Char('Thành phố')
    zip = fields.Char('Mã bưu điện')
    country_id = fields.Many2one('res.country', string="country")
    state_id = fields.Many2one('res.country.state', string="State", store=True, domain="[('country_id', '=', country_id)]")
    phone_number = fields.Char('Số điện thoại')
    work_phone = fields.Char('Điện thoại văn phòng')
    email = fields.Char('Email')
    extra_infor = fields.Char('Thông tin thêm')
    
    # prescription_duoc_dat_ids = fields.One2many(comodel_name='medical.prescription_duoc_dat', inverse_name='pharmacist_id')
    # prescription_duoc_dat_count = fields.Integer('Đơn thuốc được đặt', compute="get_count_prescription_duoc_dat", store=True)
    # @api.depends('prescription_duoc_dat_ids')
    # def get_count_prescription_duoc_dat(self):
    #     for rec in self:
    #         rec.prescription_duoc_dat_count =  len(rec.prescription_duoc_dat_ids)

class ExaminationSchedule(models.Model):
    _name = 'medical.examination_schedule'
    _description = 'medical.examination_schedule'
    _order = "schedule asc, id desc"

    doctor_id = fields.Many2one('medical.doctor','Bác sĩ' ,store=True)
    name = fields.Selection(selection='_get_next_6_days', required=True)

    @api.depends('name')
    def _get_date_schedule(self):
        for rec in self:
            if rec.name:
                rec.schedule = datetime.strptime(rec.name, '%Y-%m-%d').date()
                
    schedule = fields.Date(compute='_get_date_schedule', string='Ngày trống', store=True)

    @api.onchange('shift_id')
    def _check_schedule_date(self):
        print('doctor_id: ', self.doctor_id.name)
        print(self.env['medical.examination_schedule'].search([('doctor_id.name', '=', self.doctor_id.name)]))
        for rec in self.env['medical.examination_schedule'].search([('doctor_id.name', '=', self.doctor_id.name)]):
            if  rec.schedule == self.schedule and rec.shift_id == self.shift_id:
                raise UserError('Message: Lịch khám đã tồn tại trên hệ thống!')
    
    shift_id = fields.Many2one('medical.shift','Ca làm việc', required=True, store=True)
    schedule_time_ids = fields.One2many(related='shift_id.time_ids')
        

    @api.model
    def _get_next_6_days(self):
        # chosen_date = datetime.strptime(chosen_date, "%Y-%m-%d")  # Convert input string to datetime object
        next_days = []
        today = fields.Date.today()
        next_days.append(
            (
                str(today),
                ("Today "+ today.strftime("%Y-%m-%d"))
            )
        ) 
        for i in range(1, 7):  # Get the next 6 days
            next_day = today + timedelta(days=i)
            next_days.append(
                (
                    str(next_day),
                    (next_day.strftime("%a") + " "+ next_day.strftime("%Y-%m-%d"))
                )
            )  # Append formatted date string to the list
        return next_days

    # def _get_to_day(self):
    #     today = fields.Date.today()
    #     return today
    
    # @api.model
    # def read(self,fields=None, load='_classic_read'):
    #     today = self._get_to_day()
    #     arrExaminationSchedule = self.env['medical.examination_schedule'].search([])
    #     for rec in arrExaminationSchedule:
    #         if rec.schedule < today:
    #             rec.is_pass_date = False
    #         else:
    #             rec.is_pass_date = True

    #     res = super(ExaminationSchedule, self).read(fields=fields, load=load)
    #     return res
