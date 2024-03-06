from odoo import fields, models, api
from odoo.exceptions import ValidationError

class PhieuKhamBenh(models.Model):
    _name = 'medical.phieu_kham_benh'
    _description = 'medical.phieu_kham_benh'
    _order = "create_date desc, id desc"

    name = fields.Char('Số thứ tự #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('phieu_kham_benh.seq')

        # vals['bac_si_id'] = self.env.context.get('active_id', [])

        record =  super(PhieuKhamBenh, self).create(vals)
        return record

    state = fields.Selection([('DaLenLich', 'Đã lên lịch'), ('ChoKham', 'Chờ khám'), ('DangKiemTra', 'Đang kiểm tra'), ('ChoThanhToan', 'Chờ thanh toán'), ('HoanThanh', 'Hoàn thành')], string='Trạng thái', default='DaLenLich')
    
    def btn_da_len_lich(self):
        self.state = "DaLenLich"
    def btn_cho_kham(self):
        self.state = "ChoKham"
    def btn_dang_kiem_tra(self):
        self.state = "DangKiemTra"
    def btn_cho_thanh_toan(self):
        for rec in self:
            if not rec.bac_si_id or rec.bac_si_id == "":
                raise ValidationError("Lỗi cấu hình!\nKhông tìm thấy bác sĩ nào để tạo hóa đơn !") 
            else:
                self.state = "ChoThanhToan"
                
    def btn_hoan_thanh(self):
        self.state = "HoanThanh"

    benh_nhan_id = fields.Many2one('medical.benh_nhan', 'Bệnh nhân', store=True, required=True)

    bac_si_id = fields.Many2one('medical.bac_si', 'Bác sĩ phụ trách', store=True, required=True, readonly=True)
    
    ngay = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    ngay_sinh = fields.Date('Ngày sinh', compute="_compute_birthday")

    anh_dai_dien = fields.Binary('Ảnh đại diện', related='benh_nhan_id.anh_dai_dien',)
    tuoi = fields.Char('Tuổi', related='benh_nhan_id.tuoi_benh_nhan', store=True)
    dia_chi = fields.Char('Địa chỉ', related='benh_nhan_id.dia_chi')

    gioi_tinh = fields.Selection([('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], "Giới tính", related='benh_nhan_id.gioi_tinh', readonly=True, store=True)

    tinh_trang_hon_nhan = fields.Selection([('DocThan', 'Độc thân'), ('DaCuoi', 'Đã cưới'), ('GoaPhu', 'Góa phụ'), ('LyDi', 'Ly dị'), ('LyThan', 'Ly thân')], "Tình trạng hôn nhân", related='benh_nhan_id.tinh_trang_hon_nhan', readonly=True, store=True)

    nhom_mau = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], "Nhóm máu", related='benh_nhan_id.nhom_mau', readonly=True, store=True)

    rh =  fields.Selection([('+', '+'), ('-', '-')], 'Rh', related='benh_nhan_id.rh', readonly=True,store=True)

    ly_do_kiem_tra = fields.Char('Lý do kiểm tra')

    trieu_chung = fields.Char('Triệu chứng')

    trung_tam_y_te_id = fields.Many2one('medical.trung_tam_y_te', 'Trung tâm y tế', store=True, required=True, readonly=True)

    khoa_id = fields.Many2one('medical.khoa', 'Khoa', domain="[('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]", store=True, required=True, readonly=True)

    phong_id = fields.Many2one('medical.phong', 'Phòng', domain="[('khoa_id', '=', khoa_id), ('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]", store=True)

    vaccine_ids = fields.Many2many(comodel_name='medical.vaccine', relation='medical_phieukhambenh_vaccine', column1='phieu_kham_benh_id', column2='vaccine_id', string='Vắc xin')

    don_thuoc_ids = fields.One2many('medical.don_thuoc', inverse_name='so_thu_tu')
    

    @api.depends('benh_nhan_id')
    def _compute_birthday(self):
        for rec in self:
            if rec.benh_nhan_id:
                rec.ngay_sinh = rec.benh_nhan_id.ngay_sinh
            else: 
                rec.ngay_sinh = ""

    chan_doan = fields.Char('Chẩn đoán')

    binh_luan = fields.Char('Bình luận')

    ngay_tai_kham = fields.Date('Ngày tái khám')
    
    chan_doan_hinh_anh_ids = fields.One2many('medical.chan_doan_hinh_anh', 'phieu_kham_benh_id')

class DonThuoc(models.Model):
    _name = 'medical.don_thuoc'
    _description = 'medical.don_thuoc'
    _order = "create_date desc, id desc"

    name = fields.Char('Đơn thuốc #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('don_thuoc.seq')
        
        record =  super(DonThuoc, self).create(vals)
        return record

    state = fields.Selection([('DuThao', 'Dự thảo'), ('DaGui', 'Đã gửi')], string='Trạng thái', default='DuThao')        

    def btn_gui(self):
        self.state = 'DaGui'

    @api.model
    def write(self, vals):
        if vals.get('state'):
            if vals.get('state') == 'DaGui':
                vals_new_rec = {
                    'benh_nhan_id': self.benh_nhan_id.id,
                    'bac_si_id': self.bac_si_id.id,
                    'nha_thuoc_id': self.nha_thuoc_id.id,
                    'don_thuoc_id': self.id
                }
                self.env['medical.don_thuoc_duoc_dat'].create(vals_new_rec)
        return super(DonThuoc, self).write(vals)
    

    benh_nhan_id = fields.Many2one('medical.benh_nhan', 'Bệnh nhân', store=True, related='so_thu_tu.benh_nhan_id')

    trung_tam_y_te_id = fields.Many2one('medical.trung_tam_y_te', related='so_thu_tu.trung_tam_y_te_id')

    khoa_id = fields.Many2one('medical.khoa', related='so_thu_tu.khoa_id', readonly=True)

    nha_thuoc_id = fields.Many2one('medical.hieu_thuoc', 'Nhà thuốc', domain="[('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]", store=True, required=True)

    bac_si_id = fields.Many2one('medical.bac_si', 'Bác sĩ', store=True, related='so_thu_tu.bac_si_id' )

    ngay_ke_don = fields.Datetime('Ngày kê đơn', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    so_thu_tu = fields.Many2one('medical.phieu_kham_benh', 'Số thứ tự #', readonly=True, store=True)

    chi_tiet_toa_thuoc_ids = fields.One2many(comodel_name='medical.chi_tiet_toa_thuoc', inverse_name='don_thuoc_id')

    def action_confirm_and_print(self):
        raise ValidationError('Tính năng đang bảo trì!')

    don_thuoc_duoc_dat_ids = fields.One2many('medical.don_thuoc_duoc_dat', 'don_thuoc_id')

class ChiTietToaThuoc(models.Model):
    _name = 'medical.chi_tiet_toa_thuoc'
    _description = 'medical.chi_tiet_toa_thuoc'
    _order = "create_date desc, id desc"

    name = fields.Many2one('medical.thuoc_vaccin', 'Thuốc', domain="[('loai_thuoc', '=', 'Thuoc')]", required=True, store=True)

    don_thuoc_id = fields.Many2one('medical.don_thuoc', 'Đơn thuốc', store=True, readonly=True)

    chi_dinh = fields.Char('Chỉ định', related='name.chi_dinh', store=True)

    lieu = fields.Many2one('medical.lieu_thuoc', 'Liều', store=True, required=True)

    donvi_lieuluong = fields.Many2one('medical.donvi_lieuthuoc','Đơn vị liều lường', store=True)

    binh_luan = fields.Char('Bình luận')