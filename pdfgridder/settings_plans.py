import os
from dateutil import parser as date_parser


ISSUER_DATA = {
    "issuer_tax_number": os.environ.get('ISSUER_TAX_NUMBER', ''),
    "issuer_name": os.environ.get('ISSUER_NAME', ''),
    "issuer_street": os.environ.get('ISSUER_STREET', ''),
    "issuer_zipcode": os.environ.get('ISSUER_ZIPCODE', ''),
    "issuer_city": os.environ.get('ISSUER_CITY', ''),
    "issuer_country": os.environ.get('ISSUER_COUNTRY', ''),
}

PLANS_CURRENCY = 'USD'
PLAN_DEFAULT_GRACE_PERIOD = 30

INVOICE_TEMPLATE = 'plans/invoices/US_EN.html'
TAX = None

TAXATION_POLICY = 'billing.taxation.us.us_taxation_policy'
TAX_COUNTRY = 'US'

PLAN_VALIDATORS = {
    'MAX_GRIDS_COUNT':  'gridder.quotas.max_grids_validator',
}

PLANS_START_DATE = date_parser.parse('2014-08-01')
