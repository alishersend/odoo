from odoo import api, models, fields
from datetime import date, datetime, timedelta


class Deposits(models.Model):
    _name = 'bank.clients.deposits'
    _description = 'model for deposits'

    name = fields.Char(string='Название депозита')
    date_of_create = fields.Date(required=True, string='Дата создания депозита', default=datetime.today())
    date_of_end = fields.Date(string='Дата окончания депозита', required=True, default=lambda self: datetime.today() + timedelta(365))
    amount = fields.Integer(string='Накопленная сумма', default=0)
    percent = fields.Selection(required=True, string='Процентная ставка', selection=[
        ('10', '10%'), ('12', '12%'), ('15', '15%')], default='10')
    bank_user_id = fields.Many2one('bank.clients', required=True)
    valid = fields.Selection(selection=[('valid', 'Активен'), ('notvalid', 'Неактивен')])

    _sql_constraints = [
        ('check_amount', 'CHECK(amount > -1)',
         'Сумма накопления не может быть отрицательной')
    ]

    @api.onchange('bank_user_id')
    def action_confirm(self):
        self.valid = 'valid'

    def action_cancel(self):
        self.valid = 'notvalid'
