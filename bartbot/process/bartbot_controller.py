# import boto3
import json
import logging
import time
import wrapt

from abc import (ABC, abstractmethod)
from typing import(Any, Dict, List, Optional, Tuple, Union)

from bartbot import receive as rcv
from bartbot.process.controller import (Controller)
from bartbot.process.entities import (WitEntities)
from bartbot.send.attachment import (Asset, Template)
from bartbot.send.button import (Button)
from bartbot.send.response import (Response)
from bartbot.send.response_builder import (ResponseBuilder)
from bartbot.receive.attachment import (Attachment)
from bartbot.resources.map import (yield_map_id)


class BartbotController(Controller):

    HELP_TEXT = "[TODO: Fill in this help text.]"

    def produce_responses(self) -> ResponseBuilder:
        self.preprocess_message()
        response = self.process_message()
        self.postprocess_message()
        return response

    def preprocess_message(self):
        seenResponse = ResponseBuilder(
            recipientId=self.message.senderId,
            senderAction="mark_seen",
            description="Marking message as seen")
        seenResponse.create_and_get_chained_response(
            senderAction="typing_on",
            description="Turning typing on")
        seenResponse.send()

    def postprocess_message(self):
        typingOffResponse = ResponseBuilder(
            recipientId=self.message.senderId,
            senderAction="typing_off",
            description="Turning typing off")
        typingOffResponse.send()

    def process_message(self):
        head = ResponseBuilder(recipientId=self.message.senderId)
        respTail = head

        if isinstance(self.message, Attachment):
            respTail.text = self.message._phrase.get_phrase(
                'attachment', opt={'fn': self.message._client.fn})
            respTail.description = "Attachment response"

        elif isinstance(self.message, rcv.text.Text):
            respTail.text = f'You typed: "{self.message.text}"'
            respTail.description = "Echoing message"
            respTail = respTail.create_and_get_chained_response()
            self.entities = WitEntities(self.message.entities)
            respTail.text = str(self.entities)
            respTail.description = "Wit entities"

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
                pass

            respTail.add_quick_reply(
                text="What is love?", postbackPayload="Payload")
            respTail.add_quick_reply(
                text="Baby don't hurt me...", postbackPayload="Payload")

        return head

    def help_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text=self.HELP_TEXT,
            description="Help text response")
        return respTail

    def map_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text=self.message._phrase.get_phrase(
                'delivery', opt={'fn': self.message._client.fn}),
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

    def cost_response(self, respTail: ResponseBuilder, roundTrip: bool = False) -> ResponseBuilder:
        respTail.create_and_get_chained_response(
            text="[TODO: Fill in the cost response.]",
            description="Cost text")
        return respTail

    def travel_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.create_and_get_chained_response(
            text="[TODO: Fill in the travel response.]",
            description="Travel text")

        # HACK: Just trying to get basic functionality

        from bartbot.utils.requests import get
        from bartbot.utils.keys import BART_PUBL

        params: dict = {
            'cmd': 'depart' if self.entities.timeArr is None else 'arrive',
            'orig': self.entities.stn,
            'dest': self.entities.stnDest,
            'time': time.strftime("%-I:%M %p", self.entities.time if self.entities.timeArr is None else self.entities.timeArr),
            'b': '2',
            'a': '3',
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
            # respTail = respTail.create_and_get_chained_response(
            #     text=f"{trip['@origin']} {trip['@origTimeMin']} to {trip['@destination']} {trip['@destTimeMin']}")
        respTail = respTail.create_and_get_chained_response(
            text='\n'.join(strTrips))

        return respTail

    def weather_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.create_and_get_chained_response(
            text="[TODO: Fill in the weather response.]",
            description="Weather text")
        return respTail

    def reset_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.create_and_get_chained_response(
            text="[TODO: Fill in the reset response.]",
            description="Reset text")
        return respTail

    def send_waiting_response(self, respTail: ResponseBuilder):
        respBranch = respTail.create_and_get_separate_response(
            description="Wait text")
        respBranch.text = self.message._phrase.get_phrase(
            'wait', opt={'fn': self.message._client.fn})
        respBranch.create_and_get_chained_response(
            senderAction="typing_on",
            description="Turning typing on for waiting")
        respBranch.send()
