import { app } from 'electron'
import path from 'path'

export default function getPreloadPath() {
  return path.join(app.getAppPath(), '/dist-electron/preload.cjs')
}
