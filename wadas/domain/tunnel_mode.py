# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2024-08-16
# Description: Module containing Tunnel mode methods.

import logging

from wadas.domain.operation_mode import OperationMode

logger = logging.getLogger(__name__)


class TunnelMode(OperationMode):
    def __init__(self):
        super(TunnelMode, self).__init__()
        self.type = OperationMode.OperationModeTypes.TunnelMode

    def run(self):
        """Method to run Tunnel Mode."""
        logger.info("Starting Tunnel Mode...")

        # TODO: implement logic
        pass
