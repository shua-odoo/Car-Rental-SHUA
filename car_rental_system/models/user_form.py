from odoo import models, fields


class ReservedCarsList(models.Model):
    _inherit = "res.users"
    reserved_cars_count = fields.Integer(compute="_compute_cars_count")

    # Compute Methods

    def _compute_cars_count(self):
        for record in self:
            record.reserved_cars_count = self.env[
                "car_rental_system.car_reservation"
            ].search_count(
                [("borrower_id", "=", self.id), ("reservation_state", "!=", "returned")]
            )

    # Methods

    def get_reserved_cars(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Cars",
            "view_mode": "tree",
            "res_model": "car_rental_system.car_reservation",
            "domain": [
                ("borrower_id", "=", self.id),
                ("reservation_state", "!=", "returned"),
            ],
            "context": "{'create': False}",
        }
