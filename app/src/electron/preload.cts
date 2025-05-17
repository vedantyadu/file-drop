import { contextBridge, ipcRenderer } from 'electron'
import { Peer } from './connection-service/index.js'
// import { connectionServiceChannels } from './connection-service/ipc.js'

contextBridge.exposeInMainWorld('connectionService', {
  onRecieveAvailablePeers: (callback: (data: Peer[]) => void) =>
    ipcRenderer.on('AVAILABLE_PEERS', (_, data) => callback(data)),
})
