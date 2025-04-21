import { useCallback, useEffect, useState } from '@lynx-js/react'

import './App.css'
import lynxLogo from './assets/ophiuchus.png'

export function App() {
  const [alterLogo, setAlterLogo] = useState(false)

  useEffect(() => {
    console.info('Hello, ReactLynx')
  }, [])

  const onTap = useCallback(() => {
    'background only'
    setAlterLogo(!alterLogo)
  }, [alterLogo])

  return (
    <view>
      <view className='Background' />
      <view className='App'>
        <view className='Banner'>
          <view className='Logo' bindtap={onTap}>
            <image src={lynxLogo} className='Logo--lynx' />
          </view>
          <view className='Content'>
            <text className='Title'>Ask Aegle</text>
            <text className='subtext'>Health Made Simple</text>
          </view>
        </view>
      </view>
    </view>
  )
}
