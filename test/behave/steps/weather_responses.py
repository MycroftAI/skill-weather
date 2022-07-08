from behave import given, when, then

from mycroft.messagebus import Message
from mycroft.audio import wait_while_speaking

from test.integrationtests.voight_kampff import (mycroft_responses, then_wait,
                                                 then_wait_fail)


@then('"{skill}" should reply with dialog that includes "{dialog}"')
def then_dialog(context, skill, dialog):
    dialog_msg = None
    def check_dialog(message):
        expected_dialog = dialog.replace('.dialog', '')
        utt_dialog = message.data.get('meta', {}).get('dialog')
        return (expected_dialog == utt_dialog or expected_dialog in utt_dialog, '')

    passed, debug = then_wait('speak', check_dialog, context)
    if not passed:
        assert_msg = debug
        assert_msg += mycroft_responses(context)

    assert passed, assert_msg or 'Mycroft didn\'t respond'