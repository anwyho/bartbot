import logging

from typing import List


# List of used emojis
emojis = {
    # Faces
    'smiling_face_with_smiling_eyes' : b'\xf0\x9f\x98\x8a'.decode('utf8'),
    'grinning_face_with_sweat' : b'\xf0\x9f\x98\x85'.decode('utf8'),
    'slightly_smiling_face' : b'\xf0\x9f\x99\x82'.decode('utf8'),
    'upside-down_face' : b'\xf0\x9f\x99\x83'.decode('utf8'),
    'face_with_tears_of_joy' : b'\xf0\x9f\x99\x83'.decode('utf8'),
    'beaming_face_with_smiling_eyes' : b'\xf0\x9f\x98\x81'.decode('utf8'),
    'winking_face' : b'\xf0\x9f\x98\x89'.decode('utf8'),
    'thinking_face' : b'\xf0\x9f\xa4\x94'.decode('utf8'),
    'face_with_raised_eyebrow' : b'\xf0\x9f\xa4\xa8'.decode('utf8'),
    'sleeping_face' : b'\xf0\x9f\x98\xb4'.decode('utf8'),
    'face_with_thermometer' : b'\xf0\x9f\xa4\x92'.decode('utf8'),
    'dizzy_face' : b'\xf0\x9f\x98\xb5'.decode('utf8'),
    'smiling_face_with_sunglasses' : b'\xf0\x9f\x98\x8e'.decode('utf8'),
    'confused_face' : b'\xf0\x9f\x98\x95'.decode('utf8'),
    'worried_face' : b'\xf0\x9f\x98\x9f'.decode('utf8'),
    'slightly_frowning_face' : b'\xf0\x9f\x99\x81'.decode('utf8'),
    'face_with_open_mouth' : b'\xf0\x9f\x98\xae'.decode('utf8'),
    'crying_face' : b'\xf0\x9f\x98\xa2'.decode('utf8'),
    'loud_crying_face' : b'\xf0\x9f\x98\xad'.decode('utf8'),
    'face_screaming_in_fear' : b'\xf0\x9f\x98\xb1'.decode('utf8'),
    'shushing_face' : b'\xf0\x9f\xa4\xab'.decode('utf8'),
    'exploding_head' : b'\xf0\x9f\xa4\xaf'.decode('utf8'),
    'flushed_face' : b'\xf0\x9f\x98\xb3'.decode('utf8'),
    'child' : b'\xf0\x9f\xa7\x92'.decode('utf8'),
    'senior' : b'\xf0\x9f\xa7\x93'.decode('utf8'),
    # Hand Gestures
    'waving_hand' : b'\xf0\x9f\x91\x8b'.decode('utf8'),
    'raised_hand' : b'\xe2\x9c\x8b'.decode('utf8'),
    'OK_hand' : b'\xf0\x9f\x91\x8c'.decode('utf8'),
    'victory_hand' : b'\xe2\x9c\x8c'.decode('utf8'),
    'crossed_fingers' : b'\xf0\x9f\xa4\x9e'.decode('utf8'),
    'call_me_hand' : b'\xf0\x9f\xa4\x99'.decode('utf8'),
    'thumbs_up' : b'\xf0\x9f\x91\x8d'.decode('utf8'),
    'thumbs_down' : b'\xf0\x9f\x91\x8e'.decode('utf8'),
    'oncoming_fist' : b'\xf0\x9f\x91\x8a'.decode('utf8'),
    'right-facing_fist' : b'\xf0\x9f\xa4\x9c'.decode('utf8'),
    'clapping_hands' : b'\xf0\x9f\x91\x8f'.decode('utf8'),
    # Body parts
    'nose' : b'\xf0\x9f\x91\x83'.decode('utf8'),
    'eyes' : b'\xf0\x9f\x91\x80'.decode('utf8'),
    'tongue' : b'\xf0\x9f\x91\x85'.decode('utf8'),
    'eye' : b'\xf0\x9f\x91\x81'.decode('utf8'),
    'mouth' : b'\xf0\x9f\x91\x84'.decode('utf8'),
    'sunglasses' : b'\xf0\x9f\x95\xb6'.decode('utf8'),
    'grad_cap' : b'\xf0\x9f\x8e\x93'.decode('utf8'),
    'billed_cap' : b'\xf0\x9f\xa7\xa2'.decode('utf8'),
    # Plants
    'rose' : b'\xf0\x9f\x8c\xb9'.decode('utf8'),
    'sunflower' : b'\xf0\x9f\x8c\xbb'.decode('utf8'),
    'blossom' : b'\xf0\x9f\x8c\xbc'.decode('utf8'),
    'tulip' : b'\xf0\x9f\x8c\xb7'.decode('utf8'),
    'deciduous_tree' : b'\xf0\x9f\x8c\xb3'.decode('utf8'),
    'four_leaf_clover' : b'\xf0\x9f\x8d\x80'.decode('utf8'),
    'leaf_fluttering_in_wind' : b'\xf0\x9f\x8d\x83'.decode('utf8'),
    # Food & Drink
    'lemon' : b'\xf0\x9f\x8d\x8b'.decode('utf8'),
    'cheese_wedge' : b'\xf0\x9f\xa7\x80'.decode('utf8'),
    'cookie' : b'\xf0\x9f\x8d\xaa'.decode('utf8'),
    'glass_of_milk' : b'\xf0\x9f\xa5\x9b'.decode('utf8'),
    # Travel & Places
    'globe_showing_Americas' : b'\xf0\x9f\x8c\x8e'.decode('utf8'),
    'world_map' : b'\xf0\x9f\x97\xba'.decode('utf8'),
    'house_with_garden' : b'\xf0\x9f\x8f\xa1'.decode('utf8'),
    'office_building' : b'\xf0\x9f\x8f\xa2'.decode('utf8'),
    'school' : b'\xf0\x9f\x8f\xab'.decode('utf8'),
    'sunrise_over_mountains' : b'\xf0\x9f\x8c\x84'.decode('utf8'),
    'sunset_over_water' : b'\xf0\x9f\x8c\x85'.decode('utf8'),
    'sunrise' : b'\xf0\x9f\x8c\x85'.decode('utf8'),
    'cityscape_at_dusk' : b'\xf0\x9f\x8c\x86'.decode('utf8'),
    'cityscape_sunset' : b'\xf0\x9f\x8c\x87'.decode('utf8'),
    'sunset' : b'\xf0\x9f\x8c\x87'.decode('utf8'),
    'foggy' : b'\xf0\x9f\x8c\x81'.decode('utf8'),
    'golden_gate' : b'\xf0\x9f\x8c\x81'.decode('utf8'),
    # Means of Transportation
    'walking' : b'\xf0\x9f\x9a\xb6'.decode('utf8'),
    'running' : b'\xf0\x9f\x8f\x83'.decode('utf8'),
    'dancing' : b'\xf0\x9f\x92\x83'.decode('utf8'),
    'cartwheeling' : b'\xf0\x9f\xa4\xb8'.decode('utf8'),
    'lotusing' : b'\xf0\x9f\xa7\x98'.decode('utf8'),
    'bart_exciting_tunnel' : b'\xf0\x9f\x9a\x87'.decode('utf8'),
    'bart' : b'\xf0\x9f\x9a\x88'.decode('utf8'),
    'bart_station' : b'\xf0\x9f\x9a\x89'.decode('utf8'),
    'muni' : b'\xf0\x9f\x9a\x8a'.decode('utf8'),
    'trolley_bus' : b'\xf0\x9f\x9a\x8e'.decode('utf8'),
    'taxi' : b'\xf0\x9f\x9a\x95'.decode('utf8'),
    'car' : b'\xf0\x9f\x9a\x97'.decode('utf8'),
    'moped' : b'\xf0\x9f\x9b\xb5'.decode('utf8'),
    'bicycle' : b'\xf0\x9f\x9a\xb2'.decode('utf8'),
    'person_biking' : b'\xf0\x9f\x9a\xb4'.decode('utf8'),
    'scooter' : b'\xf0\x9f\x9b\xb4'.decode('utf8'),
    'bart_track' : b'\xf0\x9f\x9b\xa4'.decode('utf8'),
    'police_car_light' : b'\xf0\x9f\x9a\xa8'.decode('utf8'),
    'construction' : b'\xf0\x9f\x9a\xa7'.decode('utf8'),
    'airplane' : b'\xe2\x9c\x88'.decode('utf8'),
    'airplane_departure' : b'\xf0\x9f\x9b\xab'.decode('utf8'),
    'airplane_arrival' : b'\xf0\x9f\x9b\xac'.decode('utf8'),
    'rocket' : b'\xf0\x9f\x9a\x80'.decode('utf8'),
    # something 
    'hundred_points' : b'\xf0\x9f\x92\xaf'.decode('utf8'),
    'trumpet' : b'\xf0\x9f\x8e\xba'.decode('utf8'),
    # Weather
    'full_moon_face' : b'\xf0\x9f\x8c\x9d'.decode('utf8'),
    'sun_with_face' : b'\xf0\x9f\x8c\x9e'.decode('utf8'),
    'glowing_star' : b'\xf0\x9f\x8c\x9f'.decode('utf8'),
    'shooting_star' : b'\xf0\x9f\x8c\xa0'.decode('utf8'),
    'cloud' : b'\xe2\x98\x81'.decode('utf8'),
    'sun_behind_cloud' : b'\xe2\x9b\x85'.decode('utf8'),
    'cloud_with_lightning_and_rain' : b'\xe2\x9b\x88'.decode('utf8'),
    'sun_behind_small_cloud' : b'\xf0\x9f\x8c\xa4'.decode('utf8'),
    'sun_behind_large_cloud' : b'\xf0\x9f\x8c\xa5'.decode('utf8'),
    'sun_behind_rain_cloud' : b'\xf0\x9f\x8c\xa6'.decode('utf8'),
    'cloud_with_rain' : b'\xf0\x9f\x8c\xa7'.decode('utf8'),
    'cloud_with_snow' : b'\xf0\x9f\x8c\xa8'.decode('utf8'),
    'cloud_with_lightning' : b'\xf0\x9f\x8c\xa9'.decode('utf8'),
    'fog' : b'\xf0\x9f\x8c\xab'.decode('utf8'),
    'closed_umbrella' : b'\xf0\x9f\x8c\x82'.decode('utf8'),
    'umbrella' : b'\xe2\x98\x82'.decode('utf8'),
    'umbrella_with_rain_drops' : b'\xe2\x98\x94'.decode('utf8'),
    'snowman' : b'\xe2\x98\x83'.decode('utf8'),
    'fire' : b'\xf0\x9f\x94\xa5'.decode('utf8'),
    # Seasonal
    'christmas_tree' : b'\xf0\x9f\x8e\x84'.decode('utf8'),
    'fireworks' : b'\xf0\x9f\x8e\x86'.decode('utf8'),
    'sparkles' : b'\xe2\x9c\xa8'.decode('utf8'),
    'balloon' : b'\xf0\x9f\x8e\x88'.decode('utf8'),
    'party_popper' : b'\xf0\x9f\x8e\x89'.decode('utf8'),
    'wrapped_gift' : b'\xf0\x9f\x8e\x81'.decode('utf8'),
    # Trophies, Tickets, Medals
    'admit_one' : b'\xf0\x9f\x8e\x9f'.decode('utf8'),
    'ticket' : b'\xf0\x9f\x8e\xab'.decode('utf8'),
    'medal' : b'\xf0\x9f\x8f\x85'.decode('utf8'),
    'trophy' : b'\xf0\x9f\x8f\x86'.decode('utf8'),
    '1st_place' : b'\xf0\x9f\xa5\x87'.decode('utf8'),
    '2nd_place' : b'\xf0\x9f\xa5\x88'.decode('utf8'),
    '3rd_place' : b'\xf0\x9f\xa5\x89'.decode('utf8'),
    # Sports
    'soccer_ball' : b'\xe2\x9a\xbd'.decode('utf8'),
    'basketball' : b'\xf0\x9f\x8f\x80'.decode('utf8'),
    'baseball' : b'\xe2\x9a\xbe'.decode('utf8'),
    'football' : b'\xf0\x9f\x8f\x88'.decode('utf8'),
    '8_ball' : b'\xf0\x9f\x8e\xb1'.decode('utf8'),
    # Other
    'target' : b'\xf0\x9f\x8e\xaf'.decode('utf8'),
    'musical_note' : b'\xf0\x9f\x8e\xb5'.decode('utf8'),
    'musical_notes' : b'\xf0\x9f\x8e\xb6'.decode('utf8'),
    'magnifying_glass' : b'\xf0\x9f\x94\x8e'.decode('utf8'),
    'candle' : b'\xf0\x9f\x95\xaf'.decode('utf8'),
    'light_bulb' : b'\xf0\x9f\x92\xa1'.decode('utf8'),
    'books' : b'\xf0\x9f\x93\x9a'.decode('utf8'),
    'scroll' : b'\xf0\x9f\x93\x9c'.decode('utf8'),
    'newspaper' : b'\xf0\x9f\x93\xb0'.decode('utf8'),
    'rolled-up_newspaper' : b'\xf0\x9f\x97\x9e'.decode('utf8'),
    'tag label' : b'\xf0\x9f\x8f\xb7'.decode('utf8'),
    'winged money' : b'\xf0\x9f\x92\xb8'.decode('utf8'),
    'envelope' : b'\xe2\x9c\x89'.decode('utf8'),
    'package' : b'\xf0\x9f\x93\xa6'.decode('utf8'),
    'pencil' : b'\xe2\x9c\x8f'.decode('utf8'),
    'pushpin' : b'\xf0\x9f\x93\x8c'.decode('utf8'),
    'ruler' : b'\xf0\x9f\x93\x8f'.decode('utf8'),
    'scissors' : b'\xe2\x9c\x82'.decode('utf8'),
    'file cabinet' : b'\xf0\x9f\x97\x84'.decode('utf8'),
    'trash bin' : b'\xf0\x9f\x97\x91'.decode('utf8'),
    'hammer' : b'\xf0\x9f\x94\xa8'.decode('utf8'),
    'microscope' : b'\xf0\x9f\x94\xac'.decode('utf8'),
    'telescope' : b'\xf0\x9f\x94\xad'.decode('utf8'),
    'door' : b'\xf0\x9f\x9a\xaa'.decode('utf8'),
    # Signs
    'wheelchair' : b'\xe2\x99\xbf'.decode('utf8'),
    'restroom' : b'\xf0\x9f\x9a\xbb'.decode('utf8'),
    'warning' : b'\xe2\x9a\xa0'.decode('utf8'),
    'no entry' : b'\xe2\x9b\x94'.decode('utf8'),
    'prohibited' : b'\xf0\x9f\x9a\xab'.decode('utf8'),
    'up arrow' : b'\xe2\xac\x86'.decode('utf8'),
    'right arrow' : b'\xe2\x9e\xa1'.decode('utf8'),
    'soon' : b'\xf0\x9f\x94\x9c'.decode('utf8'),
    'back' : b'\xf0\x9f\x94\x99'.decode('utf8'),
    'checkmark' : b'\xe2\x9c\x85'.decode('utf8'),
    'x mark' : b'\xe2\x9d\x8c'.decode('utf8'),
    'double exclamation mark' : b'\xe2\x80\xbc'.decode('utf8'),
    'copyright' : b'\xc2\xa9'.decode('utf8'),
    'trademark' : b'\xe2\x84\xa2'.decode('utf8'),
    'info square' : b'\xe2\x84\xb9'.decode('utf8'),
    'new square' : b'\xf0\x9f\x86\x95'.decode('utf8'),
    'ok square' : b'\xf0\x9f\x86\x97'.decode('utf8'),
    'parking' : b'\xf0\x9f\x85\xbf'.decode('utf8'),
    'sos' : b'\xf0\x9f\x86\x98'.decode('utf8'),
    'red circle' : b'\xf0\x9f\x94\xb4'.decode('utf8'),
    'blue circle' : b'\xf0\x9f\x94\xb5'.decode('utf8'),
    'chequered flag' : b'\xf0\x9f\x8f\x81'.decode('utf8'),
    'triangle flag' : b'\xf0\x9f\x9a\xa9'.decode('utf8'),
    'us flag' : b'\xf0\x9f\x87\xba\xf0\x9f\x87\xb8'.decode('utf8'),
    'megaphone' : b'\xf0\x9f\x93\xa3'.decode('utf8'),
    'bell' : b'\xf0\x9f\x94\x94'.decode('utf8'),
    'no bell' : b'\xf0\x9f\x94\x95'.decode('utf8'),
    'go back' : b'\xe2\x86\xa9'.decode('utf8'),
    'cool' : b'\xf0\x9f\x86\x92'.decode('utf8'),
    'free' : b'\xf0\x9f\x86\x93'.decode('utf8'),
    'speech_balloon' : b'\xf0\x9f\x92\xac'.decode('utf8'),
    'zzz' : b'\xf0\x9f\x92\xa4'.decode('utf8'),
    'bellhop_bell' : b'\xf0\x9f\x9b\x8e'.decode('utf8'),
    'hourglass_done' : b'\xe2\x8c\x9b'.decode('utf8'),
    'hourglass_not_done' : b'\xe2\x8f\xb3'.decode('utf8'),
    'wrench' : b'\xf0\x9f\x94\xa7'.decode('utf8'),
    'gear' : b'\xe2\x9a\x99'.decode('utf8'),
    'link' : b'\xf0\x9f\x94\x97'.decode('utf8'),
    'lock' : b'\xf0\x9f\x94\x92'.decode('utf8'),
    'unlock' : b'\xf0\x9f\x94\x93'.decode('utf8'),
    'key' : b'\xf0\x9f\x94\x91'.decode('utf8'),
    'spiral_calendar' : b'\xf0\x9f\x97\x93'.decode('utf8'),
    'chart increasing' : b'\xf0\x9f\x93\x88'.decode('utf8'),
    'chart decreasing' : b'\xf0\x9f\x93\x89'.decode('utf8'),
    'bar chart' : b'\xf0\x9f\x93\x8a'.decode('utf8'),
    'clipboard' : b'\xf0\x9f\x93\x8b'.decode('utf8'),
    'round location pushpin' : b'\xf0\x9f\x93\x8d'.decode('utf8'),
}

def emoji_code_factory(emoji_names:List[str]):
    """Speed up the workflow for inputting emojis to use"""
    code = ""
    for name in emoji_names:
        print(name)
        em = input()
        code += f"'{name}' : {em.encode('utf8')}.decode('utf8'),\n    "
    print(code)

def print_all_emojis() -> str:
    all_emojis = ""
    logging.info("Printing all emojis")
    for k,v in emojis.items():
        all_emojis += f"{v}\n{{e.emojis[{k.__repr__()}]}}\n"
    return all_emojis


if __name__ == '__main__':
    print(print_all_emojis())