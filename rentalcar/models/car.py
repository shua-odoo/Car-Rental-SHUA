from odoo import models, fields , api 
from odoo.exceptions import UserError

reservation_model_id = "car_rental_system.car_reservation"
car_states = [("available", "Available"), ("rented", "Rented"), ("damaged", "Damaged")]
manager_group_id = "rentalcar.group_managers"

class Car(models.Model):
    _name = "car.rental.system.car"
    _description = "Car Rental System Car"

    name = fields.Char("Car Name", required=True)
    description = fields.Text("Brief Description")
    rent_price = fields.Float("Rent Price", required=True)
    state = fields.Selection(
        car_states,
        "State",
        default="available",
    )
    reservation_request = fields.Boolean(
        "Reservation State", compute="_compute_car_reservation_request", store=True
    )
    image=fields.Image()
    # Additional Fields
    make = fields.Char("Make")
    model = fields.Char("Model")
    year = fields.Integer("Year")
    registration_number = fields.Char("Registration Number")
    color = fields.Char("Color")
    mileage = fields.Float("Mileage")
    fuel_type = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid')
    ], "Fuel Type")
    transmission_type = fields.Selection([
        ('automatic', 'Automatic'),
        ('manual', 'Manual')
    ], "Transmission Type")
    seating_capacity = fields.Integer("Seating Capacity")
    location = fields.Char("Location")
    available_from = fields.Datetime("Available From")
    available_to = fields.Datetime("Available To")
    photos = fields.Binary("Photos")
    condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], "Condition")
    # features = fields.Many2many('car.feature', string='Features')
    insurance_details = fields.Text("Insurance Details")
    additional_info = fields.Text("Additional Info")
    last_serviced_on = fields.Date("Last Serviced On")

    '''
The code is checking if a car currently has a reservation request.
Specifically, it looks for cases where the car is currently being rented out (in the "rented" state) and a reservation for that car exists.
It also checks if the person trying to rent the car is the same person who reserved it or has permission to manage reservations.
    '''
    def _compute_car_reservation_request(self):
        reserved_car = (
            self.env[reservation_model_id]
            .sudo()
            .search([("car_id", "=", self.id), ("return_date", "=", None)])
        )
        for record in self:
            if (
                self.state == "rented"
                and (
                    reserved_car.borrower_id.id == self.env.uid
                    or self.env.user.has_group(manager_group_id)
                )
                and reserved_car.reservation_state == "ongoing"
            ):
                record.reservation_request = True
            else:
                record.reservation_request = False

    '''
   helper method for changes
    '''
    
    def change_state(self, new_state):
        for car in self:
            car.state = new_state

    def mark_available(self):
        self.change_state("available")

    def mark_reserved(self):
        self.change_state("rented")

    def mark_damaged(self):
        self.change_state("damaged")

    def reserve_car(self):
        self.ensure_one()
        if self.state != "available":
            raise UserError(("Car is not available for renting"))

        # Manager => Open the Reservation Wizard View
        
        # User => Reserve Direct
        else:
            self.env[reservation_model_id].sudo().create(
                {
                    "car_id": self.id,
                    "borrower_id": self.env.user.id,
                }
            )

        self.sudo().mark_reserved()

    # def unreserve_car(self):
    #     self.ensure_one()
    #     if self.state != "rented":
    #         raise UserError(("Car is not reserved yet"))

    