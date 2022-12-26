# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Amortization Common Aeroo Report",
    "version": "8.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account_amortization_common",
        "report_aeroo",
    ],
    "data": [
        "reports/report_account_amortization_ods.xml",
        "reports/report_account_amortization_xls.xml",
        # "reports/report_account_yearly_amortization_xls.xml",
        "wizards/wizard_account_amortization.xml",
        # "wizards/wizard_account_yearly_amortization.xml",
    ],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
