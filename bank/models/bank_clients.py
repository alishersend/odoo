from odoo import fields, models, api
from datetime import datetime, timedelta, date


class BankClient(models.Model):
    _name = 'bank.clients'
    _description = 'Bank clients module'

    name = fields.Char(string='ФИО', required=True)
    description = fields.Text(string='Описание')
    image = fields.Image()
    age = fields.Integer(string='Возраст', required=True)
    born_city = fields.Selection(string='Место рождения', required=True, selection=[
        ('capital', 'Нур-Султан'),
        ('almaty', 'Алматы'),
        ('shymkent', 'Шымкент'),
        ('abay', 'Абайская область'),
        ('akmola', 'Акмолинская область'),
        ('aktobe', 'Актюбинская область'),
        ('almatyobl', 'Алматинская область'),
        ('atyrau', 'Атырауская область'),
        ('VKO', 'Восточно-Казахстанская область'),
        ('zhambyl', 'Жамбылская область'),
        ('zhetysu', 'Жетысуская область'),
        ('ZKO', 'Западно-Казахстанская область'),
        ('karaganda', 'Карагандинская область'),
        ('kostanay', 'Костанайская область'),
        ('kyzylorda', 'Кызылординская область'),
        ('mangistau', 'Мангистауская область'),
        ('pavlodar', 'Павлодарская область'),
        ('SKO', 'Северо-Казахстанская область'),
        ('turkestan', 'Туркестанская область'),
        ('ulytau', 'Улытауская область')])
    passport_number = fields.Char(string='Номер документа', required=True)
    user_id = fields.Many2one('res.users', string='Менеджер', default=lambda self: self.env.user)
    passport = fields.Char(string='ИИН', required=True)
    passport_date = fields.Date(string='Дата выдачи документа', required=True)
    passport_end_date = fields.Date(string='Дата окончания документа', required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[
        ('new', 'Клиент'),
        ('product', 'Имеет продукт банка')], default='new')
    phone = fields.Char(required=True, string='Номер телефона /+7', default='7')
    email = fields.Char(string='Email')
    deposit = fields.Boolean()
    deposit_ids = fields.One2many("bank.clients.deposits", "bank_user_id", string="Депозиты")
    credit = fields.Boolean()
    credit_active = fields.Boolean()
    credit_ids = fields.One2many('bank.clients.credits', 'bank_id', string='Кредиты')
    card_id = fields.Many2one('bank.clients.card', string='Карта клиента')

    _sql_constraints = [
        ('check_passport', "CHECK(char_length(passport) = 12 and passport ~ '^\d+(\.\d+)?$')",
         'Некорректный ИИН.'),
        ('check_passport_number', "CHECK(char_length(passport_number) = 9 and passport_number ~ '^\d+(\.\d+)?$')",
         'Некорректный номер документа.'),
        ('check_phone', "CHECK(char_length(phone) = 10 and phone ~ '^\d+(\.\d+)?$')",
         'Некорректный номер телефона.'),
    ]

    @api.onchange('passport_date')
    def _onchange_date(self):
        for rec in self:
            rec.passport_end_date = rec.passport_date

    @api.onchange('deposit')
    def _onchange_state(self):
        self.state = 'product'

    @api.onchange('age')
    def active_credit(self):
        if self.age > 20:
            self.credit_active = True
        else:
            self.credit_active = False
