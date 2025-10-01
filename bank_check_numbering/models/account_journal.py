from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'


    check_starting_number = fields.Char(
        string='Check Starting Number',
        default='001',
        help='The starting number for check numbering with format. Example: 001, 0001, etc.'
    )
    
    check_number_digits = fields.Integer(
        string='Number of Digits',
        default=3,
        help='Number of digits for check numbering format (e.g., 3 for 001, 4 for 0001)'
    )
    

    last_check_number = fields.Integer(
        string='Last Check Number',
        default=0,
        help='The last check number used for this bank journal.'
    )
    

    enable_check_numbering = fields.Boolean(
        string='Enable Check Numbering',
        default=False,
        help='Enable automatic check numbering for this bank journal.'
    )

    @api.model
    def get_next_check_number(self, journal_id):
        """
        Get the next check number for the specified journal
        """
        journal = self.browse(journal_id)
        if not journal.enable_check_numbering:
            return False
        

        last_check = self.env['account.move'].search([
            ('journal_id', '=', journal_id),
            ('is_check', '=', True),
            ('check_number', '!=', False),
            ('check_number', '!=', '')
        ], order='id desc', limit=1)
        
        if last_check and last_check.check_number:
            try:
                last_number = int(last_check.check_number.lstrip('0') or '0')
                next_number_int = last_number + 1
            except ValueError:
                try:
                    next_number_int = int(journal.check_starting_number or '1')
                except ValueError:
                    next_number_int = 1
        else:

            try:
                next_number_int = int(journal.check_starting_number or '1')
            except ValueError:
                next_number_int = 1
        

        journal.write({'last_check_number': next_number_int})
        

        digits = journal.check_number_digits or 3
        formatted_number = str(next_number_int).zfill(digits)
        
        return formatted_number

    def reset_check_numbering(self):
        """
        Reset check numbering to the start
        """
        self.ensure_one()
        self.write({
            'last_check_number': 0
        })
        return True
