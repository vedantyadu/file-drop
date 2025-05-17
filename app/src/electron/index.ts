import { app, BrowserWindow } from 'electron'
import { spawnConnectionService } from './connection-service/index.js'
import getPreloadPath from './path-resolver.js'

function main() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      preload: getPreloadPath(),
    },
  })

  mainWindow.loadURL('http://localhost:5173')
  mainWindow.webContents.openDevTools()
  spawnConnectionService()
}

app.on('ready', main)
