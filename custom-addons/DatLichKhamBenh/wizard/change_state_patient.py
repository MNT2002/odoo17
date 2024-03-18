from odoo import fields, models, api


class ChangeStatePatientWizard(models.TransientModel):
    _name = 'change.state_patient.wizard'
    _description = 'Wizard to change the state of a "benh nhan"'

    note = fields.Char('Ghi chú')

    def action_change(self):
        patient_id = self.env.context.get('active_id', False)
        patient = self.env['medical.patient'].browse(patient_id)
        patient.write({'note': self.note})
        patient.btn_da_kham()