# -*- coding: utf-8 -*-
{
    'name': "Calificación de clientes",

    'summary': """Manage trainings""",

    'description': """
        Modulo para que los clientes evaluen a los vendedores
            -
            -
            -
            -
    """,

    'author': "Mario Alberto Solano Zavala",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '1.0.18',

    # any module necessary for this one to work correctly
    'depends': ['contacts', 'website', 'point_of_sale'],

    # always loaded
    'data': [
        'views/menu.xml',
        'views/assets.xml',
        'views/evaluacion.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}