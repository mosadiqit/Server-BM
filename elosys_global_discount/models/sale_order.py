from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount = fields.Float(
        string=_("Global discount"),
        default=0.0
    )

    @api.onchange('global_discount')
    def onchange_global_discount(self):
        for order in self:
            if order.global_discount:
                for order_line_id in order.order_line:
                    order_line_id.update({
                        'new_discount': order.global_discount,
                    })

    def check_occurrence(self, discounts, discount):
        for d in discounts:
            if d != discount:
                return False
        return True

    @api.onchange('order_line')
    def onchange_order_line(self):
        for order in self:
            if not order.check_occurrence(order.order_line.mapped('new_discount'), order.global_discount):
                order.global_discount = 0.0

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    new_discount = fields.Float(
        string=_('Discount'),
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    latest_discount = fields.Float(
        string=_('Discount'),
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    @api.model
    def create(self, vals):
        line_id = super(SaleOrderLine, self).create(vals)

        if not line_id.new_discount and line_id.order_id.global_discount:
            line_id.write({
                'new_discount': line_id.order_id.global_discount,
            })

        if not line_id.discount and line_id.new_discount:
            line_id.write({
                'discount': line_id.discount + line_id.new_discount
            })

        if not line_id.latest_discount and line_id.discount:
            line_id.write({
                'latest_discount': line_id.discount
            })

        return line_id

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)

        if 'new_discount' in vals:
            for line in self:
                line.write({'discount': line.discount - line.latest_discount + line.new_discount})

        if 'discount' in vals:
            for line in self:
                line.write({'latest_discount': line.new_discount})

        return res