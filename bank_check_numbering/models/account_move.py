from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'


    is_check = fields.Boolean(
        string='Is Check',
        default=False,
        help='Mark this journal entry as a check payment'
    )
    

    check_number = fields.Char(
        string='Check Number',
        help='Check serial number'
    )
    
    journal_supports_checks = fields.Boolean(
        string='Journal Supports Checks',
        compute='_compute_journal_supports_checks',
        store=False
    )

    @api.depends('journal_id', 'journal_id.enable_check_numbering')
    def _compute_journal_supports_checks(self):
        """
        Determine if the journal supports check numbering
        """
        for move in self:
            move.journal_supports_checks = (
                move.journal_id and 
                move.journal_id.enable_check_numbering
            )

    @api.onchange('is_check', 'journal_id')
    def _onchange_is_check(self):
        """
        When enabling/disabling the check checkbox
        """
        if self.is_check:

            self._compute_journal_supports_checks()
            
            if self.journal_supports_checks and not self.check_number:

                if self.journal_id:
                    next_check_number = self.journal_id.get_next_check_number(self.journal_id.id)
                    if next_check_number:
                        self.check_number = next_check_number
        else:

            self.check_number = False

    @api.onchange('check_number')
    def _onchange_check_number(self):
        """
        Check the validity of the check number when manually changed
        """
        if self.check_number and self.is_check:

            existing_check = self.search([
                ('journal_id', '=', self.journal_id.id),
                ('check_number', '=', self.check_number),
                ('is_check', '=', True),
                ('id', '!=', self.id)
            ])
            
            if existing_check:
                return {
                    'warning': {
                        'title': _('Duplicate Check Number'),
                        'message': _('Check number %s already exists in this journal. Please use a different number.') % self.check_number
                    }
                }

    @api.model_create_multi
    def create(self, vals_list):
        """
        Customizing the creation of constraints for handling checks
        """

        for vals in vals_list:
            if vals.get('is_check') and not vals.get('check_number'):
                journal_id = vals.get('journal_id')
                if journal_id:
                    journal = self.env['account.journal'].browse(journal_id)
                    if journal.enable_check_numbering:
                        next_check_number = journal.get_next_check_number(journal_id)
                        if next_check_number:
                            vals['check_number'] = next_check_number
        
        moves = super().create(vals_list)
        return moves

    def write(self, vals):
        """
        Customizing the update of constraints for handling checks
        """

        if vals.get('is_check') and not vals.get('check_number'):
            for move in self:

                if move.journal_supports_checks and not move.check_number:
                    next_check_number = move.journal_id.get_next_check_number(move.journal_id.id)
                    if next_check_number:
                        vals['check_number'] = next_check_number
                        break  
                        
        return super().write(vals)
    
    @api.constrains('is_check', 'check_number')
    def _check_check_number_required(self):
        """
        Check the check number upon final saving.
        """
        for move in self:
            if move.is_check and move.state != 'draft' and not move.check_number:
                raise ValidationError(_('Check number is required for posted check entries.'))
