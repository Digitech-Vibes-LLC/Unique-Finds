{
   'name': 'Unique Finds Theme',
   'description': 'Unique Finds Theme',
   'category': 'Theme/sub_category',
   'version': '16.0.0',
   'author': 'aboudasadok@gmail.com',
   'license': 'LGPL-3',
   'depends': ['website', 'auth_signup'],
   'data': [
      'views/assets.xml',
      'views/login_template.xml',
      'views/backgrounds.xml',
      'views/home.xml',

   ],
   'assets': {
      'web.assets_frontend': [
         '/theme_unique_finds/static/src/css/*',
      ],
   },
}