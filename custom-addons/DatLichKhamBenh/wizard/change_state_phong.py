from odoo import fields, models, api


class ChangeStatePhongWizard(models.TransientModel):
    _name = 'change.state_phong.wizard'
    _description = 'Wizard to change the state of a "phong"'

    def action_change(self):
        phong_id = self.env.context.get('active_id', False)
        phong = self.env['medical.phong'].browse(phong_id)
        phong.btn_co_phong()