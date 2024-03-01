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

    identification_code = fields.Char('ID của bệnh nhân', readonly=True)

    anh_dai_dien = fields.Binary("Ảnh đại diện")

    tuoi_benh_nhan = fields.Char('Tuổi bệnh nhân', compute='_compute_age', store=True)

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
                years_calc = (ngay_hien_tai - start).days / 365
                days_calc = (ngay_hien_tai - start).days % 365
                str_years = str(int(years_calc)) + ' tuổi'
                str_days = str(days_calc) + ' ngày'
                if years_calc > 0.0:
                    rec.tuoi_benh_nhan = " ".join([str_years, str_days])
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

    state = fields.Selection([('DangCho', 'Đang Chờ'), ('DaKham', 'Đã Khám')], string='Trạng thái', default='DangCho')

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

    ghi_chu = fields.Char('Ghi chú')

    #Lifestyle page
    tap_the_duc = fields.Boolean('Tập thể dục')
    so_phut_mot_ngay = fields.Integer('Phút / ngày')

    ngu_vao_ban_ngay = fields.Boolean('Ngủ vào ban ngày')
    gio_ngu = fields.Integer('Giỡ ngủ')

    bua_an_mot_ngay = fields.Integer('Bữa ăn / ngày')
    an_mot_minh = fields.Boolean('Ăn một mình')
    ca_phe = fields.Boolean('Cà phê')
    so_ly_mot_ngay = fields.Integer('Ly / ngày')

    nuoc_giai_khat = fields.Boolean('Nước giải khát (đường)')
    muoi = fields.Boolean('Muối')
    trong_che_do_an_kieng = fields.Boolean('Trong chế độ ăn kiêng')
    thong_tin_che_do_an = fields.Char('Thông tin về chế độ ăn uống')

    hut_thuoc = fields.Boolean('Hút thuốc')
    tung_hut_thuoc = fields.Boolean('Từng hút thuốc')
    tuoi_bat_dau_hut_thuoc = fields.Integer('Tuổi bắt đầu hút thuốc')
    dieu_thuoc_mot_ngay = fields.Integer('Điếu thuốc một ngày')
    nguoi_hut_thuoc_thu_dong = fields.Boolean('Người hút thuốc thụ động')
    tuoi_bo_thuoc = fields.Integer('Tuổi bỏ thuốc')

    uong_ruou_bia = fields.Boolean('Uống rượu / bia')
    tuoi_bat_dau_uong = fields.Integer('Tuổi bắt đầu uống')
    bia_tren_ngay = fields.Integer('Bia / ngày')
    ruou_tren_ngay = fields.Integer('Rượu / ngày')
    tung_uong_ruou_bia = fields.Boolean('Từng uống rượu / bia')
    thang_gan_nhat_uong_ruou = fields.Integer('Tháng gần nhất uống rượu / bia')
    tuoi_bo_ruou = fields.Integer('Tuổi bỏ rượu / bia')

    su_dung_thuoc_kich_thich = fields.Boolean('Sử dụng thuốc kích thích')
    tuoi_bat_dau_dung_thuoc_kich_thich = fields.Integer('Tuổi bắt đầu sử dụng thuốc')
    loai_thuoc_hay_dung = fields.Selection([('MaTuy', 'Ma tuý'), ('Heroin', 'Heroin'), ('Nicotin', 'Nicotin')],'Loại thuốc kích thích hay dùng',)
    tung_nghien_thuoc = fields.Boolean('Từng nghiện thuốc')
    tuoi_bo_thuoc_kich_thich = fields.Integer('Tuổi bỏ thuốc kích thích')

    chay_xe_may = fields.Boolean('Chạy xe máy')
    doi_non_bao_hiem = fields.Boolean('Đội nón bảo hiểm')
    tuan_thu_luat_giao_thong = fields.Boolean('Tuân thủ luật giao thông')
    sua_xe = fields.Boolean('Sửa xe')
    chay_xe_oto = fields.Boolean('Chạy xe ô tô')
    that_day_an_toan = fields.Boolean('Thắt dây an toàn')

    vaccine_ids = fields.One2many(comodel_name='medical.vaccine', inverse_name='benh_nhan_id')
    vaccine_count = fields.Integer('Vaccine', compute="get_count_vaccine", store=True)

    @api.depends('vaccine_ids')
    def get_count_vaccine(self):
        for rec in self:
            rec.vaccine_count =  len(rec.vaccine_ids)

    phieu_kham_benh_ids = fields.One2many(comodel_name='medical.phieu_kham_benh', inverse_name='benh_nhan_id')