from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def check_duplicated_products(self):
        if self.env.user.has_group("sale_order_duplicate_product_warning.group_manage_prices"):
            if len(self.order_line) != len(self.order_line.mapped('product_id')):
                aux = set()
                duplicated_products = []
                for line in self.order_line:
                    if line.product_id in aux:
                        duplicated_products.append(line.product_id)
                    else:
                        aux.add(line.product_id)
                duplicated_products = map(lambda l: l.name, duplicated_products)
                warning_message = _("vous avez ajouté l’article(s) " + ",".join(duplicated_products) + " en double")
                return {'warning': {
                    'title': 'Warning',
                    'message': (warning_message),
                }}
