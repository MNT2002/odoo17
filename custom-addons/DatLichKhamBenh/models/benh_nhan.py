import datetime

from odoo import models, fields, api


class BenhNhan(models.Model):
    _name = 'medical.benh_nhan'
    _description = 'Bệnh nhân'

    name = fields.Char('Họ và tên', required=True)

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    tuoi_benh_nhan = fields.Integer('Tuổi bệnh nhân', compute='_compute_age', store=True)
    tinh_trang_hon_nhan = fields.Selection([('DocThan', 'Độc thân'), ('DaCuoi', 'Đã cưới'), ('GoaPhu', 'Góa phụ'), ('LyDi', 'Ly dị'), ('LyThan', 'Ly thân')], "Tình trạng hôn nhân")

    gioi_tinh = fields.Selection([('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], "Giới tính")

    ngay_sinh = fields.Date('Ngày sinh', required=True)

    nam_sinh = fields.Char('Năm sinh', compute='_compute_year_of_birth', store=True)

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
    @api.depends("ngay_sinh")
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


    # Tai Khoan Nguoi Dung Page
    dia_chi = fields.Char('Địa chỉ')

    dia_chi_2 = fields.Char('')

    phuong_xa = fields.Char('Phường/Xã')

    quan_huyen = fields.Char('Quận/Huyện')

    thanh_pho = fields.Char('Thành phố')

    zip = fields.Char('Mã bưu điện')

    country_id_new = fields.Many2one('res.country', string="country")

    state_id_new = fields.Many2one('res.country.state', string="State", store=True)

    website_link = fields.Char('Website Link')

    chuc_vu = fields.Char('Chức vụ')

    so_dien_thoai = fields.Char('Điện thoại')

    email = fields.Char('Email')