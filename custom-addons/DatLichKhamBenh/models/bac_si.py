

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BacSi(models.Model):
    _name = 'medical.bac_si'
    _description = 'medical.bac_si'

    name = fields.Char('Tên bác sĩ', required=True)

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

    