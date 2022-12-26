# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class WizardPrintYearlyAmortization(models.TransientModel):
    _name = "account.wizard_print_yearly_amortization"
    _description = "Print Account Yearly Amortizarion"

    @api.model
    def _default_date(self):
        return fields.Date.today()

    type_id = fields.Many2one(
        string="Type",
        comodel_name="account.amortization_type",
        required=True,
    )
    year = fields.Integer(
        string="Year",
        required=True,
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        default="ods",
        selection=[("xls", "XLS"), ("ods", "ODS")],
    )

    @api.multi
    def action_print_xls(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "report_account_amortization_xls",
            "datas": datas,
        }

    @api.multi
    def action_print_ods(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "report_account_amortization_ods",
            "datas": datas,
        }

    @api.multi
    def button_print_report(self):
        self.ensure_one()

        if self.output_format == "ods":
            result = self.action_print_ods()
        elif self.output_format == "xls":
            result = self.action_print_xls()
        else:
            raise UserError(_("No Output Format Selected"))

        return result
