import json
import logging
from typing import Tuple, Union

import requests

from wit import Wit

from . import keys as k
from . import phrases
from .urls import AUTH, GRAPH_API, MESSAGES_URL

MAP_ID = "264370450851085"


def process_page_entry(entry:dict) -> str:
    """Processes a page object returned by a message subscription"""
    if not 'messaging' in entry:
        raise KeyError("Expected 'messaging' in entry")

    for m in entry['messaging']:
        try: 
            fbId:str = m['sender']['id']
        except:
            raise KeyError("Expected 'sender.id' in messaging") 

        turn_on_seen_and_typing_indicator(fbId)

        res:str = None
        if 'text' in m['message'].keys():
            res = handle_text(fbId, m['message']['text'])
        elif 'attachments' in m['message'].keys():
            res = handle_attachment(fbId, m['message']['attachments'])
        else: 
            logging.warning("Received empty message event")
            res = "Message body is empty."

        return res



def handle_attachment(fbId:str, attach:dict) -> str:
    logging.info("Received attachment message event")
    return 'OK'


def handle_text(fbId:str, text:str) -> str:
    logging.info("Received text message event")
    nlp_entities:dict = get_wit_entities(fbId, text)
    if nlp_entities == None:
        # TODO: Create fallback, either message about NLP or do cheap hack
        # TODO: Link to another suitable BART schedule thing. 
        pass

    entities:dict = nlp_entities['entities']

    # HACK: fix entity parsing
    fn,ln = get_id_name(fbId)
    if 'greeting' in entities:
        logging.info('Sending a greeting')
        text = phrases.get_phrase(phrases.hello,phrases.cta).format(fn=fn)
    elif 'intent' in entities and 'map' == entities['intent'][0]['value']:
        logging.info('Sending a map')
        text = send_map(fbId, fn)
    else:
        text = "Hello {} {}. You typed: ".format(fn,ln) + nlp_entities['_text']
    
    text += "\nDebug info: {}".format(json.dumps(entities, indent=4))

    return fb_message(fbId, text)


def send_map(fbId:str, fn:str='{fn}'):
    # TODO: Send a phrases.delivery post
    data = {
        'recipient': {'id': fbId},
        'messaging_type': 'RESPONSE',
        'message': {
            'attachment': {
                'type': 'image',
                'payload': {
                    'attachment_id': MAP_ID}}}}
    post_request(MESSAGES_URL, data=data)
    return phrases.get_phrase(phrases.delivery, fn=fn)

    # Handle code in this function instead: 
    # del data['message']['attachment']
    # data['message']['text'] = \
    #     phrases.get_phrase(phrases.delivery, fn=fn)
    # post_request(MESSAGES_URL, data=data)


def fb_message(fbId:str, text:str) -> str:
    """Function for returning response to messenger"""
    logging.info("Sending message {text} to FB ID {id}".format(text=text,id=fbId))
    
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': fbId},
        'message': {'text': text}}
    
    post_request(MESSAGES_URL, data=data)
    return 'OK'


def get_id_name(fbId:str) -> Tuple[str,str]:
    logging.info("Getting FB name")
    q = {'fields':['first_name','last_name']}
    resp = requests.get(GRAPH_API+fbId+'?'+AUTH, json=q)
    data = resp.json()
    if "error" in data.keys():
        return None
    else: 
        return (data['first_name'], data['last_name'])


def get_wit_entities(fbId:str, text:str) -> Union[None,str]:
    # TODO: log the wit entities with a json dump
    try:
        return Wit(access_token=k.WIT_TOK).message(
            msg=text, context={'session_id':fbId}, verbose=True)
    except Exception as e:
        logging.error("Failed to access Wit API. Error: {}".format(e))
        return None

def first_entity_value(entities, entity):
    """Returns first entity value"""
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def turn_on_seen_and_typing_indicator(fbId:str):
    """POST to Messenger Platform to turn on sender actions"""
    data = {
        'messaging_type': 'RESPONSE', 
        'recipient': { 'id': fbId }}

    data['sender_action'] = 'mark_seen'
    post_request(MESSAGES_URL, data=data)
    data['sender_action'] = 'typing_on'
    post_request(MESSAGES_URL, data=data)



def post_request(url:str, data:dict):
    resp = requests.post(url,json=data)
    logging.debug("Response: {}".format(json.dumps(resp.json())))
    return resp

# TODO: for unsure traits, offer a "find nearest" button







# def pre_response(fbId:str, messageObj:dict) -> None:
#     """Tasks to prep for and set up response"""
#     turn_on_seen_and_typing_indicator(fbId)    

# def post_response(result:str, fbId:str, messageObj:dict) -> str:
#     """Tasks to clean up response before returning"""
#     return result