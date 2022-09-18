from odoo import fields, models


class BankCards(models.Model):
    _name = 'bank.clients.card'
    _description = 'Clients card'

    name = fields.Char(required=True)
    clients_ids = fields.One2many('bank.clients', 'card_id')
    sequence  = fields.Integer('Sequence')


    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'The type name must be unique.'),
    ]