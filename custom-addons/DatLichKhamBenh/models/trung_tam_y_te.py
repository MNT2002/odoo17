from odoo import fields, models, api

from odoo.exceptions import ValidationError

class TrungTamYTe(models.Model):
    _name = 'medical.trung_tam_y_te'
    _description = 'Trung tâm y tế model'

    name = fields.Char('Tên trung tâm y tế', required=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()

        record = super(TrungTamYTe, self).create(vals)
        return record

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    parent_id = fields.Many2one('medical.trung_tam_y_te')

    is_headquarter = fields.Boolean('Trụ sở chính', readonly=True)

    dia_chi = fields.Char('Địa chỉ')

    dia_chi_2 = fields.Char('')

    thanh_pho = fields.Char('Thành phố')

    zip = fields.Char('Mã bưu điện')

    country_id_new = fields.Many2one('res.country', string="Quốc gia", required=True)

    state_id_new = fields.Many2one('res.country.state', string="Tỉnh/Thành phố", store=True, require=True, domain="[('country_id', '=', country_id_new)]")

    website_link = fields.Char('Website Link')

    so_dien_thoai = fields.Char('Điện thoại')

    email = fields.Char('Email')

    thong_tin_bo_sung = fields.Char('Thông tin bổ sung')
    
    khoa_ids = fields.One2many(comodel_name='medical.khoa', inverse_name='trung_tam_suc_khoe_id')
    khoa_count = fields.Integer('Khoa', compute="get_count_khoa", store=True)

    @api.depends('khoa_ids')
    def get_count_khoa(self):
        for rec in self:
            rec.khoa_count =  len(rec.khoa_ids)
    
    phong_ids_t = fields.One2many(comodel_name='medical.phong', inverse_name='trung_tam_suc_khoe_id')
    phong_count_t = fields.Integer('Phòng', compute="get_count_phong_t", store=True)

    @api.depends('phong_ids_t')
    def get_count_phong_t(self):
        for rec in self:
            rec.phong_count_t =  len(rec.phong_ids_t)


class Khoa(models.Model):
    _name = 'medical.khoa'
    _description = 'Khoa'

    name = fields.Char('Tên khoa', required=True)

    state = fields.Selection([('CoPhong', 'Có phòng'), ('KhongCoSan', 'Không có sẵn')], default='CoPhong', compute="_compute_khoa_state",)

    trung_tam_suc_khoe_id = fields.Many2one('medical.trung_tam_y_te', string="Trung tâm sức khoẻ", store=True, required=True)

    so_tang = fields.Integer('Số tầng')

    loai = fields.Selection([('BinhThuong', 'Bình thường'), ('HinhAnh', 'Hình ảnh'), ('PhongXetNghiem', 'Phòng xét nghiệm')])

    truy_cap_dien_thoai = fields.Boolean('Truy cập điện thoại')

    phong_tam_rieng = fields.Boolean('Phòng tắm riêng')

    ti_vi = fields.Boolean('Ti-vi')

    tu_lanh = fields.Boolean('Tủ lạnh')

    dieu_hoa_khong_khi = fields.Boolean('Điều hoà không khí')

    giuong_sofa_cho_khach = fields.Boolean('Giường sofa cho khách')

    truy_cap_internet = fields.Boolean('Truy cập Internet')

    lo_vi_song = fields.Boolean('Lò vi sóng')

    thong_tin_bo_sung = fields.Char('Thông tin bổ sung')

    phong_ids = fields.One2many(comodel_name='medical.phong', inverse_name='khoa_id')
    phong_count = fields.Integer('Phòng', compute="get_count_phong", store=True)

    bac_si_ids = fields.One2many('medical.bac_si', 'khoa_id')
    bac_si_count = fields.Integer('Đơn thuốc', compute="get_count_bac_si")

    @api.depends('bac_si_ids')
    def get_count_bac_si(self):
        for rec in self:
            rec.bac_si_count =  len(rec.bac_si_ids)

    don_thuoc_ids = fields.One2many('medical.don_thuoc', 'khoa_id')
    don_thuoc_count = fields.Integer('Đơn thuốc', compute="get_count_don_thuoc")

    @api.depends('don_thuoc_ids')
    def get_count_don_thuoc(self):
        for rec in self:
            rec.don_thuoc_count =  len(rec.don_thuoc_ids)

    phieu_kham_benh_ids = fields.One2many('medical.phieu_kham_benh', 'khoa_id')
    phieu_kham_benh_count = fields.Integer('Phiếu khám bệnh', compute="get_count_phieu_kham_benh")

    @api.depends('phieu_kham_benh_ids')
    def get_count_phieu_kham_benh(self):
        for rec in self:
            rec.phieu_kham_benh_count =  len(rec.phieu_kham_benh_ids)

    chan_doan_hinh_anh_ids = fields.One2many('medical.chan_doan_hinh_anh', 'khoa_id')
    chan_doan_hinh_anh_count = fields.Integer('Chẩn đoán hình ảnh', compute="get_count_chan_doan_hinh_anh")

    @api.depends('chan_doan_hinh_anh_ids')
    def get_count_chan_doan_hinh_anh(self):
        for rec in self:
            rec.chan_doan_hinh_anh_count =  len(rec.chan_doan_hinh_anh_ids)
    
    def btn_trong(self):
        self.state = "CoPhong"
    def btn_khong_co_san(self):
        self.state = "KhongCoSan"

    @api.depends('phong_ids')
    def get_count_phong(self):
        for rec in self:
            rec.phong_count =  len(rec.phong_ids)

    @api.depends("phong_ids.state")
    def _compute_khoa_state(self):
        for rec in self:
            if any(phong.state == 'Trong' for phong in rec.phong_ids):
                rec.state = "CoPhong"
            else:
                rec.state = "KhongCoSan"

    def action_tao_phieu_kham_benh_moi(self):
        # action['domain'] = {'bac_si_id': [('id', 'in', self.bac_si_ids)]}
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Phiếu khám bệnh',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.phieu_kham_benh',
            'target': 'current',
            'context': {
                'default_trung_tam_y_te_id': self.trung_tam_suc_khoe_id.id,
                'default_khoa_id': self.id
            }
        }
    def action_tao_chan_doan_hinh_anh_moi(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chẩn đoán hình ảnh',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.chan_doan_hinh_anh',
            'target': 'current',
            'context': {
                'default_khoa_id': self.id
            }
        }
    def btn_so_luong_phieu_kham_benh(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Phiếu khám bệnh',
            'view_type': 'form,kanban,tree,calendar',    
            'view_mode': 'kanban,tree,calendar,form',
            'res_model': 'medical.phieu_kham_benh',
            'context': {
                'default_trung_tam_y_te_id': self.trung_tam_suc_khoe_id.id,
                'default_khoa_id': self.id
            },
            'domain': [('khoa_id', '=', self.id)]
        }
    def btn_so_luong_chan_doan_hinh_anh(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chẩn đoán hình ảnh',
            'view_type': 'form,tree',
            'view_mode': 'tree,form',
            'res_model': 'medical.chan_doan_hinh_anh',
            'context': {
                'default_trung_tam_y_te_id': self.trung_tam_suc_khoe_id.id,
                'default_khoa_id': self.id
            },
            'domain': [('khoa_id', '=', self.id)]
        }
    def btn_so_luong_don_thuoc(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đơn thuốc',
            'view_type': 'form,tree',
            'view_mode': 'tree,form',
            'res_model': 'medical.don_thuoc',
            'context': {
                'default_trung_tam_y_te_id': self.trung_tam_suc_khoe_id.id,
                'default_khoa_id': self.id
            },
            'domain': [('khoa_id', '=', self.id)]
        }
    def btn_so_luong_bac_si(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bác sĩ',
            'view_type': 'kanban,form,tree',
            'view_mode': 'kanban,tree,form',
            'res_model': 'medical.bac_si',
            'context': {
                'default_trung_tam_y_te_id': self.trung_tam_suc_khoe_id.id,
                'default_khoa_id': self.id
            },
            'domain': [('khoa_id', '=', self.id)]
        }
    
    yeu_thich = fields.Boolean(default=False)
    
    def toggle_favorite(self):
        self.yeu_thich = self.yeu_thich == False

