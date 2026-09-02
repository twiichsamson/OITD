from odoo import api, models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"), 
            ("refused", "Refused")
        ],  
        copy=False,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            start = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(start, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - start).days
