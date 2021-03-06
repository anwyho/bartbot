# import boto3
import json
import logging
import time
import wrapt

from abc import (ABC, abstractmethod)
from concurrent.futures import (ThreadPoolExecutor)
from typing import(Any, Dict, List, Optional, Tuple, Union)

from compose import receive as rcv
from compose.process.controller import (Controller)
from compose.bartbot.bartbot_entities import (BartbotEntities)
from compose.process.user import (User)
from compose.send.attachment import (Asset, Template)
from compose.send.button import (Button)
from compose.send.response import (Response)
from compose.send.response_builder import (ResponseBuilder)
from compose.receive.attachment import (Attachment)
from compose.bartbot.resources.map import (yield_map_id)
from compose.utils.phrases.phrase import (Phrase)


DRY_RUN = False


class BartbotController(Controller):

    def __init__(self, message, dryRun: bool = False) -> None:
        super().__init__(message=message, dryRun=dryRun)
        self.user: User = User(id=message.senderId)
        self.phrase: Phrase = Phrase(initialLocale=self.user.locale)
        self._dryRun: bool = DRY_RUN

    ### PRE- & POST- PROCESSING ###

    # OVERRIDES CONTROLLER
    def preprocess_message(self):
        self.send_seen_and_typing_on_indicators()
        if hasattr(self.message, 'text'):
            self.futureEntities = self._executor.submit(
                self.get_wit_entities)

    # OVERRIDES CONTROLLER
    def postprocess_message(self):
        self.send_typing_off_indicator()

    ### Pre- and Post-Processing Helpers ###

    def send_seen_and_typing_on_indicators(self):
        seenResponse = ResponseBuilder(
            recipientId=self.message.senderId,
            senderAction="mark_seen",
            description="Marking message as seen",
            dryRun=self._dryRun)
        seenResponse.create_and_get_chained_response(
            senderAction="typing_on",
            description="Turning typing on")
        self._executor.submit(seenResponse.send())

    def send_typing_off_indicator(self):
        typingOffResponse = ResponseBuilder(
            recipientId=self.message.senderId,
            senderAction="typing_off",
            description="Turning typing off",
            dryRun=self._dryRun)
        self._executor.submit(typingOffResponse.send())

    def send_waiting_response(self, respTail: ResponseBuilder):
        respBranch = respTail.create_and_get_separate_response(
            text=self.phrase.get('wait'),
            description="Wait text")
        respBranch.create_and_get_chained_response(
            senderAction="typing_on",
            description="Turning typing on for waiting")
        self._executor.submit(respBranch.send)

    def get_wit_entities(self):
        return BartbotEntities(
            text=self.message.text,
            senderId=self.message.senderId)

    ### PROCESS MESSAGE ###

    def process_message(self):
        self.phrase.add_attributes(
            firstName=self.user.fn)

        head = respTail = ResponseBuilder(
            recipientId=self.message.senderId,
            dryRun=self._dryRun)

        if isinstance(self.message, Attachment):
            respTail = self.process_attachment(respTail)

        # BUG: Figure out why I can't call Text as `Text`
        elif isinstance(self.message, rcv.text.Text):
            respTail = self.process_text(respTail)

        return head

    def process_attachment(self, respTail) -> ResponseBuilder:
        respTail.text = self.phrase.get(
            'attachment', useName=True)
        respTail.description = "Attachment response"
        return respTail

    def process_text(self, respTail) -> ResponseBuilder:
        respTail.text = f'You typed: "{self.message.text}"'
        respTail.description = "Echoing message"

        self.entities = self.await_entities()

        respTail = respTail.create_and_get_chained_response(
            text=str(self.entities),
            description="Wit self.entities")

        intent = self.entities.intent
        if 'help' == intent:
            respTail = self.help_response(respTail)
        elif 'map' == intent:
            respTail = self.map_response(respTail)
        elif 'travel' == intent:
            respTail = self.travel_response(respTail)
        elif 'single-trip-cost' == intent:
            respTail = self.cost_response(respTail)
        elif 'round-trip-cost' == intent:
            respTail = self.cost_response(respTail, roundTrip=True)
        elif 'weather' == intent:
            respTail = self.weather_response(respTail)
        elif 'reset' == intent:
            respTail = self.reset_response(respTail)
        else:
            # TODO: Unknown request
            pass

        # TODO: self.add_quick_replies

        respTail.add_quick_reply(
            text="What is love?", postbackPayload="Payload")
        respTail.add_quick_reply(
            text="Baby don't hurt me...", postbackPayload="Payload")
        respTail.add_quick_reply(
            text="Baby don't hurt me...", postbackPayload="Payload")
        respTail.add_quick_reply(
            text="No more...!", postbackPayload="Payload")

        return respTail

    def await_entities(self) -> dict:
        while not self.futureEntities.done():
            pass
        return self.futureEntities.result()

    ### Specific Response Helpers ###

    def help_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text=self.phrase.get('helpText'),
            description="Help text response")
        return respTail

    def map_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text=self.phrase.get('delivery'),
            description="Delivery text")
        mapIdGen = yield_map_id()
        mapId = next(mapIdGen)
        if not mapId:
            self.send_waiting_response(respTail)
            mapId = next(mapIdGen)
        if mapId:
            respTail = respTail.create_and_get_chained_response(
                attachment=Asset(assetType='image', attchId=mapId),
                description="Map asset from attachment ID")
        else:
            # TODO: Backup plan
            pass

        return respTail

    def cost_response(self, respTail: ResponseBuilder, roundTrip: bool=False) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text="[TODO: Fill in the cost response.]",
            description="Cost text")
        return respTail

    def travel_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text="[TODO: Fill in the travel response.]",
            description="Travel text")

        # TODO: Outsource this to new file

        # HACK: Just trying to get basic functionality

        from compose.utils.requests import get
        from compose.utils.keys import BART_PUBL

        params: dict = {
            'cmd': 'depart' if self.entities.timeArr is None else 'arrive',
            'orig': self.entities.stn,
            'dest': self.entities.stnDest,
            'time': time.strftime("%-I:%M %p", self.entities.time if self.entities.timeArr is None else self.entities.timeArr),
            'b': '1',
            'a': '4',
            'json': 'y',
            'key': BART_PUBL
        }

        ok, resp = get(
            url="http://api.bart.gov/api/sched.aspx", params=params)

        trips: list = resp['root']['schedule']['request']['trip']
        strTrips: list = []
        for trip in trips:
            strTrips.append(
                f"{trip['@origin']} {trip['@origTimeMin']} to {trip['@destination']} {trip['@destTimeMin']}")
        respTail = respTail.create_and_get_chained_response(
            text='\n'.join(strTrips),
            description='HACK trip info')

        return respTail

    def weather_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text="[TODO: Fill in the weather response.]",
            description="Weather text")
        return respTail

    def reset_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text="[TODO: Fill in the reset response.]",
            description="Reset text")
        return respTail

    def unknown_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text="[TODO: Fill in the unknown text response.]",
            description="Unknown text")
        return respTail
