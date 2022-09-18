from odoo import api, fields, models

class BankCredits(models.Model):
    _name = 'bank.clients.credits'
    _description = 'Bank clients credits module'

    bank_id = fields.Many2one('bank.clients', required=True)
    percent = fields.Selection(string="Процентная ставка", required=True, selection=[
        ('9', '9%'), ('12', '12%'), ('14', '14%'), ('16', '16%')], default='12')
    credit_amount = fields.Integer(string="Сумма кредита", required=True)
    credit_type = fields.Selection(string="Типа кредита", required=True, selection=[
        ('mortgage', 'Ипотека'), ('consumer', 'Потребительский'), ('car_credit', 'Кредит на авто')])

    _sql_constraints = [
        ('check_credit_amount', 'CHECK(credit_amount > 0)',
         'Сумма кредита не может быть отрицательной')
    ]

