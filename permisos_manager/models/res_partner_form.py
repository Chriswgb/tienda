# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from datetime import *
import time
from datetime import datetime, timedelta
from odoo.exceptions import Warning


class PerResPartnertInherit(models.Model):
	_inherit = "res.partner"
