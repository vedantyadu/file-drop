import { useEffect, useState } from 'react'
import type { Peer } from '../../electron/connection-service'

// declare global {
//   interface Window {
//     connectionService: {
//       onRecieveAvailablePeers: (callback: (data: Peer[]) => void) => void
//     }
//   }
// }

export default function Home() {
  const [peers, setPeers] = useState<Peer[]>([])

  useEffect(() => {
    // @ts-ignore
    window.connectionService.onRecieveAvailablePeers((data) => {
      setPeers(data)
    })
  }, [])

  return (
    <div className='w-full h-full bg-neutral-950 flex items-center justify-center'>
      <pre>{peers.join(',')}</pre>
    </div>
  )
}
