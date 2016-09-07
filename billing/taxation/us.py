from plans.taxation import TaxationPolicy


class USTaxationPolicy(TaxationPolicy):
    def get_tax_rate(self, tax_id, country_code):
        # Implement this if we need nexus
        return 0

us_taxation_policy = USTaxationPolicy()