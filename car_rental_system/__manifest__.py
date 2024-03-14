{
    "name": "Car_Rental",
    "summary": """Car Rental System""",
    "description": """
        Car Rental Internal Booking System
    """,
    "version": "0.1",
    "depends": ["base", "web",'account'],
    "application": True,
    "data": [
        "security/groups.xml",
        "security/car_reservation.xml",
        "security/ir.model.access.csv",
        "views/car.xml",
        "wizards/car_reserve_wizard.xml",
        "view/car_damaged.xml",
        "views/car_reservation.xml",
        "views/user_form.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "car_rental_system/static/src/xml/custom_rainbow_man.xml",
        ],
    },
}
