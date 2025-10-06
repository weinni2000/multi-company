from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    country_id = fields.Many2one(compute="_compute_country_id", store=True)

    @api.depends("partner_id.country_id")
    def _compute_country_id(self):
        for company in self.filtered(lambda company: company.partner_id):
            address_data = company.partner_id.sudo().address_get(adr_pref=["contact"])
            if address_data["contact"]:
                partner = company.partner_id.browse(address_data["contact"]).sudo()
                company.country_id = partner.country_id
