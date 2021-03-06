# import json
import logging

from typing import (List, Optional)

from compose.utils.requests import (get)
from compose.utils.urls import (MESSENGER_USER_API)


class User:
    def __init__(self, id=None):
        self._id: str = id
        self._fn: Optional[str] = None
        self._ln: Optional[str] = None
        self._locale: Optional[str] = None
        self._history: Optional[List[str]] = None

    @property
    def fn(self) -> Optional[str]:
        if self._fn is None:
            self._fill_fields('first_name', 'last_name')
        return self._fn

    @property
    def ln(self) -> Optional[str]:
        if self._ln is None:
            self._fill_fields('first_name', 'last_name')
        return self._ln

    @property
    def locale(self) -> Optional[str]:
        if self._locale is None:
            self._fill_fields('locale')
        return self._locale

    def _fill_fields(self, *fields: str) -> bool:
        logging.info(f"Getting {fields} for id {self._id}")
        queries: dict = {'fields': list(fields)}

        # NOTE: Figure out why "json" works but not "params"
        ok, data = get(MESSENGER_USER_API.format(fbId=self._id), json=queries)
        if ok:
            if 'locale' in fields:
                self._locale = data['locale']
            if 'first_name' in fields or 'last_name' in fields:
                self._fn, self._ln = data['first_name'], data['last_name']
        else:
            logging.warning(f"Failed to retrieve {fields} for id {self._id}")

        return ok
