from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PrescriptionOrders(models.Model):
    _name = 'medical.prescription_orders'
    _description = 'medical.prescription_orders'

    name = fields.Char('Đơn thuốc #', default='/', readonly=True)
    state = fields.Selection([('draft', 'Dự thảo'), ('validate', 'Xác nhận'), ('waiting_for_invoice', 'Chờ thanh toán'), ('invoiced', 'Đã xuất hoá đơn')], string='Trạng thái', default='draft')
    patient_id = fields.Many2one('medical.patient', 'Bệnh nhân', store=True, required=True, readonly=True)
    doctor_id = fields.Many2one('medical.doctor', 'Bác sĩ phụ trách', store=True, required=True, readonly=True)
    prescription_date = fields.Datetime('Ngày', readonly=False, select=True
                                , default=lambda self: fields.datetime.now())
    health_center_id = fields.Many2one('medical.health_center', related='prescription_id.health_center_id')
    department_id = fields.Many2one('medical.department', related='prescription_id.department_id')
    pharmacies_id = fields.Many2one('medical.pharmacies', 'Nhà thuốc', domain="[('health_center_id', '=', health_center_id)]", store=True, required=True)
    pharmacist_id = fields.Many2one('medical.pharmacist', 'Dược sĩ', store=True)
    prescription_id = fields.Many2one('medical.prescription', 'Đơn thuốc #', store=True, readonly=True)
    prescription_details_ids = fields.One2many(comodel_name='medical.prescription_details', inverse_name='prescription_id', related='prescription_id.prescription_details_ids')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('prescription_orders.seq')

        record =  super(PrescriptionOrders, self).create(vals)
        return record

    def btn_validate(self):
        self.state = 'validate'
    def btn_invoiced(self):
        self.state = 'invoiced'