class Phong(models.Model):
    _name = 'medical.phong'
    _description = 'medical.phong'

    name = fields.Char('Tên phòng', required=True)

    state = fields.Selection([('Trong', 'Trống'), ('KhongCoSan', 'Không có sẵn')], default='Trong')
    
    def btn_trong(self):
        self.state = "Trong"
    def btn_khong_co_san(self):
        self.state = "KhongCoSan"

    trung_tam_suc_khoe_id = fields.Many2one('medical.trung_tam_y_te', string="Trung tâm sức khoẻ", store=True, required=True)

    khoa_id = fields.Many2one('medical.khoa', string="Khoa", store=True, domain="[('trung_tam_suc_khoe_id', '=', trung_tam_suc_khoe_id)]")

    thong_tin_bo_sung = fields.Char('Thông tin bổ sung')
        
class HieuTHuoc(models.Model):
    _name = "medical.hieu_thuoc"
    _description = "medical.hieu_thuoc"

    name = fields.Char('Tên hiệu thuốc')

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    trung_tam_suc_khoe_id = fields.Many2one('medical.trung_tam_y_te', string="Trung tâm sức khoẻ", store=True, required=True)

    dia_chi = fields.Char('Địa chỉ')

    dia_chi_2 = fields.Char('')

    thanh_pho = fields.Char('Thành phố')

    zip = fields.Char('Mã bưu điện')

    country_id_new = fields.Many2one('res.country', string="Quốc gia", required=True)

    state_id_new = fields.Many2one('res.country.state', string="Tỉnh/Thành phố", store=True, required=True, domain="[('country_id', '=', country_id_new)]")

    website_link = fields.Char('Website Link')

    so_dien_thoai = fields.Char('Điện thoại')

    email = fields.Char('Email')

    thong_tin_bo_sung = fields.Char('Thông tin bổ sung')

