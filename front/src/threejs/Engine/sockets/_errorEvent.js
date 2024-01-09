import {_waitForConnection} from "./_waitForConnection";

export async function _errorEvent(socket, message) {
    try {
        await _waitForConnection(socket._socketIO);
    } catch (e) {
        console.error('_errorEvent error event: ', e);
        return;
    }

    console.error('Server error message: ', message);
    socket._engine.setSocket(null);
}