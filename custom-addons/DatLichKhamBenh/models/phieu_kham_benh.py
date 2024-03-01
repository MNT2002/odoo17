from odoo import fields, models, api
from odoo.exceptions import ValidationError

class PhieuKhamBenh(models.Model):
    _name = 'medical.phieu_kham_benh'
    _description = 'medical.phieu_kham_benh'

    name = fields.Char('Số thứ tự #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('phieu_kham_benh.seq')
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

    bac_si_id = fields.Char('Bác sĩ phụ trách', readonly=True)
    
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

    trung_tam_y_te_id = fields.Many2one('medical.trung_tam_y_te', 'Trung tâm y tế', store=True)

    khoa_id = fields.Many2one('medical.khoa', 'Khoa', domain="[('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]", store=True)

    phong_id = fields.Many2one('medical.phong', 'Phòng', domain="[('khoa_id', '=', khoa_id), ('trung_tam_suc_khoe_id', '=', trung_tam_y_te_id)]", store=True)

    vaccine_ids = fields.Many2many(comodel_name='medical.thuoc_vaccin', relation='medical_phieukhambenh_vaccine', column1='phieu_kham_benh_id', column2='vaccine_id', string='Vắc xin')
    

    @api.depends('benh_nhan_id')
    def _compute_birthday(self):
        for rec in self:
            if rec.benh_nhan_id:
                rec.ngay_sinh = rec.benh_nhan_id.ngay_sinh
            else: 
                rec.ngay_sinh = ""
