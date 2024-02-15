from odoo import models, fields

reservation_states = [
    ("ongoing", "Ongoing"),
    ("return_request", "Return Request"),
    ("returned", "Returned"),
]


class CarReservation(models.Model):
    _name = "car_rental_system.car_reservation"
    _description = "car_rental_system.car_reservation"

    car_id = fields.Many2one(
        "car_rental_system.car", string="Car", required=True, ondelete="cascade"
    )
    borrower_id = fields.Many2one("res.users", string="Borrower", required=True)
    reservation_state = fields.Selection(
        selection= reservation_states, string="Reservation State", default="ongoing"
    )

    return_date = fields.Date(string="Return Date")
