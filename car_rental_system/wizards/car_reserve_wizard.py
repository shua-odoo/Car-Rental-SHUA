from odoo import models, fields, api

manager_group_id = "car_rental_system.group_managers"


class CarReserveWizard(models.TransientModel):
    _name = "crs.car_reservation.wizard"
    
    borrower_id = fields.Many2one(
        "res.users",
        string="Borrower",
        required=True,
        default=lambda self: self.env.user,
    )
    car_ids = fields.Many2many("car_rental_system.car", string="Cars", required=True)
    user_manager = fields.Boolean(compute="_compute_check_group", store=False)

    # Compute Methods

    @api.depends("borrower_id")
    def _compute_check_group(self):
        if self.user_has_groups(manager_group_id):
            self.user_manager = True
        else:
            self.user_manager = False

    # Methods

    @api.model
    def default_get(self, fields_list):
        defaults = super(CarReserveWizard, self).default_get(fields_list)
        if self.env.context.get("active_model"):
            defaults["car_ids"] = [self.env.context["car_ids"]]
        return defaults

    def add_car_reservation(self):
        self.ensure_one()
        rent_model = self.env["car_rental_system.car_reservation"].sudo()
        for car in self.car_ids:
            new_rent = rent_model.create(
                {"borrower_id": self.borrower_id.id, "car_id": car.id}
            )
            
       
            new_rent.car_id.mark_reserved()
        
        for car2 in self:
            self.env["account.move"].create({
                'partner_id': car2.borrower_id.id,
                'move_type':'out_invoice'
            })

        return {
            # Rainbow Man Effect
            "effect": {
                "fadeout": "slow",
                "message": "Car Rent Successfully for %s"
                % (self.borrower_id.display_name),
                "type": "rainbow_man",
            }
        }
