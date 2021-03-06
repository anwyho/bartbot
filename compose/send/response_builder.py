import json
import logging
import wrapt

from abc import (abstractmethod)
from typing import (Any, Callable, List, Optional, Tuple, Type, Union)

from compose.receive.message import (Message)
from compose.send.attachment import (Asset, Template)
from compose.send.button import (Button)
from compose.send.response import (Response)
from compose.utils.requests import (post)
from compose.utils.urls import (MESSAGES_API)


@wrapt.decorator
def require_rebuild(wrapped, instance, args, kwargs):
    """
    Setter wrapper that resets the built tag to `False`.
    """
    if instance:
        instance._built = False
        instance._passingChecks = False
    elif isinstance(args[0], Response):
        args[0]._built = False
        args[0]._passingChecks = False
    return wrapped(*args, **kwargs)

class ResponseBuilderError(Exception):
    pass


# Interface for Send API
class ResponseBuilder(Response):
    """Provides an interface for sending to Send API"""

    def __init__(self,
                 text: str = "",
                 attachment: Optional[Union[Template, Asset]] = None,
                 messagingType: str = '',
                 metadata: str = '',
                 notificationType: str = '',
                 tag: Optional[str] = None,
                 senderAction: Optional[str] = None,
                 apiUrl: Optional[str] = MESSAGES_API,
                 dryRun: bool = False,
                 description: Optional[str] = None,
                 **recipientArgs) -> None:
        super(ResponseBuilder, self).__init__(
            apiUrl=apiUrl, dryRun=dryRun, description=description)

        self._text: Optional[str] = str(text)
        self._attachment: Optional[Union[Template, Asset]] = attachment if isinstance(
            attachment, Asset) else None
        self._messagingType: str = messagingType if \
            messagingType in self.MESSAGING_TYPES else 'RESPONSE'
        self._metadata: str = metadata
        self._notificationType: str = notificationType if \
            notificationType in self.NOTIFICATION_TYPES else 'regular'
        self._tag: Optional[str] = tag
        self._senderAction: Optional[str] = senderAction
        self.quickReplies: List[dict] = []
        if recipientArgs:
            self.set_recipient(**recipientArgs)
        self._built: bool = False

    def build(self):
        """
        Construct JSON for Messenger Platform Send API. This is
            adapter for Messenger.
        """
        if self._built:
            return

        self._data: dict = {}

        self._data['messaging_type'] = self.messagingType
        self._data['recipient'] = self.recipient()

        if self.text or self.attachment:
            message: dict = {}

            if self.text:
                message['text'] = str(self.text)
            elif self.attachment:
                message['attachment'] = self.attachment.build()
            else:
                raise ResponseBuilderError("Expected either text or attachment.")

            if self.quickReplies:
                message['quick_replies'] = self.quickReplies
            # Chained response contains quickReplies but is empty
            elif getattr(self._chainedResponse, 'quickReplies', None) and \
                not (getattr(self._chainedResponse, 'attachment', None) or
                     getattr(self._chainedResponse, 'text', None)):
                self.quickReplies = self._chainedResponse.quickReplies
                self._chainedResponse = None

            if self.metadata:
                message['metadata'] = self.metadata
            self._data['message'] = message

            self._data['notification_type'] = self.notificationType
            if self.tag:
                self._data['tag'] = self.tag

        elif self.senderAction is not None:
            self._data['sender_action'] = self.senderAction

        self._built = True

    def send(self, inChain: bool = False) -> bool:
        """
        Verify that response data is built before calling super send method.
        """
        if not self._built:
            self.build()
        return super(ResponseBuilder, self).send(inChain=inChain)

    ### DUPLICATE RESPONSES ###

    def create_and_get_chained_response(self, **builderInitKwargs):
        """Create and attach a chained response and set recipient and moves quick replies."""
        self._chainedResponse = ResponseBuilder(**builderInitKwargs)
        self._chainedResponse._dryRun = self._dryRun
        self._chainedResponse._recipient = self._recipient
        self._chainedResponse.quickReplies = self.quickReplies
        self.quickReplies = []
        return self._chainedResponse

    def create_and_get_separate_response(self, **builderInitKwargs):
        """Create a new response set the same recipient."""
        resp = ResponseBuilder(**builderInitKwargs)
        resp._dryRun = self._dryRun
        resp._recipient = self._recipient
        return resp

    ### PROPERTIES ###

    @property
    def attachment(self):
        return self._attachment

    @attachment.setter
    @require_rebuild
    def attachment(self, templateOrAsset: Union[Template, Asset]):
        if isinstance(templateOrAsset, Template) or \
                isinstance(templateOrAsset, Asset):
            self._attachment = templateOrAsset
        else:
            ResponseBuilderError(
                "Attempted to set attachment to object other than Template or Asset.")

    @property
    def messagingType(self) -> str:
        return self._messagingType

    @messagingType.setter
    @require_rebuild
    def messagingType(self, messagingType: str) -> None:
        if messagingType in self.MESSAGING_TYPES:
            self._messagingType = messagingType
        else:
            ResponseBuilderError(
                f"Attempted to set messaging type to an unsupported messaging type {messagingType}.")

    @property
    def metadata(self) -> str:
        return self._metadata

    @metadata.setter
    @require_rebuild
    def metadata(self, metadata: str) -> None:
        self._metadata = metadata

    @property
    def notificationType(self) -> str:
        return self._notificationType

    @notificationType.setter
    @require_rebuild
    def notificationType(self, notificationType: str) -> None:
        if notificationType in self.NOTIFICATION_TYPES:
            self._notificationType = notificationType
        else:
            ResponseBuilderError(
                f"Attempted to set notification type to an unsupported messaging type {notificationType}.")

    def recipient(self) -> dict:
        return self._recipient

    @require_rebuild
    def set_recipient(self,
                      recipientId: Optional[str] = None,
                      phoneNumber: Optional[str] = None,
                      firstName: Optional[str] = None,
                      lastName: Optional[str] = None,
                      userRef: Optional[str] = None) -> None:
        """
        Set recipient information with Facebook ID taking priority, followed by phone number and then user referral.
        """

        if recipientId:
            self._recipient: dict = {'id': recipientId}
        elif phoneNumber:
            self._recipient: dict = {
                'id': phoneNumber, 'phone_number': phoneNumber}
            if firstName and lastName:
                self._recipient['name']: dict = {
                    'first_name': firstName, 'last_name': lastName}
        elif userRef:
            self._recipient: dict = {'id': userRef, 'user_ref': userRef}
        else:
            logging.debug(
                f"Failed to set recipient info. Variable dump: \nrecipientId: {recipientId}\nphoneNumber: {phoneNumber}\nfirstName: {firstName}\nlastName: {lastName}\nuserRef: {userRef}")
            raise ResponseBuilderError("Failed to set recipient information.")

    @property
    def senderAction(self) -> str:
        return self._senderAction

    @senderAction.setter
    @require_rebuild
    def senderAction(self, senderAction: str) -> None:
        if senderAction in self.SENDER_ACTIONS:
            self._senderAction = senderAction
        else:
            ResponseBuilderError(
                f"Attempted to set sender action to an unsupported sender action {senderAction}.")

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    @require_rebuild
    def tag(self, tag: str) -> None:
        if tag in self.TAGS:
            self._tag = tag
        else:
            ResponseBuilderError(
                f"Attempted to set tag to an unsupported tag {tag}.")

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = str(text)

    @require_rebuild
    def add_quick_reply(self,
                        contentType: str = 'text',
                        text: str = '',
                        postbackPayload: Union[str, int] = '',
                        imageUrl: str = '') -> dict:
        """
        Add a quick-reply to the message payload. Remove quick-reply not implemented yet.
        """

        if len(self.quickReplies) >= self.MAX_QUICK_REPLIES:
            raise ResponseBuilderError(
                f"Only {self.MAX_QUICK_REPLIES} quick replies are allowed per response.")
        contentType = contentType.lower()
        if contentType in self.QUICK_REPLY_TYPES:
            quickReply: dict = {'content_type': contentType}
            if contentType == 'text':
                quickReply['title'] = text
                quickReply['payload'] = postbackPayload
                if imageUrl or text == '':
                    if imageUrl:
                        quickReply['image_url'] = imageUrl
                    else:
                        raise ResponseBuilderError(
                            "Expected image URL with empty title string.")
            self.quickReplies.append(quickReply)
        else:
            raise ResponseBuilderError(
                "Attempted to create unsupported quick reply type.")