class ChuyenMon(models.Model):
    _name = 'medical.chuyen_mon'
    _description = 'medical.chuyen_mon'

    name = fields.Char('Mô tả', required=True)

    ma = fields.Char('Mã')

class TrinhDoBangCap(models.Model):
    _name = 'medical.trinhdo_bangcap'
    _description = 'medical.trinhdo_bangcap'

    name = fields.Char('Trình độ', required=True)

    ho_va_ten = fields.Char('Họ và tên', required=True)

class Thuoc_vaccine(models.Model):
    _name = 'medical.thuoc_vaccin'
    _description = 'medical.thuoc_vaccin'

    name = fields.Char('Tên thuốc', translate=True, required=True)

    loai_thuoc = fields.Selection([('Thuoc', 'Thuốc'), ('Vaccine', 'Vaccine')], 'Loại thuốc', required=True,)

    gia_ban = fields.Integer('Giá bán')

    hieu_qua_dieu_tri = fields.Char('Hiệu quả điều trị')

    canh_bao_mang_thai = fields.Boolean('Cảnh bảo mang thai')

    so_luong_hien_co = fields.Integer('Số lượng hiện có', default=0, readonly=True)

    thong_tin_them = fields.Char('Thông tin thêm')

    mang_thai_va_cho_con_bu = fields.Char('Mang thai và cho con bú')

    thanh_phan = fields.Char('Thành phần')

    huong_dan_lieu_luong = fields.Char('Hướng dẫn sử dụng liều lượng')

    phan_ung_bat_loi = fields.Char('Phản ứng bất lợi')

    chi_dinh = fields.Char('Chỉ định')

    qua_lieu = fields.Char('Quá liều')

    dieu_kien_bao_quan = fields.Char('Điều kiện bảo quản')

