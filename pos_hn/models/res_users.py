from odoo import fields, models, api


class ResUsersInherit(models.Model):
    _inherit="res.users"

    def get_all_groups(self):

        groups = []
        for group in self.groups_id:
            vals = {
                "id": group.id,
                "name": group.name,
                "full_name": group.full_name
            }

            groups.append(vals)

        return groups