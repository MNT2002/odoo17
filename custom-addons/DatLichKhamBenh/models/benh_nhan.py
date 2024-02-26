import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BenhNhan(models.Model):
    _name = 'medical.benh_nhan'
    _description = 'Bệnh nhân'

    name = fields.Char('Họ và tên', required=True)

    # Chạy hàm bên dưới khi tạo một bản ghi
    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()

        vals['identification_code'] = self.env['ir.sequence'].next_by_code('benh_nhan.seq')

        record =  super(BenhNhan, self).create(vals)
        return  record
    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        record =  super(BenhNhan, self).write(vals)
        return record
    def unlink(self):
        for benh_nhan in self:
            if benh_nhan.nhom_mau or benh_nhan.nhom_mau == '':
                raise ValidationError('Cannot delete benh nhan defined "nhom mau" already!')
        return super(BenhNhan, self).unlink()
    # def copy(self, default=None):
    #     default = default or {}
    #     departments = self.env['ten_model'].search([('description', '!=', False), ('description', '!=', '')], order='name', limit=1)
    #     default['department_id'] = departments.id
    #     return super(Employee, self).copy(default)

    identification_code = fields.Char('Mã nhận dạng', readonly=True)

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    tuoi_benh_nhan = fields.Integer('Tuổi bệnh nhân', compute='_compute_age', store=True)

    tinh_trang_hon_nhan = fields.Selection([('DocThan', 'Độc thân'), ('DaCuoi', 'Đã cưới'), ('GoaPhu', 'Góa phụ'), ('LyDi', 'Ly dị'), ('LyThan', 'Ly thân')], "Tình trạng hôn nhân")

    gioi_tinh = fields.Selection([('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], "Giới tính")

    ngay_sinh = fields.Date('Ngày sinh', required=True)

    nam_sinh = fields.Char('Năm sinh', compute='_compute_year_of_birth')

    @api.depends("ngay_sinh")
    def _compute_age(self):
        ngay_hien_tai = fields.Date.today()
        for rec in self:
            rec.tuoi_benh_nhan = 0
            if rec.ngay_sinh and rec.ngay_sinh < ngay_hien_tai:
                start = rec.ngay_sinh
                age_calc = (ngay_hien_tai - start).days / 365
                if age_calc > 0.0:
                    rec.tuoi_benh_nhan = age_calc
            elif rec.ngay_sinh and rec.ngay_sinh > ngay_hien_tai:
                return {'warning': {'title': 'Cảnh báo',
                                    'message': 'Vui lòng nhập ngày sinh phù hợp!'}}
    @api.onchange("ngay_sinh")
    def _compute_year_of_birth(self):
        for record in self:
            if record.ngay_sinh:
                date_object =  fields.Date.from_string(record.ngay_sinh).year
                record.nam_sinh = date_object


    cccd = fields.Char('CMND, CCCD/ Hộ chiếu')

    nhom_mau = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], "Nhóm máu")

    rh = fields.Selection([('+', '+'), ('-', '-')], "Rh")

    bac_si_gia_dinh = fields.Char("Bác sĩ gia đình")

    state = fields.Selection([('DangCho','Đang Chờ'), ('DaKham', 'Đã Khám')], string='Trạng thái', default='DangCho')

    def btn_da_kham(self):
        self.state = "DaKham"
    def btn_dang_cho(self):
        self.state = "DangCho"


    # Tai Khoan Nguoi Dung Page
    dia_chi = fields.Char('Địa chỉ')

    dia_chi_2 = fields.Char('')

    phuong_xa = fields.Char('Phường/Xã')

    quan_huyen = fields.Char('Quận/Huyện')

    thanh_pho = fields.Char('Thành phố')

    zip = fields.Char('Mã bưu điện')

    country_id_new = fields.Many2one('res.country', string="country")

    state_id_new = fields.Many2one('res.country.state', string="State", store=True, domain="[('country_id', '=', country_id_new)]")

    website_link = fields.Char('Website Link')

    chuc_vu = fields.Char('Chức vụ')

    so_dien_thoai = fields.Char('Điện thoại')

    email = fields.Char('Email')

    ghi_chu = fields.Char('Ghi chú', readonly=1)