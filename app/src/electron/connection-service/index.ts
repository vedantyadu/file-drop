import { ChildProcess, spawn } from 'child_process'

export type Peer = {
  address: string
  id: string
}

export function spawnConnectionService(win: Electron.BrowserWindow) {
  const connectionService = spawn('python3', ['../service/main.py'])

  connectionService.stdout.on('data', (data: Buffer) => {
    const parsed_data = JSON.parse(data.toString())
    win.webContents.send('AVAILABLE_PEERS', parsed_data)
  })

  addCleanupListeners(connectionService)
}

function cleanChildprocess(child_process: ChildProcess) {
  if (!child_process.pid) return
  process.kill(child_process.pid)
  process.exit()
}

function addCleanupListeners(child_process: ChildProcess) {
  process.on('exit', () => cleanChildprocess(child_process))
  process.on('SIGINT', () => cleanChildprocess(child_process))
  process.on('SIGTERM', () => cleanChildprocess(child_process))
}
