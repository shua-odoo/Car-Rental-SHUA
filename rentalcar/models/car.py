from odoo import models, fields , api 

# reservation_model_id = "car_rental_system.car_reservation"
car_states = [("available", "Available"), ("rented", "Rented"), ("damaged", "Damaged")]
# manager_group_id = "car_rental_system.group_managers"

class Car(models.Model):
    _name = "car.rental.system.car"
    _description = "car_rental_system.car"

    name = fields.Char("Car Name", required=True)
    description = fields.Text("Brief Description")
    rent_price = fields.Float("Rent Price", required=True)
    state = fields.Selection(
        car_states,
        "State",
        default="available",
    )
    reservation_request = fields.Boolean(
        "Reservation State", compute="_compute_car_reservation_request", store=False
    )   