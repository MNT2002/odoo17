from odoo import models, fields


class PeopleRelational(models.Model):
    _name = 'people_relational'
    _description = 'People Relational'

    name = fields.Char(string='Name')

    # One2many field
    house_ids = fields.One2many(comodel_name='house', inverse_name='people_id', string='House', limit=2)
