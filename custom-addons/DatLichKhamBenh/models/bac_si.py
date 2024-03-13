from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BacSiResUser(models.Model):
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
            
    _is_invisible = fields.Boolean(compute="_get_res_user_field")
    bac_si_ids = fields.One2many('medical.bac_si', 'res_users_id', 'Bác sĩ liên kết', domain="[('res_users_id', '=', None)]")

class BacSi(models.Model):
    _name = 'medical.bac_si'
    _description = 'medical.bac_si'

    name = fields.Char('Tên bác sĩ', required=True)

    def _get_res_user_field(self):
        users_search = self.env['res.users'].search([])
        users = []
        for user in users_search:
            if user.has_group('DatLichKhamBenh.group_employee_doctor'):
                users.append(user.id)
        return [('id', 'in', users)]
    res_users_id = fields.Many2one('res.users', 'Tài khoản bác sĩ', store=True, domain=_get_res_user_field)

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    chuyen_mon = fields.Many2one('medical.chuyen_mon', 'Chuyên môn', store=True)

    trinhdo_bangcap = fields.Many2many(comodel_name='medical.trinhdo_bangcap', relation='medical_bac_si_tt_bc_rel', column1='bac_si_id', column2='trinhdo_bangcap_id', string='Trình độ/Bằng cấp')
    
    phi_kham_benh = fields.Integer('Phí khám bệnh',default=0)

    id_giay_phep = fields.Char('ID giấy phép')

    duoc_si = fields.Boolean('Dược sĩ')

    y_ta = fields.Boolean('Y tá')

    dieu_duong = fields.Boolean('Điều dưỡng')

    trung_tam_y_te_id = fields.Many2one('medical.trung_tam_y_te', 'Trung tâm y tế', store=True, required=True)

    khoa_id = fields.Many2one('medical.khoa', 'Khoa', store=True, domain="[('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]")

    dia_chi = fields.Char('Địa chỉ')

    dia_chi_2 = fields.Char('')

    phuong_xa = fields.Char('Phường/Xã')

    quan_huyen = fields.Char('Quận/Huyện')

    thanh_pho = fields.Char('Thành phố')

    zip = fields.Char('Mã bưu điện')

    country_id_new = fields.Many2one('res.country', string="country")

    state_id_new = fields.Many2one('res.country.state', string="State", store=True, domain="[('country_id', '=', country_id_new)]")

    so_dien_thoai = fields.Char('Số điện thoại')

    so_dien_thoai_van_phong = fields.Char('Điện thoại văn phòng')

    email = fields.Char('Email')

    thong_tin_them = fields.Char('Thông tin thêm')

    examination_schedule_ids = fields.One2many("medical.examination_schedule", "doctor_id", domain=[('is_pass_date','=',True)])

    phieu_kham_benh_ids = fields.One2many(comodel_name='medical.phieu_kham_benh', inverse_name='bac_si_id')
    phieu_kham_benh_count = fields.Integer('Phiếu khám bệnh', compute="get_count_phieu_kham_benh", store=True)

    @api.depends('phieu_kham_benh_ids')
    def get_count_phieu_kham_benh(self):
        for rec in self:
            rec.phieu_kham_benh_count =  len(rec.phieu_kham_benh_ids)

    don_thuoc_ids = fields.One2many(comodel_name='medical.don_thuoc', inverse_name='bac_si_id')
    don_thuoc_count = fields.Integer('Đơn thuốc', compute="get_count_don_thuoc", store=True)

    @api.depends('don_thuoc_ids')
    def get_count_don_thuoc(self):
        for rec in self:
            rec.don_thuoc_count =  len(rec.don_thuoc_ids)

    
class DuocSi(models.Model):
    _name = 'medical.duoc_si'
    _description = 'medical.duoc_si'

    name = fields.Char('Tên dược sĩ', required=True)

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    chuyen_mon = fields.Many2one('medical.chuyen_mon', 'Chuyên môn', store=True)

    trinhdo_bangcap = fields.Many2many(comodel_name='medical.trinhdo_bangcap', relation='medical_duoc_si_tt_bc_rel', column1='duoc_si_id', column2='trinhdo_bangcap_id', string='Trình độ/Bằng cấp')

    phi_kham_benh = fields.Integer('Phí khám bệnh',default=0)

    id_giay_phep = fields.Char('ID giấy phép')

    hieu_thuoc_id = fields.Many2one('medical.hieu_thuoc', 'Hiệu thuốc', store=True, required=True)

    dia_chi = fields.Char('Địa chỉ')

    dia_chi_2 = fields.Char('')

    phuong_xa = fields.Char('Phường/Xã')

    quan_huyen = fields.Char('Quận/Huyện')

    thanh_pho = fields.Char('Thành phố')

    zip = fields.Char('Mã bưu điện')

    country_id_new = fields.Many2one('res.country', string="country")

    state_id_new = fields.Many2one('res.country.state', string="State", store=True, domain="[('country_id', '=', country_id_new)]")

    so_dien_thoai = fields.Char('Số điện thoại')

    so_dien_thoai_van_phong = fields.Char('Điện thoại văn phòng')

    email = fields.Char('Email')

    thong_tin_them = fields.Char('Thông tin thêm')
    
    # don_thuoc_duoc_dat_ids = fields.One2many(comodel_name='medical.don_thuoc_duoc_dat', inverse_name='duoc_si_id')
    # don_thuoc_duoc_dat_count = fields.Integer('Đơn thuốc được đặt', compute="get_count_don_thuoc_duoc_dat", store=True)
    # @api.depends('don_thuoc_duoc_dat_ids')
    # def get_count_don_thuoc_duoc_dat(self):
    #     for rec in self:
    #         rec.don_thuoc_duoc_dat_count =  len(rec.don_thuoc_duoc_dat_ids)

class ExaminationSchedule(models.Model):
    _name = 'medical.examination_schedule'
    _description = 'medical.examination_schedule'

    doctor_id = fields.Many2one('medical.bac_si','Bác sĩ')

    name = fields.Selection(selection='_get_next_6_days', required=True)

    schedule = fields.Date(compute='_get_date_schedule', string='Ngày trống', store=True)

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
    
    @api.depends('name')
    def _get_date_schedule(self):
        for rec in self:
            if rec.name:
                rec.schedule = datetime.strptime(rec.name, '%Y-%m-%d').date()
    
    shift = fields.Many2one('medical.shift','Ca làm việc', required=True, store=True)

    schedule_time_ids = fields.Many2many(related='shift.time')

    today = fields.Date(default=lambda self: fields.Date.today(), store=False)
    @api.model
    def _set_today(self):
        for rec in self:
            rec.today = fields.Date.today()

    @api.depends('today','schedule')
    def _check_pass_date(self):
        for rec in self:
            if rec.schedule and rec.schedule < rec.today:
                rec.is_pass_date = False
            else:
                rec.is_pass_date = True

    is_pass_date = fields.Boolean(compute="_check_pass_date", store=True)


