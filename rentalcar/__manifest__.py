{
    'name': 'car_rental',
    'summary': 'Car Rental SHUA',
    'description':"this is app by ankuR",
    'depends': [
        'base',
    ],
    'demo':[],
    'installable':True,
    'application':True,
    'auto_install':False,
    'data': [
        "security/ir.model.access.csv",
        "security/groups.xml",
        "views/car.xml",
        "views/car_menus.xml"
    ],
}