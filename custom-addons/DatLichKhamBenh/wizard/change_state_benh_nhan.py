from odoo import fields, models, api


class ChangeStateBenhNhanWizard(models.TransientModel):
    _name = 'change.state_benh_nhan.wizard'
    _description = 'Wizard to change the state of a "benh nhan"'

    ghi_chu = fields.Char('Ghi chú')

    def action_change(self):
        benh_nhan_id = self.env.context.get('active_id', False)
        benh_nhan = self.env['medical.benh_nhan'].browse(benh_nhan_id)
        benh_nhan.write({'ghi_chu': self.ghi_chu})
        benh_nhan.btn_da_kham()