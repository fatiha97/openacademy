# -*- coding: utf-8 -*-
from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('openacademy.session',string="Attended Sessions", readonly=True)
    invoice_count = fields.Integer(string="count invoice", compute="_compute_invoice_count")



    def _compute_invoice_count(self):#?????
        self.invoice_count = self.env['account.move'].search_count([('partner_id', '=', self.id)])
    def facturer(self):
        # self.button_clicked = True
        # data= les donnes envoyes au facturaion
        data = {
            # 'session_id': self.id,  # ???/????
            'partner_id': self.id,
            'type': 'out_invoice',
            # 'invoice_line_ids': [],

        }

        # line = {
        #     'product_id': self.id,
        #     'name': "session",
        #     'quantity': self.duration,
        #     'price_unit': self.price_per_hour
        # }
        # data["invoice_line_ids"].append((0, 0, line))
        # invoice = self.env['account.move'].create(data)
        invoice = self.env['account.move'].create(data)

        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'out_invoice',
        }

        action['context'] = context
        return action