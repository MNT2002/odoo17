from odoo import fields, models, api


class ConfirmStateWizard(models.TransientModel):
    _name = 'confirm.state.wizard'
    _description = 'Wizard  ghi chu benh nhan'

    ghi_chu = fields.Char('Ghi chú')

    def action_confirm(self):
        benh_nhan_id = self.env.context.get('active_id', False)
        benh_nhan = self.env['medical.benh_nhan'].browse(benh_nhan_id)
        benh_nhan.write({'ghi_chu': self.ghi_chu})
        benh_nhan.btn_da_kham()