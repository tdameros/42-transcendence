import {sleep} from "../../sleep";

export async function _waitForConnection(socketIO, waitTime = 100, timeout = 10000) {
    for (let i = 0; !socketIO.connected && i < timeout; i += waitTime) {
        await sleep(waitTime);
    }

    if (!socketIO.connected) {
        throw new Error('_waitForConnection timed out');
    }
}