class DonViLieuThuoc(models.Model):
    _name = 'medical.donvi_lieuthuoc'
    _description = 'medical.donvi_lieuthuoc'

    name = fields.Char('Đơn vị', required=True)

    mo_ta = fields.Char('Mô tả')
class LieuThuoc(models.Model):
    _name = 'medical.lieu_thuoc'
    _description = 'medical.lieu_thuoc'

    name = fields.Char('Tần số', required=True)

    ma = fields.Integer('Mã')

    viet_tat = fields.Char('Viết tắt')

class Vaccine(models.Model):
    _name = 'medical.vaccine'
    _description = 'medical.vaccine'

    name = fields.Many2one('medical.thuoc_vaccin', 'Vaccine', domain="[('loai_thuoc', '=', 'Vaccine')]", required=True, store=True)

    benh_nhan_id = fields.Many2one('medical.benh_nhan', 'Bệnh nhân', required=True, store=True)

    bac_si_id = fields.Many2one('medical.bac_si', 'Bác sĩ', required=True, store=True)

    lieu = fields.Integer('Liều', default=1)

    ngay = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    trung_tam_y_te_id = fields.Many2one('medical.trung_tam_y_te', 'Nơi thực hiện', store=True)

    quan_sat_theo_doi = fields.Char('Quan sát/Theo dõi')

class DonViXetNghiem(models.Model):
    _name = 'medical.don_vi_xet_nghiem'
    _description = 'medical.don_vi_xet_nghiem'

    name = fields.Char('Tên đơn vị')

    ma = fields.Char('Mã')

class LoaiXetNghiem(models.Model):
    _name = 'medical.loai_xet_nghiem'
    _description = 'medical.loai_xet_nghiem'

    name = fields.Char('Tên xét nghiệm', required=True)

    ma = fields.Char('Mã')

    phi_xet_nghiem = fields.Integer('Phí xét nghiệm')

    truong_hop_xet_nghiem_ids = fields.One2many('medical.truong_hop_xet_nghiem', 'loai_xet_nghiem_id')

    thong_tin_them = fields.Char('Thông tin thêm')

class TruongHopXetNghiem(models.Model):
    _name = 'medical.truong_hop_xet_nghiem'
    _description = 'medical.truong_hop_xet_nghiem'
    
    name = fields.Char('Xét nghiệm', required=True)

    ma_thu_tu = fields.Integer('Mã thứ tự')

    pham_vi_binh_thuong = fields.Text('Phạm vi bình thường')

    don_vi = fields.Many2one('medical.don_vi_xet_nghiem', 'Đơn vị')

    loai_xet_nghiem_id = fields.Many2one('medical.loai_xet_nghiem', 'Loại xét nghiệm')

class LoaiChuanDoanHinhAnh(models.Model):
    _name = 'medical.loai_chan_doan_hinh_anh'
    _description = 'medical.loai_chan_doan_hinh_anh'
    
    name = fields.Char('Tên', required=True)

    ma = fields.Char('Mã')

    phi_xet_nghiem = fields.Integer('Phí xét nghiệm')

    thong_tin_them = fields.Char('Thông tin thêm')

