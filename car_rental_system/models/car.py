from odoo import models, fields, api
from odoo.exceptions import UserError

reservation_model_id = "car_rental_system.car_reservation"
car_states = [("available", "Available"), ("rented", "Rented"), ("damaged", "Damaged")]
manager_group_id = "car_rental_system.group_managers"


class Car(models.Model):
    _name = "car_rental_system.car"
    _description = "car_rental_system.car"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char("Car Name", required=True)
    description = fields.Text("Brief Description")
    rent_price = fields.Float("Rent Price", required=True)
    state = fields.Selection(
        car_states,
        "State",
        default="available",
    )
    reservation_model_id = "car_rental_system.car_reservation"
    reservation_request = fields.Boolean(
        "Reservation State", compute="_compute_car_reservation_request", store=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=False)
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
    location = fields.Char("Location" )
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
    # Compute Methods

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

    # Methods

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
        if self.env.user.has_group(manager_group_id):
            return self.open_reservation_wizard_action_view()
        # User => Reserve Direct
        else:
            self.env[reservation_model_id].sudo().create(
                {
                    "car_id": self.id,
                    "borrower_id": self.env.user.id,
                }
            )

        self.sudo().mark_reserved()

    @api.model
    def open_reservation_wizard_action_view(self):
        action = self.env.ref("car_rental_system.action_wizard_rent_cars").read()[0]
        action["context"] = {"car_ids": self.id}
        return action

    def unreserve_car(self):
        self.ensure_one()
        if self.state != "rented":
            raise UserError(("Car is not reserved yet"))

        reserved_car = (
            self.env[reservation_model_id]
            .sudo()
            .search([("car_id", "=", self.id), ("return_date", "=", None)])
        )
        # Save the Return Date => Now
        reserved_car.return_date = fields.Datetime.now()
        reserved_car.reservation_state = "returned"

        self.mark_available()

    def request_unreserve_car(self):
        self.ensure_one()
        if self.state != "rented":
            raise UserError(("Car is not reserved yet"))

        reserved_car = (
            self.env[reservation_model_id]
            .sudo()
            .search([("car_id", "=", self.id), ("reservation_state", "=", "ongoing")])
        )
        reserved_car.reservation_state = "return_request"

    def damaged_car(self):
        self.ensure_one()
        if self.state == "damaged":
            raise UserError(("Car is already damaged"))

        reserved_car = (
            self.env[reservation_model_id]
            .sudo()
            .search([("car_id", "=", self.id), ("return_date", "=", None)])
        )
        # Save the Return Date => Now
        reserved_car.return_date = fields.Datetime.now()
        reserved_car.reservation_state = "returned"

        self.mark_damaged()
