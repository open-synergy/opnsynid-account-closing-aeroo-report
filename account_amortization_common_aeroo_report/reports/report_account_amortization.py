# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime, time

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.no = 1
        self.localcontext.update(
            {
                "time": time,
                "get_date": self.get_date,
                "get_amortization": self._get_amortization,
                "get_amortization_type": self._get_amortization_type,
            }
        )

    def set_context(self, objects, data, ids, report_type=None):
        self.form = data["form"]
        self.date = self.form["date"]
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def get_date(self):
        convert_dt = datetime.strptime(self.date, "%Y-%m-%d")
        return convert_dt.strftime("%d %B %Y")

    def _get_amortization_type(self):
        type_id = self.form["type_id"]
        ttype = self.pool.get("account.amortization_type").browse(
            self.cr, self.uid, type_id[0]
        )[0]
        return ttype.name

    def _get_amortization(self):
        self.lines = []

        # TODO
        type_id = self.form["type_id"]
        ttype = self.pool.get("account.amortization_type").browse(
            self.cr, self.uid, type_id[0]
        )[0]
        if ttype.name == "Prepaid Expense":
            obj_amortization = self.pool.get("account.prepaid_expense_amortization")
        else:
            obj_amortization = self.pool.get("account.prepaid_income_amortization")

        criteria = [
            ("date", "<=", self.date),
            ("state", "in", ["open", "done"]),
        ]

        amortization_ids = obj_amortization.search(
            self.cr, self.uid, criteria, order="date_start"
        )

        if amortization_ids:
            for amortization in obj_amortization.browse(
                self.cr, self.uid, amortization_ids
            ):
                convert_dt = datetime.strptime(amortization.date, "%Y-%m-%d")
                amount_amortized = self._get_amount_amortized(
                    amortization.id, self.date
                )
                amount_residual = amortization.amount - amount_amortized
                res = {
                    "no": self.no,
                    "name": amortization.name,
                    "amount": amortization.amount,
                    "start_date": convert_dt.strftime("%d %B %Y"),
                    "age": amortization.period_number,
                    "amount_amortized": amount_amortized,
                    "amount_residual": amount_residual,
                }

                self.lines.append(res)
                self.no += 1

        return self.lines

    def _get_amount_amortized(self, amortization_id, date):
        result = 0.0
        type_id = self.form["type_id"]
        ttype = self.pool.get("account.amortization_type").browse(
            self.cr, self.uid, type_id[0]
        )[0]
        if ttype.name == "Prepaid Expense":
            obj_line = self.pool.get("account.prepaid_expense_amortization_schedule")
        else:
            obj_line = self.pool.get("account.prepaid_income_amortization_schedule")

        criteria = [
            ("amortization_id", "=", amortization_id),
            ("date", "<=", date),
            ("state", "in", ["manual", "post"]),
        ]

        line_ids = obj_line.search(self.cr, self.uid, criteria)
        if line_ids:
            for line in obj_line.browse(self.cr, self.uid, line_ids):
                result += line.amount
        return result