class ChanDoanHinhAnh(models.Model):
    _name = 'medical.chan_doan_hinh_anh'
    _description = 'Chẩn đoán hình ảnh'
    
    name = fields.Char('Số xét nghiệm #', required=True, default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('chan_doan_hinh_anh.seq')

        record =  super(ChanDoanHinhAnh, self).create(vals)
        return record


    state = fields.Selection([('DuThao', 'Dự thảo'),('DaXuatHoaDon', 'Đã xuất hoá đơn'), ('DangThucHien', 'Đang thực hiện'), ('HoanThanh', 'Hoàn thành')], 'Trạng thái', default='DuThao')

    loai_chan_doan = fields.Many2one('medical.loai_chan_doan_hinh_anh', 'Loại chẩn đoán', store=True, required=True)

    identification_code = fields.Char('Mã bệnh nhân',related='benh_nhan_id.identification_code', readonly=True)

    benh_nhan_id = fields.Many2one('medical.benh_nhan', 'Bệnh nhân', store=True, related='phieu_kham_benh_id.benh_nhan_id')

    ngay_yeu_cau = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())

    ngay_sinh = fields.Date('Ngày sinh', related='benh_nhan_id.ngay_sinh',)

    gioi_tinh = fields.Selection([('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], "Giới tính", related='benh_nhan_id.gioi_tinh')

    bac_si_id = fields.Many2one('medical.bac_si','Bác sĩ', store=True, related='phieu_kham_benh_id.bac_si_id')

    phieu_kham_benh_id = fields.Many2one('medical.phieu_kham_benh', 'Phiếu khám bệnh', required=True, domain="[('khoa_id', '=', khoa_id)]")

    khoa_id = fields.Many2one('medical.khoa' , 'Khoa',store=True, related='phieu_kham_benh_id.khoa_id')

    ngay_phan_tich = fields.Datetime('Ngày phân tích', select=True)

    anh_1 = fields.Binary('Ảnh 1')
    anh_2 = fields.Binary('Ảnh 2')
    anh_3 = fields.Binary('Ảnh 3')
    anh_4 = fields.Binary('Ảnh 4')
    anh_5 = fields.Binary('Ảnh 5')
    anh_6 = fields.Binary('Ảnh 6')

    phan_tich = fields.Char('Phân tích')

    ket_luan = fields.Char('Kết luận')

    vat_tu_tieu_hao_ids = fields.One2many('medical.vat_tu_tieu_hao', 'chan_doan_hinh_anh_id')

    def btn_tao_hoa_don_chan_doan(self):
        self.state = 'DaXuatHoaDon'
    def btn_bat_dau_chan_doan(self):
        self.state = 'DangThucHien'
        current_dt = fields.datetime.now()
        self.ngay_phan_tich = current_dt
    def btn_hoan_thanh_chan_doan(self):
        self.state = 'HoanThanh'
    def in_chan_doan_hinh_anh(self):
        raise ValidationError('Tính năng đang bảo trì!')

class VatTuTieuHao(models.Model):
    _name = 'medical.vat_tu_tieu_hao'
    _description = 'medical.vat_tu_tieu_hao'
    
    ma_thu_tu = fields.Integer('Mã thứ tự', default=lambda self: self.env['ir.sequence'].next_by_code('vat_tu_tieu_hao.seq'))

    san_pham = fields.Char('Sản phẩm', required=True)

    so_luong = fields.Integer('Số lượng', default='1')

    don_vi = fields.Char('Đơn vị')

    chan_doan_hinh_anh_id = fields.Many2one('medical.chan_doan_hinh_anh', 'Chẩn đoán hình ảnh', store=True)


class ThoiGianKhamBenh(models.Model):
    _name = 'medical.thoi_gian_kham_benh'
    _description = 'medical.thoi_gian_kham_benh'

    name = fields.Float('Thời gian khám (Định dạng 24 giờ)')

    description = fields.Char('Mô tả')

    state = fields.Selection([('empty', 'Trống'), ('booked', 'Đã đặt')], default="empty")

    time =  fields.Float('Thời lượng', default='1')

class ExaminationTime(models.Model):
    _name = 'medical.examination_time'
    _description = 'medical.examination_time'

    name = fields.Float('Thời gian khám (Định dạng 24 giờ)')

    description = fields.Char('Mô tả')

    state = fields.Selection([('empty', 'Trống'), ('booked', 'Đã đặt')], default="empty")

    time =  fields.Float('Thời lượng (1 giờ)', default='1')

class Shift(models.Model):
    _name = 'medical.shift'
    _description = 'medical.shift'

    name = fields.Selection([('Sáng', 'Sáng'), ('Tối', 'Tối')], 'Ca làm việc')

    description = fields.Char('Mô tả')

    time = fields.Many2many('medical.examination_time', 'shift_time_rel', 'shift', 'examination', 'Thời gian khám bệnh')