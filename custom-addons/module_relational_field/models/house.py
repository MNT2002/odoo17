from odoo import models, fields


class House(models.Model):
    _name = 'house'
    _description = 'House'

    name = fields.Char(string='Name')

    # Many2one field
    people_id = fields.Many2one('people_relational', string='Owner', ondelete='restrict')

    # Many2many field
    # people_ids = fields.Many2many('people_relational', string='People Relational')
