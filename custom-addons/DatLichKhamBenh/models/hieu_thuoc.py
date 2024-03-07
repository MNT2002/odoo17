from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DonThuocDuocDat(models.Model):
    _name = 'medical.don_thuoc_duoc_dat'
    _description = 'medical.don_thuoc_duoc_dat'

    name = fields.Char('Đơn thuốc #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('don_thuoc_duoc_dat.seq')

        record =  super(DonThuocDuocDat, self).create(vals)
        return record
    
    state = fields.Selection([('DuThao', 'Dự thảo'), ('XacNhan', 'Xác nhận'), ('ChoThanhToan', 'Chờ thanh toán'), ('DaXuatHoaDon', 'Đã xuất hoá đơn')], string='Trạng thái', default='DuThao')

    benh_nhan_id = fields.Many2one('medical.benh_nhan', 'Bệnh nhân', store=True, required=True, readonly=True)

    bac_si_id = fields.Many2one('medical.bac_si', 'Bác sĩ phụ trách', store=True, required=True, readonly=True)
    
    ngay_ke_don = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    trung_tam_y_te_id = fields.Many2one('medical.trung_tam_y_te', related='don_thuoc_id.trung_tam_y_te_id')

    khoa_id = fields.Many2one('medical.khoa', related='don_thuoc_id.khoa_id', readonly=True)

    nha_thuoc_id = fields.Many2one('medical.hieu_thuoc', 'Nhà thuốc', domain="[('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]", store=True, required=True)

    duoc_si_id = fields.Many2one('medical.duoc_si', 'Dược sĩ', store=True, required='id = True')

    don_thuoc_id = fields.Many2one('medical.don_thuoc', 'Đơn thuốc #', store=True, readonly=True)

    chi_tiet_toa_thuoc_ids = fields.One2many(comodel_name='medical.chi_tiet_toa_thuoc', inverse_name='don_thuoc_id', related='don_thuoc_id.chi_tiet_toa_thuoc_ids')

    def btn_xac_nhan(self):
        self.state = 'XacNhan'
    def btn_xuat_hoa_don(self):
        self.state = 'DaXuatHoaDon'