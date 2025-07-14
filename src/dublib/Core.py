from .CLI.TextStyler import GetStyledTextFromHTML

import logging

LOGS_HANDLER = logging.StreamHandler()
LOGS_HANDLER.setFormatter(logging.Formatter(GetStyledTextFromHTML("<b>[%(name)s]</b> %(levelname)s: %(message)s")))