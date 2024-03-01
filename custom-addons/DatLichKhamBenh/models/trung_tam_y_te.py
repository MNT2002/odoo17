from odoo import fields, models, api



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

    state_id_new = fields.Many2one('res.country.state', string="Tỉnh/Thành phố", store=True, require=True, domain="[('country_id', '=', country_id_new)]")

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
    
class DonThuoc(models.Model):
    _name = 'medical.don_thuoc'
    _description = 'medical.don_thuoc'

    name = fields.Char('Số thứ tự #', default='/', readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('phieu_kham_benh.seq')
        record =  super(PhieuKhamBenh, self).create(vals)
        return record