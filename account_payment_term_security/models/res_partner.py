# Copyright 2023.2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        group = "account_payment_term_security.account_payment_term_mgmt"
        if view_type == "form" and not self.env.user.has_group(group):
            doc = etree.XML(result["arch"])
            for node in doc.xpath("//field[@name='property_payment_term_id']"):
                node.set("readonly", "1")
                node.set("force_save", "1")
            for node in doc.xpath("//field[@name='property_supplier_payment_term_id']"):
                node.set("readonly", "1")
                node.set("force_save", "1")
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result
