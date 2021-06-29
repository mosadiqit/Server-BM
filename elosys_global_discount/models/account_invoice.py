# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.addons import decimal_precision as dp

import logging

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    global_discount = fields.Float(
        string=_("Global discount"),
        default=0.0
    )

    @api.constrains('origin')
    def update_global_discount(self):
        for invoice in self:
            if invoice.origin:
                sale = self.env['sale.order'].search([('name','=',invoice.origin)])
                invoice.write({'global_discount':sale.global_discount})

    @api.onchange('global_discount')
    def onchange_global_discount(self):
        for invoice in self:
            if invoice.global_discount:
                for invoice_line_id in invoice.invoice_line_ids:
                    invoice_line_id.update({
                        'new_discount': invoice.global_discount,
                    })

    def check_occurrence(self, discounts, discount):
        for d in discounts:
            if d != discount:
                return False
        return True

    @api.onchange('invoice_line_ids')
    def onchange_invoice_line_ids(self):
        for invoice in self:
            if not invoice.check_occurrence(invoice.invoice_line_ids.mapped('new_discount'), invoice.global_discount):
                invoice.global_discount = 0.0

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    new_discount = fields.Float(
        string=_('Disc (%)'),
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    latest_discount = fields.Float(
        string=_('Disc (%)'),
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    @api.model
    def create(self, vals):
        line_id = super(AccountInvoiceLine, self).create(vals)

        if not line_id.new_discount and line_id.invoice_id.global_discount:
            line_id.write({
                'new_discount': line_id.invoice_id.global_discount,
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
        res = super(AccountInvoiceLine, self).write(vals)

        if 'new_discount' in vals:
            for line in self:
                line.write({'discount': line.discount - line.latest_discount + line.new_discount})

        if 'discount' in vals:
            for line in self:
                line.write({'latest_discount': line.new_discount})

        return res
