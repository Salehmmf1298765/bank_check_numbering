{
    'name': 'Bank Check Auto Numbering',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Automatic check numbering for all journals',
    'description': """
        هذا المديول يقوم بإدارة الترقيم التلقائي للشيكات لجميع أنواع الجورنالز:
        • إضافة حقل رقم البداية بتنسيق مخصص (001, 0001, إلخ)
        • زر لتحديد أن القيد هو شيك في أي جورنال
        • ترقيم تلقائي متسلسل مع الحفاظ على التنسيق
        • إمكانية تعديل رقم الشيك يدوياً
        • دعم عدد الأرقام المطلوبة في التنسيق
        
        This module manages automatic check numbering for all journal types:
        • Add starting number field with custom format (001, 0001, etc.)
        • Button to mark journal entry as check in any journal
        • Automatic sequential numbering maintaining format
        • Manual check number editing capability
        • Support for custom number of digits in format
    """,
    'author': "Engineer / Salah Alhjany",
    'website': "https://www.facebook.com/salh.alhjany/?rdid=plWVCqF0AkDERe3g",
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
